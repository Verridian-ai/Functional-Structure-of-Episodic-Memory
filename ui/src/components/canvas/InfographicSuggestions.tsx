'use client';

import React, { useState, useEffect, useMemo } from 'react';
import {
  Sparkles,
  Clock,
  GitBranch,
  Columns,
  BarChart2,
  GitMerge,
  List,
  Workflow,
  PieChart,
  BarChart,
  X,
  ChevronRight,
  Loader2,
  CheckCircle,
  Image as ImageIcon
} from 'lucide-react';
import {
  analyzeForInfographics,
  getTypeInfo,
  type InfographicSuggestion,
  type InfographicType
} from '@/lib/services/infographicAnalyzer';

interface InfographicSuggestionsProps {
  content: string;
  documentType?: string;
  onGenerate: (prompt: string, aspectRatio: string) => Promise<void>;
  isGenerating?: boolean;
}

// Icon mapping for infographic types
const TYPE_ICONS: Record<InfographicType, React.ComponentType<{ className?: string }>> = {
  timeline: Clock,
  process: GitBranch,
  comparison: Columns,
  statistics: BarChart2,
  hierarchy: GitMerge,
  list: List,
  flowchart: Workflow,
  'pie-chart': PieChart,
  'bar-chart': BarChart,
};

// Color mapping for badges
const TYPE_COLORS: Record<InfographicType, string> = {
  timeline: 'bg-blue-500/20 border-blue-500/50 text-blue-400',
  process: 'bg-green-500/20 border-green-500/50 text-green-400',
  comparison: 'bg-purple-500/20 border-purple-500/50 text-purple-400',
  statistics: 'bg-orange-500/20 border-orange-500/50 text-orange-400',
  hierarchy: 'bg-cyan-500/20 border-cyan-500/50 text-cyan-400',
  list: 'bg-pink-500/20 border-pink-500/50 text-pink-400',
  flowchart: 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400',
  'pie-chart': 'bg-red-500/20 border-red-500/50 text-red-400',
  'bar-chart': 'bg-indigo-500/20 border-indigo-500/50 text-indigo-400',
};

export function InfographicSuggestions({
  content,
  documentType,
  onGenerate,
  isGenerating = false,
}: InfographicSuggestionsProps) {
  const [suggestions, setSuggestions] = useState<InfographicSuggestion[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [dismissedIds, setDismissedIds] = useState<Set<string>>(new Set());
  const [generatingId, setGeneratingId] = useState<string | null>(null);
  const [completedIds, setCompletedIds] = useState<Set<string>>(new Set());

  // Analyze content for suggestions
  useEffect(() => {
    if (content && content.length > 100) {
      const newSuggestions = analyzeForInfographics(content, documentType, 0.55);
      setSuggestions(newSuggestions);
    } else {
      setSuggestions([]);
    }
  }, [content, documentType]);

  // Filter out dismissed suggestions
  const visibleSuggestions = useMemo(() =>
    suggestions.filter(s => !dismissedIds.has(s.id)),
    [suggestions, dismissedIds]
  );

  const handleDismiss = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setDismissedIds(prev => new Set([...prev, id]));
    if (expandedId === id) setExpandedId(null);
  };

  const handleGenerate = async (suggestion: InfographicSuggestion) => {
    setGeneratingId(suggestion.id);
    try {
      // Determine aspect ratio based on type
      const aspectRatio = ['timeline', 'process', 'comparison'].includes(suggestion.suggestedType)
        ? '16:9'
        : ['hierarchy', 'flowchart'].includes(suggestion.suggestedType)
        ? '4:3'
        : '1:1';

      await onGenerate(suggestion.prompt, aspectRatio);
      setCompletedIds(prev => new Set([...prev, suggestion.id]));
      setExpandedId(null);
    } finally {
      setGeneratingId(null);
    }
  };

  if (visibleSuggestions.length === 0) {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-40 max-w-sm">
      {/* Floating Badge */}
      <div className="bg-zinc-900/95 backdrop-blur-xl border border-yellow-500/30 rounded-xl shadow-2xl shadow-yellow-500/10 overflow-hidden">
        {/* Header */}
        <div className="px-4 py-3 border-b border-zinc-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-sm font-medium text-white">Infographic Suggestions</span>
            <span className="px-1.5 py-0.5 text-xs bg-yellow-500/20 text-yellow-400 rounded">
              {visibleSuggestions.length}
            </span>
          </div>
        </div>

        {/* Suggestions List */}
        <div className="max-h-[300px] overflow-y-auto custom-scrollbar">
          {visibleSuggestions.slice(0, 5).map((suggestion) => {
            const Icon = TYPE_ICONS[suggestion.suggestedType];
            const colorClass = TYPE_COLORS[suggestion.suggestedType];
            const isExpanded = expandedId === suggestion.id;
            const isThisGenerating = generatingId === suggestion.id;
            const isCompleted = completedIds.has(suggestion.id);

            return (
              <div
                key={suggestion.id}
                className={`border-b border-zinc-800/50 last:border-b-0 ${
                  isExpanded ? 'bg-zinc-800/50' : 'hover:bg-zinc-800/30'
                } transition-all`}
              >
                {/* Suggestion Header */}
                <div
                  className="px-4 py-3 cursor-pointer flex items-center gap-3"
                  onClick={() => setExpandedId(isExpanded ? null : suggestion.id)}
                >
                  <div className={`p-1.5 rounded-lg border ${colorClass}`}>
                    <Icon className="w-4 h-4" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-white">
                        {getTypeInfo(suggestion.suggestedType).label}
                      </span>
                      <span className="text-xs text-zinc-500">
                        {Math.round(suggestion.confidence * 100)}% match
                      </span>
                    </div>
                    <p className="text-xs text-zinc-400 truncate mt-0.5">
                      {suggestion.sectionText.slice(0, 60)}...
                    </p>
                  </div>

                  <div className="flex items-center gap-1">
                    {isCompleted && (
                      <CheckCircle className="w-4 h-4 text-green-400" />
                    )}
                    <button
                      onClick={(e) => handleDismiss(suggestion.id, e)}
                      className="p-1 hover:bg-zinc-700 rounded transition opacity-50 hover:opacity-100"
                    >
                      <X className="w-3 h-3 text-zinc-400" />
                    </button>
                    <ChevronRight
                      className={`w-4 h-4 text-zinc-500 transition-transform ${
                        isExpanded ? 'rotate-90' : ''
                      }`}
                    />
                  </div>
                </div>

                {/* Expanded Details */}
                {isExpanded && (
                  <div className="px-4 pb-4 space-y-3">
                    <div className="p-3 bg-black/30 rounded-lg">
                      <p className="text-xs text-zinc-400">{suggestion.reason}</p>
                    </div>

                    <div className="p-3 bg-black/30 rounded-lg">
                      <p className="text-xs text-zinc-500 mb-1">Preview of content:</p>
                      <p className="text-xs text-zinc-300 italic">
                        "{suggestion.sectionText}"
                      </p>
                    </div>

                    <button
                      onClick={() => handleGenerate(suggestion)}
                      disabled={isGenerating || isThisGenerating}
                      className="w-full py-2.5 bg-yellow-600 hover:bg-yellow-500 text-black font-medium rounded-lg transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isThisGenerating ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <ImageIcon className="w-4 h-4" />
                          Generate {getTypeInfo(suggestion.suggestedType).label}
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer - Batch Generate */}
        {visibleSuggestions.length > 1 && (
          <div className="px-4 py-3 border-t border-zinc-800 bg-black/20">
            <button
              disabled={isGenerating}
              className="w-full py-2 text-xs text-zinc-400 hover:text-white transition flex items-center justify-center gap-2"
              onClick={() => {
                // Generate all visible suggestions
                visibleSuggestions.forEach((s, i) => {
                  setTimeout(() => handleGenerate(s), i * 2000);
                });
              }}
            >
              <Sparkles className="w-3 h-3" />
              Generate All ({visibleSuggestions.length})
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// Compact inline badge for showing in document view
export function InfographicBadge({
  type,
  confidence,
  onClick,
  isGenerating,
}: {
  type: InfographicType;
  confidence: number;
  onClick: () => void;
  isGenerating?: boolean;
}) {
  const Icon = TYPE_ICONS[type];
  const colorClass = TYPE_COLORS[type];
  const { label } = getTypeInfo(type);

  return (
    <button
      onClick={onClick}
      disabled={isGenerating}
      className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full border ${colorClass} text-xs font-medium transition hover:scale-105 disabled:opacity-50`}
    >
      {isGenerating ? (
        <Loader2 className="w-3 h-3 animate-spin" />
      ) : (
        <Icon className="w-3 h-3" />
      )}
      {label}
      <span className="opacity-60">{Math.round(confidence * 100)}%</span>
    </button>
  );
}

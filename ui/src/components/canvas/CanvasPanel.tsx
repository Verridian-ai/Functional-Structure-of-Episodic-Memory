'use client';

import React, { useState } from 'react';
import {
  Download, Copy, Edit3, Save, FileText, Code, File,
  ChevronRight, Highlighter, Layout, Image as ImageIcon, Scale
} from 'lucide-react';
import { useStore } from '@/lib/store';
import type { Artifact } from '@/types';
import { SafeHtmlProse } from '@/components/ui/SafeHtml';

// Generate unique ID for artifacts (outside component to avoid purity issues)
let artifactCounter = 0;
const generateArtifactId = () => `artifact_${++artifactCounter}_${Date.now()}`;

// NanoBanana Pro Image Generation via OpenRouter
interface GenerateImageOptions {
  prompt: string;
  aspectRatio?: string;
  context?: string;
  documentType?: string;
}

interface GenerateImageResult {
  success: boolean;
  image?: string;
  text?: string;
  error?: string;
}

const generateImage = async (options: GenerateImageOptions): Promise<GenerateImageResult> => {
  try {
    const response = await fetch('/api/generate-image', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: options.prompt,
        aspectRatio: options.aspectRatio || '16:9',
        context: options.context,
        documentType: options.documentType,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        error: data.error || 'Image generation failed',
      };
    }

    return {
      success: true,
      image: data.image,
      text: data.text,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Network error',
    };
  }
};

export function CanvasPanel() {
  const {
    artifacts,
    activeArtifactId,
    showCanvas,
    setActiveArtifact,
    updateArtifact,
    addArtifact,
    toggleCanvas,
  } = useStore();

    const [showLayoutMenu, setShowLayoutMenu] = useState(false);
    const [canvasConfig, setCanvasConfig] = useState({
        fontFamily: 'Inter',
        fontSize: '16px',
        headingSize: '2.25rem',
        margin: '2rem',
        layout: 'standard' as 'standard' | 'legal' | 'newsletter' | 'report'
    });

    const [isEditing, setIsEditing] = useState(false);
    const [editContent, setEditContent] = useState('');
    const [highlighterMode, setHighlighterMode] = useState(false);
    const [imagePrompt, setImagePrompt] = useState('');
    const [showImageModal, setShowImageModal] = useState(false);
    const [isGeneratingImage, setIsGeneratingImage] = useState(false);
    const [imageError, setImageError] = useState<string | null>(null);
    const [selectedAspectRatio, setSelectedAspectRatio] = useState('16:9');

    const activeArtifact = artifacts.find(a => a.id === activeArtifactId);

    const TEMPLATES = [
      { id: 'legal', name: 'Legal Brief', icon: Scale, desc: 'Standard legal document layout with wide margins and formal font.' },
      { id: 'report', name: 'Client Report', icon: FileText, desc: 'Professional report with cover page structure and headers.' },
      { id: 'newsletter', name: 'Legal Newsletter', icon: Layout, desc: 'Multi-column layout for updates and news.' },
      { id: 'standard', name: 'Blank Document', icon: File, desc: 'Empty canvas with standard formatting.' },
    ];

    const createFromTemplate = (templateId: string) => {
      const templateName = TEMPLATES.find(t => t.id === templateId)?.name || 'Document';

      // Map template IDs to layout types
      const layoutMap: Record<string, 'standard' | 'report' | 'newsletter' | 'legal-brief'> = {
        'legal': 'legal-brief',
        'newsletter': 'newsletter',
        'report': 'report',
        'standard': 'standard',
      };
      const layout = layoutMap[templateId] || 'standard';

      const structure: NonNullable<Artifact['structure']> = {
          layout,
          sections: []
      };

      if (templateId === 'legal') {
          structure.sections = [
              { id: 'h1', type: 'text', region: 'header', content: '<div class="text-center font-bold uppercase">In the Federal Circuit and Family Court of Australia</div>' },
              { id: 'm1', type: 'text', region: 'main', content: '<h3>1. INTRODUCTION</h3><p>The Applicant applies for the following orders...</p>' },
              { id: 'f1', type: 'text', region: 'footer', content: '<div class="text-xs text-center">Page 1 of 1</div>' }
          ];
      } else if (templateId === 'newsletter') {
          structure.sections = [
               { id: 'h1', type: 'text', region: 'header', content: '<h1 class="text-4xl font-bold text-emerald-700">Legal Update</h1><p class="text-zinc-500">November 2025 Edition</p>' },
               { id: 's1', type: 'text', region: 'sidebar-left', content: '<h3>Contents</h3><ul><li>Case Law Update</li><li>Legislative Changes</li></ul>' },
               { id: 'm1', type: 'text', region: 'main', content: '<h2>New Precedent in Family Law</h2><p>A recent decision has shifted the landscape regarding...</p>' }
          ];
      } else {
           structure.sections = [
              { id: 'm1', type: 'text', region: 'main', content: '<h1>Untitled Document</h1><p>Start typing here...</p>' }
           ];
      }

      const now = new Date();
      const newArtifact: Artifact = {
          id: generateArtifactId(),
          type: 'smart-canvas',
          title: `New ${templateName}`,
          content: '',
          structure,
          createdAt: now,
          updatedAt: now,
      };

      addArtifact(newArtifact);
      setShowLayoutMenu(false);
    };

    const updateCanvasSetting = (key: keyof typeof canvasConfig, value: string) => {
        setCanvasConfig(prev => ({ ...prev, [key]: value }));
    };


  if (!showCanvas) return null;

  const handleEdit = () => {
    if (activeArtifact) {
      setEditContent(activeArtifact.content || '');
      setIsEditing(true);
    }
  };

  const handleSave = () => {
    if (activeArtifact) {
      updateArtifact(activeArtifact.id, { content: editContent });
      setIsEditing(false);
    }
  };

  // ... existing handlers ...
  const handleCopy = async () => {
    if (activeArtifact) {
      await navigator.clipboard.writeText(activeArtifact.content || '');
    }
  };
  
  const handleDownloadDOCX = async () => {
      // ... existing implementation ...
      if (activeArtifact) {
      try {
        const response = await fetch('/api/docx/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: activeArtifact.title, content: activeArtifact.content || '' }),
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${activeArtifact.title.replace(/\s+/g, '_')}.docx`;
          a.click();
          URL.revokeObjectURL(url);
        }
      } catch (error) {
        console.error('DOCX download failed:', error);
      }
    }
  };

  const handleDownloadPDF = async () => {
     // ... existing implementation ...
     if (activeArtifact) {
      try {
        const response = await fetch('/api/pdf/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: activeArtifact.title, content: activeArtifact.content || '' }),
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${activeArtifact.title.replace(/\s+/g, '_')}.pdf`;
          a.click();
          URL.revokeObjectURL(url);
        }
      } catch (error) {
        console.error('PDF download failed:', error);
      }
    }
  };
  
  const handleTextHighlight = () => {
      if (!highlighterMode) return;
      
      const selection = window.getSelection();
      if (!selection || selection.rangeCount === 0) return;
      
      const range = selection.getRangeAt(0);
      const text = range.toString();
      
      if (text) {
          // In a real rich text editor, we would wrap the range. 
          // Here, for simple artifacts, we might just store the comment/highlight.
          console.log("Highlighted:", text);
          // TODO: Persist highlight
      }
  };

  const handleAddImage = async () => {
      if (!activeArtifact || !imagePrompt.trim()) return;

      setIsGeneratingImage(true);
      setImageError(null);

      try {
        // Detect document type from artifact structure
        const documentType = activeArtifact.structure?.layout || 'standard';

        const result = await generateImage({
          prompt: imagePrompt,
          aspectRatio: selectedAspectRatio,
          context: activeArtifact.content?.slice(0, 500), // Provide context from document
          documentType,
        });

        if (!result.success) {
          setImageError(result.error || 'Failed to generate image');
          return;
        }

        if (result.image) {
          // Insert base64 image directly into content
          const imageMarkdown = `\n\n![${imagePrompt}](${result.image})\n\n`;

          updateArtifact(activeArtifact.id, {
            content: (activeArtifact.content || '') + imageMarkdown
          });

          setShowImageModal(false);
          setImagePrompt('');
          setSelectedAspectRatio('16:9');
        }
      } catch (error) {
        setImageError(error instanceof Error ? error.message : 'Unknown error');
      } finally {
        setIsGeneratingImage(false);
      }
  };

  return (
    <div className="fixed inset-0 md:relative md:inset-auto h-full flex flex-col bg-zinc-950 md:bg-zinc-950/40 backdrop-blur-xl md:border-l border-white/5 z-40 md:z-auto">
      {/* Header - Mobile optimized */}
      <div className="flex items-center justify-between px-3 sm:px-4 py-2 sm:py-3 border-b border-white/5 safe-area-pt">
        <div className="flex items-center gap-2 sm:gap-3">
          <button
            onClick={toggleCanvas}
            className="p-2 md:p-1.5 hover:bg-white/5 active:bg-white/5 rounded-lg transition touch-target"
            aria-label="Close canvas"
          >
            <ChevronRight className="w-5 h-5 text-zinc-400" />
          </button>
          <h2 className="font-semibold text-white text-sm sm:text-base">Canvas</h2>
          <span className="px-1.5 sm:px-2 py-0.5 text-[10px] sm:text-xs bg-white/5 rounded-full text-zinc-400 border border-white/10 hidden sm:inline-flex">
            {artifacts.length} items
          </span>
        </div>

        {activeArtifact && (
          <div className="flex items-center gap-1 sm:gap-2 overflow-x-auto scrollbar-hide">

            {/* NanoBanana Image Gen Button - Hidden on very small screens */}
             <button
                onClick={() => setShowImageModal(true)}
                className="hidden sm:flex p-2 hover:bg-yellow-500/20 active:bg-yellow-500/20 text-yellow-400 rounded-lg transition touch-target flex-shrink-0"
                title="Generate Image (NanoBanana Pro)"
              >
                <ImageIcon className="w-4 h-4" />
              </button>

            {/* Highlighter Toggle - Hidden on mobile */}
             <button
                onClick={() => setHighlighterMode(!highlighterMode)}
                className={`hidden sm:flex p-2 rounded-lg transition touch-target flex-shrink-0 ${highlighterMode ? 'bg-yellow-500/20 text-yellow-400' : 'hover:bg-white/5 text-zinc-400 hover:text-white'}`}
                title="Highlighter Pen"
              >
                <Highlighter className="w-4 h-4" />
              </button>

            {/* Layout/Grid Toggle */}
            <div className="relative flex-shrink-0">
              <button
                onClick={() => setShowLayoutMenu(!showLayoutMenu)}
                className={`p-2 rounded-lg transition touch-target ${showLayoutMenu ? 'bg-white/10 text-white' : 'hover:bg-white/5 active:bg-white/5 text-zinc-400 hover:text-white'}`}
                title="Layout & Templates"
              >
                <Layout className="w-4 h-4" />
              </button>

              {showLayoutMenu && (
                <div className="fixed inset-x-4 top-20 md:absolute md:inset-auto md:right-0 md:top-full md:mt-2 w-auto md:w-80 bg-zinc-900 border border-zinc-700 rounded-xl shadow-2xl overflow-hidden z-50 max-h-[70vh] md:max-h-[60vh]">
                    {/* Header */}
                    <div className="px-4 py-3 border-b border-zinc-800 bg-black/20">
                        <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                            <Layout className="w-4 h-4 text-emerald-500" />
                            Canvas Layout
                        </h3>
                    </div>

                    <div className="p-4 space-y-6 max-h-[60vh] overflow-y-auto custom-scrollbar">
                        {/* Templates Section */}
                        <div>
                            <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">New from Template</h4>
                            <div className="grid grid-cols-2 gap-2">
                                {TEMPLATES.map(t => (
                                    <button
                                        key={t.id}
                                        onClick={() => createFromTemplate(t.id)}
                                        className="flex flex-col items-center gap-2 p-3 rounded-lg bg-zinc-800 hover:bg-zinc-700 hover:ring-1 hover:ring-emerald-500/50 transition group"
                                    >
                                        <div className="w-8 h-8 rounded-full bg-black/30 flex items-center justify-center group-hover:bg-emerald-500/20 transition-colors">
                                            <t.icon className="w-4 h-4 text-zinc-400 group-hover:text-emerald-400" />
                                        </div>
                                        <span className="text-xs font-medium text-zinc-300 group-hover:text-white">{t.name}</span>
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Config Section */}
                        <div className="space-y-4 border-t border-zinc-800 pt-4">
                            <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Typography & Spacing</h4>
                            
                            <div className="space-y-3">
                                <div>
                                    <label className="text-xs text-zinc-400 mb-1 block">Font Family</label>
                                    <select 
                                        value={canvasConfig.fontFamily}
                                        onChange={(e) => updateCanvasSetting('fontFamily', e.target.value)}
                                        className="w-full bg-black/40 border border-zinc-700 rounded-lg px-2 py-1.5 text-xs text-white focus:border-emerald-500 outline-none"
                                    >
                                        <option value="Inter">Inter (Sans)</option>
                                        <option value="Merriweather">Merriweather (Serif)</option>
                                        <option value="JetBrains Mono">Monospace</option>
                                    </select>
                                </div>
                                
                                <div className="grid grid-cols-2 gap-3">
                                    <div>
                                        <label className="text-xs text-zinc-400 mb-1 block">Font Size</label>
                                        <select 
                                            value={canvasConfig.fontSize}
                                            onChange={(e) => updateCanvasSetting('fontSize', e.target.value)}
                                            className="w-full bg-black/40 border border-zinc-700 rounded-lg px-2 py-1.5 text-xs text-white focus:border-emerald-500 outline-none"
                                        >
                                            <option value="14px">Small (14px)</option>
                                            <option value="16px">Medium (16px)</option>
                                            <option value="18px">Large (18px)</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="text-xs text-zinc-400 mb-1 block">Margins</label>
                                        <select 
                                            value={canvasConfig.margin}
                                            onChange={(e) => updateCanvasSetting('margin', e.target.value)}
                                            className="w-full bg-black/40 border border-zinc-700 rounded-lg px-2 py-1.5 text-xs text-white focus:border-emerald-500 outline-none"
                                        >
                                            <option value="1rem">Compact</option>
                                            <option value="2rem">Standard</option>
                                            <option value="3rem">Wide</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
              )}
            </div>

            {isEditing ? (
              <button
                onClick={handleSave}
                className="p-2 hover:bg-green-500/20 active:bg-green-500/20 text-green-400 rounded-lg transition touch-target flex-shrink-0"
                title="Save changes"
              >
                <Save className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleEdit}
                className="p-2 hover:bg-white/5 active:bg-white/5 text-zinc-400 hover:text-white rounded-lg transition touch-target flex-shrink-0"
                title="Edit"
              >
                <Edit3 className="w-4 h-4" />
              </button>
            )}
            <button
              onClick={handleCopy}
              className="hidden sm:flex p-2 hover:bg-white/5 active:bg-white/5 text-zinc-400 hover:text-white rounded-lg transition touch-target flex-shrink-0"
              title="Copy"
            >
              <Copy className="w-4 h-4" />
            </button>

            {/* Export Menu */}
            <div className="relative group flex-shrink-0">
              <button
                className="p-2 hover:bg-white/5 active:bg-white/5 text-zinc-400 hover:text-white rounded-lg transition touch-target"
                title="Export"
              >
                <Download className="w-4 h-4" />
              </button>
              <div className="absolute right-0 top-full mt-1 w-32 bg-zinc-900 border border-zinc-800 rounded-lg shadow-xl overflow-hidden opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                <button onClick={handleDownloadDOCX} className="w-full px-3 py-2.5 sm:py-2 text-left text-sm text-zinc-400 hover:text-white active:text-white hover:bg-zinc-800 active:bg-zinc-800 transition touch-target">
                  Word (.docx)
                </button>
                <button onClick={handleDownloadPDF} className="w-full px-3 py-2.5 sm:py-2 text-left text-sm text-zinc-400 hover:text-white active:text-white hover:bg-zinc-800 active:bg-zinc-800 transition touch-target">
                  PDF (.pdf)
                </button>
                <button onClick={() => {
                    const blob = new Blob([activeArtifact.content || ''], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${activeArtifact.title.replace(/\s+/g, '_')}.txt`;
                    a.click();
                }} className="w-full px-3 py-2.5 sm:py-2 text-left text-sm text-zinc-400 hover:text-white active:text-white hover:bg-zinc-800 active:bg-zinc-800 transition touch-target">
                  Text (.txt)
                </button>
              </div>
            </div>

          </div>
        )}
      </div>

      {/* Tabs - Scrollable on mobile */}
      {artifacts.length > 0 && (
        <div className="flex items-center gap-1 px-2 py-1.5 sm:py-2 border-b border-white/5 overflow-x-auto scrollbar-hide">
          {artifacts.map((artifact) => (
            <button
              key={artifact.id}
              onClick={() => setActiveArtifact(artifact.id)}
              className={`flex items-center gap-1.5 sm:gap-2 px-2 sm:px-3 py-1.5 sm:py-1.5 rounded-lg text-xs sm:text-sm whitespace-nowrap transition touch-target ${
                artifact.id === activeArtifactId
                  ? 'bg-white/10 text-white border border-white/10 shadow-sm'
                  : 'hover:bg-white/5 active:bg-white/5 text-zinc-400 hover:text-zinc-200 border border-transparent'
              }`}
            >
              {getArtifactIcon(artifact)}
              <span className="max-w-[80px] sm:max-w-[120px] truncate">{artifact.title}</span>
            </button>
          ))}
        </div>
      )}

      {/* Content */}
      <div className="flex-1 overflow-auto relative" onMouseUp={handleTextHighlight}>
        {activeArtifact ? (
          <div className="h-full">
              
            {/* NanoBanana Pro Modal - Mobile optimized */}
            {showImageModal && (
                <div className="absolute inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-6">
                    <div className="w-full sm:max-w-md bg-zinc-900 border-t sm:border border-yellow-500/30 rounded-t-2xl sm:rounded-xl p-4 sm:p-5 shadow-2xl shadow-yellow-500/10 max-h-[90vh] overflow-y-auto">
                        <h3 className="text-base sm:text-lg font-bold text-yellow-400 mb-1 flex items-center gap-2">
                            <ImageIcon className="w-4 h-4 sm:w-5 sm:h-5" />
                            <span className="hidden sm:inline">NanoBanana Pro - Infographic Generator</span>
                            <span className="sm:hidden">Image Generator</span>
                        </h3>
                        <p className="text-[10px] sm:text-xs text-zinc-500 mb-3 sm:mb-4">Powered by Gemini 3 Pro via OpenRouter</p>

                        <div className="space-y-3 sm:space-y-4">
                          {/* Prompt Input */}
                          <div>
                            <label className="text-[10px] sm:text-xs text-zinc-400 mb-1 block">Describe your infographic</label>
                            <textarea
                                value={imagePrompt}
                                onChange={(e) => setImagePrompt(e.target.value)}
                                className="w-full h-20 sm:h-24 bg-black/50 border border-zinc-700 rounded-lg p-2.5 sm:p-3 text-sm sm:text-base text-white focus:border-yellow-500/50 outline-none resize-none"
                                placeholder="An infographic showing the timeline of family court proceedings..."
                                disabled={isGeneratingImage}
                            />
                          </div>

                          {/* Aspect Ratio Selection */}
                          <div>
                            <label className="text-[10px] sm:text-xs text-zinc-400 mb-1.5 sm:mb-2 block">Aspect Ratio</label>
                            <div className="flex gap-1.5 sm:gap-2 flex-wrap">
                              {['1:1', '16:9', '4:3', '9:16', '3:2'].map((ratio) => (
                                <button
                                  key={ratio}
                                  onClick={() => setSelectedAspectRatio(ratio)}
                                  className={`px-2.5 sm:px-3 py-1.5 text-xs rounded-lg border transition touch-target ${
                                    selectedAspectRatio === ratio
                                      ? 'bg-yellow-600/20 border-yellow-500 text-yellow-400'
                                      : 'border-zinc-700 text-zinc-400 hover:border-zinc-500 active:border-zinc-500'
                                  }`}
                                  disabled={isGeneratingImage}
                                >
                                  {ratio}
                                </button>
                              ))}
                            </div>
                          </div>

                          {/* Error Message */}
                          {imageError && (
                            <div className="p-2.5 sm:p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                              <p className="text-xs sm:text-sm text-red-400">{imageError}</p>
                            </div>
                          )}

                          {/* Action Buttons */}
                          <div className="flex justify-end gap-2 pt-2">
                              <button
                                  onClick={() => {
                                    setShowImageModal(false);
                                    setImageError(null);
                                    setImagePrompt('');
                                  }}
                                  className="px-3 sm:px-4 py-2 text-zinc-400 hover:text-white active:text-white transition touch-target"
                                  disabled={isGeneratingImage}
                              >
                                  Cancel
                              </button>
                              <button
                                  onClick={handleAddImage}
                                  disabled={!imagePrompt.trim() || isGeneratingImage}
                                  className="px-3 sm:px-4 py-2 bg-yellow-600 hover:bg-yellow-500 active:bg-yellow-500 text-black font-semibold rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 touch-target text-sm sm:text-base"
                              >
                                  {isGeneratingImage ? (
                                    <>
                                      <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                      </svg>
                                      <span className="hidden sm:inline">Generating...</span>
                                      <span className="sm:hidden">...</span>
                                    </>
                                  ) : (
                                    <>
                                      <span className="hidden sm:inline">Generate Infographic</span>
                                      <span className="sm:hidden">Generate</span>
                                    </>
                                  )}
                              </button>
                          </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Content Rendering Logic */}
            {isEditing ? (
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full h-full p-8 bg-transparent text-white font-mono text-sm resize-none outline-none leading-relaxed"
                spellCheck={false}
              />
            ) : (
              <div className="h-full w-full relative">
                 {/* Only show SmartCanvasRenderer for smart-canvas type, else standard text/markdown */}
                 {activeArtifact.type === 'smart-canvas' ? (
                    <SmartCanvasRenderer artifact={activeArtifact} />
                 ) : (
                    <ArtifactContent artifact={activeArtifact} highlighterMode={highlighterMode} />
                 )}
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-zinc-500">
            <FileText className="w-16 h-16 mb-6 opacity-20 stroke-[1.5]" />
            <p className="text-lg font-medium text-zinc-400">No artifacts selected</p>
            <p className="text-sm mt-2 max-w-xs text-center opacity-60">
              Select an item from the chat or ask Verridian to create a new document.
            </p>
          </div>
        )}
      </div>
      
      {/* Footer ... */}
      {activeArtifact && (
        <div className="px-4 py-2 border-t border-white/5 text-xs text-zinc-500 flex items-center justify-between bg-black/20">
          <span>
            {activeArtifact.type} • Created {activeArtifact.createdAt ? new Date(activeArtifact.createdAt).toLocaleString() : 'Unknown'}
          </span>
          <span>{(activeArtifact.content || '').length} characters</span>
        </div>
      )}
    </div>
  );
}

function SmartCanvasRenderer({ artifact }: { artifact: Artifact }) {
    // Render the structured layout
    const sections = artifact.structure?.sections || [];
    
    return (
        <div className="min-h-full bg-white text-black p-8 shadow-lg mx-auto max-w-[210mm] relative grid grid-cols-12 gap-4">
            {sections.map(section => (
                <div 
                    key={section.id}
                    className={`
                        relative border border-transparent hover:border-zinc-300 transition-all group p-4
                        ${getSectionClass(section.region)}
                    `}
                    style={section.style as React.CSSProperties}
                >
                    <div className="absolute top-0 right-0 opacity-0 group-hover:opacity-100 bg-zinc-100 text-zinc-800 text-[10px] px-1 uppercase font-bold">
                        {section.region}
                    </div>
                    
                    {section.type === 'image' ? (
                        /* eslint-disable-next-line @next/next/no-img-element */
                        <img src={section.content} alt={section.title || 'Document image'} className="max-w-full h-auto" loading="lazy" />
                    ) : (
                         <SafeHtmlProse content={section.content} dark={false} />
                    )}
                </div>
            ))}
            
            {sections.length === 0 && (
                <div className="col-span-12 flex items-center justify-center h-96 text-zinc-400 border-2 border-dashed border-zinc-200 rounded-xl">
                    <p>Empty Canvas. Ask Verridian to add sections.</p>
                </div>
            )}
        </div>
    );
}

function getSectionClass(region: string) {
    switch(region) {
        case 'header': return 'col-span-12 border-b-2 border-black pb-4 mb-4';
        case 'footer': return 'col-span-12 border-t pt-4 mt-8 self-end';
        case 'sidebar-left': return 'col-span-3 bg-zinc-50 h-full';
        case 'sidebar-right': return 'col-span-3 bg-zinc-50 h-full';
        case 'main': return 'col-span-9'; // Default to 9 if sidebar exists, logic can be smarter
        default: return 'col-span-12';
    }
}

// ... existing helper functions ...
function ArtifactContent({ artifact, highlighterMode }: { artifact: Artifact, highlighterMode: boolean }) {
  const content = artifact.content || '';
  
  // ... (Wrap existing return logic) ...
    if (artifact.type === 'code') {
    return (
      <div className="h-full overflow-auto">
        <pre className="p-4 text-sm font-mono text-zinc-300 whitespace-pre-wrap">
          <code>{content}</code>
        </pre>
      </div>
    );
  }

  if (artifact.type === 'html') {
    return (
      <div className="h-full overflow-auto p-4">
        <SafeHtmlProse
          content={content}
          className={highlighterMode ? 'cursor-text selection:bg-yellow-500/50' : ''}
        />
      </div>
    );
  }

  // Default: markdown/text
  return (
    <div className="h-full overflow-auto p-4">
      <div className={`prose prose-invert prose-sm max-w-none whitespace-pre-wrap ${highlighterMode ? 'cursor-text selection:bg-yellow-500/50' : ''}`}>
        {content}
      </div>
    </div>
  );
}

function getArtifactIcon(artifact: Artifact) {
  switch (artifact.type) {
    case 'code':
      return <Code className="w-4 h-4 text-green-400" />;
    case 'letter':
    case 'document':
      return <FileText className="w-4 h-4 text-cyan-400" />;
    case 'pdf':
      return <File className="w-4 h-4 text-red-400" />;
    default:
      return <FileText className="w-4 h-4 text-zinc-400" />;
  }
}


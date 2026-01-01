'use client';

import React, { useState, useEffect } from 'react';
import { Workflow, CheckCircle, Clock, Loader2, AlertCircle, Play, Pause, RotateCcw } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

type StageStatus = 'pending' | 'running' | 'complete' | 'error';

interface PipelineStage {
  id: string;
  name: string;
  description: string;
  status: StageStatus;
  progress: number;
  duration?: number;
}

const INITIAL_STAGES: PipelineStage[] = [
  { id: '1', name: 'Document Parsing', description: 'Extract text from uploaded documents', status: 'pending', progress: 0 },
  { id: '2', name: 'Entity Extraction', description: 'Identify actors, organizations, and courts', status: 'pending', progress: 0 },
  { id: '3', name: 'Event Detection', description: 'Extract temporal events and relationships', status: 'pending', progress: 0 },
  { id: '4', name: 'Relationship Mapping', description: 'Build entity relationship graph', status: 'pending', progress: 0 },
  { id: '5', name: 'GSW Integration', description: 'Integrate into Global Semantic Workspace', status: 'pending', progress: 0 },
  { id: '6', name: 'VSA Validation', description: 'Validate with Vector Symbolic Architecture', status: 'pending', progress: 0 },
];

export default function PipelinePage() {
  const [stages, setStages] = useState<PipelineStage[]>(INITIAL_STAGES);
  const [isRunning, setIsRunning] = useState(false);
  const [currentStage, setCurrentStage] = useState<number>(-1);

  const runPipeline = () => {
    setIsRunning(true);
    setCurrentStage(0);
    setStages(INITIAL_STAGES.map(s => ({ ...s, status: 'pending', progress: 0 })));
  };

  const resetPipeline = () => {
    setIsRunning(false);
    setCurrentStage(-1);
    setStages(INITIAL_STAGES);
  };

  useEffect(() => {
    if (!isRunning || currentStage < 0 || currentStage >= stages.length) return;

    // Start current stage
    setStages(prev => prev.map((s, i) => i === currentStage ? { ...s, status: 'running' } : s));

    // Simulate progress
    const interval = setInterval(() => {
      setStages(prev => prev.map((s, i) => {
        if (i !== currentStage) return s;
        const newProgress = Math.min(s.progress + Math.random() * 15, 100);
        return { ...s, progress: newProgress };
      }));
    }, 200);

    // Complete after delay
    const timeout = setTimeout(() => {
      clearInterval(interval);
      setStages(prev => prev.map((s, i) =>
        i === currentStage ? { ...s, status: 'complete', progress: 100, duration: Math.floor(Math.random() * 3000) + 1000 } : s
      ));
      if (currentStage < stages.length - 1) {
        setCurrentStage(currentStage + 1);
      } else {
        setIsRunning(false);
      }
    }, 2000 + Math.random() * 1500);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [isRunning, currentStage, stages.length]);

  const completedCount = stages.filter(s => s.status === 'complete').length;

  return (
    <FeaturePageLayout
      title="Pipeline Monitor"
      description="Real-time pipeline execution with stage-by-stage progress tracking"
      icon={<Workflow className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="emerald"
    >
      {/* Controls */}
      <div className="flex flex-wrap gap-3 mb-6">
        {!isRunning ? (
          <button
            onClick={runPipeline}
            className="flex items-center gap-2 h-11 px-5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium transition-colors touch-target"
          >
            <Play className="w-4 h-4" />
            Run Pipeline
          </button>
        ) : (
          <button
            onClick={() => setIsRunning(false)}
            className="flex items-center gap-2 h-11 px-5 bg-amber-600 hover:bg-amber-500 text-white rounded-xl font-medium transition-colors touch-target"
          >
            <Pause className="w-4 h-4" />
            Pause
          </button>
        )}
        <button
          onClick={resetPipeline}
          className="flex items-center gap-2 h-11 px-5 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl font-medium transition-colors touch-target"
        >
          <RotateCcw className="w-4 h-4" />
          Reset
        </button>
      </div>

      {/* Progress Overview */}
      <div className="p-4 bg-zinc-900/50 rounded-xl border border-white/10 mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-zinc-400">Overall Progress</span>
          <span className="text-sm font-medium text-white">{completedCount}/{stages.length} stages</span>
        </div>
        <div className="h-3 bg-zinc-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-emerald-500 transition-all duration-300"
            style={{ width: `${(completedCount / stages.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Pipeline Stages */}
      <div className="space-y-3">
        {stages.map((stage, index) => (
          <StageCard key={stage.id} stage={stage} index={index} />
        ))}
      </div>
    </FeaturePageLayout>
  );
}

function StageCard({ stage, index }: { stage: PipelineStage; index: number }) {
  const statusConfig = {
    pending: { icon: <Clock className="w-4 h-4" />, color: 'zinc', label: 'Pending' },
    running: { icon: <Loader2 className="w-4 h-4 animate-spin" />, color: 'amber', label: 'Running' },
    complete: { icon: <CheckCircle className="w-4 h-4" />, color: 'emerald', label: 'Complete' },
    error: { icon: <AlertCircle className="w-4 h-4" />, color: 'red', label: 'Error' },
  };

  const config = statusConfig[stage.status];

  return (
    <div className={`p-4 rounded-xl border transition-all ${
      stage.status === 'running' ? 'bg-amber-500/5 border-amber-500/30' :
      stage.status === 'complete' ? 'bg-emerald-500/5 border-emerald-500/30' :
      'bg-zinc-900/50 border-white/10'
    }`}>
      <div className="flex items-start gap-3">
        <div className={`w-8 h-8 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-${config.color}-500/20`}>
          <span className={`text-${config.color}-400`}>{config.icon}</span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs text-zinc-500">Stage {index + 1}</span>
            <span className={`text-xs px-2 py-0.5 rounded-full bg-${config.color}-500/20 text-${config.color}-400`}>
              {config.label}
            </span>
            {stage.duration && (
              <span className="text-xs text-zinc-500">{(stage.duration / 1000).toFixed(1)}s</span>
            )}
          </div>
          <h4 className="text-sm sm:text-base font-medium text-white">{stage.name}</h4>
          <p className="text-xs text-zinc-400 mt-0.5">{stage.description}</p>

          {stage.status === 'running' && (
            <div className="mt-2 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-amber-500 transition-all duration-200"
                style={{ width: `${stage.progress}%` }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

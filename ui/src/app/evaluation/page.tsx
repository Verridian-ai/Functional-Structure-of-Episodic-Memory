'use client';

import React, { useState } from 'react';
import { BarChart3, TrendingUp, TrendingDown, Target, CheckCircle, AlertTriangle, RefreshCw } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface Metric {
  name: string;
  value: number;
  target: number;
  trend: 'up' | 'down' | 'stable';
  change: number;
  description: string;
}

const METRICS: Metric[] = [
  { name: 'Precision', value: 0.92, target: 0.90, trend: 'up', change: 2.1, description: 'Accuracy of extracted entities' },
  { name: 'Recall', value: 0.87, target: 0.85, trend: 'up', change: 1.5, description: 'Coverage of relevant entities' },
  { name: 'F1 Score', value: 0.89, target: 0.87, trend: 'up', change: 1.8, description: 'Harmonic mean of precision & recall' },
  { name: 'Legal Accuracy', value: 0.95, target: 0.92, trend: 'stable', change: 0.2, description: 'Correctness of legal interpretations' },
  { name: 'Relationship Accuracy', value: 0.84, target: 0.80, trend: 'up', change: 3.2, description: 'Accuracy of entity relationships' },
  { name: 'Temporal Accuracy', value: 0.91, target: 0.88, trend: 'down', change: -0.8, description: 'Accuracy of date/time extractions' },
];

export default function EvaluationPage() {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('7d');

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1500);
  };

  const overallScore = (METRICS.reduce((sum, m) => sum + m.value, 0) / METRICS.length * 100).toFixed(1);
  const metricsAboveTarget = METRICS.filter(m => m.value >= m.target).length;

  return (
    <FeaturePageLayout
      title="Evaluation Dashboard"
      description="6-metric evaluation system with precision, recall, and legal accuracy"
      icon={<BarChart3 className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="amber"
    >
      {/* Header Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
        {/* Time Range Toggle */}
        <div className="flex bg-zinc-800/50 rounded-xl p-1">
          {(['24h', '7d', '30d'] as const).map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`flex-1 sm:flex-none px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all touch-target ${
                timeRange === range ? 'bg-amber-500/20 text-amber-400' : 'text-zinc-400 hover:text-white'
              }`}
            >
              {range === '24h' ? 'Last 24h' : range === '7d' ? 'Last 7 Days' : 'Last 30 Days'}
            </button>
          ))}
        </div>

        {/* Refresh Button */}
        <button
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="flex items-center justify-center gap-2 h-10 sm:h-11 px-4 bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50 text-white rounded-xl font-medium transition-colors touch-target"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Overall Score Card */}
      <div className="p-4 sm:p-6 bg-gradient-to-r from-amber-500/10 to-transparent border border-amber-500/20 rounded-2xl mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-sm text-zinc-400 mb-1">Overall Performance Score</h2>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl sm:text-5xl font-bold text-white">{overallScore}%</span>
              <span className="text-sm text-emerald-400 flex items-center gap-1">
                <TrendingUp className="w-4 h-4" />
                +1.4%
              </span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-400">{metricsAboveTarget}</div>
              <div className="text-xs text-zinc-400">Above Target</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-amber-400">{METRICS.length - metricsAboveTarget}</div>
              <div className="text-xs text-zinc-400">Below Target</div>
            </div>
          </div>
        </div>
      </div>

      {/* Metrics Grid - Mobile First */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
        {METRICS.map((metric) => (
          <MetricCard key={metric.name} metric={metric} />
        ))}
      </div>

      {/* Performance Chart Placeholder */}
      <div className="mt-6 sm:mt-8 p-4 sm:p-6 bg-zinc-900/50 rounded-2xl border border-white/10">
        <h3 className="text-sm sm:text-base font-medium text-white mb-4">Performance Trend</h3>
        <div className="h-48 sm:h-64 flex items-center justify-center border border-dashed border-zinc-700 rounded-xl">
          <div className="text-center">
            <BarChart3 className="w-10 h-10 sm:w-12 sm:h-12 text-zinc-600 mx-auto mb-2" />
            <p className="text-sm text-zinc-500">Interactive chart visualization</p>
            <p className="text-xs text-zinc-600 mt-1">Coming with data integration</p>
          </div>
        </div>
      </div>

      {/* Recent Evaluations */}
      <div className="mt-6 sm:mt-8">
        <h3 className="text-sm sm:text-base font-medium text-white mb-4">Recent Evaluations</h3>
        <div className="space-y-2">
          {[
            { id: '1', doc: 'Smith v Smith [2024] FamCA 123', score: 94, date: '2 hours ago', status: 'pass' },
            { id: '2', doc: 'Jones Family Trust Matter', score: 87, date: '5 hours ago', status: 'pass' },
            { id: '3', doc: 'Brown Property Settlement', score: 91, date: '1 day ago', status: 'pass' },
            { id: '4', doc: 'Wilson Parenting Orders', score: 78, date: '2 days ago', status: 'warn' },
          ].map((evaluation) => (
            <div
              key={evaluation.id}
              className="flex items-center gap-3 p-3 sm:p-4 bg-zinc-900/50 rounded-xl border border-white/10"
            >
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                evaluation.status === 'pass' ? 'bg-emerald-500/20' : 'bg-amber-500/20'
              }`}>
                {evaluation.status === 'pass' ? (
                  <CheckCircle className="w-5 h-5 text-emerald-400" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-amber-400" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">{evaluation.doc}</p>
                <p className="text-xs text-zinc-500">{evaluation.date}</p>
              </div>
              <div className="text-right flex-shrink-0">
                <div className={`text-lg font-bold ${
                  evaluation.score >= 90 ? 'text-emerald-400' : evaluation.score >= 80 ? 'text-amber-400' : 'text-red-400'
                }`}>
                  {evaluation.score}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </FeaturePageLayout>
  );
}

function MetricCard({ metric }: { metric: Metric }) {
  const percentage = metric.value * 100;
  const targetPercentage = metric.target * 100;
  const isAboveTarget = metric.value >= metric.target;

  return (
    <div className={`p-4 rounded-xl border transition-all ${
      isAboveTarget ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-amber-500/5 border-amber-500/20'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-medium text-white">{metric.name}</h4>
        <div className={`flex items-center gap-1 text-xs ${
          metric.trend === 'up' ? 'text-emerald-400' :
          metric.trend === 'down' ? 'text-red-400' : 'text-zinc-400'
        }`}>
          {metric.trend === 'up' ? <TrendingUp className="w-3 h-3" /> :
           metric.trend === 'down' ? <TrendingDown className="w-3 h-3" /> : null}
          {metric.change > 0 ? '+' : ''}{metric.change}%
        </div>
      </div>

      {/* Value */}
      <div className="flex items-baseline gap-2 mb-2">
        <span className={`text-2xl sm:text-3xl font-bold ${isAboveTarget ? 'text-emerald-400' : 'text-amber-400'}`}>
          {percentage.toFixed(1)}%
        </span>
        <span className="text-xs text-zinc-500 flex items-center gap-1">
          <Target className="w-3 h-3" />
          {targetPercentage}%
        </span>
      </div>

      {/* Progress Bar */}
      <div className="h-2 bg-zinc-800 rounded-full overflow-hidden mb-2">
        <div
          className={`h-full transition-all duration-500 ${isAboveTarget ? 'bg-emerald-500' : 'bg-amber-500'}`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>

      {/* Description */}
      <p className="text-[10px] sm:text-xs text-zinc-500">{metric.description}</p>
    </div>
  );
}

'use client';

import React, { useState } from 'react';
import { Clock, TrendingUp, TrendingDown, Calendar, BarChart3 } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface BenchmarkRun {
  id: string;
  date: string;
  precision: number;
  recall: number;
  f1: number;
  legalAccuracy: number;
  documentsProcessed: number;
  duration: string;
}

const MOCK_RUNS: BenchmarkRun[] = [
  { id: '1', date: '2024-12-01', precision: 92.1, recall: 87.3, f1: 89.6, legalAccuracy: 95.2, documentsProcessed: 150, duration: '2h 15m' },
  { id: '2', date: '2024-11-24', precision: 91.8, recall: 86.9, f1: 89.3, legalAccuracy: 94.8, documentsProcessed: 150, duration: '2h 22m' },
  { id: '3', date: '2024-11-17', precision: 90.5, recall: 85.2, f1: 87.8, legalAccuracy: 93.5, documentsProcessed: 145, duration: '2h 18m' },
  { id: '4', date: '2024-11-10', precision: 89.2, recall: 84.1, f1: 86.6, legalAccuracy: 92.1, documentsProcessed: 140, duration: '2h 05m' },
];

export default function BenchmarkPage() {
  const [runs] = useState<BenchmarkRun[]>(MOCK_RUNS);
  const latestRun = runs[0];
  const previousRun = runs[1];

  const getChange = (current: number, previous: number) => {
    const change = current - previous;
    return { value: change.toFixed(1), isPositive: change >= 0 };
  };

  return (
    <FeaturePageLayout
      title="Benchmarking"
      description="Continuous accuracy tracking with historical metrics and trends"
      icon={<Clock className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="amber"
    >
      {/* Latest Run Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {[
          { label: 'Precision', value: latestRun.precision, prev: previousRun.precision },
          { label: 'Recall', value: latestRun.recall, prev: previousRun.recall },
          { label: 'F1 Score', value: latestRun.f1, prev: previousRun.f1 },
          { label: 'Legal Accuracy', value: latestRun.legalAccuracy, prev: previousRun.legalAccuracy },
        ].map((metric) => {
          const change = getChange(metric.value, metric.prev);
          return (
            <div key={metric.label} className="p-3 sm:p-4 bg-zinc-900/50 rounded-xl border border-white/10">
              <div className="text-xl sm:text-2xl font-bold text-white">{metric.value}%</div>
              <div className="flex items-center gap-1 mt-1">
                <span className="text-[10px] sm:text-xs text-zinc-400">{metric.label}</span>
                <span className={`text-[10px] flex items-center gap-0.5 ${change.isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
                  {change.isPositive ? <TrendingUp className="w-2.5 h-2.5" /> : <TrendingDown className="w-2.5 h-2.5" />}
                  {change.isPositive ? '+' : ''}{change.value}%
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Chart Placeholder */}
      <div className="p-4 sm:p-6 bg-zinc-900/50 rounded-2xl border border-white/10 mb-6">
        <h3 className="text-sm sm:text-base font-medium text-white mb-4">Accuracy Trend</h3>
        <div className="h-40 sm:h-56 flex items-center justify-center border border-dashed border-zinc-700 rounded-xl">
          <div className="text-center">
            <BarChart3 className="w-10 h-10 text-zinc-600 mx-auto mb-2" />
            <p className="text-sm text-zinc-500">Trend visualization</p>
          </div>
        </div>
      </div>

      {/* Historical Runs */}
      <h3 className="text-sm font-medium text-zinc-400 mb-3">Historical Runs</h3>
      <div className="space-y-2">
        {runs.map((run) => (
          <div key={run.id} className="flex items-center gap-3 p-3 sm:p-4 bg-zinc-900/50 rounded-xl border border-white/10">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 flex items-center justify-center flex-shrink-0">
              <Calendar className="w-5 h-5 text-amber-400" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white">{new Date(run.date).toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' })}</p>
              <p className="text-xs text-zinc-500">{run.documentsProcessed} documents • {run.duration}</p>
            </div>
            <div className="text-right flex-shrink-0">
              <div className="text-lg font-bold text-emerald-400">{run.f1}%</div>
              <div className="text-[10px] text-zinc-500">F1 Score</div>
            </div>
          </div>
        ))}
      </div>
    </FeaturePageLayout>
  );
}

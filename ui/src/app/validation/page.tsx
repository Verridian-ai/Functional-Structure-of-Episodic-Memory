'use client';

import React, { useState } from 'react';
import { Shield, CheckCircle, AlertTriangle, XCircle, Search, RefreshCw } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface ValidationResult {
  id: string;
  claim: string;
  status: 'verified' | 'warning' | 'failed';
  confidence: number;
  source?: string;
  details: string;
}

const MOCK_RESULTS: ValidationResult[] = [
  { id: '1', claim: 'Marriage date: 15 March 2010', status: 'verified', confidence: 98, source: 'Marriage Certificate', details: 'Confirmed via document extraction' },
  { id: '2', claim: 'Separation date: 1 June 2023', status: 'verified', confidence: 95, source: 'Affidavit para 12', details: 'Consistent across multiple documents' },
  { id: '3', claim: 'Property value: $1.2M', status: 'warning', confidence: 72, source: 'Valuation Report', details: 'Value discrepancy detected between parties' },
  { id: '4', claim: 'Child custody arrangement', status: 'verified', confidence: 88, source: 'Interim Orders', details: 'Matched with court orders' },
  { id: '5', claim: 'Income: $150,000 p.a.', status: 'failed', confidence: 45, source: 'Financial Statement', details: 'Inconsistent with tax records' },
];

export default function ValidationPage() {
  const [results] = useState<ValidationResult[]>(MOCK_RESULTS);
  const [filter, setFilter] = useState<'all' | 'verified' | 'warning' | 'failed'>('all');

  const filteredResults = filter === 'all' ? results : results.filter(r => r.status === filter);
  const verifiedCount = results.filter(r => r.status === 'verified').length;
  const warningCount = results.filter(r => r.status === 'warning').length;
  const failedCount = results.filter(r => r.status === 'failed').length;

  return (
    <FeaturePageLayout
      title="VSA Validator"
      description="Vector Symbolic Architecture for anti-hallucination verification"
      icon={<Shield className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="cyan"
    >
      {/* Stats */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        <button onClick={() => setFilter('verified')} className={`p-3 sm:p-4 rounded-xl border transition-all touch-target ${filter === 'verified' ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-zinc-900/50 border-white/10'}`}>
          <div className="text-xl sm:text-2xl font-bold text-emerald-400">{verifiedCount}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Verified</div>
        </button>
        <button onClick={() => setFilter('warning')} className={`p-3 sm:p-4 rounded-xl border transition-all touch-target ${filter === 'warning' ? 'bg-amber-500/10 border-amber-500/30' : 'bg-zinc-900/50 border-white/10'}`}>
          <div className="text-xl sm:text-2xl font-bold text-amber-400">{warningCount}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Warnings</div>
        </button>
        <button onClick={() => setFilter('failed')} className={`p-3 sm:p-4 rounded-xl border transition-all touch-target ${filter === 'failed' ? 'bg-red-500/10 border-red-500/30' : 'bg-zinc-900/50 border-white/10'}`}>
          <div className="text-xl sm:text-2xl font-bold text-red-400">{failedCount}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Failed</div>
        </button>
      </div>

      {/* Filter Reset */}
      {filter !== 'all' && (
        <button onClick={() => setFilter('all')} className="text-xs text-cyan-400 mb-4 flex items-center gap-1">
          <RefreshCw className="w-3 h-3" /> Show all results
        </button>
      )}

      {/* Results */}
      <div className="space-y-3">
        {filteredResults.map((result) => (
          <ValidationCard key={result.id} result={result} />
        ))}
      </div>
    </FeaturePageLayout>
  );
}

function ValidationCard({ result }: { result: ValidationResult }) {
  const config = {
    verified: { icon: <CheckCircle className="w-5 h-5" />, color: 'emerald', label: 'Verified' },
    warning: { icon: <AlertTriangle className="w-5 h-5" />, color: 'amber', label: 'Warning' },
    failed: { icon: <XCircle className="w-5 h-5" />, color: 'red', label: 'Failed' },
  }[result.status];

  return (
    <div className={`p-4 rounded-xl border bg-${config.color}-500/5 border-${config.color}-500/20`}>
      <div className="flex items-start gap-3">
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-${config.color}-500/20`}>
          <span className={`text-${config.color}-400`}>{config.icon}</span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs px-2 py-0.5 rounded-full bg-${config.color}-500/20 text-${config.color}-400`}>
              {config.label}
            </span>
            <span className="text-xs text-zinc-500">{result.confidence}% confidence</span>
          </div>
          <p className="text-sm font-medium text-white mb-1">{result.claim}</p>
          <p className="text-xs text-zinc-400">{result.details}</p>
          {result.source && (
            <p className="text-xs text-zinc-500 mt-1">Source: {result.source}</p>
          )}
        </div>
      </div>
    </div>
  );
}

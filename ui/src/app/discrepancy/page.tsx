'use client';

import React, { useState } from 'react';
import { AlertTriangle, Calendar, DollarSign, User, FileText, ChevronRight } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface Discrepancy {
  id: string;
  type: 'date' | 'amount' | 'entity' | 'fact';
  severity: 'high' | 'medium' | 'low';
  field: string;
  value1: { text: string; source: string };
  value2: { text: string; source: string };
  description: string;
}

const MOCK_DISCREPANCIES: Discrepancy[] = [
  { id: '1', type: 'date', severity: 'high', field: 'Separation Date', value1: { text: '1 June 2023', source: 'Applicant Affidavit' }, value2: { text: '15 May 2023', source: 'Respondent Affidavit' }, description: '16-day discrepancy in separation date' },
  { id: '2', type: 'amount', severity: 'high', field: 'Property Value', value1: { text: '$1,200,000', source: 'Applicant Valuation' }, value2: { text: '$950,000', source: 'Respondent Valuation' }, description: '$250,000 difference in property valuation' },
  { id: '3', type: 'entity', severity: 'medium', field: 'Witness Name', value1: { text: 'Dr. Sarah Wilson', source: 'Document A' }, value2: { text: 'Dr. S. Williams', source: 'Document B' }, description: 'Potential name mismatch for expert witness' },
  { id: '4', type: 'fact', severity: 'low', field: 'Employment Status', value1: { text: 'Full-time employed', source: 'Financial Statement' }, value2: { text: 'Part-time employed', source: 'Tax Return' }, description: 'Inconsistent employment status reported' },
];

const TYPE_ICONS = {
  date: <Calendar className="w-4 h-4" />,
  amount: <DollarSign className="w-4 h-4" />,
  entity: <User className="w-4 h-4" />,
  fact: <FileText className="w-4 h-4" />,
};

export default function DiscrepancyPage() {
  const [discrepancies] = useState<Discrepancy[]>(MOCK_DISCREPANCIES);
  const [filter, setFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all');

  const filtered = filter === 'all' ? discrepancies : discrepancies.filter(d => d.severity === filter);
  const highCount = discrepancies.filter(d => d.severity === 'high').length;

  return (
    <FeaturePageLayout
      title="Discrepancy Detection"
      description="Span-level conflict detection for dates, amounts, and entity references"
      icon={<AlertTriangle className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="red"
    >
      {/* Stats */}
      <div className="grid grid-cols-4 gap-2 sm:gap-3 mb-6">
        {(['all', 'high', 'medium', 'low'] as const).map((severity) => {
          const count = severity === 'all' ? discrepancies.length : discrepancies.filter(d => d.severity === severity).length;
          const colors = { all: 'zinc', high: 'red', medium: 'amber', low: 'emerald' };
          return (
            <button
              key={severity}
              onClick={() => setFilter(severity)}
              className={`p-2 sm:p-3 rounded-xl border transition-all touch-target ${
                filter === severity ? `bg-${colors[severity]}-500/10 border-${colors[severity]}-500/30` : 'bg-zinc-900/50 border-white/10'
              }`}
            >
              <div className={`text-lg sm:text-xl font-bold text-${colors[severity]}-400`}>{count}</div>
              <div className="text-[9px] sm:text-xs text-zinc-400 capitalize">{severity}</div>
            </button>
          );
        })}
      </div>

      {/* Discrepancies */}
      <div className="space-y-3">
        {filtered.map((d) => {
          const colors = { high: 'red', medium: 'amber', low: 'emerald' };
          return (
            <div key={d.id} className={`p-4 rounded-xl border bg-${colors[d.severity]}-500/5 border-${colors[d.severity]}-500/20`}>
              <div className="flex items-start gap-3">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-${colors[d.severity]}-500/20`}>
                  <span className={`text-${colors[d.severity]}-400`}>{TYPE_ICONS[d.type]}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-xs px-2 py-0.5 rounded-full bg-${colors[d.severity]}-500/20 text-${colors[d.severity]}-400 capitalize`}>
                      {d.severity}
                    </span>
                    <span className="text-xs text-zinc-500 capitalize">{d.type}</span>
                  </div>
                  <h4 className="text-sm font-medium text-white">{d.field}</h4>
                  <p className="text-xs text-zinc-400 mt-1">{d.description}</p>

                  {/* Comparison */}
                  <div className="mt-3 grid grid-cols-2 gap-2">
                    <div className="p-2 bg-zinc-800/50 rounded-lg">
                      <p className="text-xs text-zinc-500 mb-0.5">{d.value1.source}</p>
                      <p className="text-sm text-white">{d.value1.text}</p>
                    </div>
                    <div className="p-2 bg-zinc-800/50 rounded-lg">
                      <p className="text-xs text-zinc-500 mb-0.5">{d.value2.source}</p>
                      <p className="text-sm text-white">{d.value2.text}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </FeaturePageLayout>
  );
}

'use client';

import React, { useState } from 'react';
import { CheckCircle, BookOpen, Search, ExternalLink, AlertCircle } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface StatutoryAlignment {
  id: string;
  extraction: string;
  statute: string;
  section: string;
  alignmentScore: number;
  status: 'aligned' | 'partial' | 'misaligned';
  notes: string;
}

const MOCK_ALIGNMENTS: StatutoryAlignment[] = [
  { id: '1', extraction: 'Primary residence of child with mother', statute: 'Family Law Act 1975', section: 's 61DA', alignmentScore: 95, status: 'aligned', notes: 'Consistent with presumption of equal shared parental responsibility' },
  { id: '2', extraction: 'Property division 60/40', statute: 'Family Law Act 1975', section: 's 79', alignmentScore: 88, status: 'aligned', notes: 'Proper application of contribution factors' },
  { id: '3', extraction: 'Interim spousal maintenance ordered', statute: 'Family Law Act 1975', section: 's 72', alignmentScore: 72, status: 'partial', notes: 'Needs consideration of s 75(2) factors' },
  { id: '4', extraction: 'Child support calculated at $500/week', statute: 'Child Support (Assessment) Act 1989', section: 's 35', alignmentScore: 45, status: 'misaligned', notes: 'Does not follow formula calculation method' },
];

export default function StatutoryPage() {
  const [alignments] = useState<StatutoryAlignment[]>(MOCK_ALIGNMENTS);
  const [search, setSearch] = useState('');

  const filtered = alignments.filter(a =>
    a.extraction.toLowerCase().includes(search.toLowerCase()) ||
    a.statute.toLowerCase().includes(search.toLowerCase())
  );

  const alignedCount = alignments.filter(a => a.status === 'aligned').length;
  const avgScore = Math.round(alignments.reduce((sum, a) => sum + a.alignmentScore, 0) / alignments.length);

  return (
    <FeaturePageLayout
      title="Statutory Alignment"
      description="Validate extractions against statutory corpus with compliance scoring"
      icon={<CheckCircle className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="emerald"
    >
      {/* Stats */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        <div className="p-3 sm:p-4 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
          <div className="text-xl sm:text-2xl font-bold text-emerald-400">{alignedCount}/{alignments.length}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Aligned</div>
        </div>
        <div className="p-3 sm:p-4 bg-zinc-900/50 rounded-xl border border-white/10">
          <div className="text-xl sm:text-2xl font-bold text-white">{avgScore}%</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Avg Score</div>
        </div>
        <div className="p-3 sm:p-4 bg-zinc-900/50 rounded-xl border border-white/10">
          <div className="text-xl sm:text-2xl font-bold text-white">2</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Statutes</div>
        </div>
      </div>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
        <input
          type="text"
          placeholder="Search extractions or statutes..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full h-11 pl-10 pr-4 bg-zinc-900/50 border border-white/10 rounded-xl text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-emerald-500/50"
        />
      </div>

      {/* Alignments */}
      <div className="space-y-3">
        {filtered.map((a) => {
          const colors = { aligned: 'emerald', partial: 'amber', misaligned: 'red' };
          const icons = {
            aligned: <CheckCircle className="w-4 h-4" />,
            partial: <AlertCircle className="w-4 h-4" />,
            misaligned: <AlertCircle className="w-4 h-4" />,
          };

          return (
            <div key={a.id} className={`p-4 rounded-xl border bg-${colors[a.status]}-500/5 border-${colors[a.status]}-500/20`}>
              <div className="flex items-start gap-3">
                <div className={`w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center flex-shrink-0 bg-${colors[a.status]}-500/20`}>
                  <span className={`text-${colors[a.status]}-400`}>{icons[a.status]}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-xs px-2 py-0.5 rounded-full bg-${colors[a.status]}-500/20 text-${colors[a.status]}-400 capitalize`}>
                      {a.alignmentScore}% - {a.status}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-white mb-1">{a.extraction}</p>

                  {/* Statute Reference */}
                  <div className="flex items-center gap-2 mt-2 p-2 bg-zinc-800/50 rounded-lg">
                    <BookOpen className="w-4 h-4 text-zinc-400 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-white truncate">{a.statute}</p>
                      <p className="text-[10px] text-zinc-500">{a.section}</p>
                    </div>
                    <ExternalLink className="w-3 h-3 text-zinc-500 flex-shrink-0" />
                  </div>

                  <p className="text-xs text-zinc-400 mt-2">{a.notes}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </FeaturePageLayout>
  );
}

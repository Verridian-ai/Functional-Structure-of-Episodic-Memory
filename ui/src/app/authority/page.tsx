'use client';

import React, { useState } from 'react';
import { Scale, TrendingUp, Award, Building, ChevronDown, Star } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface AuthorityScore {
  id: string;
  citation: string;
  court: string;
  courtLevel: number;
  boostScore: number;
  bindingStatus: 'binding' | 'persuasive' | 'distinguishable';
  citationCount: number;
  year: number;
}

const MOCK_SCORES: AuthorityScore[] = [
  { id: '1', citation: 'Stanford v Stanford [2012] HCA 52', court: 'High Court', courtLevel: 5, boostScore: 98, bindingStatus: 'binding', citationCount: 1250, year: 2012 },
  { id: '2', citation: 'Kennon v Kennon [1997] FamCA 27', court: 'Full Court', courtLevel: 4, boostScore: 92, bindingStatus: 'binding', citationCount: 890, year: 1997 },
  { id: '3', citation: 'Mallet v Mallet [1984] HCA 21', court: 'High Court', courtLevel: 5, boostScore: 95, bindingStatus: 'binding', citationCount: 1100, year: 1984 },
  { id: '4', citation: 'Smith v Smith [2023] FamCA 456', court: 'Family Court', courtLevel: 3, boostScore: 65, bindingStatus: 'persuasive', citationCount: 12, year: 2023 },
  { id: '5', citation: 'Brown v Brown [2022] FedCirFam 123', court: 'Federal Circuit', courtLevel: 2, boostScore: 45, bindingStatus: 'distinguishable', citationCount: 5, year: 2022 },
];

const COURT_HIERARCHY = [
  { level: 5, name: 'High Court of Australia', color: 'amber' },
  { level: 4, name: 'Full Court Family Court', color: 'purple' },
  { level: 3, name: 'Family Court of Australia', color: 'cyan' },
  { level: 2, name: 'Federal Circuit Court', color: 'emerald' },
  { level: 1, name: 'Tribunals', color: 'zinc' },
];

export default function AuthorityPage() {
  const [scores] = useState<AuthorityScore[]>(MOCK_SCORES);
  const [expandedHierarchy, setExpandedHierarchy] = useState(true);

  return (
    <FeaturePageLayout
      title="Authority Scorer"
      description="Court hierarchy precedent binding assessment with BOOST scoring"
      icon={<Scale className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="purple"
    >
      {/* Court Hierarchy */}
      <div className="mb-6">
        <button
          onClick={() => setExpandedHierarchy(!expandedHierarchy)}
          className="flex items-center gap-2 text-sm font-medium text-white mb-3"
        >
          <Building className="w-4 h-4 text-purple-400" />
          Court Hierarchy
          <ChevronDown className={`w-4 h-4 text-zinc-400 transition-transform ${expandedHierarchy ? 'rotate-180' : ''}`} />
        </button>

        {expandedHierarchy && (
          <div className="flex flex-col sm:flex-row gap-2">
            {COURT_HIERARCHY.map((court, idx) => (
              <div key={court.level} className="flex items-center gap-2 flex-1">
                <div className={`w-full p-3 rounded-xl bg-${court.color}-500/10 border border-${court.color}-500/20`}>
                  <div className="flex items-center gap-2">
                    <span className={`text-lg font-bold text-${court.color}-400`}>{court.level}</span>
                    <span className="text-xs text-zinc-300 truncate">{court.name}</span>
                  </div>
                </div>
                {idx < COURT_HIERARCHY.length - 1 && (
                  <span className="text-zinc-600 hidden sm:block">→</span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Authority Cards */}
      <h3 className="text-sm font-medium text-zinc-400 mb-3">Precedent Authority Scores</h3>
      <div className="space-y-3">
        {scores.map((score) => {
          const statusColors = { binding: 'emerald', persuasive: 'amber', distinguishable: 'zinc' };
          return (
            <div key={score.id} className="p-4 rounded-xl border bg-zinc-900/50 border-white/10">
              <div className="flex items-start gap-3">
                <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-xl bg-purple-500/20 flex flex-col items-center justify-center flex-shrink-0">
                  <span className="text-lg sm:text-xl font-bold text-purple-400">{score.boostScore}</span>
                  <span className="text-[8px] text-purple-400/60">BOOST</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <span className={`text-xs px-2 py-0.5 rounded-full bg-${statusColors[score.bindingStatus]}-500/20 text-${statusColors[score.bindingStatus]}-400 capitalize`}>
                      {score.bindingStatus}
                    </span>
                    <span className="text-xs text-zinc-500">Level {score.courtLevel} • {score.court}</span>
                  </div>
                  <h4 className="text-sm font-medium text-white truncate">{score.citation}</h4>
                  <div className="flex items-center gap-3 mt-2 text-xs text-zinc-500">
                    <span className="flex items-center gap-1">
                      <Star className="w-3 h-3" />
                      {score.citationCount} citations
                    </span>
                    <span>{score.year}</span>
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

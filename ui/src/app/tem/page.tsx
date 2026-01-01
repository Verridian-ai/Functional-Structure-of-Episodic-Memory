'use client';

import React, { useState } from 'react';
import { Layers, Search, Network, ArrowRight, Scale, FileText } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface Precedent {
  id: string;
  citation: string;
  name: string;
  similarity: number;
  structuralMatch: string;
  court: string;
  year: number;
  relevance: 'high' | 'medium' | 'low';
}

const MOCK_PRECEDENTS: Precedent[] = [
  { id: '1', citation: '[2023] FamCAFC 156', name: 'Kennon v Kennon', similarity: 94, structuralMatch: 'Property settlement methodology', court: 'Full Court', year: 2023, relevance: 'high' },
  { id: '2', citation: '[2022] FamCA 892', name: 'Rice v Asplund', similarity: 87, structuralMatch: 'Parenting assessment framework', court: 'Family Court', year: 2022, relevance: 'high' },
  { id: '3', citation: '[2021] FamCAFC 78', name: 'Stanford v Stanford', similarity: 82, structuralMatch: 'Superannuation splitting', court: 'Full Court', year: 2021, relevance: 'medium' },
  { id: '4', citation: '[2020] FamCA 445', name: 'Mallet v Mallet', similarity: 76, structuralMatch: 'Special contributions', court: 'Family Court', year: 2020, relevance: 'medium' },
];

export default function TEMPage() {
  const [query, setQuery] = useState('');
  const [precedents] = useState<Precedent[]>(MOCK_PRECEDENTS);

  return (
    <FeaturePageLayout
      title="TEM Reasoning"
      description="Tolman-Eichenbaum Machine for structural legal precedent matching"
      icon={<Layers className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="cyan"
    >
      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
        <input
          type="text"
          placeholder="Describe your legal scenario for precedent matching..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full h-12 pl-11 pr-4 bg-zinc-900/50 border border-white/10 rounded-xl text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-500/50"
        />
      </div>

      {/* How TEM Works */}
      <div className="p-4 bg-cyan-500/5 border border-cyan-500/20 rounded-xl mb-6">
        <h3 className="text-sm font-medium text-white mb-3">How TEM Reasoning Works</h3>
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="px-3 py-1.5 bg-zinc-800 rounded-lg text-zinc-300">Input Scenario</span>
          <ArrowRight className="w-4 h-4 text-cyan-400" />
          <span className="px-3 py-1.5 bg-zinc-800 rounded-lg text-zinc-300">Structural Encoding</span>
          <ArrowRight className="w-4 h-4 text-cyan-400" />
          <span className="px-3 py-1.5 bg-zinc-800 rounded-lg text-zinc-300">Hippocampal Search</span>
          <ArrowRight className="w-4 h-4 text-cyan-400" />
          <span className="px-3 py-1.5 bg-cyan-500/20 text-cyan-400 rounded-lg">Matched Precedents</span>
        </div>
      </div>

      {/* Precedents */}
      <h3 className="text-sm font-medium text-zinc-400 mb-3">Matched Precedents</h3>
      <div className="space-y-3">
        {precedents.map((p) => (
          <div key={p.id} className={`p-4 rounded-xl border ${
            p.relevance === 'high' ? 'bg-cyan-500/5 border-cyan-500/20' : 'bg-zinc-900/50 border-white/10'
          }`}>
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-cyan-500/20 flex items-center justify-center flex-shrink-0">
                <Scale className="w-5 h-5 text-cyan-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs px-2 py-0.5 bg-cyan-500/20 text-cyan-400 rounded-full">{p.similarity}% match</span>
                  <span className="text-xs text-zinc-500">{p.court} • {p.year}</span>
                </div>
                <h4 className="text-sm font-medium text-white">{p.name}</h4>
                <p className="text-xs text-zinc-400">{p.citation}</p>
                <p className="text-xs text-zinc-500 mt-1 flex items-center gap-1">
                  <Network className="w-3 h-3" />
                  Structural: {p.structuralMatch}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </FeaturePageLayout>
  );
}

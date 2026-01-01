'use client';

import React, { useState } from 'react';
import { Database, Plus, Download, Upload, Trash2, Clock, HardDrive, FolderOpen } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface Workspace {
  id: string;
  name: string;
  description: string;
  size: string;
  entities: number;
  events: number;
  lastModified: string;
}

const MOCK_WORKSPACES: Workspace[] = [
  { id: '1', name: 'Smith Family Matter', description: 'Parenting and property case files', size: '24.5 MB', entities: 45, events: 32, lastModified: '2 hours ago' },
  { id: '2', name: 'Jones Trust Dispute', description: 'Trust interpretation matters', size: '18.2 MB', entities: 28, events: 18, lastModified: '1 day ago' },
  { id: '3', name: 'Brown Estate', description: 'Estate administration dispute', size: '31.8 MB', entities: 52, events: 41, lastModified: '3 days ago' },
];

export default function WorkspacePage() {
  const [workspaces] = useState<Workspace[]>(MOCK_WORKSPACES);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  return (
    <FeaturePageLayout
      title="Workspace Manager"
      description="Save, load, and merge GSW workspaces with TOON compression"
      icon={<Database className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="emerald"
    >
      {/* Actions */}
      <div className="flex flex-wrap gap-3 mb-6">
        <button className="flex items-center gap-2 h-11 px-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium transition-colors touch-target">
          <Plus className="w-4 h-4" />
          New Workspace
        </button>
        <button className="flex items-center gap-2 h-11 px-4 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl font-medium transition-colors touch-target">
          <Upload className="w-4 h-4" />
          Import
        </button>
      </div>

      {/* Storage Stats */}
      <div className="p-4 bg-zinc-900/50 rounded-xl border border-white/10 mb-6">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <HardDrive className="w-4 h-4 text-zinc-400" />
            <span className="text-sm text-zinc-400">Storage Used</span>
          </div>
          <span className="text-sm font-medium text-white">74.5 MB / 1 GB</span>
        </div>
        <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
          <div className="h-full bg-emerald-500 w-[7.45%]" />
        </div>
      </div>

      {/* Workspaces */}
      <div className="space-y-3">
        {workspaces.map((ws) => (
          <button
            key={ws.id}
            onClick={() => setSelectedId(selectedId === ws.id ? null : ws.id)}
            className={`w-full text-left p-4 rounded-xl border transition-all touch-target ${
              selectedId === ws.id ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-zinc-900/50 border-white/10 hover:border-white/20'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center flex-shrink-0">
                <FolderOpen className="w-5 h-5 text-emerald-400" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm sm:text-base font-medium text-white">{ws.name}</h3>
                <p className="text-xs text-zinc-400 mt-0.5">{ws.description}</p>
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-2 text-[10px] sm:text-xs text-zinc-500">
                  <span>{ws.entities} entities</span>
                  <span>{ws.events} events</span>
                  <span>{ws.size}</span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{ws.lastModified}</span>
                </div>
              </div>
            </div>

            {selectedId === ws.id && (
              <div className="flex gap-2 mt-4 pt-4 border-t border-white/10">
                <button className="flex-1 h-10 flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition-colors">
                  <FolderOpen className="w-4 h-4" /> Load
                </button>
                <button className="flex-1 h-10 flex items-center justify-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-sm font-medium transition-colors">
                  <Download className="w-4 h-4" /> Export
                </button>
                <button className="h-10 px-3 flex items-center justify-center bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            )}
          </button>
        ))}
      </div>
    </FeaturePageLayout>
  );
}

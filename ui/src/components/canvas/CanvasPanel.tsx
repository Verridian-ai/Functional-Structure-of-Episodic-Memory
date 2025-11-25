'use client';

import React, { useState } from 'react';
import {
  X, Download, Copy, Edit3, Save, FileText, Code, File,
  ChevronLeft, ChevronRight, Trash2, Plus, ExternalLink
} from 'lucide-react';
import { useStore } from '@/lib/store';
import type { Artifact } from '@/types';

export function CanvasPanel() {
  const {
    artifacts,
    activeArtifactId,
    showCanvas,
    setActiveArtifact,
    updateArtifact,
    toggleCanvas,
  } = useStore();

  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState('');

  const activeArtifact = artifacts.find(a => a.id === activeArtifactId);

  if (!showCanvas) return null;

  const handleEdit = () => {
    if (activeArtifact) {
      setEditContent(activeArtifact.content);
      setIsEditing(true);
    }
  };

  const handleSave = () => {
    if (activeArtifact) {
      updateArtifact(activeArtifact.id, { content: editContent });
      setIsEditing(false);
    }
  };

  const handleCopy = async () => {
    if (activeArtifact) {
      await navigator.clipboard.writeText(activeArtifact.content);
    }
  };

  const handleDownload = () => {
    if (activeArtifact) {
      const ext = getFileExtension(activeArtifact);
      const blob = new Blob([activeArtifact.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${activeArtifact.title.replace(/\s+/g, '_')}${ext}`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="h-full flex flex-col bg-blue-950/40 backdrop-blur-xl border-l border-cyan-500/20">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-cyan-500/20">
        <div className="flex items-center gap-3">
          <button
            onClick={toggleCanvas}
            className="p-1.5 hover:bg-blue-900/30 rounded-lg transition"
          >
            <ChevronRight className="w-5 h-5 text-cyan-300/70" />
          </button>
          <h2 className="font-semibold text-white">Canvas</h2>
          <span className="px-2 py-0.5 text-xs bg-blue-900/30 rounded-full text-cyan-300/70 border border-cyan-500/10">
            {artifacts.length} items
          </span>
        </div>

        {activeArtifact && (
          <div className="flex items-center gap-2">
            {isEditing ? (
              <button
                onClick={handleSave}
                className="p-2 hover:bg-green-500/20 text-green-400 rounded-lg transition"
                title="Save changes"
              >
                <Save className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleEdit}
                className="p-2 hover:bg-blue-900/30 text-zinc-400 hover:text-white rounded-lg transition"
                title="Edit"
              >
                <Edit3 className="w-4 h-4" />
              </button>
            )}
            <button
              onClick={handleCopy}
              className="p-2 hover:bg-blue-900/30 text-zinc-400 hover:text-white rounded-lg transition"
              title="Copy"
            >
              <Copy className="w-4 h-4" />
            </button>
            <button
              onClick={handleDownload}
              className="p-2 hover:bg-blue-900/30 text-zinc-400 hover:text-white rounded-lg transition"
              title="Download"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>

      {/* Tabs */}
      {artifacts.length > 0 && (
        <div className="flex items-center gap-1 px-2 py-2 border-b border-cyan-500/20 overflow-x-auto">
          {artifacts.map((artifact) => (
            <button
              key={artifact.id}
              onClick={() => setActiveArtifact(artifact.id)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm whitespace-nowrap transition ${
                artifact.id === activeArtifactId
                  ? 'bg-cyan-600/20 text-cyan-300 border border-cyan-500/30 shadow-lg shadow-cyan-500/10'
                  : 'hover:bg-blue-900/30 text-cyan-300/50 border border-transparent'
              }`}
            >
              {getArtifactIcon(artifact)}
              <span className="max-w-[120px] truncate">{artifact.title}</span>
            </button>
          ))}
        </div>
      )}

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {activeArtifact ? (
          <div className="h-full">
            {isEditing ? (
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full h-full p-4 bg-transparent text-white font-mono text-sm resize-none outline-none"
                spellCheck={false}
              />
            ) : (
              <ArtifactContent artifact={activeArtifact} />
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-cyan-300/30">
            <FileText className="w-12 h-12 mb-4 opacity-50" />
            <p>No artifacts yet</p>
            <p className="text-sm mt-1">Documents, code, and letters will appear here</p>
          </div>
        )}
      </div>

      {/* Footer with metadata */}
      {activeArtifact && (
        <div className="px-4 py-2 border-t border-cyan-500/20 text-xs text-cyan-300/50 flex items-center justify-between bg-blue-900/10">
          <span>
            {activeArtifact.type} • Created {activeArtifact.createdAt.toLocaleString()}
          </span>
          <span>{activeArtifact.content.length} characters</span>
        </div>
      )}
    </div>
  );
}

function ArtifactContent({ artifact }: { artifact: Artifact }) {
  if (artifact.type === 'code') {
    return (
      <div className="h-full overflow-auto">
        <pre className="p-4 text-sm font-mono text-zinc-300 whitespace-pre-wrap">
          <code>{artifact.content}</code>
        </pre>
      </div>
    );
  }

  if (artifact.type === 'html') {
    return (
      <div className="h-full overflow-auto p-4">
        <div
          className="prose prose-invert prose-sm max-w-none"
          dangerouslySetInnerHTML={{ __html: artifact.content }}
        />
      </div>
    );
  }

  // Default: markdown/text
  return (
    <div className="h-full overflow-auto p-4">
      <div className="prose prose-invert prose-sm max-w-none whitespace-pre-wrap">
        {artifact.content}
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

function getFileExtension(artifact: Artifact): string {
  switch (artifact.type) {
    case 'code':
      return artifact.language === 'python' ? '.py' :
             artifact.language === 'javascript' ? '.js' :
             artifact.language === 'typescript' ? '.ts' : '.txt';
    case 'html':
      return '.html';
    case 'markdown':
      return '.md';
    default:
      return '.txt';
  }
}

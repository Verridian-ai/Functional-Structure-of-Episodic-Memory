'use client';

import React, { useState, useRef } from 'react';
import {
  X, Download, Copy, Edit3, Save, FileText, Code, File,
  ChevronLeft, ChevronRight, Trash2, Plus, ExternalLink, Highlighter, Layout, Image as ImageIcon, Type, Grid
} from 'lucide-react';
import { useStore } from '@/lib/store';
import type { Artifact, ArtifactSection } from '@/types';

// Mock NanoBanana Pro Image Generation
const generateImage = async (prompt: string): Promise<string> => {
  // In a real app, call /api/generate-image
  // For demo, return a placeholder based on the prompt hash or similar
  return `https://placehold.co/600x400/1e1e1e/06b6d4?text=${encodeURIComponent(prompt.slice(0, 20))}`;
};

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
  const [highlighterMode, setHighlighterMode] = useState(false);
  const [imagePrompt, setImagePrompt] = useState('');
  const [showImageModal, setShowImageModal] = useState(false);

  const activeArtifact = artifacts.find(a => a.id === activeArtifactId);

  if (!showCanvas) return null;

  const handleEdit = () => {
    if (activeArtifact) {
      setEditContent(activeArtifact.content || '');
      setIsEditing(true);
    }
  };

  const handleSave = () => {
    if (activeArtifact) {
      updateArtifact(activeArtifact.id, { content: editContent });
      setIsEditing(false);
    }
  };

  // ... existing handlers ...
  const handleCopy = async () => {
    if (activeArtifact) {
      await navigator.clipboard.writeText(activeArtifact.content || '');
    }
  };
  
  const handleDownloadDOCX = async () => {
      // ... existing implementation ...
      if (activeArtifact) {
      try {
        const response = await fetch('/api/docx/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: activeArtifact.title, content: activeArtifact.content || '' }),
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${activeArtifact.title.replace(/\s+/g, '_')}.docx`;
          a.click();
          URL.revokeObjectURL(url);
        }
      } catch (error) {
        console.error('DOCX download failed:', error);
      }
    }
  };

  const handleDownloadPDF = async () => {
     // ... existing implementation ...
     if (activeArtifact) {
      try {
        const response = await fetch('/api/pdf/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: activeArtifact.title, content: activeArtifact.content || '' }),
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${activeArtifact.title.replace(/\s+/g, '_')}.pdf`;
          a.click();
          URL.revokeObjectURL(url);
        }
      } catch (error) {
        console.error('PDF download failed:', error);
      }
    }
  };
  
  const handleTextHighlight = () => {
      if (!highlighterMode) return;
      
      const selection = window.getSelection();
      if (!selection || selection.rangeCount === 0) return;
      
      const range = selection.getRangeAt(0);
      const text = range.toString();
      
      if (text) {
          // In a real rich text editor, we would wrap the range. 
          // Here, for simple artifacts, we might just store the comment/highlight.
          console.log("Highlighted:", text);
          // TODO: Persist highlight
      }
  };

  const handleAddImage = async () => {
      if (!activeArtifact) return;
      const url = await generateImage(imagePrompt);
      
      // For now, append markdown image to content
      const imageMarkdown = `\n\n![${imagePrompt}](${url})\n\n`;
      
      updateArtifact(activeArtifact.id, { 
          content: (activeArtifact.content || '') + imageMarkdown
      });
      setShowImageModal(false);
      setImagePrompt('');
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
            
            {/* NanoBanana Image Gen Button */}
             <button
                onClick={() => setShowImageModal(true)}
                className="p-2 hover:bg-yellow-500/20 text-yellow-400 rounded-lg transition"
                title="Generate Image (NanoBanana Pro)"
              >
                <ImageIcon className="w-4 h-4" />
              </button>

            {/* Highlighter Toggle */}
             <button
                onClick={() => setHighlighterMode(!highlighterMode)}
                className={`p-2 rounded-lg transition ${highlighterMode ? 'bg-yellow-500/20 text-yellow-400' : 'hover:bg-blue-900/30 text-zinc-400 hover:text-white'}`}
                title="Highlighter Pen"
              >
                <Highlighter className="w-4 h-4" />
              </button>

            {/* Layout/Grid Toggle (Placeholder for now) */}
             <button
                className="p-2 hover:bg-blue-900/30 text-zinc-400 hover:text-white rounded-lg transition"
                title="Layout Options"
              >
                <Grid className="w-4 h-4" />
              </button>

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
            
            {/* Export Menu */}
            <div className="relative group">
              <button
                className="p-2 hover:bg-blue-900/30 text-zinc-400 hover:text-white rounded-lg transition"
                title="Export"
              >
                <Download className="w-4 h-4" />
              </button>
              <div className="absolute right-0 top-full mt-1 w-32 bg-zinc-900 border border-zinc-800 rounded-lg shadow-xl overflow-hidden opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                <button onClick={handleDownloadDOCX} className="w-full px-3 py-2 text-left text-sm text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  Word (.docx)
                </button>
                <button onClick={handleDownloadPDF} className="w-full px-3 py-2 text-left text-sm text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  PDF (.pdf)
                </button>
                <button onClick={() => {
                    const blob = new Blob([activeArtifact.content || ''], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${activeArtifact.title.replace(/\s+/g, '_')}.txt`;
                    a.click();
                }} className="w-full px-3 py-2 text-left text-sm text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  Text (.txt)
                </button>
              </div>
            </div>

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
      <div className="flex-1 overflow-auto relative" onMouseUp={handleTextHighlight}>
        {activeArtifact ? (
          <div className="h-full">
              
            {/* NanoBanana Modal */}
            {showImageModal && (
                <div className="absolute inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6">
                    <div className="w-full max-w-md bg-zinc-900 border border-yellow-500/30 rounded-xl p-4 shadow-2xl shadow-yellow-500/10">
                        <h3 className="text-lg font-bold text-yellow-400 mb-2 flex items-center gap-2">
                            <ImageIcon className="w-5 h-5" />
                            NanoBanana Pro
                        </h3>
                        <p className="text-sm text-zinc-400 mb-4">Describe the image you want to generate for this document.</p>
                        <textarea 
                            value={imagePrompt}
                            onChange={(e) => setImagePrompt(e.target.value)}
                            className="w-full h-24 bg-black/50 border border-zinc-700 rounded-lg p-3 text-white mb-4 focus:border-yellow-500/50 outline-none resize-none"
                            placeholder="A professional legal letterhead with a scale of justice logo..."
                        />
                        <div className="flex justify-end gap-2">
                            <button 
                                onClick={() => setShowImageModal(false)}
                                className="px-4 py-2 text-zinc-400 hover:text-white transition"
                            >
                                Cancel
                            </button>
                            <button 
                                onClick={handleAddImage}
                                disabled={!imagePrompt}
                                className="px-4 py-2 bg-yellow-600 hover:bg-yellow-500 text-black font-semibold rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Generate
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {isEditing ? (
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full h-full p-4 bg-transparent text-white font-mono text-sm resize-none outline-none"
                spellCheck={false}
              />
            ) : activeArtifact.type === 'smart-canvas' ? (
               <SmartCanvasRenderer artifact={activeArtifact} />
            ) : (
              <ArtifactContent artifact={activeArtifact} highlighterMode={highlighterMode} />
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
      
      {/* Footer ... */}
      {activeArtifact && (
        <div className="px-4 py-2 border-t border-cyan-500/20 text-xs text-cyan-300/50 flex items-center justify-between bg-blue-900/10">
          <span>
            {activeArtifact.type} • Created {activeArtifact.createdAt ? new Date(activeArtifact.createdAt).toLocaleString() : 'Unknown'}
          </span>
          <span>{(activeArtifact.content || '').length} characters</span>
        </div>
      )}
    </div>
  );
}

function SmartCanvasRenderer({ artifact }: { artifact: Artifact }) {
    // Render the structured layout
    const sections = artifact.structure?.sections || [];
    
    return (
        <div className="min-h-full bg-white text-black p-8 shadow-lg mx-auto max-w-[210mm] relative grid grid-cols-12 gap-4">
            {sections.map(section => (
                <div 
                    key={section.id}
                    className={`
                        relative border border-transparent hover:border-cyan-500/30 transition-all group p-4
                        ${getSectionClass(section.region)}
                    `}
                    style={section.style as any}
                >
                    <div className="absolute top-0 right-0 opacity-0 group-hover:opacity-100 bg-cyan-100 text-cyan-800 text-[10px] px-1 uppercase font-bold">
                        {section.region}
                    </div>
                    
                    {section.type === 'image' ? (
                        <img src={section.content} alt={section.title} className="max-w-full h-auto" />
                    ) : (
                         <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: section.content }} />
                    )}
                </div>
            ))}
            
            {sections.length === 0 && (
                <div className="col-span-12 flex items-center justify-center h-96 text-zinc-400 border-2 border-dashed border-zinc-200 rounded-xl">
                    <p>Empty Canvas. Ask Verridian to add sections.</p>
                </div>
            )}
        </div>
    );
}

function getSectionClass(region: string) {
    switch(region) {
        case 'header': return 'col-span-12 border-b-2 border-black pb-4 mb-4';
        case 'footer': return 'col-span-12 border-t pt-4 mt-8 self-end';
        case 'sidebar-left': return 'col-span-3 bg-zinc-50 h-full';
        case 'sidebar-right': return 'col-span-3 bg-zinc-50 h-full';
        case 'main': return 'col-span-9'; // Default to 9 if sidebar exists, logic can be smarter
        default: return 'col-span-12';
    }
}

// ... existing helper functions ...
function ArtifactContent({ artifact, highlighterMode }: { artifact: Artifact, highlighterMode: boolean }) {
  const content = artifact.content || '';
  
  // ... (Wrap existing return logic) ...
    if (artifact.type === 'code') {
    return (
      <div className="h-full overflow-auto">
        <pre className="p-4 text-sm font-mono text-zinc-300 whitespace-pre-wrap">
          <code>{content}</code>
        </pre>
      </div>
    );
  }

  if (artifact.type === 'html') {
    return (
      <div className="h-full overflow-auto p-4">
        <div
          className={`prose prose-invert prose-sm max-w-none ${highlighterMode ? 'cursor-text selection:bg-yellow-500/50' : ''}`}
          dangerouslySetInnerHTML={{ __html: content }}
        />
      </div>
    );
  }

  // Default: markdown/text
  return (
    <div className="h-full overflow-auto p-4">
      <div className={`prose prose-invert prose-sm max-w-none whitespace-pre-wrap ${highlighterMode ? 'cursor-text selection:bg-yellow-500/50' : ''}`}>
        {content}
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

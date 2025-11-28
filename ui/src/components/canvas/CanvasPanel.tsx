'use client';

import React, { useState } from 'react';
import {
  Download, Copy, Edit3, Save, FileText, Code, File,
  ChevronRight, Highlighter, Layout, Image as ImageIcon, Scale
} from 'lucide-react';
import { useStore } from '@/lib/store';
import type { Artifact } from '@/types';
import { SafeHtmlProse } from '@/components/ui/SafeHtml';

// Generate unique ID for artifacts (outside component to avoid purity issues)
let artifactCounter = 0;
const generateArtifactId = () => `artifact_${++artifactCounter}_${Date.now()}`;

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
    addArtifact,
    toggleCanvas,
  } = useStore();

    const [showLayoutMenu, setShowLayoutMenu] = useState(false);
    const [canvasConfig, setCanvasConfig] = useState({
        fontFamily: 'Inter',
        fontSize: '16px',
        headingSize: '2.25rem',
        margin: '2rem',
        layout: 'standard' as 'standard' | 'legal' | 'newsletter' | 'report'
    });

    const [isEditing, setIsEditing] = useState(false);
    const [editContent, setEditContent] = useState('');
    const [highlighterMode, setHighlighterMode] = useState(false);
    const [imagePrompt, setImagePrompt] = useState('');
    const [showImageModal, setShowImageModal] = useState(false);

    const activeArtifact = artifacts.find(a => a.id === activeArtifactId);

    const TEMPLATES = [
      { id: 'legal', name: 'Legal Brief', icon: Scale, desc: 'Standard legal document layout with wide margins and formal font.' },
      { id: 'report', name: 'Client Report', icon: FileText, desc: 'Professional report with cover page structure and headers.' },
      { id: 'newsletter', name: 'Legal Newsletter', icon: Layout, desc: 'Multi-column layout for updates and news.' },
      { id: 'standard', name: 'Blank Document', icon: File, desc: 'Empty canvas with standard formatting.' },
    ];

    const createFromTemplate = (templateId: string) => {
      const templateName = TEMPLATES.find(t => t.id === templateId)?.name || 'Document';

      // Map template IDs to layout types
      const layoutMap: Record<string, 'standard' | 'report' | 'newsletter' | 'legal-brief'> = {
        'legal': 'legal-brief',
        'newsletter': 'newsletter',
        'report': 'report',
        'standard': 'standard',
      };
      const layout = layoutMap[templateId] || 'standard';

      const structure: NonNullable<Artifact['structure']> = {
          layout,
          sections: []
      };

      if (templateId === 'legal') {
          structure.sections = [
              { id: 'h1', type: 'text', region: 'header', content: '<div class="text-center font-bold uppercase">In the Federal Circuit and Family Court of Australia</div>' },
              { id: 'm1', type: 'text', region: 'main', content: '<h3>1. INTRODUCTION</h3><p>The Applicant applies for the following orders...</p>' },
              { id: 'f1', type: 'text', region: 'footer', content: '<div class="text-xs text-center">Page 1 of 1</div>' }
          ];
      } else if (templateId === 'newsletter') {
          structure.sections = [
               { id: 'h1', type: 'text', region: 'header', content: '<h1 class="text-4xl font-bold text-emerald-700">Legal Update</h1><p class="text-zinc-500">November 2025 Edition</p>' },
               { id: 's1', type: 'text', region: 'sidebar-left', content: '<h3>Contents</h3><ul><li>Case Law Update</li><li>Legislative Changes</li></ul>' },
               { id: 'm1', type: 'text', region: 'main', content: '<h2>New Precedent in Family Law</h2><p>A recent decision has shifted the landscape regarding...</p>' }
          ];
      } else {
           structure.sections = [
              { id: 'm1', type: 'text', region: 'main', content: '<h1>Untitled Document</h1><p>Start typing here...</p>' }
           ];
      }

      const now = new Date();
      const newArtifact: Artifact = {
          id: generateArtifactId(),
          type: 'smart-canvas',
          title: `New ${templateName}`,
          content: '',
          structure,
          createdAt: now,
          updatedAt: now,
      };

      addArtifact(newArtifact);
      setShowLayoutMenu(false);
    };

    const updateCanvasSetting = (key: keyof typeof canvasConfig, value: string) => {
        setCanvasConfig(prev => ({ ...prev, [key]: value }));
    };


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
    <div className="h-full flex flex-col bg-zinc-950/40 backdrop-blur-xl border-l border-white/5">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/5">
        <div className="flex items-center gap-3">
          <button
            onClick={toggleCanvas}
            className="p-1.5 hover:bg-white/5 rounded-lg transition"
          >
            <ChevronRight className="w-5 h-5 text-zinc-400" />
          </button>
          <h2 className="font-semibold text-white">Canvas</h2>
          <span className="px-2 py-0.5 text-xs bg-white/5 rounded-full text-zinc-400 border border-white/10">
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
                className={`p-2 rounded-lg transition ${highlighterMode ? 'bg-yellow-500/20 text-yellow-400' : 'hover:bg-white/5 text-zinc-400 hover:text-white'}`}
                title="Highlighter Pen"
              >
                <Highlighter className="w-4 h-4" />
              </button>

            {/* Layout/Grid Toggle */}
            <div className="relative">
              <button
                onClick={() => setShowLayoutMenu(!showLayoutMenu)}
                className={`p-2 rounded-lg transition ${showLayoutMenu ? 'bg-white/10 text-white' : 'hover:bg-white/5 text-zinc-400 hover:text-white'}`}
                title="Layout & Templates"
              >
                <Layout className="w-4 h-4" />
              </button>

              {showLayoutMenu && (
                <div className="absolute right-0 top-full mt-2 w-80 bg-zinc-900 border border-zinc-700 rounded-xl shadow-2xl overflow-hidden z-50">
                    {/* Header */}
                    <div className="px-4 py-3 border-b border-zinc-800 bg-black/20">
                        <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                            <Layout className="w-4 h-4 text-emerald-500" />
                            Canvas Layout
                        </h3>
                    </div>

                    <div className="p-4 space-y-6 max-h-[60vh] overflow-y-auto custom-scrollbar">
                        {/* Templates Section */}
                        <div>
                            <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">New from Template</h4>
                            <div className="grid grid-cols-2 gap-2">
                                {TEMPLATES.map(t => (
                                    <button
                                        key={t.id}
                                        onClick={() => createFromTemplate(t.id)}
                                        className="flex flex-col items-center gap-2 p-3 rounded-lg bg-zinc-800 hover:bg-zinc-700 hover:ring-1 hover:ring-emerald-500/50 transition group"
                                    >
                                        <div className="w-8 h-8 rounded-full bg-black/30 flex items-center justify-center group-hover:bg-emerald-500/20 transition-colors">
                                            <t.icon className="w-4 h-4 text-zinc-400 group-hover:text-emerald-400" />
                                        </div>
                                        <span className="text-xs font-medium text-zinc-300 group-hover:text-white">{t.name}</span>
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Config Section */}
                        <div className="space-y-4 border-t border-zinc-800 pt-4">
                            <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Typography & Spacing</h4>
                            
                            <div className="space-y-3">
                                <div>
                                    <label className="text-xs text-zinc-400 mb-1 block">Font Family</label>
                                    <select 
                                        value={canvasConfig.fontFamily}
                                        onChange={(e) => updateCanvasSetting('fontFamily', e.target.value)}
                                        className="w-full bg-black/40 border border-zinc-700 rounded-lg px-2 py-1.5 text-xs text-white focus:border-emerald-500 outline-none"
                                    >
                                        <option value="Inter">Inter (Sans)</option>
                                        <option value="Merriweather">Merriweather (Serif)</option>
                                        <option value="JetBrains Mono">Monospace</option>
                                    </select>
                                </div>
                                
                                <div className="grid grid-cols-2 gap-3">
                                    <div>
                                        <label className="text-xs text-zinc-400 mb-1 block">Font Size</label>
                                        <select 
                                            value={canvasConfig.fontSize}
                                            onChange={(e) => updateCanvasSetting('fontSize', e.target.value)}
                                            className="w-full bg-black/40 border border-zinc-700 rounded-lg px-2 py-1.5 text-xs text-white focus:border-emerald-500 outline-none"
                                        >
                                            <option value="14px">Small (14px)</option>
                                            <option value="16px">Medium (16px)</option>
                                            <option value="18px">Large (18px)</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="text-xs text-zinc-400 mb-1 block">Margins</label>
                                        <select 
                                            value={canvasConfig.margin}
                                            onChange={(e) => updateCanvasSetting('margin', e.target.value)}
                                            className="w-full bg-black/40 border border-zinc-700 rounded-lg px-2 py-1.5 text-xs text-white focus:border-emerald-500 outline-none"
                                        >
                                            <option value="1rem">Compact</option>
                                            <option value="2rem">Standard</option>
                                            <option value="3rem">Wide</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
              )}
            </div>

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
                className="p-2 hover:bg-white/5 text-zinc-400 hover:text-white rounded-lg transition"
                title="Edit"
              >
                <Edit3 className="w-4 h-4" />
              </button>
            )}
            <button
              onClick={handleCopy}
              className="p-2 hover:bg-white/5 text-zinc-400 hover:text-white rounded-lg transition"
              title="Copy"
            >
              <Copy className="w-4 h-4" />
            </button>
            
            {/* Export Menu */}
            <div className="relative group">
              <button
                className="p-2 hover:bg-white/5 text-zinc-400 hover:text-white rounded-lg transition"
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
        <div className="flex items-center gap-1 px-2 py-2 border-b border-white/5 overflow-x-auto">
          {artifacts.map((artifact) => (
            <button
              key={artifact.id}
              onClick={() => setActiveArtifact(artifact.id)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm whitespace-nowrap transition ${
                artifact.id === activeArtifactId
                  ? 'bg-white/10 text-white border border-white/10 shadow-sm'
                  : 'hover:bg-white/5 text-zinc-400 hover:text-zinc-200 border border-transparent'
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

            {/* Content Rendering Logic */}
            {isEditing ? (
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full h-full p-8 bg-transparent text-white font-mono text-sm resize-none outline-none leading-relaxed"
                spellCheck={false}
              />
            ) : (
              <div className="h-full w-full relative">
                 {/* Only show SmartCanvasRenderer for smart-canvas type, else standard text/markdown */}
                 {activeArtifact.type === 'smart-canvas' ? (
                    <SmartCanvasRenderer artifact={activeArtifact} />
                 ) : (
                    <ArtifactContent artifact={activeArtifact} highlighterMode={highlighterMode} />
                 )}
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-zinc-500">
            <FileText className="w-16 h-16 mb-6 opacity-20 stroke-[1.5]" />
            <p className="text-lg font-medium text-zinc-400">No artifacts selected</p>
            <p className="text-sm mt-2 max-w-xs text-center opacity-60">
              Select an item from the chat or ask Verridian to create a new document.
            </p>
          </div>
        )}
      </div>
      
      {/* Footer ... */}
      {activeArtifact && (
        <div className="px-4 py-2 border-t border-white/5 text-xs text-zinc-500 flex items-center justify-between bg-black/20">
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
                        relative border border-transparent hover:border-zinc-300 transition-all group p-4
                        ${getSectionClass(section.region)}
                    `}
                    style={section.style as React.CSSProperties}
                >
                    <div className="absolute top-0 right-0 opacity-0 group-hover:opacity-100 bg-zinc-100 text-zinc-800 text-[10px] px-1 uppercase font-bold">
                        {section.region}
                    </div>
                    
                    {section.type === 'image' ? (
                        /* eslint-disable-next-line @next/next/no-img-element */
                        <img src={section.content} alt={section.title || 'Document image'} className="max-w-full h-auto" loading="lazy" />
                    ) : (
                         <SafeHtmlProse content={section.content} dark={false} />
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
        <SafeHtmlProse
          content={content}
          className={highlighterMode ? 'cursor-text selection:bg-yellow-500/50' : ''}
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


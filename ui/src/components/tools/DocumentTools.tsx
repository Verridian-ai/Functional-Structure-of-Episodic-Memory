'use client';

import React, { useState, useRef } from 'react';
import {
  FileText, File, Download, Upload, X, Plus,
  Bold, Italic, Underline, AlignLeft, AlignCenter, AlignRight,
  List, ListOrdered, Link2, Image, Save, Eye, Edit3
} from 'lucide-react';

interface DocumentToolsProps {
  onDocumentCreate?: (doc: DocumentData) => void;
  initialContent?: string;
  initialTitle?: string;
}

interface DocumentData {
  id: string;
  title: string;
  content: string;
  type: 'letter' | 'document' | 'pdf';
  createdAt: Date;
  updatedAt: Date;
}

// Letter templates
const LETTER_TEMPLATES = [
  {
    id: 'formal_letter',
    name: 'Formal Letter',
    template: `[Your Name]
[Your Address]
[City, State, ZIP]
[Your Email]
[Date]

[Recipient Name]
[Recipient Title]
[Company/Organization]
[Address]
[City, State, ZIP]

Dear [Recipient Name],

[Opening paragraph - State the purpose of your letter]

[Body paragraphs - Provide details, explanations, or arguments]

[Closing paragraph - Summarize and state any action required]

Sincerely,

[Your Name]
[Your Title]`,
  },
  {
    id: 'legal_demand',
    name: 'Legal Demand Letter',
    template: `WITHOUT PREJUDICE

[Date]

BY EMAIL AND REGISTERED POST

[Recipient Name]
[Address]

Dear [Recipient Name],

RE: [MATTER DESCRIPTION]

We act for [Client Name] in relation to the above matter.

BACKGROUND
[Provide background facts]

LEGAL POSITION
[State the legal basis for the claim]

DEMAND
Our client demands that you:

1. [First demand]
2. [Second demand]

TIME FOR COMPLIANCE
You are required to comply with the above demands within [X] days from the date of this letter.

CONSEQUENCES OF NON-COMPLIANCE
Should you fail to comply with our client's demands within the specified timeframe, our client will commence legal proceedings against you without further notice.

We reserve all of our client's rights.

Yours faithfully,

[Your Name]
[Law Firm Name]`,
  },
  {
    id: 'parenting_letter',
    name: 'Parenting Arrangements Letter',
    template: `[Date]

[Recipient Name]
[Address]

Dear [Recipient Name],

RE: Parenting Arrangements for [Child's Name]

I am writing to discuss the parenting arrangements for our child/children.

CURRENT SITUATION
[Describe the current arrangements]

PROPOSED CHANGES
I propose the following changes to our current arrangements:

1. [Proposed change 1]
2. [Proposed change 2]

REASONS FOR PROPOSED CHANGES
[Explain the reasons for the proposed changes and how they benefit the children]

NEXT STEPS
I would like to discuss these proposals with you. Please let me know a suitable time for us to meet/speak.

If we are unable to reach an agreement, I suggest we consider attending mediation through a Family Dispute Resolution service.

I look forward to hearing from you.

Yours sincerely,

[Your Name]`,
  },
];

export function DocumentTools({ onDocumentCreate, initialContent = '', initialTitle = 'Untitled Document' }: DocumentToolsProps) {
  const [title, setTitle] = useState(initialTitle);
  const [content, setContent] = useState(initialContent);
  const [isPreview, setIsPreview] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);
  const editorRef = useRef<HTMLTextAreaElement>(null);

  const applyTemplate = (template: typeof LETTER_TEMPLATES[0]) => {
    setContent(template.template);
    setTitle(template.name);
    setShowTemplates(false);
  };

  const downloadAsText = () => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.replace(/\s+/g, '_')}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadAsMarkdown = () => {
    const markdown = `# ${title}\n\n${content}`;
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.replace(/\s+/g, '_')}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadAsPDF = async () => {
    try {
      const response = await fetch('/api/pdf/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${title.replace(/\s+/g, '_')}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('PDF generation failed:', error);
    }
  };

  const handleSave = () => {
    const doc: DocumentData = {
      id: `doc_${Date.now()}`,
      title,
      content,
      type: 'document',
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    onDocumentCreate?.(doc);
  };

  return (
    <div className="flex flex-col h-full bg-zinc-900 rounded-xl border border-zinc-800 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
            <FileText className="w-4 h-4 text-white" />
          </div>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="bg-transparent text-white font-medium text-lg outline-none border-b border-transparent hover:border-zinc-700 focus:border-cyan-500 transition"
          />
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowTemplates(!showTemplates)}
            className="flex items-center gap-2 px-3 py-1.5 text-sm bg-zinc-800 hover:bg-zinc-700 rounded-lg transition"
          >
            <Plus className="w-4 h-4" />
            Templates
          </button>
          <button
            onClick={() => setIsPreview(!isPreview)}
            className={`p-2 rounded-lg transition ${
              isPreview ? 'bg-cyan-600/20 text-cyan-400' : 'hover:bg-zinc-800 text-zinc-400'
            }`}
          >
            {isPreview ? <Edit3 className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Templates Dropdown */}
      {showTemplates && (
        <div className="p-4 border-b border-zinc-800 bg-zinc-800/30">
          <h4 className="text-sm font-medium text-white mb-3">Choose a Template</h4>
          <div className="grid grid-cols-3 gap-3">
            {LETTER_TEMPLATES.map((template) => (
              <button
                key={template.id}
                onClick={() => applyTemplate(template)}
                className="p-3 text-left bg-zinc-800 hover:bg-zinc-700 rounded-lg border border-zinc-700 hover:border-cyan-500/50 transition"
              >
                <FileText className="w-5 h-5 text-blue-400 mb-2" />
                <div className="text-sm font-medium text-white">{template.name}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Editor/Preview */}
      <div className="flex-1 overflow-auto">
        {isPreview ? (
          <div className="p-6 prose prose-invert prose-sm max-w-none">
            <h1>{title}</h1>
            <div className="whitespace-pre-wrap">{content}</div>
          </div>
        ) : (
          <textarea
            ref={editorRef}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Start writing your document..."
            className="w-full h-full p-6 bg-transparent text-white resize-none outline-none font-mono text-sm leading-relaxed"
            spellCheck
          />
        )}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-zinc-800 bg-zinc-800/30">
        <div className="text-sm text-zinc-500">
          {content.length} characters • {content.split(/\s+/).filter(Boolean).length} words
        </div>

        <div className="flex items-center gap-2">
          <div className="relative group">
            <button className="flex items-center gap-2 px-3 py-1.5 text-sm bg-zinc-800 hover:bg-zinc-700 rounded-lg transition">
              <Download className="w-4 h-4" />
              Export
            </button>
            <div className="absolute right-0 bottom-full mb-2 w-40 py-2 bg-zinc-800 rounded-lg border border-zinc-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition">
              <button
                onClick={downloadAsText}
                className="w-full px-4 py-2 text-sm text-left text-zinc-300 hover:bg-zinc-700"
              >
                Text (.txt)
              </button>
              <button
                onClick={downloadAsMarkdown}
                className="w-full px-4 py-2 text-sm text-left text-zinc-300 hover:bg-zinc-700"
              >
                Markdown (.md)
              </button>
              <button
                onClick={downloadAsPDF}
                className="w-full px-4 py-2 text-sm text-left text-zinc-300 hover:bg-zinc-700"
              >
                PDF (.pdf)
              </button>
            </div>
          </div>

          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-4 py-1.5 text-sm bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition"
          >
            <Save className="w-4 h-4" />
            Save to Canvas
          </button>
        </div>
      </div>
    </div>
  );
}

// PDF Viewer Component
export function PDFViewer({ url, onClose }: { url: string; onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center">
      <div className="w-full max-w-5xl h-[90vh] flex flex-col">
        <div className="flex items-center justify-between px-4 py-3 bg-zinc-900 rounded-t-xl border border-zinc-800">
          <div className="flex items-center gap-3">
            <File className="w-5 h-5 text-red-400" />
            <span className="font-medium text-white">PDF Viewer</span>
          </div>
          <div className="flex items-center gap-2">
            <a
              href={url}
              download
              className="flex items-center gap-2 px-3 py-1.5 text-sm bg-zinc-800 hover:bg-zinc-700 rounded-lg transition"
            >
              <Download className="w-4 h-4" />
              Download
            </a>
            <button
              onClick={onClose}
              className="p-2 hover:bg-zinc-800 rounded-lg transition"
            >
              <X className="w-5 h-5 text-zinc-400" />
            </button>
          </div>
        </div>
        <iframe
          src={url}
          className="flex-1 w-full bg-white rounded-b-xl"
          title="PDF Viewer"
        />
      </div>
    </div>
  );
}

// Document Editor Modal
export function DocumentEditorModal({
  isOpen,
  onClose,
  onSave,
  initialContent,
  initialTitle,
}: {
  isOpen: boolean;
  onClose: () => void;
  onSave?: (doc: DocumentData) => void;
  initialContent?: string;
  initialTitle?: string;
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl h-[80vh] relative">
        <button
          onClick={onClose}
          className="absolute -top-2 -right-2 z-10 p-2 bg-zinc-800 hover:bg-zinc-700 rounded-full transition"
        >
          <X className="w-5 h-5 text-zinc-400" />
        </button>
        <DocumentTools
          onDocumentCreate={(doc) => {
            onSave?.(doc);
            onClose();
          }}
          initialContent={initialContent}
          initialTitle={initialTitle}
        />
      </div>
    </div>
  );
}

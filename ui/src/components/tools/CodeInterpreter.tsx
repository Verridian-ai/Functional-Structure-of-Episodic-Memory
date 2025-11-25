'use client';

import React, { useState, useRef } from 'react';
import {
  Play, Square, Terminal, X, Maximize2, Minimize2,
  Copy, Download, Trash2, Code, FileCode
} from 'lucide-react';

interface CodeInterpreterProps {
  onClose?: () => void;
  initialCode?: string;
}

interface ExecutionResult {
  id: string;
  code: string;
  output: string;
  error?: string;
  timestamp: Date;
  executionTime?: number;
}

export function CodeInterpreter({ onClose, initialCode = '' }: CodeInterpreterProps) {
  const [code, setCode] = useState(initialCode);
  const [isExecuting, setIsExecuting] = useState(false);
  const [results, setResults] = useState<ExecutionResult[]>([]);
  const [isMaximized, setIsMaximized] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const executeCode = async () => {
    if (!code.trim() || isExecuting) return;

    setIsExecuting(true);
    const startTime = Date.now();

    try {
      // Call backend API to execute Python code
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language: 'python' }),
      });

      const data = await response.json();
      const executionTime = Date.now() - startTime;

      const result: ExecutionResult = {
        id: `exec_${Date.now()}`,
        code,
        output: data.output || '',
        error: data.error,
        timestamp: new Date(),
        executionTime,
      };

      setResults(prev => [result, ...prev]);
    } catch (error) {
      const executionTime = Date.now() - startTime;
      const result: ExecutionResult = {
        id: `exec_${Date.now()}`,
        code,
        output: '',
        error: error instanceof Error ? error.message : 'Execution failed',
        timestamp: new Date(),
        executionTime,
      };
      setResults(prev => [result, ...prev]);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      executeCode();
    }
    // Handle Tab for indentation
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = textareaRef.current?.selectionStart ?? 0;
      const end = textareaRef.current?.selectionEnd ?? 0;
      setCode(code.substring(0, start) + '    ' + code.substring(end));
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.selectionStart = textareaRef.current.selectionEnd = start + 4;
        }
      }, 0);
    }
  };

  const copyOutput = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const clearResults = () => {
    setResults([]);
  };

  return (
    <div className={`flex flex-col bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden ${
      isMaximized ? 'fixed inset-4 z-50' : 'h-[500px]'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800 bg-zinc-900/50">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
            <Terminal className="w-4 h-4 text-white" />
          </div>
          <div>
            <h3 className="font-medium text-white">Code Interpreter</h3>
            <p className="text-xs text-zinc-500">Python Environment</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsMaximized(!isMaximized)}
            className="p-2 hover:bg-zinc-800 rounded-lg transition"
          >
            {isMaximized ? (
              <Minimize2 className="w-4 h-4 text-zinc-400" />
            ) : (
              <Maximize2 className="w-4 h-4 text-zinc-400" />
            )}
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="p-2 hover:bg-zinc-800 rounded-lg transition"
            >
              <X className="w-4 h-4 text-zinc-400" />
            </button>
          )}
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Code Editor */}
        <div className="flex-1 flex flex-col border-r border-zinc-800">
          <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800 bg-zinc-800/30">
            <div className="flex items-center gap-2">
              <FileCode className="w-4 h-4 text-zinc-400" />
              <span className="text-sm text-zinc-400">main.py</span>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={executeCode}
                disabled={isExecuting || !code.trim()}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition ${
                  isExecuting || !code.trim()
                    ? 'bg-zinc-800 text-zinc-500'
                    : 'bg-green-600 hover:bg-green-500 text-white'
                }`}
              >
                {isExecuting ? (
                  <>
                    <Square className="w-3 h-3" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="w-3 h-3" />
                    Run
                  </>
                )}
              </button>
            </div>
          </div>

          <textarea
            ref={textareaRef}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="# Enter Python code here...
# Press Ctrl+Enter to execute

print('Hello, World!')"
            spellCheck={false}
            className="flex-1 w-full p-4 bg-zinc-950 text-zinc-100 font-mono text-sm resize-none outline-none"
          />

          <div className="px-4 py-2 border-t border-zinc-800 bg-zinc-800/30 text-xs text-zinc-500">
            Press Ctrl+Enter to run
          </div>
        </div>

        {/* Output Panel */}
        <div className="w-1/2 flex flex-col">
          <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800 bg-zinc-800/30">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-zinc-400" />
              <span className="text-sm text-zinc-400">Output</span>
            </div>
            {results.length > 0 && (
              <button
                onClick={clearResults}
                className="p-1 hover:bg-zinc-700 rounded transition"
                title="Clear output"
              >
                <Trash2 className="w-4 h-4 text-zinc-500" />
              </button>
            )}
          </div>

          <div className="flex-1 overflow-auto p-4 space-y-4">
            {results.length === 0 ? (
              <div className="text-center text-zinc-500 py-8">
                <Terminal className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>Run code to see output</p>
              </div>
            ) : (
              results.map((result) => (
                <div
                  key={result.id}
                  className={`p-3 rounded-lg border ${
                    result.error
                      ? 'bg-red-950/20 border-red-900/50'
                      : 'bg-zinc-800/50 border-zinc-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-zinc-500">
                      {result.timestamp.toLocaleTimeString()}
                      {result.executionTime && (
                        <span className="ml-2">({result.executionTime}ms)</span>
                      )}
                    </span>
                    <button
                      onClick={() => copyOutput(result.output || result.error || '')}
                      className="p-1 hover:bg-zinc-700 rounded transition"
                    >
                      <Copy className="w-3 h-3 text-zinc-500" />
                    </button>
                  </div>
                  <pre className={`text-sm font-mono whitespace-pre-wrap ${
                    result.error ? 'text-red-400' : 'text-zinc-300'
                  }`}>
                    {result.error || result.output || '(no output)'}
                  </pre>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Code execution modal wrapper
export function CodeInterpreterModal({
  isOpen,
  onClose,
  initialCode,
}: {
  isOpen: boolean;
  onClose: () => void;
  initialCode?: string;
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
      <div className="w-full max-w-5xl">
        <CodeInterpreter onClose={onClose} initialCode={initialCode} />
      </div>
    </div>
  );
}

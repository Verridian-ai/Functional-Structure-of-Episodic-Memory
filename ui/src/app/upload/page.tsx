'use client';

import React, { useState, useRef, useCallback } from 'react';
import { Upload, FileText, X, CheckCircle, AlertCircle, Loader2, File, Image, FileType } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  status: 'uploading' | 'processing' | 'complete' | 'error';
  progress: number;
  error?: string;
}

const ACCEPTED_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain',
  'image/png',
  'image/jpeg',
];

const FILE_ICONS: Record<string, React.ReactNode> = {
  'application/pdf': <FileType className="w-5 h-5 text-red-400" />,
  'text/plain': <FileText className="w-5 h-5 text-zinc-400" />,
  'image/png': <Image className="w-5 h-5 text-purple-400" />,
  'image/jpeg': <Image className="w-5 h-5 text-purple-400" />,
};

export default function UploadPage() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const simulateUpload = useCallback((file: File) => {
    const uploadedFile: UploadedFile = {
      id: `${Date.now()}-${file.name}`,
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'uploading',
      progress: 0,
    };

    setFiles(prev => [...prev, uploadedFile]);

    // Simulate upload progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 20;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);

        // Simulate processing
        setFiles(prev => prev.map(f =>
          f.id === uploadedFile.id ? { ...f, status: 'processing', progress: 100 } : f
        ));

        // Simulate completion
        setTimeout(() => {
          setFiles(prev => prev.map(f =>
            f.id === uploadedFile.id ? { ...f, status: 'complete' } : f
          ));
        }, 1500);
      } else {
        setFiles(prev => prev.map(f =>
          f.id === uploadedFile.id ? { ...f, progress } : f
        ));
      }
    }, 200);
  }, []);

  const handleFiles = useCallback((fileList: FileList) => {
    Array.from(fileList).forEach(file => {
      if (ACCEPTED_TYPES.includes(file.type)) {
        simulateUpload(file);
      } else {
        const uploadedFile: UploadedFile = {
          id: `${Date.now()}-${file.name}`,
          name: file.name,
          size: file.size,
          type: file.type,
          status: 'error',
          progress: 0,
          error: 'Unsupported file type',
        };
        setFiles(prev => [...prev, uploadedFile]);
      }
    });
  }, [simulateUpload]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragActive(false);
    if (e.dataTransfer.files) {
      handleFiles(e.dataTransfer.files);
    }
  }, [handleFiles]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragActive(false);
  }, []);

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const completedCount = files.filter(f => f.status === 'complete').length;
  const processingCount = files.filter(f => f.status === 'uploading' || f.status === 'processing').length;

  return (
    <FeaturePageLayout
      title="Document Upload"
      description="Upload and process legal documents through the GSW extraction pipeline"
      icon={<Upload className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="emerald"
    >
      {/* Stats */}
      {files.length > 0 && (
        <div className="grid grid-cols-3 gap-3 mb-6">
          <div className="p-3 bg-zinc-900/50 rounded-xl border border-white/10 text-center">
            <div className="text-lg sm:text-xl font-bold text-white">{files.length}</div>
            <div className="text-[10px] sm:text-xs text-zinc-400">Total Files</div>
          </div>
          <div className="p-3 bg-zinc-900/50 rounded-xl border border-white/10 text-center">
            <div className="text-lg sm:text-xl font-bold text-emerald-400">{completedCount}</div>
            <div className="text-[10px] sm:text-xs text-zinc-400">Processed</div>
          </div>
          <div className="p-3 bg-zinc-900/50 rounded-xl border border-white/10 text-center">
            <div className="text-lg sm:text-xl font-bold text-amber-400">{processingCount}</div>
            <div className="text-[10px] sm:text-xs text-zinc-400">Processing</div>
          </div>
        </div>
      )}

      {/* Drop Zone - Mobile First */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
        className={`relative flex flex-col items-center justify-center p-6 sm:p-8 md:p-12 border-2 border-dashed rounded-2xl sm:rounded-3xl cursor-pointer transition-all touch-target ${
          isDragActive
            ? 'border-emerald-500 bg-emerald-500/10'
            : 'border-zinc-700 bg-zinc-900/30 hover:border-zinc-600 hover:bg-zinc-900/50'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={ACCEPTED_TYPES.join(',')}
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
          className="hidden"
        />

        <div className={`w-14 h-14 sm:w-16 sm:h-16 md:w-20 md:h-20 rounded-2xl flex items-center justify-center mb-4 transition-colors ${
          isDragActive ? 'bg-emerald-500/20' : 'bg-zinc-800/50'
        }`}>
          <Upload className={`w-7 h-7 sm:w-8 sm:h-8 md:w-10 md:h-10 ${isDragActive ? 'text-emerald-400' : 'text-zinc-400'}`} />
        </div>

        <h3 className="text-base sm:text-lg md:text-xl font-semibold text-white mb-1 sm:mb-2 text-center">
          {isDragActive ? 'Drop files here' : 'Drop files or tap to upload'}
        </h3>
        <p className="text-xs sm:text-sm text-zinc-400 text-center mb-4">
          Supports PDF, Word, TXT, and images up to 50MB
        </p>

        <button
          onClick={(e) => {
            e.stopPropagation();
            fileInputRef.current?.click();
          }}
          className="px-4 sm:px-6 py-2.5 sm:py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium text-sm sm:text-base transition-colors touch-target"
        >
          Select Files
        </button>
      </div>

      {/* File List - Mobile First */}
      {files.length > 0 && (
        <div className="mt-6 space-y-3">
          <h3 className="text-sm font-medium text-zinc-400">Uploaded Files</h3>

          <div className="space-y-2">
            {files.map((file) => (
              <FileCard key={file.id} file={file} onRemove={() => removeFile(file.id)} formatSize={formatFileSize} />
            ))}
          </div>
        </div>
      )}

      {/* Pipeline Info */}
      <div className="mt-8 p-4 sm:p-6 bg-zinc-900/50 rounded-2xl border border-white/10">
        <h3 className="text-sm sm:text-base font-medium text-white mb-3">GSW Processing Pipeline</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { step: '1', label: 'Upload', desc: 'File validation' },
            { step: '2', label: 'Parse', desc: 'Text extraction' },
            { step: '3', label: 'Extract', desc: 'Entity & event detection' },
            { step: '4', label: 'Index', desc: 'GSW integration' },
          ].map((stage) => (
            <div key={stage.step} className="p-3 bg-zinc-800/50 rounded-xl">
              <div className="flex items-center gap-2 mb-1">
                <span className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold flex items-center justify-center">
                  {stage.step}
                </span>
                <span className="text-xs sm:text-sm font-medium text-white">{stage.label}</span>
              </div>
              <p className="text-[10px] sm:text-xs text-zinc-500">{stage.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </FeaturePageLayout>
  );
}

function FileCard({ file, onRemove, formatSize }: { file: UploadedFile; onRemove: () => void; formatSize: (bytes: number) => string }) {
  const icon = FILE_ICONS[file.type] || <File className="w-5 h-5 text-zinc-400" />;

  return (
    <div className={`flex items-center gap-3 p-3 sm:p-4 rounded-xl border transition-all ${
      file.status === 'error'
        ? 'bg-red-500/10 border-red-500/30'
        : file.status === 'complete'
          ? 'bg-emerald-500/10 border-emerald-500/30'
          : 'bg-zinc-900/50 border-white/10'
    }`}>
      {/* Icon */}
      <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-zinc-800/50 flex items-center justify-center flex-shrink-0">
        {file.status === 'uploading' || file.status === 'processing' ? (
          <Loader2 className="w-5 h-5 text-emerald-400 animate-spin" />
        ) : file.status === 'complete' ? (
          <CheckCircle className="w-5 h-5 text-emerald-400" />
        ) : file.status === 'error' ? (
          <AlertCircle className="w-5 h-5 text-red-400" />
        ) : (
          icon
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-white truncate">{file.name}</p>
        <p className="text-xs text-zinc-400">
          {formatSize(file.size)}
          {file.status === 'uploading' && ` • ${Math.round(file.progress)}%`}
          {file.status === 'processing' && ' • Processing...'}
          {file.status === 'complete' && ' • Complete'}
          {file.status === 'error' && ` • ${file.error}`}
        </p>

        {/* Progress Bar */}
        {(file.status === 'uploading' || file.status === 'processing') && (
          <div className="mt-2 h-1 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-300 ${file.status === 'processing' ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'}`}
              style={{ width: `${file.progress}%` }}
            />
          </div>
        )}
      </div>

      {/* Remove Button */}
      <button
        onClick={onRemove}
        className="p-2 hover:bg-white/5 rounded-lg transition-colors touch-target flex-shrink-0"
        aria-label="Remove file"
      >
        <X className="w-4 h-4 text-zinc-500 hover:text-white" />
      </button>
    </div>
  );
}

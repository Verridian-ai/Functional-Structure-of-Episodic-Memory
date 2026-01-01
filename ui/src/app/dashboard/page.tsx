'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import {
  ArrowLeft,
  Brain,
  Network,
  Search,
  FileText,
  Scale,
  Users,
  Calendar,
  BarChart3,
  Shield,
  Sparkles,
  Database,
  Workflow,
  AlertTriangle,
  CheckCircle,
  Clock,
  Layers,
  Sun,
  Moon,
  Upload,
  Play,
  Settings,
  ChevronRight,
} from 'lucide-react';

type FeatureCategory = 'core' | 'analysis' | 'pipeline' | 'validation';

interface Feature {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  category: FeatureCategory;
  status: 'active' | 'coming-soon' | 'beta';
  action?: string;
  href?: string;
}

const FEATURES: Feature[] = [
  // Core Features
  {
    id: 'gsw',
    title: 'Global Semantic Workspace',
    description: 'Actor-centric episodic memory extraction with entity tracking and relationship mapping.',
    icon: <Brain className="w-5 h-5" />,
    category: 'core',
    status: 'active',
    href: '/',
  },
  {
    id: 'graph',
    title: 'Knowledge Graph',
    description: 'Interactive 3D citation network with court hierarchy visualization.',
    icon: <Network className="w-5 h-5" />,
    category: 'core',
    status: 'active',
    href: '/visualize',
  },
  {
    id: 'search',
    title: 'Hybrid Search',
    description: 'GSW semantic + BM25 keyword search with automatic mode selection.',
    icon: <Search className="w-5 h-5" />,
    category: 'core',
    status: 'active',
    href: '/',
  },
  {
    id: 'tem',
    title: 'TEM Reasoning',
    description: 'Tolman-Eichenbaum Machine for structural legal precedent matching.',
    icon: <Layers className="w-5 h-5" />,
    category: 'core',
    status: 'active',
    href: '/tem',
  },
  {
    id: 'vsa',
    title: 'VSA Validator',
    description: 'Vector Symbolic Architecture for anti-hallucination verification.',
    icon: <Shield className="w-5 h-5" />,
    category: 'core',
    status: 'active',
    href: '/validation',
  },
  // Analysis Features
  {
    id: 'entity-browser',
    title: 'Entity Browser',
    description: 'Explore actors, roles, and relationships extracted from legal documents.',
    icon: <Users className="w-5 h-5" />,
    category: 'analysis',
    status: 'active',
    href: '/entities',
  },
  {
    id: 'timeline',
    title: 'Timeline Builder',
    description: 'Chronological reconstruction of events with temporal relationship mapping.',
    icon: <Calendar className="w-5 h-5" />,
    category: 'analysis',
    status: 'active',
    href: '/timeline',
  },
  {
    id: 'discrepancy',
    title: 'Discrepancy Detection',
    description: 'Span-level conflict detection for dates, amounts, and entity references.',
    icon: <AlertTriangle className="w-5 h-5" />,
    category: 'analysis',
    status: 'active',
    href: '/discrepancy',
  },
  {
    id: 'authority',
    title: 'Authority Scorer',
    description: 'Court hierarchy precedent binding assessment with BOOST scoring.',
    icon: <Scale className="w-5 h-5" />,
    category: 'analysis',
    status: 'active',
    href: '/authority',
  },
  // Pipeline Features
  {
    id: 'upload',
    title: 'Document Upload',
    description: 'Upload and process legal documents through the GSW extraction pipeline.',
    icon: <Upload className="w-5 h-5" />,
    category: 'pipeline',
    status: 'active',
    href: '/upload',
  },
  {
    id: 'pipeline',
    title: 'Pipeline Monitor',
    description: 'Real-time pipeline execution with stage-by-stage progress tracking.',
    icon: <Workflow className="w-5 h-5" />,
    category: 'pipeline',
    status: 'active',
    href: '/pipeline',
  },
  {
    id: 'workspace',
    title: 'Workspace Manager',
    description: 'Save, load, and merge GSW workspaces with TOON compression.',
    icon: <Database className="w-5 h-5" />,
    category: 'pipeline',
    status: 'active',
    href: '/workspace',
  },
  // Validation Features
  {
    id: 'statutory',
    title: 'Statutory Alignment',
    description: 'Validate extractions against statutory corpus with compliance scoring.',
    icon: <CheckCircle className="w-5 h-5" />,
    category: 'validation',
    status: 'active',
    href: '/statutory',
  },
  {
    id: 'evaluation',
    title: 'Evaluation Dashboard',
    description: '6-metric evaluation system with precision, recall, and legal accuracy.',
    icon: <BarChart3 className="w-5 h-5" />,
    category: 'validation',
    status: 'active',
    href: '/evaluation',
  },
  {
    id: 'benchmark',
    title: 'Benchmarking',
    description: 'Continuous accuracy tracking with historical metrics and trends.',
    icon: <Clock className="w-5 h-5" />,
    category: 'validation',
    status: 'active',
    href: '/benchmark',
  },
];

const CATEGORY_INFO: Record<FeatureCategory, { label: string; color: string }> = {
  core: { label: 'Core Intelligence', color: 'cyan' },
  analysis: { label: 'Analysis & Insights', color: 'purple' },
  pipeline: { label: 'Pipeline & Processing', color: 'emerald' },
  validation: { label: 'Validation & Quality', color: 'amber' },
};

export default function DashboardPage() {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [selectedCategory, setSelectedCategory] = useState<FeatureCategory | 'all'>('all');
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'dark' | 'light' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute('data-theme', savedTheme);
    }

    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  const filteredFeatures = selectedCategory === 'all'
    ? FEATURES
    : FEATURES.filter(f => f.category === selectedCategory);

  const activeCount = FEATURES.filter(f => f.status === 'active').length;
  const betaCount = FEATURES.filter(f => f.status === 'beta').length;

  return (
    <div className="min-h-screen bg-zinc-950 text-white safe-area-inset">
      {/* Background */}
      <div className="fixed inset-0 bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950 pointer-events-none" />
      <div className="fixed inset-0 gradient-mesh pointer-events-none opacity-50" />

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4 border-b border-white/5 bg-zinc-950/60 backdrop-blur-xl safe-area-pt">
        <div className="flex items-center gap-3 sm:gap-4">
          <Link
            href="/"
            className="p-2 hover:bg-white/5 rounded-xl transition-colors touch-target"
          >
            <ArrowLeft className="w-5 h-5 text-zinc-400" />
          </Link>
          <div className="hidden sm:block">
            <Image
              src={theme === 'dark' ? '/Law_OS_Dark_Mode_Logo.png' : '/Law_OS_Light_Mode_Logo.png'}
              alt="LAW OS"
              width={100}
              height={40}
              className="object-contain h-8 w-auto"
            />
          </div>
          <div className="sm:hidden">
            <h1 className="text-lg font-bold text-white">Dashboard</h1>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3">
          <Link
            href="/visualize"
            className="flex items-center gap-2 px-3 py-2 bg-cyan-500/10 hover:bg-cyan-500/20 rounded-full border border-cyan-500/30 transition-all touch-target"
          >
            <Network className="w-4 h-4 text-cyan-400" />
            <span className="text-xs text-cyan-300 hidden sm:inline">Graph</span>
          </Link>
          <button
            onClick={toggleTheme}
            className="p-2.5 hover:bg-white/5 rounded-xl transition-colors touch-target"
          >
            {theme === 'dark' ? (
              <Moon className="w-5 h-5 text-amber-400" />
            ) : (
              <Sun className="w-5 h-5 text-amber-500" />
            )}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8 max-w-7xl mx-auto">
        {/* Hero Section */}
        <div className="mb-5 sm:mb-8 lg:mb-12">
          <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-bold text-white mb-1.5 sm:mb-2 lg:mb-3">
            LAW OS Dashboard
          </h1>
          <p className="text-xs sm:text-sm md:text-base text-zinc-400 max-w-2xl leading-relaxed">
            Brain-inspired legal intelligence with episodic memory and vector symbolic architecture.
          </p>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3 lg:gap-4 mb-5 sm:mb-6 lg:mb-8">
          <div className="stat-card">
            <div className="stat-card-value">{activeCount}</div>
            <div className="stat-card-label">Active</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-value">{betaCount}</div>
            <div className="stat-card-label">Beta</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-value flex items-center gap-1">
              <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-emerald-400 text-base sm:text-lg lg:text-2xl">Online</span>
            </div>
            <div className="stat-card-label">GSW Status</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-value flex items-center gap-1">
              <Sparkles className="w-4 h-4 sm:w-5 sm:h-5 text-amber-400" />
              <span className="text-amber-400 text-base sm:text-lg lg:text-2xl">Gemini</span>
            </div>
            <div className="stat-card-label">AI Model</div>
          </div>
        </div>

        {/* Category Filter - Horizontal scroll on mobile */}
        <div className="category-filter-scroll mb-6">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`category-filter-btn ${
              selectedCategory === 'all'
                ? 'bg-white/10 text-white border border-white/20'
                : 'bg-white/5 text-zinc-400 border border-transparent active:bg-white/10'
            }`}
          >
            All Features
          </button>
          {(Object.keys(CATEGORY_INFO) as FeatureCategory[]).map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`category-filter-btn ${
                selectedCategory === cat
                  ? `bg-${CATEGORY_INFO[cat].color}-500/20 text-${CATEGORY_INFO[cat].color}-400 border border-${CATEGORY_INFO[cat].color}-500/30`
                  : 'bg-white/5 text-zinc-400 border border-transparent active:bg-white/10'
              }`}
            >
              {CATEGORY_INFO[cat].label}
            </button>
          ))}
        </div>

        {/* Features Grid */}
        <div className="features-grid">
          {filteredFeatures.map((feature) => (
            <FeatureCard key={feature.id} feature={feature} />
          ))}
        </div>

        {/* Quick Actions */}
        <div className="mt-6 sm:mt-8 lg:mt-12 dashboard-section">
          <h2 className="dashboard-section-title">
            <Play className="w-4 h-4 sm:w-5 sm:h-5 text-cyan-400" />
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
            <Link href="/" className="quick-action-card group" style={{ background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, transparent 100%)' }}>
              <div className="quick-action-icon bg-cyan-500/20">
                <Brain className="w-5 h-5 sm:w-6 sm:h-6 text-cyan-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-white font-medium text-sm sm:text-base">Start New Query</div>
                <div className="text-[11px] sm:text-xs text-zinc-400 mt-0.5">Begin legal research with AI</div>
              </div>
              <ChevronRight className="w-4 h-4 sm:w-5 sm:h-5 text-zinc-500 group-hover:text-cyan-400 transition-colors flex-shrink-0" />
            </Link>

            <Link href="/visualize" className="quick-action-card group" style={{ background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, transparent 100%)', borderColor: 'rgba(168, 85, 247, 0.2)' }}>
              <div className="quick-action-icon bg-purple-500/20">
                <Network className="w-5 h-5 sm:w-6 sm:h-6 text-purple-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-white font-medium text-sm sm:text-base">Explore Graph</div>
                <div className="text-[11px] sm:text-xs text-zinc-400 mt-0.5">Navigate citation network</div>
              </div>
              <ChevronRight className="w-4 h-4 sm:w-5 sm:h-5 text-zinc-500 group-hover:text-purple-400 transition-colors flex-shrink-0" />
            </Link>

            <Link href="/upload" className="quick-action-card group" style={{ background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, transparent 100%)', borderColor: 'rgba(16, 185, 129, 0.2)' }}>
              <div className="quick-action-icon bg-emerald-500/20">
                <Upload className="w-5 h-5 sm:w-6 sm:h-6 text-emerald-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-white font-medium text-sm sm:text-base">Upload Document</div>
                <div className="text-[11px] sm:text-xs text-zinc-400 mt-0.5">Process through GSW pipeline</div>
              </div>
              <ChevronRight className="w-4 h-4 sm:w-5 sm:h-5 text-zinc-500 group-hover:text-emerald-400 transition-colors flex-shrink-0" />
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 px-4 sm:px-6 lg:px-8 py-6 border-t border-white/5 mt-8 safe-area-pb">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-zinc-500">
          <div>LAW OS by Verridian AI - Brain-inspired Legal Intelligence</div>
          <div className="flex items-center gap-4">
            <span>v1.0.0</span>
            <span className="hidden sm:inline">|</span>
            <span className="hidden sm:inline">Australian Family Law</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ feature }: { feature: Feature }) {
  const categoryInfo = CATEGORY_INFO[feature.category];

  const content = (
    <div className={`feature-card group ${feature.status === 'coming-soon' ? 'opacity-60' : ''}`}>
      <div
        className={`feature-card-icon bg-${categoryInfo.color}-500/20`}
      >
        <span className={`text-${categoryInfo.color}-400 [&>svg]:w-4 [&>svg]:h-4 sm:[&>svg]:w-5 sm:[&>svg]:h-5`}>
          {feature.icon}
        </span>
      </div>
      <h3 className="feature-card-title flex items-center gap-1.5 flex-wrap">
        <span className="truncate">{feature.title}</span>
        {feature.status === 'beta' && (
          <span className="px-1 py-0.5 bg-amber-500/20 text-amber-400 text-[9px] sm:text-[10px] rounded flex-shrink-0">BETA</span>
        )}
        {feature.status === 'coming-soon' && (
          <span className="px-1 py-0.5 bg-zinc-700 text-zinc-400 text-[9px] sm:text-[10px] rounded flex-shrink-0">SOON</span>
        )}
      </h3>
      <p className="feature-card-description">{feature.description}</p>
      {feature.href && feature.status === 'active' && (
        <div className="mt-auto pt-2 flex items-center text-[11px] sm:text-xs text-cyan-400 group-hover:text-cyan-300 group-active:text-cyan-300">
          <span>Open</span>
          <ChevronRight className="w-3.5 h-3.5 sm:w-4 sm:h-4 ml-0.5 transition-transform group-hover:translate-x-1" />
        </div>
      )}
    </div>
  );

  if (feature.href && feature.status === 'active') {
    return <Link href={feature.href}>{content}</Link>;
  }

  return content;
}

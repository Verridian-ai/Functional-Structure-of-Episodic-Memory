'use client';

import React, { useState } from 'react';
import { Users, Search, Filter, ChevronDown, User, Building, Briefcase, Scale, MapPin, Calendar, Tag, ChevronRight } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

type EntityType = 'all' | 'person' | 'organization' | 'court' | 'location' | 'role';

interface Entity {
  id: string;
  name: string;
  type: EntityType;
  role?: string;
  mentions: number;
  relationships: number;
  firstSeen: string;
  tags: string[];
}

// Mock data - in real app, this would come from the backend
const MOCK_ENTITIES: Entity[] = [
  { id: '1', name: 'John Smith', type: 'person', role: 'Applicant', mentions: 45, relationships: 12, firstSeen: '2024-01-15', tags: ['party', 'primary'] },
  { id: '2', name: 'Jane Doe', type: 'person', role: 'Respondent', mentions: 38, relationships: 10, firstSeen: '2024-01-15', tags: ['party', 'primary'] },
  { id: '3', name: 'Family Court of Australia', type: 'court', mentions: 22, relationships: 8, firstSeen: '2024-01-10', tags: ['jurisdiction'] },
  { id: '4', name: 'Smith & Associates', type: 'organization', role: 'Legal Representative', mentions: 15, relationships: 5, firstSeen: '2024-01-20', tags: ['legal'] },
  { id: '5', name: 'Melbourne', type: 'location', mentions: 12, relationships: 3, firstSeen: '2024-01-12', tags: ['venue'] },
  { id: '6', name: 'Federal Circuit Court', type: 'court', mentions: 8, relationships: 4, firstSeen: '2024-02-01', tags: ['jurisdiction'] },
  { id: '7', name: 'Dr. Sarah Wilson', type: 'person', role: 'Expert Witness', mentions: 6, relationships: 2, firstSeen: '2024-02-15', tags: ['witness'] },
  { id: '8', name: 'Child Support Agency', type: 'organization', mentions: 10, relationships: 3, firstSeen: '2024-01-25', tags: ['government'] },
];

const TYPE_CONFIG: Record<EntityType, { icon: React.ReactNode; label: string; color: string }> = {
  all: { icon: <Users className="w-4 h-4" />, label: 'All Entities', color: 'zinc' },
  person: { icon: <User className="w-4 h-4" />, label: 'People', color: 'cyan' },
  organization: { icon: <Building className="w-4 h-4" />, label: 'Organizations', color: 'purple' },
  court: { icon: <Scale className="w-4 h-4" />, label: 'Courts', color: 'amber' },
  location: { icon: <MapPin className="w-4 h-4" />, label: 'Locations', color: 'emerald' },
  role: { icon: <Briefcase className="w-4 h-4" />, label: 'Roles', color: 'red' },
};

export default function EntitiesPage() {
  const [search, setSearch] = useState('');
  const [selectedType, setSelectedType] = useState<EntityType>('all');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);

  const filteredEntities = MOCK_ENTITIES.filter(entity => {
    const matchesSearch = entity.name.toLowerCase().includes(search.toLowerCase()) ||
      entity.role?.toLowerCase().includes(search.toLowerCase()) ||
      entity.tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()));
    const matchesType = selectedType === 'all' || entity.type === selectedType;
    return matchesSearch && matchesType;
  });

  return (
    <FeaturePageLayout
      title="Entity Browser"
      description="Explore actors, roles, and relationships extracted from legal documents"
      icon={<Users className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="purple"
    >
      {/* Search and Filters - Mobile First */}
      <div className="space-y-3 sm:space-y-4 mb-4 sm:mb-6">
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 sm:w-5 sm:h-5 text-zinc-500" />
          <input
            type="text"
            placeholder="Search entities, roles, or tags..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-10 sm:h-12 pl-9 sm:pl-11 pr-4 bg-zinc-900/50 border border-white/10 rounded-xl text-sm sm:text-base text-white placeholder:text-zinc-500 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/30 transition-all"
          />
        </div>

        {/* Filter Toggle & Type Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide -mx-3 px-3 sm:mx-0 sm:px-0 sm:flex-wrap">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-full text-xs sm:text-sm font-medium transition-all whitespace-nowrap flex-shrink-0 touch-target ${
              showFilters ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'bg-white/5 text-zinc-400 border border-transparent hover:bg-white/10'
            }`}
          >
            <Filter className="w-3.5 h-3.5" />
            Filters
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
          </button>

          {(Object.keys(TYPE_CONFIG) as EntityType[]).map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-full text-xs sm:text-sm font-medium transition-all whitespace-nowrap flex-shrink-0 touch-target ${
                selectedType === type
                  ? `bg-${TYPE_CONFIG[type].color}-500/20 text-${TYPE_CONFIG[type].color}-400 border border-${TYPE_CONFIG[type].color}-500/30`
                  : 'bg-white/5 text-zinc-400 border border-transparent hover:bg-white/10'
              }`}
            >
              {TYPE_CONFIG[type].icon}
              <span className="hidden sm:inline">{TYPE_CONFIG[type].label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between mb-3 sm:mb-4">
        <p className="text-xs sm:text-sm text-zinc-400">
          <span className="text-white font-medium">{filteredEntities.length}</span> entities found
        </p>
      </div>

      {/* Entity Grid - Mobile First */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
        {filteredEntities.map((entity) => (
          <EntityCard
            key={entity.id}
            entity={entity}
            isSelected={selectedEntity?.id === entity.id}
            onClick={() => setSelectedEntity(selectedEntity?.id === entity.id ? null : entity)}
          />
        ))}
      </div>

      {/* Empty State */}
      {filteredEntities.length === 0 && (
        <div className="flex flex-col items-center justify-center py-12 sm:py-16 text-center">
          <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-zinc-800/50 border border-dashed border-zinc-600/50 flex items-center justify-center mb-4">
            <Users className="w-8 h-8 sm:w-10 sm:h-10 text-zinc-500" />
          </div>
          <p className="text-sm sm:text-base text-zinc-400 font-medium mb-1">No entities found</p>
          <p className="text-xs sm:text-sm text-zinc-500">Try adjusting your search or filters</p>
        </div>
      )}

      {/* Entity Detail Modal (Mobile Bottom Sheet / Desktop Side Panel) */}
      {selectedEntity && (
        <EntityDetail entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}
    </FeaturePageLayout>
  );
}

function EntityCard({ entity, isSelected, onClick }: { entity: Entity; isSelected: boolean; onClick: () => void }) {
  const typeConfig = TYPE_CONFIG[entity.type];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-3 sm:p-4 rounded-xl sm:rounded-2xl border transition-all touch-target ${
        isSelected
          ? 'bg-purple-500/10 border-purple-500/30 shadow-lg shadow-purple-500/10'
          : 'bg-zinc-900/50 border-white/10 hover:border-white/20 active:bg-zinc-800/50'
      }`}
    >
      <div className="flex items-start gap-3">
        <div className={`w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center flex-shrink-0 bg-${typeConfig.color}-500/20`}>
          <span className={`text-${typeConfig.color}-400`}>{typeConfig.icon}</span>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-sm sm:text-base font-medium text-white truncate">{entity.name}</h3>
          {entity.role && (
            <p className="text-xs text-zinc-400 mt-0.5">{entity.role}</p>
          )}
          <div className="flex items-center gap-2 sm:gap-3 mt-2 text-[10px] sm:text-xs text-zinc-500">
            <span>{entity.mentions} mentions</span>
            <span className="w-1 h-1 rounded-full bg-zinc-600" />
            <span>{entity.relationships} relationships</span>
          </div>
        </div>
        <ChevronRight className="w-4 h-4 text-zinc-500 flex-shrink-0" />
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-1.5 mt-3">
        {entity.tags.map((tag) => (
          <span
            key={tag}
            className="px-2 py-0.5 bg-white/5 rounded-full text-[10px] sm:text-xs text-zinc-400"
          >
            {tag}
          </span>
        ))}
      </div>
    </button>
  );
}

function EntityDetail({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const typeConfig = TYPE_CONFIG[entity.type];

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 md:hidden"
        onClick={onClose}
      />

      {/* Bottom Sheet (Mobile) / Side Panel (Desktop) */}
      <div className="fixed inset-x-0 bottom-0 md:inset-y-0 md:left-auto md:right-0 md:w-96 bg-zinc-900 border-t md:border-t-0 md:border-l border-white/10 rounded-t-3xl md:rounded-none z-50 max-h-[80vh] md:max-h-none overflow-y-auto safe-area-pb">
        {/* Handle (Mobile) */}
        <div className="md:hidden flex justify-center pt-3 pb-2">
          <div className="w-10 h-1 rounded-full bg-zinc-600" />
        </div>

        <div className="p-4 sm:p-6">
          {/* Header */}
          <div className="flex items-start gap-4 mb-6">
            <div className={`w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center bg-${typeConfig.color}-500/20`}>
              <span className={`text-${typeConfig.color}-400 scale-125`}>{typeConfig.icon}</span>
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-lg sm:text-xl font-bold text-white">{entity.name}</h2>
              <p className="text-sm text-zinc-400">{typeConfig.label}</p>
              {entity.role && (
                <span className="inline-block mt-2 px-2 py-1 bg-purple-500/20 text-purple-400 rounded-lg text-xs">
                  {entity.role}
                </span>
              )}
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-3 mb-6">
            <div className="p-3 bg-zinc-800/50 rounded-xl">
              <div className="text-xl sm:text-2xl font-bold text-white">{entity.mentions}</div>
              <div className="text-xs text-zinc-400">Mentions</div>
            </div>
            <div className="p-3 bg-zinc-800/50 rounded-xl">
              <div className="text-xl sm:text-2xl font-bold text-white">{entity.relationships}</div>
              <div className="text-xs text-zinc-400">Relationships</div>
            </div>
          </div>

          {/* Metadata */}
          <div className="space-y-3 mb-6">
            <div className="flex items-center gap-3 text-sm">
              <Calendar className="w-4 h-4 text-zinc-500" />
              <span className="text-zinc-400">First seen:</span>
              <span className="text-white">{new Date(entity.firstSeen).toLocaleDateString()}</span>
            </div>
          </div>

          {/* Tags */}
          <div className="mb-6">
            <h3 className="text-xs font-medium text-zinc-400 uppercase tracking-wider mb-2">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {entity.tags.map((tag) => (
                <span
                  key={tag}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-white/5 rounded-full text-sm text-zinc-300"
                >
                  <Tag className="w-3 h-3" />
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="space-y-2">
            <button className="w-full h-11 sm:h-12 flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl font-medium transition-colors touch-target">
              View in Graph
            </button>
            <button
              onClick={onClose}
              className="w-full h-11 sm:h-12 flex items-center justify-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl font-medium transition-colors touch-target"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

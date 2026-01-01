'use client';

import React, { useState } from 'react';
import { Calendar, Plus, ChevronLeft, ChevronRight, Clock, FileText, User, AlertTriangle, CheckCircle } from 'lucide-react';
import { FeaturePageLayout } from '@/components/layout/FeaturePageLayout';

interface TimelineEvent {
  id: string;
  date: string;
  title: string;
  description: string;
  type: 'filing' | 'hearing' | 'order' | 'event' | 'deadline';
  entities: string[];
  source?: string;
  isVerified: boolean;
}

// Mock timeline data
const MOCK_EVENTS: TimelineEvent[] = [
  { id: '1', date: '2024-01-15', title: 'Application Filed', description: 'Initial application for parenting orders filed by applicant', type: 'filing', entities: ['John Smith'], source: 'Court Registry', isVerified: true },
  { id: '2', date: '2024-01-22', title: 'Response Filed', description: 'Respondent filed response to application', type: 'filing', entities: ['Jane Doe'], source: 'Court Registry', isVerified: true },
  { id: '3', date: '2024-02-10', title: 'First Mention', description: 'First court mention before Registrar Brown', type: 'hearing', entities: ['John Smith', 'Jane Doe'], source: 'Transcript', isVerified: true },
  { id: '4', date: '2024-02-15', title: 'Interim Orders Made', description: 'Interim parenting orders granted', type: 'order', entities: ['Judge Williams'], source: 'Court Order', isVerified: true },
  { id: '5', date: '2024-03-01', title: 'Family Report Ordered', description: 'Court ordered preparation of family report', type: 'order', entities: [], source: 'Court Order', isVerified: true },
  { id: '6', date: '2024-04-15', title: 'Family Report Due', description: 'Deadline for family report submission', type: 'deadline', entities: ['Dr. Sarah Wilson'], isVerified: false },
  { id: '7', date: '2024-05-01', title: 'Final Hearing', description: 'Scheduled final hearing for determination of parenting orders', type: 'hearing', entities: [], isVerified: false },
];

const TYPE_CONFIG = {
  filing: { color: 'cyan', icon: <FileText className="w-4 h-4" />, label: 'Filing' },
  hearing: { color: 'purple', icon: <Calendar className="w-4 h-4" />, label: 'Hearing' },
  order: { color: 'emerald', icon: <CheckCircle className="w-4 h-4" />, label: 'Order' },
  event: { color: 'amber', icon: <Clock className="w-4 h-4" />, label: 'Event' },
  deadline: { color: 'red', icon: <AlertTriangle className="w-4 h-4" />, label: 'Deadline' },
};

export default function TimelinePage() {
  const [events] = useState<TimelineEvent[]>(MOCK_EVENTS);
  const [selectedEvent, setSelectedEvent] = useState<TimelineEvent | null>(null);
  const [viewMode, setViewMode] = useState<'list' | 'calendar'>('list');

  const sortedEvents = [...events].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  return (
    <FeaturePageLayout
      title="Timeline Builder"
      description="Chronological reconstruction of events with temporal relationship mapping"
      icon={<Calendar className="w-5 h-5 sm:w-6 sm:h-6" />}
      color="amber"
    >
      {/* Controls - Mobile First */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4 sm:mb-6">
        {/* View Toggle */}
        <div className="flex bg-zinc-800/50 rounded-xl p-1">
          <button
            onClick={() => setViewMode('list')}
            className={`flex-1 sm:flex-none px-4 py-2 rounded-lg text-sm font-medium transition-all touch-target ${
              viewMode === 'list' ? 'bg-amber-500/20 text-amber-400' : 'text-zinc-400 hover:text-white'
            }`}
          >
            List View
          </button>
          <button
            onClick={() => setViewMode('calendar')}
            className={`flex-1 sm:flex-none px-4 py-2 rounded-lg text-sm font-medium transition-all touch-target ${
              viewMode === 'calendar' ? 'bg-amber-500/20 text-amber-400' : 'text-zinc-400 hover:text-white'
            }`}
          >
            Calendar
          </button>
        </div>

        {/* Add Event Button */}
        <button className="flex items-center justify-center gap-2 h-10 sm:h-11 px-4 bg-amber-600 hover:bg-amber-500 text-white rounded-xl font-medium transition-colors touch-target">
          <Plus className="w-4 h-4" />
          <span>Add Event</span>
        </button>
      </div>

      {/* Timeline Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        <div className="p-3 bg-zinc-900/50 rounded-xl border border-white/10">
          <div className="text-lg sm:text-xl font-bold text-white">{events.length}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Total Events</div>
        </div>
        <div className="p-3 bg-zinc-900/50 rounded-xl border border-white/10">
          <div className="text-lg sm:text-xl font-bold text-emerald-400">{events.filter(e => e.isVerified).length}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Verified</div>
        </div>
        <div className="p-3 bg-zinc-900/50 rounded-xl border border-white/10">
          <div className="text-lg sm:text-xl font-bold text-purple-400">{events.filter(e => e.type === 'hearing').length}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Hearings</div>
        </div>
        <div className="p-3 bg-zinc-900/50 rounded-xl border border-white/10">
          <div className="text-lg sm:text-xl font-bold text-red-400">{events.filter(e => e.type === 'deadline').length}</div>
          <div className="text-[10px] sm:text-xs text-zinc-400">Deadlines</div>
        </div>
      </div>

      {/* Timeline View */}
      {viewMode === 'list' ? (
        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-4 sm:left-6 top-0 bottom-0 w-0.5 bg-zinc-800" />

          {/* Events */}
          <div className="space-y-4">
            {sortedEvents.map((event, index) => {
              const config = TYPE_CONFIG[event.type];
              const isPast = new Date(event.date) < new Date();

              return (
                <div
                  key={event.id}
                  className="relative pl-10 sm:pl-14"
                >
                  {/* Timeline Node */}
                  <div className={`absolute left-2 sm:left-4 w-5 h-5 sm:w-6 sm:h-6 rounded-full border-2 flex items-center justify-center ${
                    isPast
                      ? `bg-${config.color}-500/20 border-${config.color}-500/50`
                      : 'bg-zinc-800 border-zinc-600'
                  }`}>
                    <span className={`[&>svg]:w-2.5 [&>svg]:h-2.5 sm:[&>svg]:w-3 sm:[&>svg]:h-3 ${isPast ? `text-${config.color}-400` : 'text-zinc-500'}`}>
                      {config.icon}
                    </span>
                  </div>

                  {/* Event Card */}
                  <button
                    onClick={() => setSelectedEvent(event)}
                    className={`w-full text-left p-3 sm:p-4 rounded-xl border transition-all touch-target ${
                      selectedEvent?.id === event.id
                        ? 'bg-amber-500/10 border-amber-500/30'
                        : 'bg-zinc-900/50 border-white/10 hover:border-white/20 active:bg-zinc-800/50'
                    }`}
                  >
                    {/* Date Badge */}
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-medium bg-${config.color}-500/20 text-${config.color}-400`}>
                        {config.label}
                      </span>
                      <span className="text-[10px] sm:text-xs text-zinc-500">
                        {new Date(event.date).toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' })}
                      </span>
                      {event.isVerified && (
                        <CheckCircle className="w-3 h-3 text-emerald-400" />
                      )}
                    </div>

                    <h3 className="text-sm sm:text-base font-medium text-white mb-1">{event.title}</h3>
                    <p className="text-xs sm:text-sm text-zinc-400 line-clamp-2">{event.description}</p>

                    {/* Entities */}
                    {event.entities.length > 0 && (
                      <div className="flex items-center gap-2 mt-2">
                        <User className="w-3 h-3 text-zinc-500" />
                        <span className="text-[10px] sm:text-xs text-zinc-500">
                          {event.entities.join(', ')}
                        </span>
                      </div>
                    )}
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <CalendarView events={sortedEvents} onSelectEvent={setSelectedEvent} />
      )}

      {/* Event Detail Sheet */}
      {selectedEvent && (
        <EventDetailSheet event={selectedEvent} onClose={() => setSelectedEvent(null)} />
      )}
    </FeaturePageLayout>
  );
}

function CalendarView({ events, onSelectEvent }: { events: TimelineEvent[]; onSelectEvent: (e: TimelineEvent) => void }) {
  const [currentMonth, setCurrentMonth] = useState(new Date());

  const daysInMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0).getDate();
  const firstDayOfMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1).getDay();

  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);
  const paddingDays = Array.from({ length: firstDayOfMonth }, (_, i) => i);

  const getEventsForDay = (day: number) => {
    const dateStr = `${currentMonth.getFullYear()}-${String(currentMonth.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return events.filter(e => e.date === dateStr);
  };

  return (
    <div className="bg-zinc-900/50 rounded-2xl border border-white/10 overflow-hidden">
      {/* Month Navigation */}
      <div className="flex items-center justify-between p-3 sm:p-4 border-b border-white/10">
        <button
          onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
          className="p-2 hover:bg-white/5 rounded-lg transition-colors touch-target"
        >
          <ChevronLeft className="w-5 h-5 text-zinc-400" />
        </button>
        <h3 className="text-sm sm:text-base font-medium text-white">
          {currentMonth.toLocaleDateString('en-AU', { month: 'long', year: 'numeric' })}
        </h3>
        <button
          onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
          className="p-2 hover:bg-white/5 rounded-lg transition-colors touch-target"
        >
          <ChevronRight className="w-5 h-5 text-zinc-400" />
        </button>
      </div>

      {/* Day Headers */}
      <div className="grid grid-cols-7 border-b border-white/10">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
          <div key={day} className="p-2 text-center text-[10px] sm:text-xs text-zinc-500 font-medium">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7">
        {paddingDays.map((_, i) => (
          <div key={`pad-${i}`} className="aspect-square p-1 border-b border-r border-white/5 bg-zinc-950/50" />
        ))}
        {days.map((day) => {
          const dayEvents = getEventsForDay(day);
          const hasEvents = dayEvents.length > 0;

          return (
            <button
              key={day}
              onClick={() => hasEvents && onSelectEvent(dayEvents[0])}
              className={`aspect-square p-1 border-b border-r border-white/5 flex flex-col items-center justify-start transition-colors ${
                hasEvents ? 'hover:bg-white/5 cursor-pointer' : ''
              }`}
            >
              <span className={`text-xs sm:text-sm ${hasEvents ? 'text-white font-medium' : 'text-zinc-500'}`}>
                {day}
              </span>
              {hasEvents && (
                <div className="flex gap-0.5 mt-1">
                  {dayEvents.slice(0, 3).map((event) => (
                    <div
                      key={event.id}
                      className={`w-1.5 h-1.5 rounded-full bg-${TYPE_CONFIG[event.type].color}-400`}
                    />
                  ))}
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function EventDetailSheet({ event, onClose }: { event: TimelineEvent; onClose: () => void }) {
  const config = TYPE_CONFIG[event.type];

  return (
    <>
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40" onClick={onClose} />
      <div className="fixed inset-x-0 bottom-0 md:inset-y-0 md:left-auto md:right-0 md:w-96 bg-zinc-900 border-t md:border-t-0 md:border-l border-white/10 rounded-t-3xl md:rounded-none z-50 max-h-[80vh] md:max-h-none overflow-y-auto safe-area-pb">
        <div className="md:hidden flex justify-center pt-3 pb-2">
          <div className="w-10 h-1 rounded-full bg-zinc-600" />
        </div>

        <div className="p-4 sm:p-6">
          <div className="flex items-center gap-2 mb-4">
            <span className={`px-3 py-1 rounded-full text-sm font-medium bg-${config.color}-500/20 text-${config.color}-400`}>
              {config.label}
            </span>
            {event.isVerified && (
              <span className="flex items-center gap-1 text-xs text-emerald-400">
                <CheckCircle className="w-3 h-3" />
                Verified
              </span>
            )}
          </div>

          <h2 className="text-xl font-bold text-white mb-2">{event.title}</h2>
          <p className="text-sm text-zinc-400 mb-4">{event.description}</p>

          <div className="space-y-3 mb-6">
            <div className="flex items-center gap-3 text-sm">
              <Calendar className="w-4 h-4 text-zinc-500" />
              <span className="text-zinc-400">Date:</span>
              <span className="text-white">{new Date(event.date).toLocaleDateString('en-AU', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}</span>
            </div>
            {event.source && (
              <div className="flex items-center gap-3 text-sm">
                <FileText className="w-4 h-4 text-zinc-500" />
                <span className="text-zinc-400">Source:</span>
                <span className="text-white">{event.source}</span>
              </div>
            )}
          </div>

          {event.entities.length > 0 && (
            <div className="mb-6">
              <h3 className="text-xs font-medium text-zinc-400 uppercase tracking-wider mb-2">Related Entities</h3>
              <div className="flex flex-wrap gap-2">
                {event.entities.map((entity) => (
                  <span key={entity} className="flex items-center gap-1.5 px-3 py-1.5 bg-white/5 rounded-full text-sm text-zinc-300">
                    <User className="w-3 h-3" />
                    {entity}
                  </span>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={onClose}
            className="w-full h-11 sm:h-12 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl font-medium transition-colors touch-target"
          >
            Close
          </button>
        </div>
      </div>
    </>
  );
}

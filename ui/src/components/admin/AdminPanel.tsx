'use client';

import React, { useState } from 'react';
import {
  X, Settings, Key, Sliders, Zap, Server, Plus, Trash2, Save, RotateCcw,
  Brain, MessageSquare, Code, FileText, Check
} from 'lucide-react';
import { useStore } from '@/lib/store';
import { MODELS } from '@/lib/api/gemini';
import type { AgentConfig, MCPServer, UserSettings } from '@/types';

export function AdminPanel() {
  const { showAdmin, toggleAdmin, agentConfig, updateAgentConfig, settings, updateSettings } = useStore();
  const [activeTab, setActiveTab] = useState<'prompt' | 'model' | 'tools' | 'mcp' | 'settings'>('prompt');
  const [saved, setSaved] = useState(false);

  if (!showAdmin) return null;

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-0 md:p-4">
      <div className="w-full h-full md:max-w-4xl md:h-[80vh] bg-zinc-900 md:rounded-2xl border border-zinc-800 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-4 md:px-6 py-4 border-b border-zinc-800 flex-shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-600 to-blue-600 flex items-center justify-center flex-shrink-0">
              <Settings className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Admin Configuration</h2>
              <p className="text-sm text-zinc-400 hidden md:block">Configure your AI assistant</p>
            </div>
          </div>
          <button
            onClick={toggleAdmin}
            className="p-2 hover:bg-zinc-800 rounded-lg transition"
          >
            <X className="w-5 h-5 text-zinc-400" />
          </button>
        </div>

        <div className="flex flex-col md:flex-row flex-1 overflow-hidden">
          {/* Sidebar */}
          <div className="w-full md:w-48 border-b md:border-b-0 md:border-r border-zinc-800 p-2 flex md:flex-col gap-2 overflow-x-auto flex-shrink-0 bg-zinc-900/50">
            {[
              { id: 'prompt', label: 'Prompt', icon: MessageSquare },
              { id: 'model', label: 'Model', icon: Brain },
              { id: 'tools', label: 'Tools', icon: Zap },
              { id: 'mcp', label: 'MCP', icon: Server },
              { id: 'settings', label: 'Settings', icon: Sliders },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`flex items-center gap-3 px-4 py-3 md:py-2 rounded-lg text-sm transition whitespace-nowrap flex-1 md:flex-none justify-center md:justify-start ${
                  activeTab === tab.id
                    ? 'bg-cyan-600/20 text-cyan-300'
                    : 'text-zinc-400 hover:bg-zinc-800'
                }`}
              >
                <tab.icon className="w-5 h-5 md:w-4 md:h-4" />
                <span className="hidden md:inline">{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="flex-1 overflow-auto p-4 md:p-6 bg-zinc-900/30">
            {activeTab === 'prompt' && (
              <PromptTab
                systemPrompt={agentConfig.systemPrompt}
                onUpdate={(prompt) => updateAgentConfig({ systemPrompt: prompt })}
              />
            )}
            {activeTab === 'model' && (
              <ModelTab
                config={agentConfig}
                onUpdate={updateAgentConfig}
              />
            )}
            {activeTab === 'tools' && (
              <ToolsTab
                enabledTools={agentConfig.enabledTools}
                onUpdate={(tools) => updateAgentConfig({ enabledTools: tools })}
              />
            )}
            {activeTab === 'mcp' && (
              <MCPTab
                servers={agentConfig.mcpServers}
                onUpdate={(servers) => updateAgentConfig({ mcpServers: servers })}
              />
            )}
            {activeTab === 'settings' && (
              <SettingsTab
                settings={settings}
                onUpdate={updateSettings}
              />
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-4 md:px-6 py-4 border-t border-zinc-800 bg-zinc-900 flex-shrink-0">
          <button
            onClick={() => updateAgentConfig({
              systemPrompt: useStore.getState().agentConfig.systemPrompt
            })}
            className="flex items-center gap-2 px-3 md:px-4 py-2 text-zinc-400 hover:text-white transition text-sm md:text-base"
          >
            <RotateCcw className="w-4 h-4" />
            <span className="hidden md:inline">Reset to Default</span>
            <span className="md:hidden">Reset</span>
          </button>
          <button
            onClick={handleSave}
            className={`flex items-center gap-2 px-4 md:px-6 py-2 rounded-lg transition text-sm md:text-base ${
              saved
                ? 'bg-green-600 text-white'
                : 'bg-cyan-600 hover:bg-cyan-500 text-white'
            }`}
          >
            {saved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
            {saved ? 'Saved!' : 'Save Changes'}
          </button>
        </div>
      </div>
    </div>
  );
}

function PromptTab({
  systemPrompt,
  onUpdate
}: {
  systemPrompt: string;
  onUpdate: (prompt: string) => void;
}) {
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-white mb-2">System Prompt</label>
        <p className="text-sm text-zinc-400 mb-4">
          This prompt defines how the AI assistant behaves. You can customize its personality,
          capabilities, and instructions.
        </p>
        <textarea
          value={systemPrompt}
          onChange={(e) => onUpdate(e.target.value)}
          rows={20}
          className="w-full p-4 bg-zinc-800 border border-zinc-700 rounded-xl text-white text-sm font-mono resize-none focus:outline-none focus:border-cyan-500 transition"
          placeholder="Enter system prompt..."
        />
      </div>
    </div>
  );
}

function ModelTab({
  config,
  onUpdate
}: {
  config: AgentConfig;
  onUpdate: (updates: Partial<AgentConfig>) => void;
}) {
  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-white mb-2">Model</label>
        <select
          value={config.model}
          onChange={(e) => onUpdate({ model: e.target.value })}
          className="w-full p-3 bg-zinc-800 border border-zinc-700 rounded-xl text-white focus:outline-none focus:border-cyan-500 transition"
        >
          {Object.entries(MODELS).map(([name, id]) => (
            <option key={id} value={id}>{name} ({id})</option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-white mb-2">
          Temperature: {config.temperature}
        </label>
        <input
          type="range"
          min="0"
          max="2"
          step="0.1"
          value={config.temperature}
          onChange={(e) => onUpdate({ temperature: parseFloat(e.target.value) })}
          className="w-full accent-cyan-500"
        />
        <div className="flex justify-between text-xs text-zinc-500 mt-1">
          <span>Precise (0)</span>
          <span>Creative (2)</span>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-white mb-2">Max Tokens</label>
        <input
          type="number"
          value={config.maxTokens}
          onChange={(e) => onUpdate({ maxTokens: parseInt(e.target.value) })}
          className="w-full p-3 bg-zinc-800 border border-zinc-700 rounded-xl text-white focus:outline-none focus:border-cyan-500 transition"
        />
      </div>
    </div>
  );
}

function ToolsTab({
  enabledTools,
  onUpdate
}: {
  enabledTools: string[];
  onUpdate: (tools: string[]) => void;
}) {
  const allTools = [
    // Statutory Reasoning (Primary)
    { id: 'statutory_alignment', name: 'Statutory Alignment', description: 'Find applicable law + similar cases together', icon: '📜' },
    { id: 'get_applicable_law', name: 'Get Applicable Law', description: 'Look up Family Law Act sections', icon: '⚖️' },
    // Case Search Tools
    { id: 'find_similar_cases', name: 'Find Similar Cases', description: 'Match your story to relevant precedents', icon: '🔎' },
    { id: 'search_cases', name: 'Search Cases', description: 'Search cases by keywords or citation', icon: '🔍' },
    { id: 'get_case_details', name: 'Case Details', description: 'Get full details of a specific case', icon: '📑' },
    // Knowledge Base Tools
    { id: 'find_parties', name: 'Find Parties', description: 'Search parties in knowledge base', icon: '👥' },
    { id: 'get_case_questions', name: 'Case Questions', description: 'Get questions by case type', icon: '❓' },
    { id: 'get_unanswered_questions', name: 'Unanswered Questions', description: 'Track predictive questions', icon: '📋' },
    { id: 'find_actors_by_role', name: 'Find by Role', description: 'Find actors by their role', icon: '🎭' },
    { id: 'get_knowledge_context', name: 'Knowledge Context', description: 'Get GSW context for prompts', icon: '🧠' },
    // Utility Tools
    { id: 'create_artifact', name: 'Create Artifact', description: 'Create documents and code', icon: '📄' },
    { id: 'execute_code', name: 'Code Interpreter', description: 'Execute Python code', icon: '🐍' },
  ];

  const toggle = (toolId: string) => {
    if (enabledTools.includes(toolId)) {
      onUpdate(enabledTools.filter(t => t !== toolId));
    } else {
      onUpdate([...enabledTools, toolId]);
    }
  };

  return (
    <div className="space-y-3 sm:space-y-4">
      <p className="text-xs sm:text-sm text-zinc-400">
        Enable or disable tools available to the AI assistant.
      </p>
      <div className="grid gap-2 sm:gap-3">
        {allTools.map((tool) => (
          <button
            key={tool.id}
            onClick={() => toggle(tool.id)}
            className={`flex items-center gap-2.5 sm:gap-4 p-3 sm:p-4 rounded-lg sm:rounded-xl border transition touch-target ${
              enabledTools.includes(tool.id)
                ? 'bg-cyan-600/20 border-cyan-500/50'
                : 'bg-zinc-800 border-zinc-700 hover:border-zinc-600 active:border-zinc-600'
            }`}
          >
            <span className="text-xl sm:text-2xl flex-shrink-0">{tool.icon}</span>
            <div className="flex-1 text-left min-w-0">
              <div className="font-medium text-sm sm:text-base text-white truncate">{tool.name}</div>
              <div className="text-xs sm:text-sm text-zinc-400 truncate">{tool.description}</div>
            </div>
            <div className={`flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center ${
              enabledTools.includes(tool.id)
                ? 'bg-cyan-600 border-cyan-600'
                : 'border-zinc-600'
            }`}>
              {enabledTools.includes(tool.id) && (
                <Check className="w-3 h-3 text-white" />
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

function MCPTab({
  servers,
  onUpdate
}: {
  servers: MCPServer[];
  onUpdate: (servers: MCPServer[]) => void;
}) {
  const [newUrl, setNewUrl] = useState('');

  const addServer = () => {
    if (newUrl) {
      onUpdate([
        ...servers,
        {
          id: `mcp_${Date.now()}`,
          name: new URL(newUrl).hostname,
          url: newUrl,
          enabled: true,
          tools: [],
        }
      ]);
      setNewUrl('');
    }
  };

  return (
    <div className="space-y-4 sm:space-y-6">
      <p className="text-xs sm:text-sm text-zinc-400">
        Connect to MCP (Model Context Protocol) servers for additional tools and capabilities.
      </p>

      {/* Add Server - Stacked on mobile */}
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
        <input
          type="url"
          value={newUrl}
          onChange={(e) => setNewUrl(e.target.value)}
          placeholder="Enter MCP server URL..."
          className="flex-1 p-2.5 sm:p-3 bg-zinc-800 border border-zinc-700 rounded-lg sm:rounded-xl text-sm sm:text-base text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-500 transition"
        />
        <button
          onClick={addServer}
          className="px-4 py-2.5 sm:py-2 bg-cyan-600 hover:bg-cyan-500 active:bg-cyan-500 text-white rounded-lg sm:rounded-xl transition flex items-center justify-center gap-2 touch-target"
        >
          <Plus className="w-4 h-4" />
          <span>Add Server</span>
        </button>
      </div>

      {/* Server List */}
      <div className="space-y-2 sm:space-y-3">
        {servers.length === 0 ? (
          <div className="text-center py-6 sm:py-8 text-zinc-500">
            <Server className="w-10 h-10 sm:w-12 sm:h-12 mx-auto mb-2 sm:mb-3 opacity-50" />
            <p className="text-xs sm:text-sm">No MCP servers configured</p>
          </div>
        ) : (
          servers.map((server) => (
            <div
              key={server.id}
              className="flex items-center gap-2.5 sm:gap-4 p-3 sm:p-4 bg-zinc-800 rounded-lg sm:rounded-xl border border-zinc-700"
            >
              <Server className="w-4 h-4 sm:w-5 sm:h-5 text-zinc-400 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="font-medium text-sm sm:text-base text-white truncate">{server.name}</div>
                <div className="text-xs sm:text-sm text-zinc-500 truncate">{server.url}</div>
              </div>
              <button
                onClick={() => onUpdate(servers.filter(s => s.id !== server.id))}
                className="flex-shrink-0 p-2 hover:bg-zinc-700 active:bg-zinc-700 rounded-lg transition touch-target"
              >
                <Trash2 className="w-4 h-4 text-red-400" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function SettingsTab({
  settings,
  onUpdate
}: {
  settings: UserSettings;
  onUpdate: (updates: Partial<UserSettings>) => void;
}) {
  return (
    <div className="space-y-4 sm:space-y-6">
      {/* API Key */}
      <div>
        <label className="block text-xs sm:text-sm font-medium text-white mb-1.5 sm:mb-2">
          <Key className="w-3.5 h-3.5 sm:w-4 sm:h-4 inline mr-1.5 sm:mr-2" />
          OpenRouter API Key
        </label>
        <input
          type="password"
          value={settings.apiKey || ''}
          onChange={(e) => onUpdate({ apiKey: e.target.value })}
          placeholder="sk-or-..."
          className="w-full p-2.5 sm:p-3 bg-zinc-800 border border-zinc-700 rounded-lg sm:rounded-xl text-sm sm:text-base text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-500 transition"
        />
        <p className="text-[10px] sm:text-xs text-zinc-500 mt-1.5 sm:mt-2">
          Get your API key from <a href="https://openrouter.ai/keys" target="_blank" className="text-cyan-400 hover:underline active:underline">openrouter.ai/keys</a>
        </p>
      </div>

      {/* Theme */}
      <div>
        <label className="block text-xs sm:text-sm font-medium text-white mb-1.5 sm:mb-2">Theme</label>
        <div className="flex gap-2 sm:gap-3">
          {(['dark', 'light', 'system'] as const).map((theme) => (
            <button
              key={theme}
              onClick={() => onUpdate({ theme })}
              className={`flex-1 sm:flex-none px-3 sm:px-4 py-2 rounded-lg capitalize transition text-sm sm:text-base touch-target ${
                settings.theme === theme
                  ? 'bg-cyan-600 text-white'
                  : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700 active:bg-zinc-700'
              }`}
            >
              {theme}
            </button>
          ))}
        </div>
      </div>

      {/* Voice */}
      <div className="flex items-center justify-between p-3 sm:p-4 bg-zinc-800 rounded-lg sm:rounded-xl">
        <div className="flex-1 pr-3">
          <div className="font-medium text-sm sm:text-base text-white">Voice Input</div>
          <div className="text-xs sm:text-sm text-zinc-400">Enable microphone for voice commands</div>
        </div>
        <button
          onClick={() => onUpdate({ voiceEnabled: !settings.voiceEnabled })}
          className={`flex-shrink-0 w-11 sm:w-12 h-6 rounded-full transition touch-target ${
            settings.voiceEnabled ? 'bg-cyan-600' : 'bg-zinc-600'
          }`}
        >
          <div className={`w-5 h-5 bg-white rounded-full transition transform ${
            settings.voiceEnabled ? 'translate-x-5 sm:translate-x-6' : 'translate-x-0.5'
          }`} />
        </button>
      </div>

      {/* Code Interpreter */}
      <div className="flex items-center justify-between p-3 sm:p-4 bg-zinc-800 rounded-lg sm:rounded-xl">
        <div className="flex-1 pr-3">
          <div className="font-medium text-sm sm:text-base text-white">Code Interpreter</div>
          <div className="text-xs sm:text-sm text-zinc-400">Allow executing Python code</div>
        </div>
        <button
          onClick={() => onUpdate({ codeInterpreterEnabled: !settings.codeInterpreterEnabled })}
          className={`flex-shrink-0 w-11 sm:w-12 h-6 rounded-full transition touch-target ${
            settings.codeInterpreterEnabled ? 'bg-cyan-600' : 'bg-zinc-600'
          }`}
        >
          <div className={`w-5 h-5 bg-white rounded-full transition transform ${
            settings.codeInterpreterEnabled ? 'translate-x-5 sm:translate-x-6' : 'translate-x-0.5'
          }`} />
        </button>
      </div>
    </div>
  );
}

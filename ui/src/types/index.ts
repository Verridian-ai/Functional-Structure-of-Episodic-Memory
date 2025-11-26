// Types for the Legal AI Agent UI

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  artifacts?: Artifact[];
  toolCalls?: ToolCall[];
  isStreaming?: boolean;
}

export interface ArtifactSection {
  id: string;
  type: 'text' | 'image' | 'chart';
  title?: string;
  content: string;
  region: 'header' | 'footer' | 'main' | 'sidebar-left' | 'sidebar-right';
  style?: Record<string, string>;
  highlights?: { start: number; end: number; color: string; comment?: string }[];
}

export interface Artifact {
  id: string;
  type: 'document' | 'code' | 'pdf' | 'letter' | 'markdown' | 'html' | 'smart-canvas';
  title: string;
  content: string;
  structure?: {
    layout: 'standard' | 'report' | 'newsletter' | 'legal-brief';
    sections: ArtifactSection[];
  };
  language?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
  result?: string;
  status: 'pending' | 'running' | 'completed' | 'error';
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface AgentConfig {
  id: string;
  name: string;
  systemPrompt: string;
  model: string;
  temperature: number;
  maxTokens: number;
  enabledTools: string[];
  mcpServers: MCPServer[];
}

export interface MCPServer {
  id: string;
  name: string;
  url: string;
  enabled: boolean;
  tools: MCPTool[];
}

export interface MCPTool {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
}

export interface VoiceState {
  isListening: boolean;
  isSpeaking: boolean;
  transcript: string;
  audioLevel: number;
}

export interface UserSettings {
  theme: 'light' | 'dark' | 'system';
  voiceEnabled: boolean;
  voiceAutoSend: boolean;
  codeInterpreterEnabled: boolean;
  apiKey?: string;
}

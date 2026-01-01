// Types for the Legal AI Agent UI
// Pro-level TypeScript with strict typing and discriminated unions

// ============================================================================
// Message Types with Discriminated Unions
// ============================================================================

export type MessageRole = 'user' | 'assistant' | 'system';

/** Base message properties shared by all message types */
interface BaseMessage {
  id: string;
  content: string;
  timestamp: Date;
}

/** User message - simple text input */
export interface UserMessage extends BaseMessage {
  role: 'user';
  attachments?: MessageAttachment[];
}

/** Assistant message - may include streaming, tools, and artifacts */
export interface AssistantMessage extends BaseMessage {
  role: 'assistant';
  artifacts?: Artifact[];
  toolCalls?: ToolCall[];
  isStreaming?: boolean;
  /** Processing metadata for UX states */
  processingState?: 'idle' | 'thinking' | 'calling-tools' | 'generating';
}

/** System message - internal instructions */
export interface SystemMessage extends BaseMessage {
  role: 'system';
}

/** Discriminated union of all message types */
export type Message = UserMessage | AssistantMessage | SystemMessage;

/** Type guard for user messages */
export function isUserMessage(msg: Message): msg is UserMessage {
  return msg.role === 'user';
}

/** Type guard for assistant messages */
export function isAssistantMessage(msg: Message): msg is AssistantMessage {
  return msg.role === 'assistant';
}

/** Type guard for system messages */
export function isSystemMessage(msg: Message): msg is SystemMessage {
  return msg.role === 'system';
}

/** File attachment for messages */
export interface MessageAttachment {
  id: string;
  name: string;
  type: 'image' | 'document' | 'pdf';
  url: string;
  size: number;
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
  /** Accessibility preferences */
  reduceMotion?: boolean;
  highContrast?: boolean;
}

// ============================================================================
// UI State Types
// ============================================================================

/** Loading states for async operations */
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

/** Generic async state wrapper */
export interface AsyncState<T> {
  data: T | null;
  status: LoadingState;
  error: string | null;
}

/** Form field validation state */
export interface FieldState<T = string> {
  value: T;
  error: string | null;
  touched: boolean;
  dirty: boolean;
}

// ============================================================================
// Component Prop Types
// ============================================================================

/** Common size variants for UI components */
export type ComponentSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

/** Common color variants aligned with design system */
export type ComponentColor =
  | 'primary'    // Cyan/Emerald
  | 'secondary'  // Zinc
  | 'accent'     // Amber
  | 'success'    // Emerald
  | 'warning'    // Amber
  | 'error'      // Red
  | 'info';      // Blue

/** Base props for polymorphic components */
export interface PolymorphicProps<T extends React.ElementType> {
  as?: T;
  children?: React.ReactNode;
}

// ============================================================================
// API Response Types
// ============================================================================

/** Standard API response wrapper */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  meta?: {
    timestamp: string;
    requestId: string;
  };
}

/** Paginated response */
export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

// ============================================================================
// Event Types
// ============================================================================

/** Custom event payloads for inter-component communication */
export interface AppEvents {
  'theme:change': { theme: 'dark' | 'light' };
  'message:send': { content: string; attachments?: File[] };
  'artifact:select': { artifactId: string };
  'canvas:toggle': { open: boolean };
  'voice:start': undefined;
  'voice:stop': { transcript: string };
}

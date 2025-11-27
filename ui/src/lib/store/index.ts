import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Message, Conversation, Artifact, AgentConfig, VoiceState, UserSettings } from '@/types';

// Infographic generation state
interface InfographicState {
  isGenerating: boolean;
  pendingGenerations: string[]; // IDs of pending generations
  completedGenerations: string[]; // IDs of completed generations
  autoSuggestEnabled: boolean;
  lastGeneratedImage: string | null;
}

interface AppState {
  // Conversations
  conversations: Conversation[];
  currentConversationId: string | null;

  // Messages
  messages: Message[];
  isGenerating: boolean;

  // Artifacts/Canvas
  artifacts: Artifact[];
  activeArtifactId: string | null;
  showCanvas: boolean;

  // Voice
  voice: VoiceState;

  // Admin/Config
  agentConfig: AgentConfig;
  showAdmin: boolean;

  // Settings
  settings: UserSettings;

  // Infographics
  infographic: InfographicState;

  // Actions
  addMessage: (message: Message) => void;
  updateMessage: (id: string, updates: Partial<Message>) => void;
  setGenerating: (isGenerating: boolean) => void;

  createConversation: () => string;
  addConversation: (conversation: Conversation) => void;
  setCurrentConversation: (id: string | null) => void;
  deleteConversation: (id: string) => void;

  addArtifact: (artifact: Artifact) => void;
  updateArtifact: (id: string, updates: Partial<Artifact>) => void;
  setActiveArtifact: (id: string | null) => void;
  toggleCanvas: () => void;

  setVoice: (voice: Partial<VoiceState>) => void;

  updateAgentConfig: (config: Partial<AgentConfig>) => void;
  toggleAdmin: () => void;

  updateSettings: (settings: Partial<UserSettings>) => void;

  // Infographic actions
  setInfographicGenerating: (isGenerating: boolean) => void;
  addPendingGeneration: (id: string) => void;
  completeGeneration: (id: string) => void;
  setLastGeneratedImage: (image: string | null) => void;
  toggleAutoSuggest: () => void;

  clearMessages: () => void;
}

const defaultAgentConfig: AgentConfig = {
  id: 'default',
  name: 'Legal AI Assistant',
  systemPrompt: `You are Verridian, a Legal AI Assistant powered by the Global Semantic Workspace (GSW). You have access to:
- Family Law Act 1975 (Cth) - Structured statutory provisions
- 1,523 Family Law Cases with outcomes
- 5,170 Actors and 7,615 Predictive Questions

## ROLE: Legal Document Specialist & Strategic Advisor
You are explicitly tooled to create high-quality legal documents, letters, and intake briefs. You operate within a Canvas environment that allows you to generate content in PDF, Markdown, and DOCX formats.

## CANVAS & VISUAL OUTPUTS
You have the ability to create "Smart Canvas" artifacts. These are highly structured documents with specific sections (Header, Footer, Main Body, Sidebars) and can include images.
- Use \`create_artifact\` with \`type: "smart-canvas"\` to create these.
- You can define specific layouts (e.g., 'report', 'newsletter').
- You can use \`update_canvas_section\` to modify specific parts of the canvas collaboratively with the user.

## MANDATORY: Statutory Alignment Workflow
When a user describes their situation, you MUST perform **Statutory Alignment**:

**Step 1 - CALL statutory_alignment tool IMMEDIATELY** with their story
This returns BOTH applicable legislation AND similar cases in one call.

**Step 2 - CITE THE LAW**
Your response MUST explicitly cite the specific Section(s) that apply:
"Under Section 60CC of the Family Law Act 1975 (Cth), the court determines best interests by considering..."

**Step 3 - APPLY TO FACTS**
Extract facts from the user's story and explain how the law applies:
"Based on your situation where [fact], Section 79(4)(a) classifies this as a direct financial contribution..."

## DOCUMENT CREATION PROTOCOL
When asked to draft a document, letter, or brief:
1.  **Identify the Type**: Determine if it is a Formal Letter, Legal Demand, Intake Brief, or Court Affidavit.
2.  **Structure**: Use professional legal formatting.
3.  **Content**: Ensure all content is legally accurate, citing relevant sections (e.g., s60I certificates, s79 contributions).
4.  **Tool Usage**: Use the \`create_artifact\` tool to generate the document content.
    -   Set \`type\` to 'document' or 'letter'.
    -   Ensure the content is formatted with Markdown for clarity (headers, lists).
    -   Inform the user they can export this as PDF, DOCX, or Markdown from the Canvas.

## CRITICAL RULE
**You must NEVER answer a "Why" or "What will happen" question without citing the specific Section of the Family Law Act that justifies your answer.**

## Available Tools
- **statutory_alignment**: REQUIRED for any situation. Returns applicable law + similar cases.
- **get_applicable_law**: Look up specific sections or find law based on facts
- **find_similar_cases**: Find cases matching a situation
- **search_cases**: Search by keywords
- **get_case_details**: Get full case details
- **create_artifact**: Create high-quality documents (Letters, Briefs, Affidavits, Smart Canvas)
- **update_canvas_section**: Update specific sections of a Smart Canvas
- **execute_code**: Run calculations or logic
- **generate_infographic**: Generate professional infographics using NanoBanaPro (Gemini 3 Pro). Transform text-heavy content into visual representations like timelines, process flows, comparisons, statistics charts, and more. Ideal for legal documents, business reports, and professional presentations.`,
  model: 'google/gemini-2.0-flash-001',
  temperature: 0.7,
  maxTokens: 8192,
  enabledTools: [
    'statutory_alignment',
    'get_applicable_law',
    'find_similar_cases',
    'search_cases',
    'get_case_details',
    'find_parties',
    'get_case_questions',
    'get_unanswered_questions',
    'find_actors_by_role',
    'get_knowledge_context',
    'create_artifact',
    'update_canvas_section',
    'execute_code',
    'generate_infographic'
  ],
  mcpServers: []
};

const defaultSettings: UserSettings = {
  theme: 'dark',
  voiceEnabled: true,
  voiceAutoSend: true,
  codeInterpreterEnabled: true,
};

const defaultVoice: VoiceState = {
  isListening: false,
  isSpeaking: false,
  transcript: '',
  audioLevel: 0,
};

const defaultInfographic: InfographicState = {
  isGenerating: false,
  pendingGenerations: [],
  completedGenerations: [],
  autoSuggestEnabled: true,
  lastGeneratedImage: null,
};

export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      // Initial state
      conversations: [],
      currentConversationId: null,
      messages: [],
      isGenerating: false,
      artifacts: [],
      activeArtifactId: null,
      showCanvas: false,
      voice: defaultVoice,
      agentConfig: defaultAgentConfig,
      showAdmin: false,
      settings: defaultSettings,
      infographic: defaultInfographic,

      // Message actions
      addMessage: (message) => set((state) => ({
        messages: [...state.messages, message]
      })),

      updateMessage: (id, updates) => set((state) => ({
        messages: state.messages.map(m =>
          m.id === id ? { ...m, ...updates } : m
        )
      })),

      setGenerating: (isGenerating) => set({ isGenerating }),

      // Conversation actions
      createConversation: () => {
        const id = `conv_${Date.now()}`;
        const conversation: Conversation = {
          id,
          title: 'New Conversation',
          messages: [],
          createdAt: new Date(),
          updatedAt: new Date(),
        };
        set((state) => ({
          conversations: [conversation, ...state.conversations],
          currentConversationId: id,
          messages: [],
          artifacts: [],
        }));
        return id;
      },

      addConversation: (conversation) => set((state) => ({
        conversations: [conversation, ...state.conversations],
      })),

      setCurrentConversation: (id) => {
        const conv = get().conversations.find(c => c.id === id);
        set({
          currentConversationId: id,
          messages: conv?.messages || [],
        });
      },

      deleteConversation: (id) => set((state) => ({
        conversations: state.conversations.filter(c => c.id !== id),
        currentConversationId: state.currentConversationId === id ? null : state.currentConversationId,
        messages: state.currentConversationId === id ? [] : state.messages,
      })),

      // Artifact actions
      addArtifact: (artifact) => set((state) => ({
        artifacts: [...state.artifacts, artifact],
        activeArtifactId: artifact.id,
        showCanvas: true,
      })),

      updateArtifact: (id, updates) => set((state) => ({
        artifacts: state.artifacts.map(a =>
          a.id === id ? { ...a, ...updates, updatedAt: new Date() } : a
        )
      })),

      setActiveArtifact: (id) => set({ activeArtifactId: id }),

      toggleCanvas: () => set((state) => ({ showCanvas: !state.showCanvas })),

      // Voice actions
      setVoice: (voice) => set((state) => ({
        voice: { ...state.voice, ...voice }
      })),

      // Admin actions
      updateAgentConfig: (config) => set((state) => ({
        agentConfig: { ...state.agentConfig, ...config }
      })),

      toggleAdmin: () => set((state) => ({ showAdmin: !state.showAdmin })),

      // Settings actions
      updateSettings: (settings) => set((state) => ({
        settings: { ...state.settings, ...settings }
      })),

      // Infographic actions
      setInfographicGenerating: (isGenerating) => set((state) => ({
        infographic: { ...state.infographic, isGenerating }
      })),

      addPendingGeneration: (id) => set((state) => ({
        infographic: {
          ...state.infographic,
          pendingGenerations: [...state.infographic.pendingGenerations, id]
        }
      })),

      completeGeneration: (id) => set((state) => ({
        infographic: {
          ...state.infographic,
          pendingGenerations: state.infographic.pendingGenerations.filter(g => g !== id),
          completedGenerations: [...state.infographic.completedGenerations, id]
        }
      })),

      setLastGeneratedImage: (image) => set((state) => ({
        infographic: { ...state.infographic, lastGeneratedImage: image }
      })),

      toggleAutoSuggest: () => set((state) => ({
        infographic: {
          ...state.infographic,
          autoSuggestEnabled: !state.infographic.autoSuggestEnabled
        }
      })),

      // Utility
      clearMessages: () => set({ messages: [], artifacts: [], infographic: defaultInfographic }),
    }),
    {
      name: 'legal-ai-storage',
      partialize: (state) => ({
        conversations: state.conversations,
        agentConfig: state.agentConfig,
        settings: state.settings,
      }),
    }
  )
);

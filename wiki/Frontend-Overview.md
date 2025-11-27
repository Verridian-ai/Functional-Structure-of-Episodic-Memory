# Frontend Overview

The Verridian AI frontend is a **Next.js 16** application with **React 19** that provides an interactive interface for legal AI queries.

## Overview

**Location**: `ui/`

```mermaid
graph TB
    subgraph "Frontend Architecture"
        App[Next.js App Router]
        Pages[Pages]
        Components[Components]
        API[API Routes]
        Lib[Libraries]
    end

    subgraph "Pages"
        Home[/ - Chat Interface]
        Viz[/visualize - 3D Graph]
    end

    subgraph "External"
        OR[OpenRouter API]
        M0[Mem0 Memory]
    end

    User[User] --> App
    App --> Pages
    Pages --> Components
    Pages --> API
    API --> OR
    API --> M0
```

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16 | React framework with App Router |
| React | 19 | UI components |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 3.x | Styling |
| Three.js | Latest | 3D visualization |
| Zustand | Latest | State management |

---

## Directory Structure

```
ui/
├── src/
│   ├── app/                    # App Router pages
│   │   ├── api/               # API routes
│   │   │   ├── chat/          # Chat completions
│   │   │   ├── gsw/           # GSW extraction
│   │   │   ├── graph/         # Graph data
│   │   │   ├── memory/        # Mem0 integration
│   │   │   ├── execute/       # Code execution
│   │   │   ├── pdf/           # PDF generation
│   │   │   └── docx/          # DOCX generation
│   │   ├── visualize/         # 3D visualization page
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Home page
│   ├── components/            # React components
│   │   ├── chat/              # Chat interface
│   │   ├── ui/                # UI primitives
│   │   ├── layout/            # Layout components
│   │   ├── visualization/     # 3D components
│   │   ├── admin/             # Admin panel
│   │   ├── voice/             # Voice interface
│   │   ├── tools/             # Document tools
│   │   └── canvas/            # Canvas panel
│   ├── hooks/                 # Custom hooks
│   ├── lib/                   # Libraries
│   │   ├── api/               # API clients
│   │   ├── store/             # Zustand stores
│   │   ├── tem/               # TEM TypeScript
│   │   ├── vsa/               # VSA TypeScript
│   │   └── active_inference/  # Agency TypeScript
│   └── types/                 # TypeScript types
├── public/                    # Static assets
├── package.json
└── tailwind.config.js
```

---

## Pages

### Home Page (`/`)

**File**: `ui/src/app/page.tsx`

Main chat interface:
- Message input with streaming responses
- Conversation history
- Settings panel for API configuration
- Document tools integration

### Visualize Page (`/visualize`)

**File**: `ui/src/app/visualize/page.tsx`

3D legal knowledge graph visualization:
- Three.js-powered graph rendering
- Actor nodes and relationship edges
- Interactive navigation

---

## API Routes

### Chat API

**File**: `ui/src/app/api/chat/route.ts`

```typescript
POST /api/chat
Body: {
    messages: Message[],
    apiKey: string,
    model?: string,
    temperature?: number,
    systemPrompt?: string,
    userId?: string
}
Response: Server-Sent Events stream
```

### GSW API

**File**: `ui/src/app/api/gsw/route.ts`

```typescript
POST /api/gsw
Body: {
    text: string,
    situation?: string
}
Response: ChunkExtraction JSON
```

### Memory API

**File**: `ui/src/app/api/memory/add/route.ts`

```typescript
POST /api/memory/add
Body: {
    content: string,
    userId?: string,
    metadata?: object
}
Response: { success: boolean, memoryId?: string }
```

---

## State Management

### Zustand Store

**File**: `ui/src/lib/store/index.ts`

```typescript
interface AppState {
    messages: Message[];
    settings: Settings;
    isLoading: boolean;

    // Actions
    addMessage: (message: Message) => void;
    updateSettings: (settings: Partial<Settings>) => void;
    clearMessages: () => void;
}

export const useStore = create<AppState>((set) => ({
    messages: [],
    settings: defaultSettings,
    isLoading: false,

    addMessage: (message) =>
        set((state) => ({ messages: [...state.messages, message] })),

    updateSettings: (settings) =>
        set((state) => ({ settings: { ...state.settings, ...settings } })),

    clearMessages: () => set({ messages: [] }),
}));
```

---

## TypeScript Libraries

### TEM Types

**File**: `ui/src/lib/tem/types.ts`

TypeScript implementation of TEM concepts for client-side use.

### VSA Types

**File**: `ui/src/lib/vsa/types.ts`

TypeScript implementation of VSA operations.

### Active Inference

**File**: `ui/src/lib/active_inference/types.ts`

TypeScript implementation of Active Inference concepts.

---

## Configuration

### Tailwind Config

```javascript
// tailwind.config.js
module.exports = {
    content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
    theme: {
        extend: {
            colors: {
                verridian: {
                    primary: '#00ff88',
                    dark: '#0a0a0a',
                    accent: '#ff00ff'
                }
            }
        }
    }
};
```

### Next.js Config

```javascript
// next.config.js
module.exports = {
    experimental: {
        serverActions: true
    },
    async headers() {
        return [{
            source: '/api/:path*',
            headers: [
                { key: 'Access-Control-Allow-Origin', value: '*' }
            ]
        }];
    }
};
```

---

## Development

### Local Development

```bash
cd ui
npm install
npm run dev
```

Access at: `http://localhost:3000`

### Build

```bash
npm run build
npm start
```

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
```

---

## Environment Variables

```bash
# .env.local
OPENROUTER_API_KEY=sk-or-...    # Optional: Server-side default
MEM0_API_KEY=m0-...             # Optional: Memory service
```

Note: API keys are typically provided by the user in the UI settings.

---

## Related Pages

- [Frontend-Components](Frontend-Components) - Component catalog
- [Frontend-API-Routes](Frontend-API-Routes) - API documentation
- [Quick-Start](Quick-Start) - Getting started
- [Development-Guide](Development-Guide) - Development setup

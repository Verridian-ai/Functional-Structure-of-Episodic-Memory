import { NextRequest, NextResponse } from 'next/server';
import { MemoryClient } from 'mem0ai';

const OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions';

export async function POST(request: NextRequest) {
  try {
    const { messages, model, temperature, maxTokens, apiKey, systemPrompt, tools, userId } = await request.json();

    if (!apiKey) {
      return NextResponse.json(
        { error: 'API key is required. Please configure it in Settings.' },
        { status: 400 }
      );
    }

    // --- Mem0 Integration ---
    let memoryContext = "";
    let memoryClient = null;
    
    // Initialize Mem0 if API key exists in env or request (assuming env for now)
    // Note: For this test session, we assume MEM0_API_KEY is available or we fallback gracefully
    if (process.env.MEM0_API_KEY) {
      try {
        memoryClient = new MemoryClient({
          apiKey: process.env.MEM0_API_KEY
        });

        const lastMessage = messages[messages.length - 1];
        if (lastMessage.role === 'user') {
           // 1. Add to Memory (Store interaction)
           // We add it async but don't block heavily? 
           // Actually, usually you search BEFORE adding the current query to get context relevant to it.
           // Then add the query + response later.
           
           // Search for relevant memories
           const searchResults = await memoryClient.search(lastMessage.content, { 
             user_id: userId || 'test_session_user' 
           });

           if (searchResults && searchResults.length > 0) {
             memoryContext = `\n\nRELEVANT MEMORY FROM PREVIOUS INTERACTIONS:\n${searchResults.map((m: any) => `- ${m.memory}`).join('\n')}`;
           }
           
           // Add current user message to memory (fire and forget or await)
           await memoryClient.add(lastMessage.content, { 
             user_id: userId || 'test_session_user', 
             metadata: { role: 'user' } 
           });
        }
      } catch (memError) {
        console.warn("Mem0 Error:", memError);
      }
    }
    // ------------------------

    // Build the request
    const requestBody: any = {
      model: model || 'google/gemini-2.5-flash-preview-05-20',
      messages: [
        ...(systemPrompt ? [{ role: 'system', content: systemPrompt + memoryContext }] : []),
        ...messages.map((m: any) => ({
          role: m.role,
          content: m.content,
        })),
      ],
      temperature: temperature ?? 0.7,
      max_tokens: maxTokens ?? 4096,
      stream: true,
    };

    // Add tools if provided
    if (tools && tools.length > 0) {
      requestBody.tools = tools;
      requestBody.tool_choice = 'auto';
    }

    const response = await fetch(OPENROUTER_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': 'http://localhost:3000',
        'X-Title': 'Legal AI Assistant',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: error.error?.message || `API error: ${response.status}` },
        { status: response.status }
      );
    }

    // Return streaming response
    const encoder = new TextEncoder();
    const decoder = new TextDecoder();

    const stream = new ReadableStream({
      async start(controller) {
        const reader = response.body?.getReader();
        if (!reader) {
          controller.close();
          return;
        }

        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') {
                  controller.enqueue(encoder.encode('data: [DONE]\n\n'));
                  continue;
                }

                try {
                  const parsed = JSON.parse(data);
                  controller.enqueue(encoder.encode(`data: ${JSON.stringify(parsed)}\n\n`));
                } catch {
                  // Skip invalid JSON
                }
              }
            }
          }
        } finally {
          reader.releaseLock();
          controller.close();
        }
      },
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Chat request failed' },
      { status: 500 }
    );
  }
}

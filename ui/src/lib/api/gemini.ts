import OpenAI from 'openai';
import type { Message, AgentConfig, ToolCall } from '@/types';
import { executeTool, formatToolResult } from './tools';

// OpenRouter configuration for Gemini models
const getClient = (apiKey?: string) => new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: apiKey || process.env.NEXT_PUBLIC_OPENROUTER_API_KEY || '',
  dangerouslyAllowBrowser: true,
});

// Available models
export const MODELS = {
  'gemini-3-pro': 'google/gemini-3-pro-preview', // Added Gemini 3 Pro
  'gemini-2.0-flash': 'google/gemini-2.0-flash-001',
  'gemini-2.5-flash': 'google/gemini-2.5-flash-preview-05-20',
  'gemini-2.5-pro': 'google/gemini-2.5-pro-preview',
  'gemini-exp': 'google/gemini-exp-1206',
  'claude-sonnet': 'anthropic/claude-sonnet-4',
  'gpt-4o': 'openai/gpt-4o',
} as const;

// Tool definitions for function calling
export const TOOL_DEFINITIONS = [
  {
    type: 'function' as const,
    function: {
      name: 'find_parties',
      description: 'Search for parties (people) in the legal knowledge base by name',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Optional name to search for (case-insensitive)',
          },
        },
        required: [],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'get_case_questions',
      description: 'Get questions about a specific case type (parenting, property, divorce, child_support)',
      parameters: {
        type: 'object',
        properties: {
          case_type: {
            type: 'string',
            enum: ['parenting', 'property', 'divorce', 'child_support'],
            description: 'Type of case',
          },
        },
        required: ['case_type'],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'get_unanswered_questions',
      description: 'Get unanswered predictive questions from the knowledge base',
      parameters: {
        type: 'object',
        properties: {
          limit: {
            type: 'number',
            description: 'Maximum number of questions (default 10)',
          },
        },
        required: [],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'find_actors_by_role',
      description: 'Find actors by role (Applicant, Respondent, Judge, Mother, Father, etc.)',
      parameters: {
        type: 'object',
        properties: {
          role: {
            type: 'string',
            description: 'The role to search for',
          },
        },
        required: ['role'],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'get_knowledge_context',
      description: 'Get compressed knowledge context for inclusion in prompts',
      parameters: {
        type: 'object',
        properties: {
          format: {
            type: 'string',
            enum: ['toon', 'json'],
            description: 'Output format (toon is ~40% smaller)',
          },
          max_actors: {
            type: 'number',
            description: 'Maximum actors to include',
          },
        },
        required: [],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'create_artifact',
      description: 'Create a document, letter, or code artifact for the user',
      parameters: {
        type: 'object',
        properties: {
          type: {
            type: 'string',
            enum: ['document', 'code', 'letter', 'markdown', 'html'],
            description: 'Type of artifact',
          },
          title: {
            type: 'string',
            description: 'Title of the artifact',
          },
          content: {
            type: 'string',
            description: 'Content of the artifact',
          },
          language: {
            type: 'string',
            description: 'Programming language (for code artifacts)',
          },
        },
        required: ['type', 'title', 'content'],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'execute_code',
      description: 'Execute Python code in the code interpreter',
      parameters: {
        type: 'object',
        properties: {
          code: {
            type: 'string',
            description: 'Python code to execute',
          },
        },
        required: ['code'],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'find_similar_cases',
      description: 'Find similar family law cases based on user story or situation. Analyzes the story to extract key issues (parenting, property, custody, etc.) and finds relevant precedent cases with outcomes.',
      parameters: {
        type: 'object',
        properties: {
          story: {
            type: 'string',
            description: 'The user\'s situation or story describing their family law issue',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of similar cases to return (default 5)',
          },
        },
        required: ['story'],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'search_cases',
      description: 'Search for specific family law cases by keywords, case name, or legal terms',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Search query (keywords, case name, or legal terms)',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of cases to return (default 10)',
          },
        },
        required: ['query'],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'get_case_details',
      description: 'Get full details of a specific case by citation',
      parameters: {
        type: 'object',
        properties: {
          citation: {
            type: 'string',
            description: 'Case citation (e.g., "Smith v Jones [2020] FamCA 123")',
          },
        },
        required: ['citation'],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'get_applicable_law',
      description: 'Find applicable sections of the Family Law Act 1975 based on facts or retrieve specific sections. Returns statutory provisions with legal tests.',
      parameters: {
        type: 'object',
        properties: {
          facts: {
            type: 'string',
            description: 'The facts or situation to find applicable law for',
          },
          section: {
            type: 'string',
            description: 'Specific section number to retrieve (e.g., "79", "60CC", "75(2)")',
          },
        },
        required: [],
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'statutory_alignment',
      description: 'Combined analysis: finds both applicable legislation AND similar cases for a user situation. Use this for comprehensive legal analysis.',
      parameters: {
        type: 'object',
        properties: {
          story: {
            type: 'string',
            description: 'The user\'s situation or story describing their family law issue',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of cases to return (default 5)',
          },
        },
        required: ['story'],
      },
    },
  },
];

// Convert messages to OpenAI format
function toOpenAIMessages(messages: Message[], systemPrompt: string) {
  const formatted: OpenAI.Chat.ChatCompletionMessageParam[] = [
    { role: 'system', content: systemPrompt },
  ];

  for (const msg of messages) {
    if (msg.role === 'user') {
      formatted.push({ role: 'user', content: msg.content });
    } else if (msg.role === 'assistant') {
      formatted.push({ role: 'assistant', content: msg.content });
    }
  }

  return formatted;
}

export interface StreamCallbacks {
  onToken: (token: string) => void;
  onToolCall: (toolCall: ToolCall) => void;
  onComplete: (fullContent: string) => void;
  onError: (error: Error) => void;
}

// Stream chat completion with tool execution
export async function streamChat(
  messages: Message[],
  config: AgentConfig,
  callbacks: StreamCallbacks,
  apiKey?: string
) {
  const client = getClient(apiKey);
  let formattedMessages = toOpenAIMessages(messages, config.systemPrompt);
  const enabledTools = TOOL_DEFINITIONS.filter(t =>
    config.enabledTools.includes(t.function.name)
  );

  try {
    let fullContent = '';
    const allToolCalls: ToolCall[] = [];
    let continueLoop = true;
    let iterations = 0;
    const maxIterations = 5; // Prevent infinite loops

    while (continueLoop && iterations < maxIterations) {
      iterations++;
      continueLoop = false;

      const stream = await client.chat.completions.create({
        model: config.model,
        messages: formattedMessages,
        temperature: config.temperature,
        max_tokens: config.maxTokens,
        stream: true,
        tools: enabledTools.length > 0 ? enabledTools : undefined,
      });

      const currentToolCalls: Map<number, ToolCall> = new Map();
      let currentContent = '';
      let argumentsBuffer: Map<number, string> = new Map();

      for await (const chunk of stream) {
        const delta = chunk.choices[0]?.delta;
        const finishReason = chunk.choices[0]?.finish_reason;

        // Handle content
        if (delta?.content) {
          currentContent += delta.content;
          fullContent += delta.content;
          callbacks.onToken(delta.content);
        }

        // Handle tool calls (accumulate arguments properly)
        if (delta?.tool_calls) {
          for (const tc of delta.tool_calls) {
            const index = tc.index;
            let existing = currentToolCalls.get(index);

            if (!existing && tc.id) {
              existing = {
                id: tc.id,
                name: tc.function?.name || '',
                arguments: {},
                status: 'running',
              };
              currentToolCalls.set(index, existing);
              argumentsBuffer.set(index, '');
              callbacks.onToolCall(existing);
            }

            if (existing) {
              if (tc.function?.name) {
                existing.name = tc.function.name;
              }
              if (tc.function?.arguments) {
                const buffer = argumentsBuffer.get(index) || '';
                argumentsBuffer.set(index, buffer + tc.function.arguments);
              }
            }
          }
        }

        // Check if we need to execute tools
        if (finishReason === 'tool_calls') {
          continueLoop = true;
        }
      }

      // Parse accumulated arguments and execute tools
      if (currentToolCalls.size > 0) {
        // First, parse all arguments
        for (const [index, tc] of currentToolCalls) {
          const argsString = argumentsBuffer.get(index) || '{}';
          try {
            tc.arguments = JSON.parse(argsString);
          } catch {
            tc.arguments = {};
          }
        }

        // Add assistant message with tool calls to conversation
        const assistantToolCallsMessage: OpenAI.Chat.ChatCompletionMessageParam = {
          role: 'assistant',
          content: currentContent || null,
          tool_calls: Array.from(currentToolCalls.values()).map(tc => ({
            id: tc.id,
            type: 'function' as const,
            function: {
              name: tc.name,
              arguments: JSON.stringify(tc.arguments),
            },
          })),
        };
        formattedMessages.push(assistantToolCallsMessage);

        // Execute each tool and add results
        for (const [, tc] of currentToolCalls) {
          tc.status = 'running';
          callbacks.onToolCall(tc);

          // Execute the tool
          const result = await executeTool(tc.name, tc.arguments);

          // Update tool call status
          tc.status = result.success ? 'completed' : 'error';
          tc.result = formatToolResult(tc.name, result);
          callbacks.onToolCall(tc);

          // Add tool result to conversation
          const toolResultMessage: OpenAI.Chat.ChatCompletionMessageParam = {
            role: 'tool',
            tool_call_id: tc.id,
            content: tc.result,
          };
          formattedMessages.push(toolResultMessage);

          allToolCalls.push(tc);
        }
      }
    }

    callbacks.onComplete(fullContent);
    return { content: fullContent, toolCalls: allToolCalls };

  } catch (error) {
    callbacks.onError(error as Error);
    throw error;
  }
}

// Non-streaming chat for simpler use cases
export async function chat(
  messages: Message[],
  config: AgentConfig,
  apiKey?: string
) {
  const client = getClient(apiKey);
  const formattedMessages = toOpenAIMessages(messages, config.systemPrompt);

  const response = await client.chat.completions.create({
    model: config.model,
    messages: formattedMessages,
    temperature: config.temperature,
    max_tokens: config.maxTokens,
    tools: TOOL_DEFINITIONS.filter(t =>
      config.enabledTools.includes(t.function.name)
    ),
  });

  return response.choices[0];
}

// Tool execution handlers for GSW knowledge base integration

export interface ToolResult {
  success: boolean;
  data: unknown;
  error?: string;
}

// Execute a tool and return the result
export async function executeTool(
  toolName: string,
  args: Record<string, unknown>
): Promise<ToolResult> {
  try {
    switch (toolName) {
      case 'find_parties':
        return await callGSW('find_parties', args);

      case 'get_case_questions':
        return await callGSW('get_case_questions', args);

      case 'get_unanswered_questions':
        return await callGSW('get_unanswered_questions', args);

      case 'find_actors_by_role':
        return await callGSW('find_actors_by_role', args);

      case 'get_knowledge_context':
        return await callGSW('get_knowledge_context', args);

      case 'search_cases':
        return await callGSW('search_cases', args);

      case 'find_similar_cases':
        return await callGSW('find_similar_cases', args);

      case 'get_case_details':
        return await callGSW('get_case_details', args);

      case 'get_applicable_law':
        return await callGSW('get_applicable_law', args);

      case 'statutory_alignment':
        return await callGSW('statutory_alignment', args);

      case 'create_artifact':
        // Artifacts are handled directly in the UI
        return { success: true, data: { message: 'Artifact created' } };

      case 'execute_code':
        return await executeCode(args.code as string);

      default:
        return { success: false, data: null, error: `Unknown tool: ${toolName}` };
    }
  } catch (error) {
    return {
      success: false,
      data: null,
      error: error instanceof Error ? error.message : 'Tool execution failed',
    };
  }
}

// Call the GSW API
async function callGSW(
  action: string,
  params: Record<string, unknown>
): Promise<ToolResult> {
  try {
    const response = await fetch('/api/gsw', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, params }),
    });

    if (!response.ok) {
      const error = await response.json();
      return { success: false, data: null, error: error.error || 'GSW request failed' };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      data: null,
      error: error instanceof Error ? error.message : 'GSW request failed',
    };
  }
}

// Execute Python code (calls the execute API)
async function executeCode(code: string): Promise<ToolResult> {
  try {
    const response = await fetch('/api/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    });

    if (!response.ok) {
      const error = await response.json();
      return { success: false, data: null, error: error.error || 'Code execution failed' };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      data: null,
      error: error instanceof Error ? error.message : 'Code execution failed',
    };
  }
}

// Format tool results for display
export function formatToolResult(toolName: string, result: ToolResult): string {
  if (!result.success) {
    return `Error: ${result.error}`;
  }

  const data = result.data as Record<string, unknown>;

  switch (toolName) {
    case 'find_parties':
    case 'find_actors_by_role': {
      const results = (data.results || []) as Array<{
        id: string;
        name: string;
        role: string;
        document_count?: number;
      }>;
      if (results.length === 0) return 'No parties found.';
      return results
        .map((r) => `• ${r.name} (${r.role}) - ${r.document_count || 0} documents`)
        .join('\n');
    }

    case 'get_case_questions':
    case 'get_unanswered_questions': {
      const results = (data.results || []) as Array<{
        id: string;
        text: string;
        category: string;
        answered?: boolean;
      }>;
      if (results.length === 0) return 'No questions found.';
      return results
        .map((q) => `• ${q.text} [${q.category}]${q.answered ? ' ✓' : ''}`)
        .join('\n');
    }

    case 'get_knowledge_context': {
      const actors = (data.actors || []) as Array<{ name: string; role: string }>;
      const questions = (data.questions || []) as Array<{ text: string; category: string }>;
      let output = `Knowledge Context (${data.total_actors} actors, ${data.total_questions} questions total)\n\n`;
      if (actors.length > 0) {
        output += 'Relevant Actors:\n' + actors.map((a) => `• ${a.name} (${a.role})`).join('\n') + '\n\n';
      }
      if (questions.length > 0) {
        output += 'Relevant Questions:\n' + questions.map((q) => `• ${q.text}`).join('\n');
      }
      return output;
    }

    case 'execute_code': {
      const output = data.output as string || '';
      const error = data.error as string || '';
      if (error) return `Execution Error:\n${error}`;
      return output || 'Code executed successfully (no output)';
    }

    case 'search_cases':
    case 'find_similar_cases': {
      const results = (data.results || []) as Array<{
        citation: string;
        date: string | null;
        category: string;
        summary: string;
        outcome: string | null;
        relevance_score?: number;
        matched_keywords?: string[];
      }>;
      const message = (data as { message?: string }).message;

      if (results.length === 0) {
        return message || 'No similar cases found. Try providing more details about your situation.';
      }

      let output = message ? `${message}\n\n` : '';
      output += '📚 **Relevant Cases Found:**\n\n';

      results.forEach((c, i) => {
        output += `**${i + 1}. ${c.citation}**\n`;
        if (c.date) output += `   📅 Date: ${c.date}\n`;
        output += `   📂 Category: ${c.category}\n`;
        if (c.relevance_score) output += `   ⭐ Relevance: ${c.relevance_score}\n`;
        if (c.matched_keywords && c.matched_keywords.length > 0) {
          output += `   🔑 Matched: ${c.matched_keywords.join(', ')}\n`;
        }
        output += `   📝 Summary: ${c.summary}\n`;
        if (c.outcome) {
          output += `   ⚖️ Outcome: ${c.outcome}\n`;
        }
        output += '\n';
      });

      return output;
    }

    case 'get_case_details': {
      const caseData = data as {
        citation: string;
        date: string | null;
        category: string;
        summary: string;
        outcome: string | null;
        full_text: string;
      };

      let output = `**${caseData.citation}**\n\n`;
      if (caseData.date) output += `📅 Date: ${caseData.date}\n`;
      output += `📂 Category: ${caseData.category}\n\n`;
      output += `**Summary:**\n${caseData.summary}\n\n`;
      if (caseData.outcome) {
        output += `**Outcome:**\n${caseData.outcome}\n`;
      }
      return output;
    }

    case 'get_applicable_law': {
      const sections = (data.relevant_sections || data.sections || []) as Array<{
        section: string;
        title: string;
        legal_test: string;
        summary?: string;
        citation?: string;
      }>;
      const message = (data as { message?: string }).message;
      const act = (data as { act?: { name: string; citation: string } }).act;

      if (sections.length === 0 && !data.section) {
        return message || 'No applicable sections found.';
      }

      let output = '';
      if (act) {
        output += `**${act.citation}**\n\n`;
      }
      if (message) {
        output += `${message}\n\n`;
      }

      // Single section
      if (data.section) {
        const s = data.section as { section: string; title: string; legal_test: string; summary: string };
        output += `**Section ${s.section}: ${s.title}**\n`;
        output += `Legal Test: ${s.legal_test}\n`;
        output += `${s.summary}\n`;
        return output;
      }

      // Multiple sections
      output += '**Applicable Statutory Provisions:**\n\n';
      sections.forEach((s, i) => {
        output += `${i + 1}. **Section ${s.section}** - ${s.title}\n`;
        output += `   Legal Test: ${s.legal_test}\n`;
        if (s.summary) output += `   ${s.summary}\n`;
        output += '\n';
      });

      return output;
    }

    case 'statutory_alignment': {
      const applicableLaw = (data.applicable_law || []) as Array<{
        citation: string;
        section: string;
        title: string;
        legal_test: string;
        summary: string;
      }>;
      const similarCases = (data.similar_cases || []) as Array<{
        citation: string;
        date: string | null;
        relevance_score: number;
        summary: string;
        outcome: string | null;
      }>;
      const message = (data as { message?: string }).message;

      let output = '**STATUTORY ALIGNMENT ANALYSIS**\n\n';
      if (message) {
        output += `${message}\n\n`;
      }

      // Part A: Applicable Law
      output += '**A. APPLICABLE LEGISLATION (Family Law Act 1975)**\n\n';
      if (applicableLaw.length === 0) {
        output += 'No specific sections identified.\n\n';
      } else {
        applicableLaw.forEach((law, i) => {
          output += `${i + 1}. **${law.citation}**\n`;
          output += `   Title: ${law.title}\n`;
          output += `   Legal Test: ${law.legal_test}\n`;
          output += `   Summary: ${law.summary}\n\n`;
        });
      }

      // Part B: Case Law
      output += '**B. RELEVANT CASE LAW**\n\n';
      if (similarCases.length === 0) {
        output += 'No similar cases found.\n\n';
      } else {
        similarCases.forEach((c, i) => {
          output += `${i + 1}. **${c.citation}**\n`;
          if (c.date) output += `   Date: ${c.date}\n`;
          output += `   Relevance: ${c.relevance_score}\n`;
          output += `   Summary: ${c.summary}\n`;
          if (c.outcome) output += `   Outcome: ${c.outcome}\n`;
          output += '\n';
        });
      }

      return output;
    }

    default:
      return JSON.stringify(data, null, 2);
  }
}

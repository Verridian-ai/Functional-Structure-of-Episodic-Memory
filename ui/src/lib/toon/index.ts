/**
 * TOON (Token-Oriented Object Notation) Encoder/Decoder
 *
 * A compact serialization format optimized for LLM context efficiency.
 * Achieves ~40% fewer tokens than JSON while maintaining readability.
 *
 * Format:
 * EntityType[count]{header1,header2,header3}
 * value1,value2,value3
 * value1,value2,value3
 */

export interface ToonBlock {
  name: string;
  headers: string[];
  data: string[][];
}

/**
 * TOON Encoder
 */
export class ToonEncoder {
  /**
   * Encode generic data to TOON format
   */
  static encode(name: string, headers: string[], data: unknown[][]): string {
    const count = data.length;
    const headerStr = `${name}[${count}]{${headers.join(',')}}`;

    const rows = data.map((row) =>
      row.map((val) => this.escapeValue(val)).join(',')
    );

    return [headerStr, ...rows].join('\n');
  }

  /**
   * Encode actors array to TOON format
   */
  static encodeActors(
    actors: Array<{
      id: string;
      name: string;
      role?: string;
      actor_type?: string;
    }>
  ): string {
    const headers = ['id', 'name', 'type', 'role'];
    const data = actors.map((a) => [
      a.id || '',
      a.name || '',
      a.actor_type || '',
      a.role || '',
    ]);
    return this.encode('Actors', headers, data);
  }

  /**
   * Encode questions array to TOON format
   */
  static encodeQuestions(
    questions: Array<{
      id: string;
      text: string;
      category?: string;
      answered?: boolean;
    }>
  ): string {
    const headers = ['id', 'text', 'category', 'answered'];
    const data = questions.map((q) => [
      q.id || '',
      q.text || '',
      q.category || '',
      q.answered ? 'yes' : 'no',
    ]);
    return this.encode('Questions', headers, data);
  }

  /**
   * Encode knowledge context to TOON format
   */
  static encodeKnowledgeContext(context: {
    actors: Array<{ id: string; name: string; role: string }>;
    questions: Array<{ id: string; text: string; category: string; answered?: boolean }>;
    total_actors: number;
    total_questions: number;
  }): string {
    const parts: string[] = [];

    // Metadata line
    parts.push(`Context{total_actors:${context.total_actors},total_questions:${context.total_questions}}`);
    parts.push('');

    // Actors block
    if (context.actors.length > 0) {
      parts.push(this.encodeActors(context.actors));
      parts.push('');
    }

    // Questions block
    if (context.questions.length > 0) {
      parts.push(this.encodeQuestions(context.questions));
    }

    return parts.join('\n');
  }

  /**
   * Escape special characters in TOON values
   */
  private static escapeValue(val: unknown): string {
    if (val === null || val === undefined) return '';
    const str = String(val);
    // Escape commas with semicolons, newlines with spaces
    return str.replace(/,/g, ';').replace(/\n/g, ' ');
  }
}

/**
 * TOON Decoder
 */
export class ToonDecoder {
  /**
   * Decode TOON string to structured data
   */
  static decode(toon: string): ToonBlock[] {
    const blocks: ToonBlock[] = [];
    const lines = toon.trim().split('\n');
    let i = 0;

    while (i < lines.length) {
      const line = lines[i].trim();

      // Skip empty lines
      if (!line) {
        i++;
        continue;
      }

      // Parse header line: EntityType[count]{col1,col2}
      const headerMatch = line.match(/^(\w+)\[(\d+)\]\{([^}]*)\}$/);
      if (headerMatch) {
        const name = headerMatch[1];
        const count = parseInt(headerMatch[2], 10);
        const headers = headerMatch[3].split(',').map((h) => h.trim());

        // Read data rows
        const data: string[][] = [];
        for (let j = 0; j < count && i + 1 + j < lines.length; j++) {
          const rowLine = lines[i + 1 + j];
          if (rowLine.trim()) {
            data.push(this.parseRow(rowLine, headers.length));
          }
        }

        blocks.push({ name, headers, data });
        i += 1 + count;
      } else {
        i++;
      }
    }

    return blocks;
  }

  /**
   * Decode actors block to structured array
   */
  static decodeActors(
    toon: string
  ): Array<{ id: string; name: string; type: string; role: string }> {
    const blocks = this.decode(toon);
    const actorsBlock = blocks.find((b) => b.name === 'Actors');

    if (!actorsBlock) return [];

    return actorsBlock.data.map((row) => ({
      id: row[0] || '',
      name: row[1] || '',
      type: row[2] || '',
      role: row[3] || '',
    }));
  }

  /**
   * Decode questions block to structured array
   */
  static decodeQuestions(
    toon: string
  ): Array<{ id: string; text: string; category: string; answered: boolean }> {
    const blocks = this.decode(toon);
    const questionsBlock = blocks.find((b) => b.name === 'Questions');

    if (!questionsBlock) return [];

    return questionsBlock.data.map((row) => ({
      id: row[0] || '',
      text: row[1] || '',
      category: row[2] || '',
      answered: row[3] === 'yes' || row[3] === 'true',
    }));
  }

  /**
   * Parse a data row, handling escaped values
   */
  private static parseRow(line: string, expectedCols: number): string[] {
    const values = line.split(',');

    // Handle case where we have more or fewer columns than expected
    while (values.length < expectedCols) {
      values.push('');
    }

    return values.slice(0, expectedCols).map((v) => v.trim());
  }
}

/**
 * Format tool result as TOON (for compact context injection)
 */
export function formatResultAsToon(
  toolName: string,
  result: { success: boolean; data: unknown }
): string {
  if (!result.success) {
    return `Error{message:Tool execution failed}`;
  }

  const data = result.data as Record<string, unknown>;

  switch (toolName) {
    case 'get_knowledge_context': {
      const actors = (data.actors || []) as Array<{
        id: string;
        name: string;
        role: string;
      }>;
      const questions = (data.questions || []) as Array<{
        id: string;
        text: string;
        category: string;
        answered?: boolean;
      }>;

      return ToonEncoder.encodeKnowledgeContext({
        actors,
        questions,
        total_actors: (data.total_actors as number) || 0,
        total_questions: (data.total_questions as number) || 0,
      });
    }

    case 'find_parties':
    case 'find_actors_by_role': {
      const results = (data.results || []) as Array<{
        id: string;
        name: string;
        role: string;
        actor_type?: string;
      }>;
      return ToonEncoder.encodeActors(results);
    }

    case 'get_case_questions':
    case 'get_unanswered_questions': {
      const results = (data.results || []) as Array<{
        id: string;
        text: string;
        category: string;
        answered?: boolean;
      }>;
      return ToonEncoder.encodeQuestions(results);
    }

    default:
      // Fallback to JSON for unsupported tools
      return JSON.stringify(data);
  }
}

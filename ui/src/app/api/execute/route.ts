import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { code, language } = await request.json();

    if (!code || !language) {
      return NextResponse.json(
        { error: 'Missing code or language parameter' },
        { status: 400 }
      );
    }

    if (language !== 'python') {
      return NextResponse.json(
        { error: 'Only Python is currently supported' },
        { status: 400 }
      );
    }

    // For demo purposes, simulate Python execution
    // In production, this would connect to a secure Python sandbox
    const output = await executePythonCode(code);

    return NextResponse.json({ output });
  } catch (error) {
    console.error('Code execution error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Execution failed' },
      { status: 500 }
    );
  }
}

async function executePythonCode(code: string): Promise<string> {
  // In production, this would use a sandboxed Python environment
  // Options:
  // 1. Docker container with restricted permissions
  // 2. WebAssembly-based Python (Pyodide)
  // 3. External service like Judge0 or similar

  // For demo, we'll simulate some basic outputs
  const lines = code.split('\n');
  const outputs: string[] = [];

  for (const line of lines) {
    const trimmed = line.trim();

    // Simulate print statements
    const printMatch = trimmed.match(/^print\s*\((.*)\)\s*$/);
    if (printMatch) {
      const content = printMatch[1];
      // Handle string literals
      if ((content.startsWith('"') && content.endsWith('"')) ||
          (content.startsWith("'") && content.endsWith("'"))) {
        outputs.push(content.slice(1, -1));
      } else if (content.startsWith('f"') || content.startsWith("f'")) {
        // f-string (simplified)
        outputs.push(content.slice(2, -1));
      } else {
        // Evaluate simple expressions
        try {
          // Only allow safe expressions
          if (/^[\d\s+\-*/().]+$/.test(content)) {
            outputs.push(String(eval(content)));
          } else {
            outputs.push(`[Variable: ${content}]`);
          }
        } catch {
          outputs.push(`[Expression: ${content}]`);
        }
      }
    }
  }

  if (outputs.length === 0) {
    // If no print statements, check for expression results
    const lastLine = lines[lines.length - 1]?.trim();
    if (lastLine && !lastLine.startsWith('#') && !lastLine.includes('=')) {
      return '[Code executed successfully - no output]';
    }
  }

  return outputs.join('\n') || '[Code executed successfully]';
}

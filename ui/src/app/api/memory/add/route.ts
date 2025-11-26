import { NextRequest, NextResponse } from 'next/server';
import { Memory } from 'mem0ai';

export async function POST(request: NextRequest) {
  try {
    const { content, userId, role } = await request.json();
    
    if (process.env.MEM0_API_KEY) {
        const memory = new Memory({ apiKey: process.env.MEM0_API_KEY });
        await memory.add(content, { 
            user_id: userId || 'test_session_user', 
            metadata: { role: role || 'assistant' } 
        });
        return NextResponse.json({ success: true });
    }
    
    return NextResponse.json({ skipped: true, reason: "No MEM0_API_KEY" });
  } catch (error) {
    console.error("Memory Add Error:", error);
    return NextResponse.json({ error: 'Failed to add memory' }, { status: 500 });
  }
}


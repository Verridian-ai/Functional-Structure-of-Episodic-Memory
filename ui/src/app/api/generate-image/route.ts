import { NextRequest, NextResponse } from 'next/server';

const NANOBANAPRO_MODEL = 'google/gemini-3-pro-image-preview';

// Build an optimized prompt for infographic generation
function buildInfographicPrompt(prompt: string, context?: string, style?: string): string {
  const styleGuide = style || 'professional, clean, modern design';

  let fullPrompt = `Create a professional infographic: ${prompt}

Style Requirements:
- ${styleGuide}
- Use a cohesive color palette (blues, greens, or brand colors)
- Include clear visual hierarchy
- Minimize text, maximize visual representation
- Use icons and simple graphics where appropriate
- Ensure all text is crisp and readable`;

  if (context) {
    fullPrompt += `\n\nContext for the infographic:\n${context}`;
  }

  return fullPrompt;
}

export async function POST(req: NextRequest) {
  try {
    const {
      prompt,
      aspectRatio = '16:9',
      context,
      style,
      documentType
    } = await req.json();

    if (!prompt) {
      return NextResponse.json(
        { error: 'Prompt is required' },
        { status: 400 }
      );
    }

    const apiKey = process.env.OPENROUTER_API_KEY || process.env.NEXT_PUBLIC_OPENROUTER_API_KEY;

    if (!apiKey) {
      return NextResponse.json(
        { error: 'OpenRouter API key not configured. Set OPENROUTER_API_KEY in environment.' },
        { status: 500 }
      );
    }

    // Adjust prompt based on document type
    let stylePreset = style;
    if (!stylePreset && documentType) {
      switch (documentType) {
        case 'legal':
          stylePreset = 'formal, professional, conservative colors (navy, gray), scales of justice imagery';
          break;
        case 'business':
          stylePreset = 'corporate, clean lines, professional blue/green palette, data-focused';
          break;
        case 'report':
          stylePreset = 'analytical, chart-focused, clear data visualization, minimal decoration';
          break;
        case 'newsletter':
          stylePreset = 'engaging, modern, colorful but professional, magazine-style layout';
          break;
        default:
          stylePreset = 'professional, clean, modern design';
      }
    }

    const fullPrompt = buildInfographicPrompt(prompt, context, stylePreset);

    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
        'X-Title': 'Verridian Document Platform',
      },
      body: JSON.stringify({
        model: NANOBANAPRO_MODEL,
        messages: [
          {
            role: 'user',
            content: fullPrompt,
          },
        ],
        modalities: ['image', 'text'],
        image_config: {
          aspect_ratio: aspectRatio,
        },
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('OpenRouter API error:', errorData);
      return NextResponse.json(
        {
          error: 'Image generation failed',
          details: errorData.error?.message || response.statusText
        },
        { status: response.status }
      );
    }

    const data = await response.json();

    // Extract image from response
    // OpenRouter returns images in the assistant message content
    const assistantMessage = data.choices?.[0]?.message;

    if (!assistantMessage) {
      return NextResponse.json(
        { error: 'No response from image generation model' },
        { status: 500 }
      );
    }

    // Images are returned as base64 in content array or as image_url
    let imageData: string | null = null;
    let textResponse: string = '';

    // Handle different response formats
    if (Array.isArray(assistantMessage.content)) {
      for (const part of assistantMessage.content) {
        if (part.type === 'image_url' && part.image_url?.url) {
          imageData = part.image_url.url;
        } else if (part.type === 'text') {
          textResponse = part.text || '';
        }
      }
    } else if (typeof assistantMessage.content === 'string') {
      textResponse = assistantMessage.content;
    }

    // Check for images in a separate field (some models return it differently)
    if (!imageData && assistantMessage.images) {
      imageData = assistantMessage.images[0]?.url || assistantMessage.images[0];
    }

    if (!imageData) {
      return NextResponse.json(
        {
          error: 'No image generated',
          textResponse,
          debug: { responseKeys: Object.keys(assistantMessage) }
        },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      image: imageData, // base64 data URL or URL
      text: textResponse,
      model: NANOBANAPRO_MODEL,
      aspectRatio,
    });

  } catch (error) {
    console.error('Image generation error:', error);
    return NextResponse.json(
      {
        error: 'Internal server error during image generation',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// GET endpoint for health check
export async function GET() {
  const apiKey = process.env.OPENROUTER_API_KEY || process.env.NEXT_PUBLIC_OPENROUTER_API_KEY;

  return NextResponse.json({
    service: 'NanoBanaPro Image Generation',
    model: NANOBANAPRO_MODEL,
    configured: !!apiKey,
    supportedAspectRatios: ['1:1', '2:3', '3:2', '3:4', '4:3', '4:5', '5:4', '9:16', '16:9', '21:9'],
    documentTypes: ['legal', 'business', 'report', 'newsletter'],
  });
}

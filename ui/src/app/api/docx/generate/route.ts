import { NextRequest, NextResponse } from 'next/server';
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } from 'docx';

export async function POST(request: NextRequest) {
  try {
    const { title, content } = await request.json();

    if (!content) {
      return NextResponse.json(
        { error: 'Missing content parameter' },
        { status: 400 }
      );
    }

    // Split content into paragraphs
    const lines = content.split('\n');
    const children = [];

    // Add Title
    if (title) {
      children.push(
        new Paragraph({
          text: title,
          heading: HeadingLevel.TITLE,
          alignment: AlignmentType.CENTER,
          spacing: {
            after: 200,
          },
        })
      );
    }

    // Process lines
    for (const line of lines) {
      if (line.trim() === '') {
        children.push(new Paragraph({ text: '' })); // Empty line
        continue;
      }

      // Simple Markdown-like parsing
      if (line.startsWith('# ')) {
        children.push(
          new Paragraph({
            text: line.replace('# ', ''),
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 240, after: 120 },
          })
        );
      } else if (line.startsWith('## ')) {
        children.push(
          new Paragraph({
            text: line.replace('## ', ''),
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          })
        );
      } else if (line.startsWith('### ')) {
        children.push(
          new Paragraph({
            text: line.replace('### ', ''),
            heading: HeadingLevel.HEADING_3,
            spacing: { before: 120, after: 60 },
          })
        );
      } else if (line.startsWith('- ') || line.startsWith('* ')) {
        children.push(
          new Paragraph({
            text: line.substring(2),
            bullet: {
              level: 0,
            },
          })
        );
      } else {
        // Regular paragraph
        children.push(
          new Paragraph({
            children: [
              new TextRun({
                text: line,
                font: 'Calibri',
                size: 24, // 12pt
              }),
            ],
            spacing: {
              after: 120,
            },
          })
        );
      }
    }

    const doc = new Document({
      sections: [
        {
          properties: {},
          children: children,
        },
      ],
    });

    const buffer = await Packer.toBuffer(doc);

    return new Response(new Uint8Array(buffer), {
      headers: {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'Content-Disposition': `attachment; filename="${title || 'document'}.docx"`,
      },
    });
  } catch (error) {
    console.error('DOCX generation error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'DOCX generation failed' },
      { status: 500 }
    );
  }
}


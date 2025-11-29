/**
 * InfographicAnalyzer Service
 *
 * Analyzes document sections to identify content suitable for infographic conversion.
 * Uses pattern matching and heuristics to detect data-rich content.
 */

export interface InfographicSuggestion {
  id: string;
  sectionIndex: number;
  sectionText: string;
  suggestedType: InfographicType;
  confidence: number; // 0-1
  prompt: string; // Pre-generated prompt for NanoBanaPro
  reason: string;
}

export type InfographicType =
  | 'timeline'
  | 'process'
  | 'comparison'
  | 'statistics'
  | 'hierarchy'
  | 'list'
  | 'flowchart'
  | 'pie-chart'
  | 'bar-chart';

interface PatternMatch {
  type: InfographicType;
  patterns: RegExp[];
  keywords: string[];
  minConfidence: number;
}

// Pattern definitions for detecting infographic-suitable content
const INFOGRAPHIC_PATTERNS: PatternMatch[] = [
  {
    type: 'timeline',
    patterns: [
      /\b(timeline|chronolog|sequence|history)\b/i,
      /\b(first|second|third|then|next|finally|before|after)\b.*\b(first|second|third|then|next|finally|before|after)\b/i,
      /\b\d{4}\b.*\b\d{4}\b/, // Multiple years
      /\b(january|february|march|april|may|june|july|august|september|october|november|december)\b.*\b(january|february|march|april|may|june|july|august|september|october|november|december)\b/i,
    ],
    keywords: ['timeline', 'history', 'evolution', 'progression', 'dates', 'milestones'],
    minConfidence: 0.6,
  },
  {
    type: 'process',
    patterns: [
      /\bstep\s*\d+\b/i,
      /\b(step|stage|phase)\s*[:|-]/i,
      /\b(first|second|third|fourth|fifth)\s+(step|stage|phase)\b/i,
      /\d+\.\s*[A-Z]/gm, // Numbered lists
      /\b(procedure|process|workflow|how to)\b/i,
    ],
    keywords: ['step', 'process', 'procedure', 'workflow', 'how to', 'guide', 'instructions'],
    minConfidence: 0.65,
  },
  {
    type: 'comparison',
    patterns: [
      /\b(vs\.?|versus|compared to|comparison|difference between)\b/i,
      /\b(advantages?|disadvantages?|pros?|cons?)\b/i,
      /\b(better|worse|more|less|higher|lower)\s+than\b/i,
      /\b(option\s*[abc123]|alternative\s*\d)\b/i,
    ],
    keywords: ['comparison', 'versus', 'vs', 'difference', 'contrast', 'pros', 'cons', 'advantages'],
    minConfidence: 0.7,
  },
  {
    type: 'statistics',
    patterns: [
      /\d+(\.\d+)?%/g, // Percentages
      /\$[\d,]+(\.\d{2})?/g, // Currency
      /\b\d+\s*(million|billion|thousand|k|m|b)\b/i,
      /\b(increase|decrease|growth|decline)\s*(of|by)?\s*\d+/i,
      /\b(average|median|mean|total|sum)\b/i,
    ],
    keywords: ['statistics', 'data', 'numbers', 'percentage', 'growth', 'rate', 'average'],
    minConfidence: 0.75,
  },
  {
    type: 'hierarchy',
    patterns: [
      /\b(organization|structure|hierarchy|levels?)\b/i,
      /\b(top|middle|bottom)\s+(level|tier|management)\b/i,
      /\b(report to|under|above|supervise)\b/i,
      /\b(ceo|cto|manager|director|lead|senior|junior)\b/i,
    ],
    keywords: ['hierarchy', 'organization', 'structure', 'chain', 'levels', 'management'],
    minConfidence: 0.6,
  },
  {
    type: 'list',
    patterns: [
      /^[-*]\s+/gm, // Bullet points
      /^\d+\.\s+/gm, // Numbered lists
      /\b(following|these|include|such as):\s*$/im,
      /\b(key|main|important|essential)\s+(points?|factors?|elements?|features?)\b/i,
    ],
    keywords: ['list', 'items', 'points', 'factors', 'elements', 'key', 'main'],
    minConfidence: 0.5,
  },
  {
    type: 'flowchart',
    patterns: [
      /\b(if|when|unless)\b.*\b(then|else|otherwise)\b/i,
      /\b(decision|choose|select|option)\b/i,
      /\b(flow|diagram|chart)\b/i,
      /\b(yes|no)\s*(->|:)/i,
    ],
    keywords: ['decision', 'flow', 'choose', 'branch', 'if', 'then', 'else'],
    minConfidence: 0.65,
  },
  {
    type: 'pie-chart',
    patterns: [
      /\d+(\.\d+)?%\s*of\s*(the\s*)?(total|whole|all)/i,
      /\b(distribution|breakdown|composition|share)\b/i,
      /\b(portion|segment|slice|part)\b/i,
    ],
    keywords: ['distribution', 'breakdown', 'share', 'portion', 'percentage', 'composition'],
    minConfidence: 0.7,
  },
  {
    type: 'bar-chart',
    patterns: [
      /\b(ranking|ranked|top\s*\d+|bottom\s*\d+)\b/i,
      /\b(compare|comparing)\s+\d+/i,
      /\b(highest|lowest|most|least)\b/i,
    ],
    keywords: ['ranking', 'compare', 'highest', 'lowest', 'most', 'least'],
    minConfidence: 0.65,
  },
];

// Generate optimized prompt for NanoBanaPro
function generatePrompt(type: InfographicType, content: string, documentType?: string): string {
  const stylePrefix = documentType === 'legal'
    ? 'formal, professional legal infographic with'
    : documentType === 'business'
    ? 'corporate business infographic with'
    : 'clean, modern infographic with';

  const typePrompts: Record<InfographicType, string> = {
    timeline: `${stylePrefix} a horizontal timeline showing key events and dates. Use connecting lines between milestones.`,
    process: `${stylePrefix} a step-by-step process flow. Use numbered circles or arrows connecting each step.`,
    comparison: `${stylePrefix} a side-by-side comparison layout. Use columns or opposing sections with clear labels.`,
    statistics: `${stylePrefix} data visualization using charts, numbers, and icons. Highlight key statistics prominently.`,
    hierarchy: `${stylePrefix} an organizational hierarchy or tree structure. Use boxes and connecting lines.`,
    list: `${stylePrefix} an organized visual list using icons and brief text. Group related items together.`,
    flowchart: `${stylePrefix} a decision flowchart with clear yes/no branches and outcomes.`,
    'pie-chart': `${stylePrefix} a pie or donut chart showing proportional distribution. Label each segment.`,
    'bar-chart': `${stylePrefix} a bar chart comparing values across categories. Use clear axis labels.`,
  };

  // Extract key points from content (first 200 chars for context)
  const contentPreview = content.slice(0, 200).replace(/\n/g, ' ').trim();

  return `${typePrompts[type]}

Content to visualize:
${contentPreview}...

Requirements:
- Minimal text, maximum visual clarity
- Professional color scheme
- Clear visual hierarchy
- Easy to understand at a glance`;
}

// Split content into analyzable sections
function splitIntoSections(content: string): string[] {
  // Split by headers, double newlines, or significant breaks
  const sections = content
    .split(/(?:\n\n+|^#{1,3}\s+.+$)/m)
    .map(s => s.trim())
    .filter(s => s.length > 50); // Minimum length for meaningful analysis

  // If no good splits, chunk by paragraphs
  if (sections.length === 0) {
    return content
      .split(/\n/)
      .filter(s => s.trim().length > 50);
  }

  return sections;
}

// Calculate confidence score for a pattern match
function calculateConfidence(
  content: string,
  pattern: PatternMatch
): number {
  let score = 0;
  let matchCount = 0;

  // Check regex patterns
  for (const regex of pattern.patterns) {
    const matches = content.match(regex);
    if (matches) {
      matchCount += matches.length;
      score += 0.2; // Base score per pattern match
    }
  }

  // Check keywords
  const lowerContent = content.toLowerCase();
  for (const keyword of pattern.keywords) {
    if (lowerContent.includes(keyword)) {
      score += 0.1;
    }
  }

  // Normalize score
  const normalizedScore = Math.min(score, 1);

  // Apply minimum confidence threshold
  return normalizedScore >= pattern.minConfidence ? normalizedScore : 0;
}

// Get human-readable reason for suggestion
function getReason(type: InfographicType, confidence: number): string {
  const reasons: Record<InfographicType, string> = {
    timeline: 'Contains chronological events or dates that would benefit from visual timeline representation',
    process: 'Describes a step-by-step process that could be visualized as a flow',
    comparison: 'Contains comparison or contrast between options that could be shown side-by-side',
    statistics: 'Contains numerical data or statistics that would be more impactful as a chart',
    hierarchy: 'Describes organizational or hierarchical relationships',
    list: 'Contains a list of items that could be visualized with icons and layout',
    flowchart: 'Contains decision logic or branching paths suitable for a flowchart',
    'pie-chart': 'Contains proportional data suitable for pie/donut chart visualization',
    'bar-chart': 'Contains comparative values suitable for bar chart visualization',
  };

  const confidenceLabel = confidence >= 0.8 ? 'Highly recommended' :
    confidence >= 0.6 ? 'Recommended' : 'Suggested';

  return `${confidenceLabel}: ${reasons[type]}`;
}

/**
 * Analyze document content and return infographic suggestions
 */
export function analyzeForInfographics(
  content: string,
  documentType?: string,
  minConfidence: number = 0.5
): InfographicSuggestion[] {
  const suggestions: InfographicSuggestion[] = [];
  const sections = splitIntoSections(content);

  sections.forEach((section, index) => {
    let bestMatch: { type: InfographicType; confidence: number } | null = null;

    // Find the best matching infographic type for this section
    for (const pattern of INFOGRAPHIC_PATTERNS) {
      const confidence = calculateConfidence(section, pattern);

      if (confidence >= minConfidence) {
        if (!bestMatch || confidence > bestMatch.confidence) {
          bestMatch = { type: pattern.type, confidence };
        }
      }
    }

    if (bestMatch) {
      suggestions.push({
        id: `suggestion_${index}_${Date.now()}`,
        sectionIndex: index,
        sectionText: section.slice(0, 150) + (section.length > 150 ? '...' : ''),
        suggestedType: bestMatch.type,
        confidence: bestMatch.confidence,
        prompt: generatePrompt(bestMatch.type, section, documentType),
        reason: getReason(bestMatch.type, bestMatch.confidence),
      });
    }
  });

  // Sort by confidence (highest first)
  return suggestions.sort((a, b) => b.confidence - a.confidence);
}

/**
 * Quick check if content has any infographic potential
 */
export function hasInfographicPotential(content: string): boolean {
  const suggestions = analyzeForInfographics(content, undefined, 0.6);
  return suggestions.length > 0;
}

/**
 * Get infographic type display info
 */
export function getTypeInfo(type: InfographicType): { label: string; icon: string; color: string } {
  const info: Record<InfographicType, { label: string; icon: string; color: string }> = {
    timeline: { label: 'Timeline', icon: 'clock', color: 'blue' },
    process: { label: 'Process Flow', icon: 'git-branch', color: 'green' },
    comparison: { label: 'Comparison', icon: 'columns', color: 'purple' },
    statistics: { label: 'Statistics', icon: 'bar-chart-2', color: 'orange' },
    hierarchy: { label: 'Hierarchy', icon: 'git-merge', color: 'cyan' },
    list: { label: 'Visual List', icon: 'list', color: 'pink' },
    flowchart: { label: 'Flowchart', icon: 'workflow', color: 'yellow' },
    'pie-chart': { label: 'Pie Chart', icon: 'pie-chart', color: 'red' },
    'bar-chart': { label: 'Bar Chart', icon: 'bar-chart', color: 'indigo' },
  };

  return info[type];
}

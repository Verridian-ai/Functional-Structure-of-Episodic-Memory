import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import * as readline from 'readline';
import { createReadStream } from 'fs';
import path from 'path';
import { TEMFactorizer, ZeroShotLegalReasoner } from '@/lib/tem/caseFactorizer';
import { LegalEvidenceDetector } from '@/lib/active_inference/evidenceDetector';
import { LegalVSA } from '@/lib/vsa/legalVSA';
import { ToonEncoder } from '@/lib/toon';

// TEM Singleton
let legalReasoner: ZeroShotLegalReasoner | null = null;
// Active Inference Singleton
let evidenceDetector: LegalEvidenceDetector | null = null;
// VSA Singleton
let legalVSA: LegalVSA | null = null;

function getLegalVSA() {
  if (!legalVSA) {
    legalVSA = new LegalVSA();
  }
  return legalVSA;
}

function getEvidenceDetector() {
  if (!evidenceDetector) {
    evidenceDetector = new LegalEvidenceDetector();
  }
  return evidenceDetector;
}

async function getLegalReasoner(cases: CaseRecord[]) {
  if (!legalReasoner) {
    console.log('Initializing Zero-Shot Legal Reasoner...');
    legalReasoner = new ZeroShotLegalReasoner();
    
    // Pre-process cases for TEM (this might take a moment on first load)
    const actualCases = cases.filter(c => isActualCase(c));
    
    // In a real prod env, this would be pre-computed. 
    // Here we'll just load a subset to keep startup fast, or all if possible.
    // Let's load top 200 most relevant looking ones or just first 200 for speed demo
    const sampleCases = actualCases.slice(0, 200).map(c => ({
      citation: c.citation,
      text: c.text,
      outcome: extractOutcome(c.text) || undefined
    }));
    
    legalReasoner.loadPrecedents(sampleCases);
    console.log(`Zero-Shot Legal Reasoner initialized with ${sampleCases.length} structural precedents.`);
  }
  return legalReasoner;
}

// Case data structure from family.jsonl
interface CaseRecord {
  version_id: string;
  type: string;
  jurisdiction: string;
  source: string;
  date: string | null;
  citation: string;
  url: string;
  text: string;
  _classification: {
    primary_domain: string;
    primary_category: string;
  };
}

// Cache for cases (loaded on demand)
let casesCache: CaseRecord[] | null = null;
let casesLoading = false;

// Legislation section structure
interface LegislationSection {
  section: string;
  subsection?: string;
  title: string;
  legal_test: string;
  keywords: string[];
  summary: string;
}

interface LegislationData {
  act: {
    name: string;
    jurisdiction: string;
    citation: string;
    url: string;
    version: string;
  };
  sections: LegislationSection[];
  related_legislation: Array<{
    name: string;
    citation: string;
    relevance: string;
  }>;
}

// Cache for legislation
let legislationCache: LegislationData | null = null;

// GSW Workspace data structure (matches actual family_law_gsw.json)
interface GSWWorkspace {
  actors: Record<string, {
    id: string;
    name: string;
    actor_type: string;
    roles: string[];
    involved_cases: string[];
    source_chunk_ids: string[];
  }>;
  questions: Record<string, {
    id: string;
    question_text: string;
    question_type: string;
    answerable: boolean;
    answer_text: string | null;
    source_chunk_id: string;
  }>;
  verb_phrases: Record<string, any>;
  spatio_temporal_links: Record<string, any>;
  entity_summaries: Record<string, any>;
  metadata: {
    created_at: string;
    last_updated: string;
    chunk_count: number;
    document_count: number;
    domain: string;
  };
}

let workspace: GSWWorkspace | null = null;

// Load workspace on first request
async function loadWorkspace(): Promise<GSWWorkspace> {
  if (workspace) return workspace;

  // Try multiple possible paths
  const possiblePaths = [
    path.join(process.cwd(), '..', 'data', 'workspaces', 'family_law_gsw.json'),
    path.join(process.cwd(), 'data', 'workspaces', 'family_law_gsw.json'),
    path.resolve(__dirname, '..', '..', '..', '..', '..', 'data', 'workspaces', 'family_law_gsw.json'),
    'C:/Users/Danie/Desktop/Fuctional Structure of Episodic Memory/data/workspaces/family_law_gsw.json',
  ];

  for (const workspacePath of possiblePaths) {
    try {
      console.log('Trying to load workspace from:', workspacePath);
      const data = await fs.readFile(workspacePath, 'utf-8');
      workspace = JSON.parse(data);
      console.log('Successfully loaded workspace from:', workspacePath);
      console.log('Actors:', Object.keys(workspace!.actors).length);
      console.log('Questions:', Object.keys(workspace!.questions).length);
      return workspace!;
    } catch (error) {
      console.log('Failed to load from:', workspacePath);
      continue;
    }
  }

  console.error('Failed to load workspace from any path');
  // Return empty workspace if file not found
  return {
    actors: {},
    questions: {},
    verb_phrases: {},
    spatio_temporal_links: {},
    entity_summaries: {},
    metadata: {
      created_at: '',
      last_updated: '',
      chunk_count: 0,
      document_count: 0,
      domain: 'family_law',
    },
  };
}

// Load cases from family.jsonl
async function loadCases(): Promise<CaseRecord[]> {
  if (casesCache) return casesCache;
  if (casesLoading) {
    // Wait for loading to complete
    while (casesLoading) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return casesCache || [];
  }

  casesLoading = true;
  const cases: CaseRecord[] = [];

  const possiblePaths = [
    path.join(process.cwd(), '..', 'data', 'domains', 'family.jsonl'),
    path.join(process.cwd(), 'data', 'domains', 'family.jsonl'),
    'C:/Users/Danie/Desktop/Fuctional Structure of Episodic Memory/data/domains/family.jsonl',
  ];

  for (const casesPath of possiblePaths) {
    try {
      console.log('Trying to load cases from:', casesPath);
      const fileStream = createReadStream(casesPath, { encoding: 'utf-8' });
      const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity,
      });

      for await (const line of rl) {
        if (line.trim()) {
          try {
            const caseData = JSON.parse(line) as CaseRecord;
            cases.push(caseData);
          } catch (e) {
            // Skip malformed lines
          }
        }
      }

      console.log('Successfully loaded', cases.length, 'cases from:', casesPath);
      casesCache = cases;
      casesLoading = false;
      return cases;
    } catch (error) {
      console.log('Failed to load cases from:', casesPath);
      continue;
    }
  }

  casesLoading = false;
  return [];
}

// Load legislation sections
async function loadLegislation(): Promise<LegislationData | null> {
  if (legislationCache) return legislationCache;

  const possiblePaths = [
    path.join(process.cwd(), '..', 'data', 'legislation', 'family_law_act_1975_sections.json'),
    path.join(process.cwd(), 'data', 'legislation', 'family_law_act_1975_sections.json'),
    'C:/Users/Danie/Desktop/Fuctional Structure of Episodic Memory/data/legislation/family_law_act_1975_sections.json',
  ];

  for (const legPath of possiblePaths) {
    try {
      console.log('Trying to load legislation from:', legPath);
      const data = await fs.readFile(legPath, 'utf-8');
      legislationCache = JSON.parse(data);
      console.log('Successfully loaded legislation with', legislationCache!.sections.length, 'sections');
      return legislationCache;
    } catch (error) {
      console.log('Failed to load legislation from:', legPath);
      continue;
    }
  }

  return null;
}

// Find relevant legislation sections based on facts/keywords
function findRelevantSections(facts: string, legislation: LegislationData): LegislationSection[] {
  const factsLower = facts.toLowerCase();
  const scoredSections = legislation.sections.map(section => {
    let score = 0;

    // Score based on keyword matches
    for (const keyword of section.keywords) {
      if (factsLower.includes(keyword.toLowerCase())) {
        score += 10;
      }
    }

    // Score based on legal test relevance
    const legalTestWords = section.legal_test.toLowerCase().split(/\s+/);
    for (const word of legalTestWords) {
      if (word.length > 3 && factsLower.includes(word)) {
        score += 5;
      }
    }

    // Score based on title relevance
    const titleWords = section.title.toLowerCase().split(/\s+/);
    for (const word of titleWords) {
      if (word.length > 3 && factsLower.includes(word)) {
        score += 3;
      }
    }

    return { section, score };
  });

  // Return sections with score > 0, sorted by relevance
  return scoredSections
    .filter(s => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map(s => s.section);
}

// Extract key terms from user story for case matching
function extractKeyTerms(story: string): string[] {
  const lowerStory = story.toLowerCase();

  // Family law keywords to look for
  const keywords = [
    // Parenting
    'child', 'children', 'custody', 'parenting', 'visitation', 'access',
    'mother', 'father', 'parent', 'guardian', 'grandparent',
    // Property
    'property', 'asset', 'house', 'home', 'superannuation', 'super',
    'division', 'split', 'settlement', 'financial',
    // Divorce/Separation
    'divorce', 'separation', 'separated', 'marriage', 'married', 'spouse',
    'husband', 'wife', 'partner', 'de facto',
    // Issues
    'domestic violence', 'abuse', 'violence', 'relocation', 'move',
    'consent', 'orders', 'court', 'mediation',
    // Specific concerns
    'welfare', 'best interest', 'risk', 'safety', 'harm',
    'contact', 'overnight', 'school', 'holiday',
  ];

  const found: string[] = [];
  for (const kw of keywords) {
    if (lowerStory.includes(kw)) {
      found.push(kw);
    }
  }

  return found;
}

// Check if a record is legislation (not a case)
function isLegislation(caseRecord: CaseRecord): boolean {
  const citation = caseRecord.citation || '';

  // Legislation patterns: "Act YYYY", "Rules YYYY", "Regulations YYYY"
  if (/\bAct\s+\d{4}\b/i.test(citation)) return true;
  if (/\bRules?\s+\d{4}\b/i.test(citation)) return true;
  if (/\bRegulations?\s+\d{4}\b/i.test(citation)) return true;

  // Also check if type indicates legislation
  if (caseRecord.type === 'legislation' || caseRecord.type === 'act') return true;

  return false;
}

// Check if a record is an actual court case
function isActualCase(caseRecord: CaseRecord): boolean {
  const citation = caseRecord.citation || '';

  // Court case patterns: [YYYY] followed by court identifiers
  // e.g., [2020] FamCA 123, [1984] HCA 21, [2019] FamCAFC 45
  if (/\[\d{4}\]\s*(FamCA|FamCAFC|HCA|FCA|FCCA|FCWA|FLC)\s*\d+/i.test(citation)) return true;

  // Also match "In the Marriage of", "In the Matter of" etc.
  if (/^In\s+the\s+(Marriage|Matter)\s+of/i.test(citation)) return true;

  // If it's not legislation, it might still be a case
  return !isLegislation(caseRecord);
}

// Hierarchy weights for Australian courts
const COURT_HIERARCHY: Record<string, { weight: number; name: string }> = {
  'HCA': { weight: 10, name: 'High Court of Australia' },
  'FCAFC': { weight: 9, name: 'Federal Court Full Court' },
  'FamCAFC': { weight: 8, name: 'Family Court Full Court' },
  'FCA': { weight: 7, name: 'Federal Court' },
  'FamCA': { weight: 6, name: 'Family Court' },
  'FCCA': { weight: 5, name: 'Federal Circuit Court' },
  'NSWSC': { weight: 4, name: 'NSW Supreme Court' },
  'VSC': { weight: 4, name: 'Supreme Court of Victoria' },
  'QSC': { weight: 4, name: 'Supreme Court of Queensland' },
  'SASC': { weight: 4, name: 'Supreme Court of SA' },
  'WASC': { weight: 4, name: 'Supreme Court of WA' },
  'NSWDC': { weight: 3, name: 'District Court' },
  'Tribunal': { weight: 2, name: 'Administrative Tribunal' },
};

// Score how relevant a case is to keywords, with authority boosting
function scoreCaseRelevance(caseRecord: CaseRecord, keywords: string[]): number {
  const textLower = caseRecord.text.toLowerCase();
  let baseScore = 0;

  for (const kw of keywords) {
    // Count occurrences (up to a max to prevent bias)
    const regex = new RegExp(kw, 'gi');
    const matches = textLower.match(regex);
    if (matches) {
      baseScore += Math.min(matches.length, 10);
    }
  }

  // Apply Authority Boosting
  const citation = caseRecord.citation || '';
  let authorityBoost = 1.0;
  
  // Extract court identifier from citation [YYYY] COURT ###
  const courtMatch = citation.match(/\[\d{4}\]\s*(\w+)\s*\d+/);
  if (courtMatch) {
    const courtCode = courtMatch[1];
    const hierarchy = COURT_HIERARCHY[courtCode] || COURT_HIERARCHY[courtCode.toUpperCase()];
    
    if (hierarchy) {
      // Boost score: HCA (10) gets 1.5x, Tribunal (2) gets 1.1x
      authorityBoost = 1 + (hierarchy.weight / 20); 
    }
  }

  return baseScore * authorityBoost;
}

// Extract case summary (first ~500 chars that look like a summary)
function extractCaseSummary(text: string): string {
  // Look for "Summary" section
  const summaryMatch = text.match(/Summary[\s\n]+([^]+?)(?=\n\n|\n[A-Z][a-z]+:|\n\d+\.)/i);
  if (summaryMatch) {
    return summaryMatch[1].slice(0, 500).trim() + '...';
  }

  // Otherwise take first meaningful paragraph
  const paragraphs = text.split('\n\n').filter(p => p.length > 100);
  if (paragraphs.length > 0) {
    return paragraphs[0].slice(0, 500).trim() + '...';
  }

  return text.slice(0, 500).trim() + '...';
}

// Extract outcome/orders from case
function extractOutcome(text: string): string | null {
  // Look for common outcome patterns
  const patterns = [
    /(?:Orders?|Held|Ordered|The Court orders?)[\s:]+([^]+?)(?=\n\n|\n[A-Z][a-z]+:)/i,
    /(?:Conclusion|Result|Outcome)[\s:]+([^]+?)(?=\n\n)/i,
    /(?:dismissed|allowed|granted|refused|made the following orders?)([^]+?)(?=\n\n)/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1].slice(0, 300).trim();
    }
  }

  return null;
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action');

  try {
    const ws = await loadWorkspace();

    switch (action) {
      case 'stats':
        return NextResponse.json({
          actors: Object.keys(ws.actors).length,
          questions: Object.keys(ws.questions).length,
          verb_phrases: Object.keys(ws.verb_phrases || {}).length,
          spatio_temporal_links: Object.keys(ws.spatio_temporal_links || {}).length,
          documents: ws.metadata.document_count,
        });

      case 'metadata':
        return NextResponse.json(ws.metadata);

      default:
        return NextResponse.json({
          error: 'Invalid action. Use: stats, ontology',
        }, { status: 400 });
    }
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'GSW operation failed' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const { action, params } = await request.json();
    const ws = await loadWorkspace();

    switch (action) {
      case 'find_parties': {
        const { query, limit = 10 } = params || {};
        const results = Object.entries(ws.actors)
          .filter(([_, actor]) => {
            if (!query) return true;
            const name = actor.name?.toLowerCase() || '';
            const roles = (actor.roles || []).join(' ').toLowerCase();
            const cases = (actor.involved_cases || []).join(' ').toLowerCase();
            const q = query.toLowerCase();
            return name.includes(q) || roles.includes(q) || cases.includes(q);
          })
          .slice(0, limit)
          .map(([id, actor]) => ({
            id,
            name: actor.name,
            role: actor.roles?.join(', ') || 'Unknown',
            actor_type: actor.actor_type,
            cases: actor.involved_cases?.length || 0,
          }));

        return NextResponse.json({ results });
      }

      case 'get_case_questions': {
        const { case_type, limit = 20 } = params || {};
        const results = Object.entries(ws.questions)
          .filter(([_, q]) => {
            if (!case_type) return true;
            // Match on question_type or source_chunk_id for case-related questions
            const questionType = q.question_type?.toLowerCase() || '';
            const questionText = q.question_text?.toLowerCase() || '';
            const sourceChunk = q.source_chunk_id?.toLowerCase() || '';
            const caseTypeLower = case_type.toLowerCase();
            return questionType.includes(caseTypeLower) ||
                   questionText.includes(caseTypeLower) ||
                   sourceChunk.includes(caseTypeLower);
          })
          .slice(0, limit)
          .map(([id, q]) => ({
            id,
            text: q.question_text,
            category: q.question_type,
            answered: q.answerable && q.answer_text !== null,
            answer: q.answer_text,
          }));

        return NextResponse.json({ results });
      }

      case 'get_unanswered_questions': {
        const { category, limit = 20 } = params || {};
        const results = Object.entries(ws.questions)
          .filter(([_, q]) => {
            const matchesCategory = !category ||
              q.question_type?.toLowerCase().includes(category.toLowerCase()) ||
              q.question_text?.toLowerCase().includes(category.toLowerCase());
            // Unanswered = no answer_text
            return matchesCategory && !q.answer_text;
          })
          .slice(0, limit)
          .map(([id, q]) => ({
            id,
            text: q.question_text,
            category: q.question_type,
          }));

        return NextResponse.json({ results });
      }

      case 'find_actors_by_role': {
        const { role, limit = 10 } = params || {};
        const results = Object.entries(ws.actors)
          .filter(([_, actor]) => {
            if (!role) return true;
            const roles = (actor.roles || []).join(' ').toLowerCase();
            return roles.includes(role.toLowerCase());
          })
          .slice(0, limit)
          .map(([id, actor]) => ({
            id,
            name: actor.name,
            role: actor.roles?.join(', ') || 'Unknown',
            actor_type: actor.actor_type,
            cases: actor.involved_cases?.length || 0,
          }));

        return NextResponse.json({ results });
      }

      case 'get_knowledge_context': {
        const { query, max_actors = 5, max_questions = 10, format = 'json' } = params || {};

        // Get relevant actors
        const actors = Object.entries(ws.actors)
          .filter(([_, actor]) => {
            if (!query) return true;
            const name = actor.name?.toLowerCase() || '';
            const roles = (actor.roles || []).join(' ').toLowerCase();
            const cases = (actor.involved_cases || []).join(' ').toLowerCase();
            const q = query.toLowerCase();
            return name.includes(q) || roles.includes(q) || cases.includes(q);
          })
          .slice(0, max_actors)
          .map(([id, actor]) => ({
            id,
            name: actor.name,
            role: actor.roles?.join(', ') || 'Unknown',
          }));

        // Get relevant questions
        const questions = Object.entries(ws.questions)
          .filter(([_, q]) => {
            if (!query) return true;
            return q.question_text?.toLowerCase().includes(query.toLowerCase()) ||
              q.question_type?.toLowerCase().includes(query.toLowerCase());
          })
          .slice(0, max_questions)
          .map(([id, q]) => ({
            id,
            text: q.question_text,
            category: q.question_type,
            answered: q.answerable && q.answer_text !== null,
          }));

        const total_actors = Object.keys(ws.actors).length;
        const total_questions = Object.keys(ws.questions).length;

        // Return TOON format if requested (~40% token reduction)
        if (format === 'toon') {
          const toonOutput = ToonEncoder.encodeKnowledgeContext({
            actors,
            questions,
            total_actors,
            total_questions,
          });
          return new NextResponse(toonOutput, {
            headers: { 'Content-Type': 'text/plain' },
          });
        }

        return NextResponse.json({
          actors,
          questions,
          total_actors,
          total_questions,
        });
      }

      case 'search_cases': {
        const { query, limit = 10 } = params || {};
        if (!query) {
          return NextResponse.json({ error: 'Query is required' }, { status: 400 });
        }

        const cases = await loadCases();
        const queryLower = query.toLowerCase();
        const queryTerms = queryLower.split(/\s+/).filter((t: string) => t.length > 2);

        const results = cases
          .filter(c => isActualCase(c)) // Only include actual court cases, not legislation
          .filter(c => {
            const textLower = c.text.toLowerCase();
            const citationLower = c.citation.toLowerCase();
            // Match if any query term appears
            return queryTerms.some((term: string) =>
              textLower.includes(term) || citationLower.includes(term)
            );
          })
          .slice(0, limit)
          .map(c => ({
            citation: c.citation,
            date: c.date,
            jurisdiction: c.jurisdiction,
            source: c.source,
            url: c.url,
            category: c._classification?.primary_category || 'Unknown',
            summary: extractCaseSummary(c.text),
            outcome: extractOutcome(c.text),
          }));

        return NextResponse.json({
          results,
          total_searched: cases.length,
          query_terms: queryTerms,
        });
      }

      case 'find_similar_cases': {
        const { story, limit = 5 } = params || {};
        if (!story) {
          return NextResponse.json({ error: 'Story/situation is required' }, { status: 400 });
        }

        const cases = await loadCases();
        const keywords = extractKeyTerms(story);

        // Initialize TEM Reasoner
        const reasoner = await getLegalReasoner(cases);
        const structuralMatches = reasoner.findStructuralPrecedents(story, limit);

        if (keywords.length === 0 && structuralMatches.length === 0) {
          return NextResponse.json({
            results: [],
            message: 'Could not identify relevant legal keywords or patterns from your story.',
            keywords: [],
          });
        }

        // Classic Keyword Matching
        const keywordResults = cases
          .filter(c => isActualCase(c))
          .map(c => ({
            case: c,
            score: scoreCaseRelevance(c, keywords),
            type: 'keyword'
          }))
          .filter(sc => sc.score > 0)
          .sort((a, b) => b.score - a.score)
          .slice(0, limit);

        // Convert TEM matches back to CaseRecords if possible
        const structuralResults = structuralMatches.map(match => {
          const foundCase = cases.find(c => c.citation === match.citation);
          return foundCase ? {
            case: foundCase,
            score: match.similarity * 100, // Scale 0-1 to 0-100 approx
            reasoning: match.reasoning,
            type: 'structural'
          } : null;
        }).filter(Boolean) as Array<{ case: CaseRecord, score: number, reasoning?: string, type: string }>;

        // Merge results (deduplicate by citation)
        const combined = [...structuralResults, ...keywordResults];
        const seen = new Set();
        const uniqueResults = combined.filter(item => {
          if (seen.has(item.case.citation)) return false;
          seen.add(item.case.citation);
          return true;
        }).slice(0, limit);

        const results = uniqueResults.map(sc => ({
          citation: sc.case.citation,
          date: sc.case.date,
          jurisdiction: sc.case.jurisdiction,
          source: sc.case.source,
          url: sc.case.url,
          category: sc.case._classification?.primary_category || 'Unknown',
          relevance_score: sc.score,
          match_type: sc.type,
          structural_reasoning: sc.reasoning,
          summary: extractCaseSummary(sc.case.text),
          outcome: extractOutcome(sc.case.text),
          matched_keywords: keywords.filter(kw =>
            sc.case.text.toLowerCase().includes(kw)
          ),
        }));

        return NextResponse.json({
          results,
          keywords_identified: keywords,
          total_cases_searched: cases.length,
          message: `Found ${results.length} cases. ${structuralResults.length} structural matches, ${keywordResults.length} keyword matches.`,
        });
      }

      case 'get_case_details': {
        const { citation } = params || {};
        if (!citation) {
          return NextResponse.json({ error: 'Citation is required' }, { status: 400 });
        }

        const cases = await loadCases();
        const foundCase = cases.find(c =>
          c.citation.toLowerCase().includes(citation.toLowerCase())
        );

        if (!foundCase) {
          return NextResponse.json({ error: 'Case not found' }, { status: 404 });
        }

        return NextResponse.json({
          citation: foundCase.citation,
          date: foundCase.date,
          jurisdiction: foundCase.jurisdiction,
          source: foundCase.source,
          url: foundCase.url,
          category: foundCase._classification?.primary_category || 'Unknown',
          full_text: foundCase.text,
          summary: extractCaseSummary(foundCase.text),
          outcome: extractOutcome(foundCase.text),
        });
      }

      case 'get_applicable_law': {
        const { facts, section } = params || {};

        const legislation = await loadLegislation();
        if (!legislation) {
          return NextResponse.json({ error: 'Legislation not loaded' }, { status: 500 });
        }

        // If specific section requested
        if (section) {
          const foundSection = legislation.sections.find(s =>
            s.section === section || s.section.startsWith(section)
          );

          if (!foundSection) {
            return NextResponse.json({ error: 'Section not found' }, { status: 404 });
          }

          return NextResponse.json({
            act: legislation.act,
            section: foundSection,
            citation: `Section ${foundSection.section} of the ${legislation.act.name}`,
          });
        }

        // If facts provided, find relevant sections
        if (facts) {
          const relevantSections = findRelevantSections(facts, legislation);

          return NextResponse.json({
            act: legislation.act,
            relevant_sections: relevantSections.map(s => ({
              section: s.section,
              subsection: s.subsection,
              title: s.title,
              legal_test: s.legal_test,
              summary: s.summary,
              citation: `Section ${s.section}${s.subsection ? `(${s.subsection})` : ''} of the ${legislation.act.name}`,
            })),
            message: `Found ${relevantSections.length} applicable sections based on the provided facts`,
          });
        }

        // Return all sections for reference
        return NextResponse.json({
          act: legislation.act,
          sections: legislation.sections.map(s => ({
            section: s.section,
            title: s.title,
            legal_test: s.legal_test,
          })),
          related_legislation: legislation.related_legislation,
        });
      }

      case 'statutory_alignment': {
        // Combined case + legislation search
        const { story, limit = 5 } = params || {};
        if (!story) {
          return NextResponse.json({ error: 'Story/situation is required' }, { status: 400 });
        }

        // Get relevant legislation
        const legislation = await loadLegislation();
        const relevantSections = legislation ? findRelevantSections(story, legislation) : [];

        // Get similar cases (filter out legislation documents - only actual court cases)
        const cases = await loadCases();
        const keywords = extractKeyTerms(story);

        // Initialize TEM Reasoner and predict outcome
        const reasoner = await getLegalReasoner(cases);
        const prediction = reasoner.predictOutcome(story);
        
        // Active Inference: Detect Gaps
        const detector = getEvidenceDetector();
        const gaps = detector.detectGaps(story);
        const significantGaps = gaps.filter(g => g.evi > 0.5); // Filter for significant gaps

        // Score cases with hybrid approach
        const scoredCases = cases
          .filter(c => isActualCase(c))
          .map(c => ({ case: c, score: scoreCaseRelevance(c, keywords) }))
          .filter(sc => sc.score > 0)
          .sort((a, b) => b.score - a.score)
          .slice(0, limit);

        // VSA: Anti-Hallucination Check
        const vsa = getLegalVSA();
        const vsaCheck = vsa.verifyNoHallucination(story);

        return NextResponse.json({
          // Active Inference: Missing Evidence
          missing_evidence: significantGaps.length > 0 ? {
            status: 'incomplete',
            gaps: significantGaps.slice(0, 3), // Top 3 gaps
            recommendation: "Providing this information will significantly improve the accuracy of the advice."
          } : { status: 'complete' },
          // TEM Predictive Insight
          prediction: {
            outcome: prediction.prediction,
            confidence: prediction.confidence,
            reasoning: prediction.reasoning,
            structural_precedents: prediction.supporting_precedents
          },
          // VSA Validation
          validation: {
            valid: vsaCheck.valid,
            issues: vsaCheck.issues,
            confidence_score: vsaCheck.confidence
          },
          // Legislation (the LAW)
          applicable_law: relevantSections.map(s => ({
            citation: `Section ${s.section} of the Family Law Act 1975 (Cth)`,
            section: s.section,
            title: s.title,
            legal_test: s.legal_test,
            summary: s.summary,
          })),
          // Cases (how the LAW was applied)
          similar_cases: scoredCases.map(sc => ({
            citation: sc.case.citation,
            date: sc.case.date,
            relevance_score: sc.score,
            summary: extractCaseSummary(sc.case.text),
            outcome: extractOutcome(sc.case.text),
          })),
          // Analysis guidance
          keywords_identified: keywords,
          message: `Found ${relevantSections.length} applicable sections and ${scoredCases.length} similar cases`,
        });
      }

      default:
        return NextResponse.json({
          error: 'Invalid action',
          available: [
            'find_parties',
            'get_case_questions',
            'get_unanswered_questions',
            'find_actors_by_role',
            'get_knowledge_context',
            'search_cases',
            'find_similar_cases',
            'get_case_details',
            'get_applicable_law',
            'statutory_alignment',
          ],
        }, { status: 400 });
    }
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'GSW operation failed' },
      { status: 500 }
    );
  }
}

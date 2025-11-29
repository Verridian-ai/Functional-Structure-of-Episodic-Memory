import { CaseStructure, CaseFacts, StructuralMatch, OutcomePrediction } from './types';

// Helper to clean text
const clean = (text: string) => text.toLowerCase().replace(/\s+/g, ' ').trim();

export class TEMFactorizer {
  
  /**
   * Factorizes a raw case text into Structure (g) and Facts (x).
   * This separates the abstract legal pattern from specific details.
   */
  factorize(text: string): { structure: CaseStructure; facts: CaseFacts } {
    const cleanedText = clean(text);

    const structure = this.extractStructure(cleanedText);
    const facts = this.extractFacts(cleanedText);

    return { structure, facts };
  }

  private extractStructure(text: string): CaseStructure {
    return {
      party_pattern: this.classifyPartyPattern(text),
      issue_types: this.identifyIssues(text),
      temporal_pattern: this.classifyTemporal(text),
      asset_complexity: this.assessAssetComplexity(text),
      child_factors: this.analyzeChildren(text)
    };
  }

  private extractFacts(text: string): CaseFacts {
    // Simple regex extraction for demo purposes
    // In a full system, this would use NER (Named Entity Recognition)
    return {
      party_names: {
        applicant: "Applicant", // Placeholder logic
        respondent: "Respondent"
      },
      dates: this.extractDates(text),
      values: this.extractValues(text),
      locations: {},
      children: []
    };
  }

  // --- Classification Logic ---

  private classifyPartyPattern(text: string): string {
    if (text.includes('homemaker') && (text.includes('high income') || text.includes('breadwinner'))) {
      return 'high_income_vs_primary_carer';
    }
    if (text.includes('business') && text.includes('employee')) {
      return 'business_owner_vs_employee';
    }
    if (text.includes('equal contribution') || text.includes('dual income')) {
      return 'equal_partners';
    }
    return 'standard_dispute';
  }

  private identifyIssues(text: string): string[] {
    const issues = [];
    if (text.match(/child|parenting|custody|live with|spend time/)) issues.push('parenting');
    if (text.match(/property|asset|pool|superannuation|house/)) issues.push('property');
    if (text.match(/support|maintenance/)) issues.push('child_support');
    return issues;
  }

  private classifyTemporal(text: string): string {
    if (text.match(/\b(1[5-9]|[2-9]\d)\s*years?\s*marriage/)) return 'long_marriage'; // >15 years
    if (text.match(/\b([0-4])\s*years?\s*marriage/)) return 'short_marriage'; // <5 years
    if (text.match(/de facto/)) return 'de_facto';
    return 'medium_marriage';
  }

  private assessAssetComplexity(text: string): string {
    if (text.match(/trust|company|structure|offshore/)) return 'complex_structure';
    if (text.match(/business|partnership/)) return 'business_interests';
    if (text.match(/million|high net worth/)) return 'high_value';
    return 'simple_pool';
  }

  private analyzeChildren(text: string): { count: number; age_range: string; special_needs: boolean } {
    let count = 0;
    const countMatch = text.match(/(\d+)\s*children/);
    if (countMatch) count = parseInt(countMatch[1]);
    else if (text.includes('child')) count = 1;

    let age_range = 'primary';
    if (text.match(/baby|infant|toddler/)) age_range = 'preschool';
    if (text.match(/teenager|adolescent|1[3-9]/)) age_range = 'teenager';

    const special_needs = /autism|adhd|disability|special needs/.test(text);

    return { count, age_range, special_needs };
  }

  // --- Fact Extraction Helpers ---

  private extractDates(text: string): Record<string, string> {
    const dates: Record<string, string> = {};
    const yearMatch = text.match(/\b(19|20)\d{2}\b/g);
    if (yearMatch) {
      if (yearMatch[0]) dates['start'] = yearMatch[0];
      if (yearMatch[1]) dates['end'] = yearMatch[1];
    }
    return dates;
  }

  private extractValues(text: string): Record<string, number> {
    const values: Record<string, number> = {};
    // Match $500,000 or $1.2m
    const moneyMatch = text.match(/\$[\d,]+(?:\.\d+)?(?:k|m)?/g);
    if (moneyMatch) {
      values['detected_value'] = 100000; // Placeholder for first match parsing
    }
    return values;
  }

  // --- Similarity Computation ---

  /**
   * Computes structural similarity between two cases.
   * This is the core of TEM: matching patterns (g) regardless of facts (x).
   */
  computeSimilarity(structA: CaseStructure, structB: CaseStructure): number {
    let score = 0;
    const weights = {
      party_pattern: 0.35,
      issue_types: 0.25,
      temporal_pattern: 0.15,
      asset_complexity: 0.15,
      child_factors: 0.10
    };

    // 1. Party Pattern
    if (structA.party_pattern === structB.party_pattern) score += weights.party_pattern;

    // 2. Issue Types (Jaccard similarity)
    const intersection = structA.issue_types.filter(t => structB.issue_types.includes(t)).length;
    const union = new Set([...structA.issue_types, ...structB.issue_types]).size;
    if (union > 0) score += weights.issue_types * (intersection / union);

    // 3. Temporal Pattern
    if (structA.temporal_pattern === structB.temporal_pattern) score += weights.temporal_pattern;

    // 4. Asset Complexity
    if (structA.asset_complexity === structB.asset_complexity) score += weights.asset_complexity;

    // 5. Child Factors
    if (structA.child_factors.count > 0 && structB.child_factors.count > 0) {
        // Match if age range is same
        if (structA.child_factors.age_range === structB.child_factors.age_range) {
            score += weights.child_factors;
        }
    } else if (structA.child_factors.count === 0 && structB.child_factors.count === 0) {
        // Both have no children
        score += weights.child_factors;
    }

    return score;
  }
}

export class ZeroShotLegalReasoner {
  private factorizer: TEMFactorizer;
  private precedents: Array<{ citation: string; structure: CaseStructure; outcome?: string; text: string }>;

  constructor() {
    this.factorizer = new TEMFactorizer();
    this.precedents = [];
  }

  /**
   * Load precedents and pre-compute their structures.
   */
  loadPrecedents(cases: Array<{ citation: string; text: string; outcome?: string }>) {
    this.precedents = cases.map(c => ({
      ...c,
      structure: this.factorizer.factorize(c.text).structure
    }));
  }

  /**
   * Find structurally similar precedents for a new case story.
   */
  findStructuralPrecedents(story: string, topK: number = 5): StructuralMatch[] {
    const newStructure = this.factorizer.factorize(story).structure;

    const matches = this.precedents.map(p => ({
      citation: p.citation,
      similarity: this.factorizer.computeSimilarity(newStructure, p.structure),
      outcome: p.outcome,
      pattern_match: newStructure.party_pattern === p.structure.party_pattern,
      reasoning: `Matched pattern: ${p.structure.party_pattern} with similarity ${(this.factorizer.computeSimilarity(newStructure, p.structure) * 100).toFixed(0)}%`
    }));

    return matches
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, topK);
  }

  /**
   * Predict outcome based on weighted structural neighbors.
   */
  predictOutcome(story: string): OutcomePrediction {
    const matches = this.findStructuralPrecedents(story, 5);
    
    if (matches.length === 0) {
        return {
            prediction: null,
            confidence: 0,
            supporting_precedents: [],
            reasoning: "No structural precedents found."
        };
    }

    // Simple voting logic (can be enhanced)
    // For now, return the top match's outcome
    const topMatch = matches[0];

    return {
        prediction: topMatch.outcome || "Outcome dependent on judicial discretion",
        confidence: topMatch.similarity,
        supporting_precedents: matches.map(m => m.citation),
        reasoning: `Based on structural similarity to ${topMatch.citation} (${(topMatch.similarity * 100).toFixed(0)}% match)`
    };
  }
}


import { VSARole, VSAConcept, ValidationResult, ValidationIssue } from './types';

export class LegalVSA {
  private ontology: Record<VSARole, Set<string>>;

  constructor() {
    this.ontology = {
      'PARTY_ROLE': new Set(['applicant', 'respondent', 'child', 'third_party', 'wife', 'husband', 'mother', 'father', 'grandmother', 'grandfather']),
      'ASSET_ROLE': new Set(['real_property', 'superannuation', 'business', 'vehicle', 'savings', 'shares', 'home', 'house', 'cash', 'furniture']),
      'LIABILITY_ROLE': new Set(['mortgage', 'loan', 'credit_card', 'tax_debt', 'debt']),
      'INCOME_ROLE': new Set(['salary', 'wages', 'dividends', 'rent', 'Centrelink', 'pension']),
      'CONTRIBUTION_ROLE': new Set(['financial', 'non_financial', 'homemaker', 'parenting', 'initial', 'inheritance', 'gift', 'windfall']),
      'OUTCOME_ROLE': new Set(['equal_division', 'unequal_division', 'sole_custody', 'shared_care', 'sale', 'transfer']),
      'TEMPORAL_ROLE': new Set(['marriage', 'separation', 'cohabitation', 'divorce', 'final_hearing']),
      'LEGAL_TEST_ROLE': new Set(['best_interests', 'just_and_equitable', 'clean_break', 'parental_responsibility']),
      'SECTION_ROLE': new Set(['s79', 's79(4)', 's75(2)', 's60CC', 's60B', 's60CA', 's60I'])
    };
  }

  /**
   * Verify that the text contains only valid legal concepts from the ontology.
   * This prevents "hallucination" of invalid legal terms or non-existent sections.
   */
  verifyNoHallucination(text: string): ValidationResult {
    const concepts = this.extractPotentialConcepts(text);
    const issues: ValidationIssue[] = [];

    for (const concept of concepts) {
        if (!this.isValidConcept(concept)) {
            const nearest = this.findNearestValid(concept.filler, concept.role);
            issues.push({
                invalid: `${concept.role}:${concept.filler}`,
                suggested: nearest ? `${concept.role}:${nearest}` : undefined,
                reason: `Concept '${concept.filler}' is not a recognized filler for role '${concept.role}'`
            });
        }
    }

    return {
        valid: issues.length === 0,
        issues,
        confidence: Math.max(0, 1.0 - (issues.length / Math.max(1, concepts.length)))
    };
  }

  private extractPotentialConcepts(text: string): VSAConcept[] {
    const concepts: VSAConcept[] = [];
    const lowerText = text.toLowerCase();

    // Simple heuristic extraction based on context keywords
    // In a full VSA, this would be the "Unbinding" step from the query vector
    
    // Check for Assets (avoid confusing with liabilities)
    if (lowerText.includes('asset') || lowerText.includes('property')) {
        // Look for asset fillers
        for (const filler of this.ontology['ASSET_ROLE']) {
            if (lowerText.includes(filler.replace('_', ' '))) {
                concepts.push({ role: 'ASSET_ROLE', filler });
            }
        }
    }

    // Check for Liabilities
    if (lowerText.includes('debt') || lowerText.includes('liability') || lowerText.includes('loan')) {
        for (const filler of this.ontology['LIABILITY_ROLE']) {
            if (lowerText.includes(filler.replace('_', ' '))) {
                concepts.push({ role: 'LIABILITY_ROLE', filler });
            }
        }
    }

    // Check for Sections
    const sectionMatch = text.match(/s\s*(\d+[A-Z]*(\(\d+\))?)/g);
    if (sectionMatch) {
        for (const s of sectionMatch) {
            const normalized = s.replace(/\s+/g, '').replace('section', 's');
            concepts.push({ role: 'SECTION_ROLE', filler: normalized });
        }
    }

    return concepts;
  }

  private isValidConcept(concept: VSAConcept): boolean {
    const validFillers = this.ontology[concept.role];
    if (!validFillers) return false;
    
    // Exact match check
    if (validFillers.has(concept.filler)) return true;

    // Loose match for sections (e.g. s79 vs s79(4))
    if (concept.role === 'SECTION_ROLE') {
        for (const valid of validFillers) {
            if (concept.filler.startsWith(valid)) return true;
        }
    }

    return false;
  }

  private findNearestValid(filler: string, role: VSARole): string | undefined {
    const validFillers = Array.from(this.ontology[role]);
    // Simple Levenshtein or inclusion check could go here
    // For now, return the first one that contains the string or undefined
    return validFillers.find(v => v.includes(filler) || filler.includes(v));
  }
}


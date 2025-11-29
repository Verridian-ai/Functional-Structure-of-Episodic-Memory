import { EvidenceGap, DiscoveryQuestion, CaseContext } from './types';

export class LegalEvidenceDetector {
  
  /**
   * Detects missing evidence and calculates Expected Value of Information (EVI)
   * to prioritize what to ask next.
   */
  detectGaps(text: string): EvidenceGap[] {
    const context = this.analyzeContext(text);
    const potentialGaps = this.getRequiredElements(context.case_type);
    
    const gaps: EvidenceGap[] = [];
    const textLower = text.toLowerCase();

    for (const element of potentialGaps) {
      // Check if element is present (simple keyword heuristic for now)
      const isPresent = element.keywords.some(kw => textLower.includes(kw));
      
      if (!isPresent) {
        const evi = this.computeEVI(element, context);
        gaps.push({
          element: element.name,
          importance: element.importance,
          reason: element.reason,
          suggested_query: element.query,
          evi
        });
      }
    }

    // Sort by EVI (highest first)
    return gaps.sort((a, b) => b.evi - a.evi);
  }

  private analyzeContext(text: string): CaseContext {
    let case_type = 'property'; // Default
    if (text.match(/child|parenting|custody/i)) case_type = 'parenting';
    if (text.match(/property|asset|finance|split/i) && text.match(/child|parenting/i)) case_type = 'mixed';
    
    // Rough timeline coverage estimation
    const dates = text.match(/\b(19|20)\d{2}\b/g) || [];
    const timeline_coverage = Math.min(dates.length * 0.2, 1.0);

    return {
      case_type,
      facts_present: [], // populated by extraction if needed
      timeline_coverage
    };
  }

  private computeEVI(element: any, context: CaseContext): number {
    // EVI = Impact * Entropy * Reduction_Probability
    
    // 1. Impact: How much does this change the outcome?
    const impact = element.importance;

    // 2. Entropy: How uncertain are we? (Simplified: High if timeline is sparse)
    const entropy = 1.0 - (context.timeline_coverage * 0.5); 

    // 3. Reduction Probability: How likely is the user to know this?
    // Core facts (marriage date) are high probability. Nuanced facts (exact super balance) are lower.
    const reductionProb = element.accessibility || 0.8;

    return impact * entropy * reductionProb;
  }

  private getRequiredElements(caseType: string) {
    const propertyElements = [
      {
        name: 'marriage_date',
        keywords: ['married', 'marriage', 'wedding'],
        importance: 0.9,
        reason: 'Determines length of relationship and contributions',
        query: 'When did the parties marry?',
        accessibility: 1.0
      },
      {
        name: 'separation_date',
        keywords: ['separated', 'separation'],
        importance: 0.95,
        reason: 'Defines asset pool valuation date',
        query: 'When did the parties separate?',
        accessibility: 1.0
      },
      {
        name: 'asset_pool',
        keywords: ['assets', 'property', 'value', 'worth', 'pool'],
        importance: 1.0,
        reason: 'Required for s79 step 1 identification',
        query: 'What are the assets and liabilities of the parties?',
        accessibility: 0.9
      },
      {
        name: 'contributions',
        keywords: ['contribution', 'financial', 'homemaker'],
        importance: 0.9,
        reason: 'Required for s79 step 2 assessment',
        query: 'What financial and non-financial contributions were made?',
        accessibility: 0.8
      },
      {
        name: 'future_needs',
        keywords: ['health', 'income', 'earning', 'age'],
        importance: 0.85,
        reason: 'Required for s75(2) adjustment',
        query: 'What are the future needs (health, income, age) of each party?',
        accessibility: 0.9
      }
    ];

    const parentingElements = [
      {
        name: 'children_details',
        keywords: ['ages', 'dob', 'born', 'old'],
        importance: 1.0,
        reason: 'Core jurisdiction requirement',
        query: 'What are the ages of the children?',
        accessibility: 1.0
      },
      {
        name: 'current_arrangements',
        keywords: ['live with', 'spend time', 'care', 'schedule'],
        importance: 0.9,
        reason: 'Status quo is a key factor',
        query: 'What are the current parenting arrangements?',
        accessibility: 1.0
      },
      {
        name: 'safety_risk',
        keywords: ['safety', 'violence', 'abuse', 'risk', 'harm'],
        importance: 1.0,
        reason: 'Paramount consideration s60CC(2)(b)',
        query: 'Are there any family violence or safety concerns?',
        accessibility: 0.9
      },
      {
        name: 'relationship_quality',
        keywords: ['relationship', 'bond', 'attachment'],
        importance: 0.8,
        reason: 'Primary consideration s60CC(2)(a)',
        query: 'What is the nature of the child\'s relationship with each parent?',
        accessibility: 0.7
      }
    ];

    if (caseType === 'property') return propertyElements;
    if (caseType === 'parenting') return parentingElements;
    return [...propertyElements, ...parentingElements]; // Mixed
  }
}


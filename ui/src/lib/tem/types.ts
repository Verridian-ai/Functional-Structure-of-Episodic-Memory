export interface CaseStructure {
  party_pattern: string; // "high_income_vs_primary_carer", "equal_income_equal_care"
  issue_types: string[]; // ["custody", "property", "child_support"]
  temporal_pattern: string; // "long_marriage", "short_marriage", "de_facto"
  asset_complexity: string; // "simple", "complex_pool", "business_interests"
  child_factors: {
    count: number;
    age_range: string; // "preschool", "primary", "teenager"
    special_needs: boolean;
  };
}

export interface CaseFacts {
  party_names: Record<string, string>; // {"applicant": "John", "respondent": "Jane"}
  dates: Record<string, string>; // {"marriage": "2010", "separation": "2020"}
  values: Record<string, number>; // {"pool": 500000}
  locations: Record<string, string>;
  children: Array<{ name: string; age?: number }>;
}

export interface StructuralMatch {
  citation: string;
  similarity: number;
  outcome?: string;
  reasoning?: string;
  pattern_match: boolean;
}

export interface OutcomePrediction {
  prediction: string | null;
  confidence: number;
  supporting_precedents: string[];
  reasoning: string;
}


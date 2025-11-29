export type VSARole = 
  | 'PARTY_ROLE' 
  | 'ASSET_ROLE' 
  | 'LIABILITY_ROLE' 
  | 'INCOME_ROLE' 
  | 'CONTRIBUTION_ROLE' 
  | 'OUTCOME_ROLE' 
  | 'TEMPORAL_ROLE' 
  | 'LEGAL_TEST_ROLE' 
  | 'SECTION_ROLE';

export interface VSAConcept {
  role: VSARole;
  filler: string;
}

export interface ValidationIssue {
  invalid: string;
  suggested?: string;
  reason: string;
}

export interface ValidationResult {
  valid: boolean;
  issues: ValidationIssue[];
  confidence: number;
}


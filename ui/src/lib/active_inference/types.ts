export interface EvidenceGap {
  element: string;
  importance: number; // 0.0 to 1.0
  reason: string;
  suggested_query: string;
  evi: number; // Expected Value of Information
}

export interface DiscoveryQuestion {
  question_text: string;
  type: 'fact' | 'document' | 'timeline';
  priority: 'high' | 'medium' | 'low';
  evi: number;
}

export interface CaseContext {
  case_type: string; // 'property', 'parenting', 'divorce', 'mixed'
  facts_present: string[];
  timeline_coverage: number; // 0.0 to 1.0
}


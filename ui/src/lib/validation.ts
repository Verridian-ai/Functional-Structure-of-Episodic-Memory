import stateTransitions from '../../../data/validation/state_transitions.json';

export interface ValidationResult {
  valid: boolean;
  error?: string;
  suggestion?: string;
}

export interface StateEvent {
  name: string;
  value: string;
  start_date: string;
  end_date?: string;
}

export interface Actor {
  id: string;
  states: StateEvent[];
}

/**
 * Validates that the sequence of states for an actor follows logical rules.
 * e.g. Married -> Separated -> Divorced is valid.
 *      Married -> Divorced (without separation) is technically possible but usually implies separation date = divorce date.
 *      Divorced -> Married is valid.
 *      Divorced -> Separated is invalid (must marry again first).
 */
export function validateStateSequence(actor: Actor): ValidationResult {
  // Group states by name (e.g. RelationshipStatus)
  const statesByName: Record<string, StateEvent[]> = {};
  
  for (const state of actor.states) {
    if (!statesByName[state.name]) {
      statesByName[state.name] = [];
    }
    statesByName[state.name].push(state);
  }

  // Validate each state type
  for (const [stateName, events] of Object.entries(statesByName)) {
    // @ts-expect-error - JSON import might not match strict typing perfectly without casting
    const rules = stateTransitions[stateName];
    
    if (!rules) continue; // No rules for this state type

    // Sort by date
    const sorted = events.sort((a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime());

    for (let i = 0; i < sorted.length - 1; i++) {
      const current = sorted[i].value;
      const next = sorted[i + 1].value;

      const allowed = rules.valid_transitions[current];

      if (!allowed || !allowed.includes(next)) {
        return {
          valid: false,
          error: `Invalid transition for ${stateName}: ${current} → ${next}`,
          suggestion: `Expected one of: ${allowed?.join(', ') || 'None'}`
        };
      }
    }
  }

  return { valid: true };
}

/**
 * Check if an event date is chronologically impossible
 */
export function validateDates(events: StateEvent[]): ValidationResult {
  for (const event of events) {
    if (event.end_date && new Date(event.end_date) < new Date(event.start_date)) {
      return {
        valid: false,
        error: `Invalid dates for ${event.name}: End date (${event.end_date}) is before start date (${event.start_date})`
      };
    }
  }
  return { valid: true };
}


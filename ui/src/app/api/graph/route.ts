import { NextRequest, NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';

// Types for our Graph Data
type Node = {
  id: string;
  x: number;
  y: number;
  z: number;
  color: string;
  size: number;
  label: string;
  type: 'case' | 'statute' | 'concept';
  uncertainty: number;
  court?: string;
  date?: string;
  state?: string;       // NSW, VIC, QLD, WA, SA, TAS, NT, ACT, Federal
  domain?: string;      // family, criminal, commercial, constitutional, etc.
  courtLevel?: string;  // high_court, appeals, supreme, district, magistrate
};

type Edge = {
  source: string;
  target: string;
  weight: number;
  type?: string;
};

type GraphData = {
  nodes: Node[];
  edges: Edge[];
  stats: {
    totalNodes: number;
    totalEdges: number;
    loadedNodes: number;
    loadedEdges: number;
  };
  filters?: {
    availableStates: string[];
    availableDomains: string[];
    availableCourtLevels: string[];
  };
};

type FilterOptions = {
  state?: string;       // Filter by state/jurisdiction
  domain?: string;      // Filter by legal domain
  courtLevel?: string;  // Filter by court level
};

// State/Jurisdiction detection from citation codes
function detectState(nodeId: string, court: string): string {
  const id = nodeId.toUpperCase();
  const courtUpper = court.toUpperCase();

  // Federal courts
  if (id.includes('HCA') || id.includes('FCA') || id.includes('FCAFC') ||
      id.includes('FAMCA') || id.includes('FAMCAFC') || id.includes('AAT') ||
      id.includes('FWC') || id.includes('AIRC') ||
      courtUpper.includes('HIGH COURT') || courtUpper.includes('FEDERAL')) {
    return 'Federal';
  }
  // NSW
  if (id.includes('NSW') || id.includes('NSWSC') || id.includes('NSWCA') ||
      id.includes('NSWCCA') || id.includes('NSWLEC') || id.includes('NCAT') ||
      courtUpper.includes('NEW SOUTH WALES')) {
    return 'NSW';
  }
  // VIC
  if (id.includes('VSC') || id.includes('VSCA') || id.includes('VCC') ||
      id.includes('VCAT') || courtUpper.includes('VICTORIA')) {
    return 'VIC';
  }
  // QLD
  if (id.includes('QSC') || id.includes('QCA') || id.includes('QDC') ||
      id.includes('QCAT') || courtUpper.includes('QUEENSLAND')) {
    return 'QLD';
  }
  // WA
  if (id.includes('WASC') || id.includes('WASCA') || id.includes('WADC') ||
      courtUpper.includes('WESTERN AUSTRALIA')) {
    return 'WA';
  }
  // SA
  if (id.includes('SASC') || id.includes('SASCFC') || id.includes('SADC') ||
      id.includes('SACAT') || courtUpper.includes('SOUTH AUSTRALIA')) {
    return 'SA';
  }
  // TAS
  if (id.includes('TASSC') || id.includes('TASCCA') ||
      courtUpper.includes('TASMANIA')) {
    return 'TAS';
  }
  // NT
  if (id.includes('NTSC') || id.includes('NTCA') ||
      courtUpper.includes('NORTHERN TERRITORY')) {
    return 'NT';
  }
  // ACT
  if (id.includes('ACTSC') || id.includes('ACTCA') ||
      courtUpper.includes('AUSTRALIAN CAPITAL')) {
    return 'ACT';
  }

  return 'Other';
}

// Legal domain detection from case content/title
function detectDomain(nodeId: string, court: string, title: string = ''): string {
  const text = `${nodeId} ${court} ${title}`.toLowerCase();

  if (text.includes('famca') || text.includes('family') || text.includes('child') ||
      text.includes('custody') || text.includes('divorce') || text.includes('marriage') ||
      text.includes('parenting') || text.includes('spousal')) {
    return 'Family';
  }
  if (text.includes('cca') || text.includes('criminal') || text.includes('murder') ||
      text.includes('assault') || text.includes('robbery') || text.includes('drug') ||
      text.includes('sentence') || text.includes('conviction') || text.includes('parole')) {
    return 'Criminal';
  }
  if (text.includes('commercial') || text.includes('contract') || text.includes('company') ||
      text.includes('corporation') || text.includes('insolvency') || text.includes('bankruptcy') ||
      text.includes('trade') || text.includes('business')) {
    return 'Commercial';
  }
  if (text.includes('constitutional') || text.includes('referendum') ||
      text.includes('federation') || text.includes('sovereignty')) {
    return 'Constitutional';
  }
  if (text.includes('property') || text.includes('land') || text.includes('real estate') ||
      text.includes('conveyancing') || text.includes('mortgage') || text.includes('lease')) {
    return 'Property';
  }
  if (text.includes('employment') || text.includes('fwc') || text.includes('fair work') ||
      text.includes('unfair dismissal') || text.includes('workplace') || text.includes('industrial')) {
    return 'Employment';
  }
  if (text.includes('tort') || text.includes('negligence') || text.includes('personal injury') ||
      text.includes('defamation') || text.includes('nuisance')) {
    return 'Tort';
  }
  if (text.includes('admin') || text.includes('tribunal') || text.includes('aat') ||
      text.includes('judicial review') || text.includes('government')) {
    return 'Administrative';
  }
  if (text.includes('equity') || text.includes('trust') || text.includes('fiduciary') ||
      text.includes('injunction') || text.includes('specific performance')) {
    return 'Equity';
  }
  if (text.includes('immigration') || text.includes('visa') || text.includes('refugee') ||
      text.includes('asylum') || text.includes('migration')) {
    return 'Immigration';
  }

  return 'General';
}

// Court level detection
function detectCourtLevel(courtKey: string): string {
  if (courtKey === 'high_court') return 'Apex';
  if (courtKey.includes('appeals') || courtKey.includes('_appeals')) return 'Appeals';
  if (courtKey.includes('supreme') || courtKey.includes('_supreme')) return 'Supreme';
  if (courtKey === 'federal_court') return 'Federal';
  if (courtKey === 'federal_circuit') return 'Circuit';
  if (courtKey === 'family') return 'Specialized';
  if (courtKey === 'criminal') return 'Criminal';
  if (courtKey === 'admin_tribunal') return 'Tribunal';
  if (courtKey === 'industrial') return 'Tribunal';
  if (courtKey === 'land_environment') return 'Specialized';
  return 'Other';
}

// Cache for loaded graph data
let cachedGraph: GraphData | null = null;
let cacheTimestamp: number = 0;
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

// Expanded court type to color mapping - 16 distinct categories
const COURT_COLORS: Record<string, string> = {
  // Federal Courts
  'high_court': '#fbbf24',       // Gold - High Court of Australia (HCA)
  'federal_court': '#3b82f6',    // Blue - Federal Court (FCA, FedCFamC)
  'federal_circuit': '#60a5fa',  // Light Blue - Federal Circuit Court

  // State Supreme Courts
  'nsw_supreme': '#22c55e',      // Green - NSW Supreme Court (NSWSC)
  'vic_supreme': '#10b981',      // Emerald - VIC Supreme Court (VSC)
  'qld_supreme': '#14b8a6',      // Teal - QLD Supreme Court (QSC)
  'wa_supreme': '#06b6d4',       // Cyan - WA Supreme Court (WASC)
  'sa_supreme': '#0ea5e9',       // Sky - SA Supreme Court (SASC)

  // Courts of Appeal
  'nsw_appeals': '#a855f7',      // Purple - NSW Court of Appeal (NSWCA)
  'vic_appeals': '#8b5cf6',      // Violet - VIC Court of Appeal (VSCA)
  'qld_appeals': '#7c3aed',      // Indigo - QLD Court of Appeal (QCA)

  // Specialized Courts
  'family': '#ec4899',           // Pink - Family Court (FamCA, FamCAFC)
  'criminal': '#ef4444',         // Red - Criminal courts (CCA, NSWCCA)
  'land_environment': '#84cc16', // Lime - Land & Environment (NSWLEC)
  'admin_tribunal': '#f97316',   // Orange - Admin tribunals (AAT, NCAT)
  'industrial': '#eab308',       // Yellow - Industrial/Employment (FWC)

  // Default
  'default': '#94a3b8',          // Gray - Other/Unknown
};

// Generate 3D coordinates using force-directed-like clustering
function generateCoordinates(
  nodeId: string,
  index: number,
  total: number,
  courtType: string
): { x: number; y: number; z: number } {
  // Use court type to create clusters
  const courtIndex = Object.keys(COURT_COLORS).indexOf(courtType);
  const clusterAngle = (courtIndex >= 0 ? courtIndex : 0) * (Math.PI * 2 / Object.keys(COURT_COLORS).length);

  // Spherical distribution within cluster
  const theta = clusterAngle + (Math.random() - 0.5) * 0.8;
  const phi = Math.acos((Math.random() * 2) - 1);
  const r = 30 + Math.random() * 40; // Radius between 30-70

  return {
    x: r * Math.sin(phi) * Math.cos(theta),
    y: r * Math.sin(phi) * Math.sin(theta),
    z: r * Math.cos(phi),
  };
}

// Load graph data from JSONL files with optional filtering
async function loadGraphFromFiles(limit: number = 5000, filters: FilterOptions = {}): Promise<GraphData> {
  const projectRoot = path.resolve(process.cwd(), '..');
  // Use demo files (smaller, GitHub-compatible) - fall back to full files if available
  const nodesPath = path.join(projectRoot, 'data', 'processed', 'graph', 'spcnet_nodes_demo.jsonl');
  const edgesPath = path.join(projectRoot, 'data', 'processed', 'graph', 'spcnet_edges_demo.jsonl');

  // Fallback paths
  const altNodesPath = path.join(process.cwd(), '..', 'data', 'processed', 'graph', 'spcnet_nodes_demo.jsonl');
  const altEdgesPath = path.join(process.cwd(), '..', 'data', 'processed', 'graph', 'spcnet_edges_demo.jsonl');

  // Determine which paths exist
  let finalNodesPath = nodesPath;
  let finalEdgesPath = edgesPath;

  if (!fs.existsSync(nodesPath)) {
    if (fs.existsSync(altNodesPath)) {
      finalNodesPath = altNodesPath;
      finalEdgesPath = altEdgesPath;
    } else {
      console.warn('Graph data files not found, using mock data');
      return generateMockGraph(limit);
    }
  }

  const nodes: Node[] = [];
  const nodeIdSet = new Set<string>();
  const citationToId = new Map<string, string>(); // Map short citations to full IDs
  let totalNodes = 0;
  let filteredOut = 0;

  // Track available filter values
  const availableStates = new Set<string>();
  const availableDomains = new Set<string>();
  const availableCourtLevels = new Set<string>();

  // Read nodes
  try {
    const nodesFileStream = fs.createReadStream(finalNodesPath);
    const nodesRl = readline.createInterface({
      input: nodesFileStream,
      crlfDelay: Infinity,
    });

    for await (const line of nodesRl) {
      totalNodes++;
      if (nodes.length >= limit) continue;

      try {
        const data = JSON.parse(line);
        const nodeId = data.id || data.citation;
        if (!nodeId) continue;

        // Determine court/category from citation codes in the ID
        const court = data.court || data.jurisdiction || nodeId;
        const courtLower = court.toLowerCase();
        const title = data.title || '';

        // Parse citation codes - order matters (most specific first)
        let courtKey = 'default';

        // High Court of Australia (apex court)
        if (nodeId.includes('HCA') || nodeId.includes(' CLR ') || courtLower.includes('high court')) {
          courtKey = 'high_court';
        }
        // Federal Courts
        else if (nodeId.includes('FCAFC') || nodeId.includes('FCA')) {
          courtKey = 'federal_court';
        }
        else if (nodeId.includes('FedCFamC') || nodeId.includes('FCCA')) {
          courtKey = 'federal_circuit';
        }
        // Family Courts (specialized)
        else if (nodeId.includes('FamCA') || nodeId.includes('FamCAFC') || nodeId.includes('FamC') || courtLower.includes('family')) {
          courtKey = 'family';
        }
        // NSW Courts
        else if (nodeId.includes('NSWCA') || nodeId.includes('NSWCCA')) {
          courtKey = 'nsw_appeals';
        }
        else if (nodeId.includes('NSWSC')) {
          courtKey = 'nsw_supreme';
        }
        else if (nodeId.includes('NSWLEC')) {
          courtKey = 'land_environment';
        }
        // VIC Courts
        else if (nodeId.includes('VSCA') || nodeId.includes('VicCA')) {
          courtKey = 'vic_appeals';
        }
        else if (nodeId.includes('VSC')) {
          courtKey = 'vic_supreme';
        }
        // QLD Courts
        else if (nodeId.includes('QCA')) {
          courtKey = 'qld_appeals';
        }
        else if (nodeId.includes('QSC')) {
          courtKey = 'qld_supreme';
        }
        // WA Courts
        else if (nodeId.includes('WASCA') || nodeId.includes('WASC')) {
          courtKey = 'wa_supreme';
        }
        // SA Courts
        else if (nodeId.includes('SASCFC') || nodeId.includes('SASC')) {
          courtKey = 'sa_supreme';
        }
        // Criminal Courts
        else if (nodeId.includes('CCA') || courtLower.includes('criminal')) {
          courtKey = 'criminal';
        }
        // Admin Tribunals
        else if (nodeId.includes('AAT') || nodeId.includes('NCAT') || nodeId.includes('AATA') || courtLower.includes('tribunal')) {
          courtKey = 'admin_tribunal';
        }
        // Industrial/Employment
        else if (nodeId.includes('FWC') || nodeId.includes('AIRC') || courtLower.includes('fair work') || courtLower.includes('industrial')) {
          courtKey = 'industrial';
        }
        // Fallback: distribute by hash for visual diversity
        else {
          const hash = nodeId.split('').reduce((acc: number, char: string) => acc + char.charCodeAt(0), 0);
          const fallbackKeys = ['nsw_supreme', 'vic_supreme', 'qld_supreme', 'federal_court', 'family', 'criminal'];
          courtKey = fallbackKeys[hash % fallbackKeys.length];
        }

        // Detect state, domain, and court level
        const state = detectState(nodeId, court);
        const domain = detectDomain(nodeId, court, title);
        const courtLevel = detectCourtLevel(courtKey);

        // Track available filter values (before filtering)
        availableStates.add(state);
        availableDomains.add(domain);
        availableCourtLevels.add(courtLevel);

        // Apply filters if specified
        if (filters.state && filters.state !== 'all' && state !== filters.state) {
          filteredOut++;
          continue;
        }
        if (filters.domain && filters.domain !== 'all' && domain !== filters.domain) {
          filteredOut++;
          continue;
        }
        if (filters.courtLevel && filters.courtLevel !== 'all' && courtLevel !== filters.courtLevel) {
          filteredOut++;
          continue;
        }

        const coords = generateCoordinates(nodeId, nodes.length, limit, courtKey);

        nodes.push({
          id: nodeId,
          x: coords.x,
          y: coords.y,
          z: coords.z,
          color: COURT_COLORS[courtKey] || COURT_COLORS.default,
          size: 0.5 + Math.random() * 0.5,
          label: title || nodeId.slice(0, 30),
          type: data.type === 'legislation' ? 'statute' : 'case',
          uncertainty: Math.random() * 0.5,
          court: court,
          date: data.date,
          state: state,
          domain: domain,
          courtLevel: courtLevel,
        });

        nodeIdSet.add(nodeId);

        // Extract citation patterns and create lookup mappings
        // Match MNC: [YYYY] COURT NUM (e.g., [2013] NSWSC 1668)
        const mncMatch = nodeId.match(/\[\d{4}\]\s+[A-Z]+\s+\d+/);
        if (mncMatch) {
          citationToId.set(mncMatch[0], nodeId);
        }

        // Match CLR: (YYYY) NUM COURT NUM (e.g., (1986) 6 NSWLR 497)
        const clrMatch = nodeId.match(/\(\d{4}\)\s+\d+\s+[A-Z]+\s+\d+/);
        if (clrMatch) {
          citationToId.set(clrMatch[0], nodeId);
        }
      } catch (e) {
        // Skip malformed lines
      }
    }
  } catch (error) {
    console.error('Error reading nodes:', error);
    return generateMockGraph(limit);
  }

  const edges: Edge[] = [];
  let totalEdges = 0;
  const edgeLimit = limit * 3; // More edges than nodes

  // Read edges
  try {
    const edgesFileStream = fs.createReadStream(finalEdgesPath);
    const edgesRl = readline.createInterface({
      input: edgesFileStream,
      crlfDelay: Infinity,
    });

    for await (const line of edgesRl) {
      totalEdges++;
      if (edges.length >= edgeLimit) continue;

      try {
        const data = JSON.parse(line);
        let source = data.source;
        let target = data.target;

        // Resolve citations to full node IDs
        const resolvedSource = citationToId.get(source) || source;
        const resolvedTarget = citationToId.get(target) || target;

        // Only include edges where both nodes are in our loaded set
        if (nodeIdSet.has(resolvedSource) && nodeIdSet.has(resolvedTarget)) {
          edges.push({
            source: resolvedSource,
            target: resolvedTarget,
            weight: data.weight || 0.5,
            type: data.type,
          });
        }
      } catch (e) {
        // Skip malformed lines
      }
    }
  } catch (error) {
    console.error('Error reading edges:', error);
  }

  return {
    nodes,
    edges,
    stats: {
      totalNodes,
      totalEdges,
      loadedNodes: nodes.length,
      loadedEdges: edges.length,
    },
    filters: {
      availableStates: Array.from(availableStates).sort(),
      availableDomains: Array.from(availableDomains).sort(),
      availableCourtLevels: Array.from(availableCourtLevels).sort(),
    },
  };
}

// Mock Data Generator (fallback)
function generateMockGraph(count: number): GraphData {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const categories = ['case', 'statute', 'concept'] as const;

  for (let i = 0; i < count; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos((Math.random() * 2) - 1);
    const r = 50 * Math.cbrt(Math.random());

    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);

    const type = categories[Math.floor(Math.random() * categories.length)];
    let color = '#ffffff';
    if (type === 'case') color = '#60a5fa';
    if (type === 'statute') color = '#34d399';
    if (type === 'concept') color = '#f472b6';

    nodes.push({
      id: `node_${i}`,
      x, y, z,
      color,
      size: Math.random() * 0.5 + 0.5,
      label: `${type.toUpperCase()} ${i}`,
      type,
      uncertainty: Math.random(),
    });
  }

  for (let i = 0; i < count * 2; i++) {
    const sourceIdx = Math.floor(Math.random() * count);
    let targetIdx = Math.floor(Math.random() * count);
    while (targetIdx === sourceIdx) targetIdx = Math.floor(Math.random() * count);

    edges.push({
      source: `node_${sourceIdx}`,
      target: `node_${targetIdx}`,
      weight: Math.random(),
    });
  }

  return {
    nodes,
    edges,
    stats: {
      totalNodes: count,
      totalEdges: count * 2,
      loadedNodes: count,
      loadedEdges: count * 2,
    },
  };
}

// Load graph data from JSONL files or Neo4j
async function loadGraph(limit: number = 5000, useNeo4j: boolean = false, filters: FilterOptions = {}): Promise<GraphData> {
  if (useNeo4j && process.env.NEO4J_URI) {
      try {
          // TODO: Implement real Neo4j fetching
          console.log("Neo4j integration pending");
      } catch (e) {
          console.error("Neo4j Error:", e);
      }
  }

  return loadGraphFromFiles(limit, filters);
}

// Cache per filter combination
const filterCache = new Map<string, { data: GraphData; timestamp: number }>();

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const limit = parseInt(searchParams.get('limit') || '5000', 10);
  const refresh = searchParams.get('refresh') === 'true';
  const mock = searchParams.get('mock') === 'true';
  const source = searchParams.get('source'); // 'neo4j' or 'file'

  // Filter parameters
  const filters: FilterOptions = {
    state: searchParams.get('state') || undefined,
    domain: searchParams.get('domain') || undefined,
    courtLevel: searchParams.get('courtLevel') || undefined,
  };

  // Use mock data if requested
  if (mock) {
    const data = generateMockGraph(limit);
    return NextResponse.json(data);
  }

  // Create cache key based on filters
  const cacheKey = `${limit}-${filters.state || 'all'}-${filters.domain || 'all'}-${filters.courtLevel || 'all'}`;

  // Check cache
  const now = Date.now();
  const cached = filterCache.get(cacheKey);
  if (source !== 'neo4j' && !refresh && cached && (now - cached.timestamp) < CACHE_TTL) {
    return NextResponse.json(cached.data);
  }

  // Load data
  try {
    const data = await loadGraph(limit, source === 'neo4j', filters);
    if (source !== 'neo4j') {
      filterCache.set(cacheKey, { data, timestamp: now });
      // Keep cache size manageable
      if (filterCache.size > 20) {
        const oldestKey = filterCache.keys().next().value;
        if (oldestKey) filterCache.delete(oldestKey);
      }
    }
    return NextResponse.json(data);
  } catch (error) {
    console.error('Failed to load graph:', error);
    const fallback = generateMockGraph(limit);
    return NextResponse.json(fallback);
  }
}

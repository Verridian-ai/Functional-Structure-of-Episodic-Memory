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
};

// Cache for loaded graph data
let cachedGraph: GraphData | null = null;
let cacheTimestamp: number = 0;
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

// Court type to color mapping
const COURT_COLORS: Record<string, string> = {
  'family': '#f472b6',        // Pink - Family Law
  'federal_court': '#60a5fa', // Blue - Federal Court
  'appeals': '#a78bfa',       // Purple - Appeals
  'apex_court': '#fbbf24',    // Yellow - High Court
  'supreme_court': '#34d399', // Green - Supreme Court
  'criminal': '#ef4444',      // Red - Criminal
  'commercial': '#06b6d4',    // Cyan - Commercial
  'admin_tribunal': '#f97316', // Orange - Admin
  'default': '#94a3b8',       // Gray - Other
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

// Load graph data from JSONL files
async function loadGraphFromFiles(limit: number = 5000): Promise<GraphData> {
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
  let totalNodes = 0;

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

        // Determine court/category from the data
        const court = data.court || data.jurisdiction || 'default';
        const courtKey = Object.keys(COURT_COLORS).find(k => court.toLowerCase().includes(k)) || 'default';

        const coords = generateCoordinates(nodeId, nodes.length, limit, courtKey);

        nodes.push({
          id: nodeId,
          x: coords.x,
          y: coords.y,
          z: coords.z,
          color: COURT_COLORS[courtKey] || COURT_COLORS.default,
          size: 0.5 + Math.random() * 0.5,
          label: data.title || nodeId.slice(0, 30),
          type: data.type === 'legislation' ? 'statute' : 'case',
          uncertainty: Math.random() * 0.5, // Lower uncertainty for real data
          court: court,
          date: data.date,
        });

        nodeIdSet.add(nodeId);
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
        const source = data.source;
        const target = data.target;

        // Only include edges where both nodes are in our loaded set
        if (nodeIdSet.has(source) && nodeIdSet.has(target)) {
          edges.push({
            source,
            target,
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
async function loadGraph(limit: number = 5000, useNeo4j: boolean = false): Promise<GraphData> {
  if (useNeo4j && process.env.NEO4J_URI) {
      try {
          // TODO: Implement real Neo4j fetching
          // const driver = neo4j.driver(process.env.NEO4J_URI, neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD));
          // const session = driver.session();
          // ...
          console.log("Neo4j integration pending");
      } catch (e) {
          console.error("Neo4j Error:", e);
      }
  }
  
  return loadGraphFromFiles(limit);
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const limit = parseInt(searchParams.get('limit') || '5000', 10);
  const refresh = searchParams.get('refresh') === 'true';
  const mock = searchParams.get('mock') === 'true';
  const source = searchParams.get('source'); // 'neo4j' or 'file'

  // Use mock data if requested
  if (mock) {
    const data = generateMockGraph(limit);
    return NextResponse.json(data);
  }

  // Check cache if not Neo4j (Neo4j should probably not cache the same way or have its own)
  const now = Date.now();
  if (source !== 'neo4j' && !refresh && cachedGraph && (now - cacheTimestamp) < CACHE_TTL) {
    return NextResponse.json(cachedGraph);
  }

  // Load data
  try {
    const data = await loadGraph(limit, source === 'neo4j');
    if (source !== 'neo4j') {
        cachedGraph = data;
        cacheTimestamp = now;
    }
    return NextResponse.json(data);
  } catch (error) {
    console.error('Failed to load graph:', error);
    const fallback = generateMockGraph(limit);
    return NextResponse.json(fallback);
  }
}

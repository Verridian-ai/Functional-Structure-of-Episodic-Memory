import { NextResponse } from 'next/server';

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
  uncertainty: number; // For Agency Heatmap (U4.5)
};

type Edge = {
  source: string;
  target: string;
  weight: number;
};

type GraphData = {
  nodes: Node[];
  edges: Edge[];
};

// Mock Data Generator (simulating UMAP projection of TEM manifold - U4.3)
function generateMockGraph(count: number): GraphData {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const categories = ['case', 'statute', 'concept'] as const;

  // Generate Nodes (instanced mesh requires simpler data, but we pass full objects for now)
  for (let i = 0; i < count; i++) {
    // Generate random 3D coordinates (spherical cluster)
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos((Math.random() * 2) - 1);
    const r = 50 * Math.cbrt(Math.random()); // Cluster radius 50
    
    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);

    // Assign type and color
    const type = categories[Math.floor(Math.random() * categories.length)];
    let color = '#ffffff';
    if (type === 'case') color = '#60a5fa'; // Blue
    if (type === 'statute') color = '#34d399'; // Green
    if (type === 'concept') color = '#f472b6'; // Pink

    nodes.push({
      id: `node_${i}`,
      x,
      y,
      z,
      color,
      size: Math.random() * 0.5 + 0.5,
      label: `${type.toUpperCase()} ${i}`,
      type,
      uncertainty: Math.random() // 0 to 1
    });
  }

  // Generate Edges (Random connections for demo)
  for (let i = 0; i < count * 2; i++) {
    const sourceIdx = Math.floor(Math.random() * count);
    let targetIdx = Math.floor(Math.random() * count);
    while (targetIdx === sourceIdx) targetIdx = Math.floor(Math.random() * count);
    
    edges.push({
      source: `node_${sourceIdx}`,
      target: `node_${targetIdx}`,
      weight: Math.random()
    });
  }

  return { nodes, edges };
}

export async function GET() {
  // In a real implementation, this would fetch from the Python backend or Neo4j
  // For Phase 4 demo, we generate 1000 nodes
  const data = generateMockGraph(2000);
  
  return NextResponse.json(data);
}


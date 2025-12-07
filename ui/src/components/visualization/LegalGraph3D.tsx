'use client';

import React, { useRef, useMemo, useState, useEffect } from 'react';
import { Canvas, useFrame, ThreeEvent } from '@react-three/fiber';
import { OrbitControls, Text, Html } from '@react-three/drei';
import * as THREE from 'three';

// Types
type Node = {
  id: string;
  x: number;
  y: number;
  z: number;
  color: string;
  size: number;
  label: string;
  uncertainty: number;
  court?: string;
  date?: string;
  type?: 'case' | 'statute' | 'concept';
  state?: string;
  domain?: string;
  courtLevel?: string;
};

type Edge = {
  source: string;
  target: string;
  weight: number;
};

type GraphData = {
  nodes: Node[];
  edges: Edge[];
  stats?: {
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

type FilterState = {
  state: string;
  domain: string;
  courtLevel: string;
};

// Custom shader for circular glowing points
const vertexShader = `
  attribute float size;
  varying vec3 vColor;
  void main() {
    vColor = color;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = size * (300.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
  }
`;

const fragmentShader = `
  varying vec3 vColor;
  void main() {
    // Create circular point with soft glow
    vec2 center = gl_PointCoord - vec2(0.5);
    float dist = length(center);

    // Soft circular falloff with glow
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
    float glow = exp(-dist * 4.0) * 0.5;

    // Combine base color with glow
    vec3 finalColor = vColor * (1.0 + glow);

    if (dist > 0.5) discard;

    gl_FragColor = vec4(finalColor, alpha);
  }
`;

// --- Points-based Nodes Component for colored tensor visualization ---
function ColoredNodes({ nodes, onNodeClick }: { nodes: Node[], onNodeClick: (node: Node) => void }) {
  const pointsRef = useRef<THREE.Points>(null);

  const { geometry, shaderMaterial } = useMemo(() => {
    const positions = new Float32Array(nodes.length * 3);
    const colors = new Float32Array(nodes.length * 3);
    const sizes = new Float32Array(nodes.length);
    const tempColor = new THREE.Color();

    nodes.forEach((node, i) => {
      // Position
      positions[i * 3] = node.x;
      positions[i * 3 + 1] = node.y;
      positions[i * 3 + 2] = node.z;

      // Color from court type - boost saturation
      tempColor.set(node.color);
      colors[i * 3] = Math.min(1.0, tempColor.r * 1.2);
      colors[i * 3 + 1] = Math.min(1.0, tempColor.g * 1.2);
      colors[i * 3 + 2] = Math.min(1.0, tempColor.b * 1.2);

      // Size - varied for visual interest
      sizes[i] = (node.size + 0.5) * 2.5;
    });

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const material = new THREE.ShaderMaterial({
      uniforms: {},
      vertexShader,
      fragmentShader,
      vertexColors: true,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });

    return { geometry: geo, shaderMaterial: material };
  }, [nodes]);

  const handleClick = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    if (e.index !== undefined && nodes[e.index]) {
      onNodeClick(nodes[e.index]);
    }
  };

  return (
    <points
      ref={pointsRef}
      geometry={geometry}
      material={shaderMaterial}
      onClick={handleClick}
      onPointerOver={() => document.body.style.cursor = 'pointer'}
      onPointerOut={() => document.body.style.cursor = 'auto'}
    />
  );
}

// --- Edges Component ---
function Edges({ edges, nodes }: { edges: Edge[], nodes: Node[] }) {
  const linesGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry();
    const positions: number[] = [];
    
    // Create map for fast lookup
    const nodeMap = new Map(nodes.map(n => [n.id, n]));

    edges.forEach(edge => {
      const source = nodeMap.get(edge.source);
      const target = nodeMap.get(edge.target);

      if (source && target) {
        positions.push(source.x, source.y, source.z);
        positions.push(target.x, target.y, target.z);
      }
    });

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    return geometry;
  }, [edges, nodes]);

  return (
    <lineSegments geometry={linesGeometry}>
      <lineBasicMaterial
        attach="material"
        color="#4488ff"
        opacity={0.3}
        transparent
        linewidth={1}
      />
    </lineSegments>
  );
}

// --- Main Visualizer Component ---
export default function LegalGraph3D() {
  const [data, setData] = useState<GraphData>({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<FilterState>({
    state: 'all',
    domain: 'all',
    courtLevel: 'all',
  });
  const [availableFilters, setAvailableFilters] = useState<{
    states: string[];
    domains: string[];
    courtLevels: string[];
  }>({ states: [], domains: [], courtLevels: [] });

  // Fetch data with filters
  const fetchGraph = async (currentFilters: FilterState) => {
    setLoading(true);
    const params = new URLSearchParams();
    if (currentFilters.state !== 'all') params.set('state', currentFilters.state);
    if (currentFilters.domain !== 'all') params.set('domain', currentFilters.domain);
    if (currentFilters.courtLevel !== 'all') params.set('courtLevel', currentFilters.courtLevel);

    try {
      const res = await fetch(`/api/graph?${params.toString()}`);
      const graphData = await res.json();
      setData(graphData);
      if (graphData.filters) {
        setAvailableFilters({
          states: graphData.filters.availableStates || [],
          domains: graphData.filters.availableDomains || [],
          courtLevels: graphData.filters.availableCourtLevels || [],
        });
      }
    } catch (error) {
      console.error('Failed to fetch graph:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchGraph(filters);
  }, []);

  const handleFilterChange = (filterType: keyof FilterState, value: string) => {
    const newFilters = { ...filters, [filterType]: value };
    setFilters(newFilters);
    fetchGraph(newFilters);
  };

  return (
    <div className="w-full h-full relative bg-zinc-950">
      {/* Overlay UI (U4.4) */}
      <div className="absolute top-4 left-4 z-10 pointer-events-none">
        <div className="bg-zinc-900/90 backdrop-blur-md border border-zinc-700 p-4 rounded-lg pointer-events-auto max-w-sm">
          <h2 className="text-white font-bold text-lg mb-2">Legal Citation Network</h2>

          {/* Filter Controls */}
          <div className="space-y-2 mb-4 pb-3 border-b border-zinc-700">
            <div className="text-xs text-cyan-400 font-medium mb-2">Filter Knowledge Graph</div>

            {/* State/Jurisdiction Filter */}
            <div className="flex items-center gap-2">
              <label className="text-xs text-zinc-400 w-20">State:</label>
              <select
                value={filters.state}
                onChange={(e) => handleFilterChange('state', e.target.value)}
                className="flex-1 bg-zinc-800 border border-zinc-600 rounded px-2 py-1 text-xs text-white focus:border-cyan-500 focus:outline-none"
              >
                <option value="all">All States</option>
                {availableFilters.states.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            {/* Legal Domain Filter */}
            <div className="flex items-center gap-2">
              <label className="text-xs text-zinc-400 w-20">Domain:</label>
              <select
                value={filters.domain}
                onChange={(e) => handleFilterChange('domain', e.target.value)}
                className="flex-1 bg-zinc-800 border border-zinc-600 rounded px-2 py-1 text-xs text-white focus:border-cyan-500 focus:outline-none"
              >
                <option value="all">All Domains</option>
                {availableFilters.domains.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>

            {/* Court Level Filter */}
            <div className="flex items-center gap-2">
              <label className="text-xs text-zinc-400 w-20">Level:</label>
              <select
                value={filters.courtLevel}
                onChange={(e) => handleFilterChange('courtLevel', e.target.value)}
                className="flex-1 bg-zinc-800 border border-zinc-600 rounded px-2 py-1 text-xs text-white focus:border-cyan-500 focus:outline-none"
              >
                <option value="all">All Levels</option>
                {availableFilters.courtLevels.map(cl => (
                  <option key={cl} value={cl}>{cl}</option>
                ))}
              </select>
            </div>

            {/* Active Filters Display */}
            {(filters.state !== 'all' || filters.domain !== 'all' || filters.courtLevel !== 'all') && (
              <div className="flex flex-wrap gap-1 mt-2">
                {filters.state !== 'all' && (
                  <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 rounded text-xs">
                    {filters.state}
                  </span>
                )}
                {filters.domain !== 'all' && (
                  <span className="px-2 py-0.5 bg-pink-500/20 text-pink-400 rounded text-xs">
                    {filters.domain}
                  </span>
                )}
                {filters.courtLevel !== 'all' && (
                  <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 rounded text-xs">
                    {filters.courtLevel}
                  </span>
                )}
                <button
                  onClick={() => {
                    const resetFilters = { state: 'all', domain: 'all', courtLevel: 'all' };
                    setFilters(resetFilters);
                    fetchGraph(resetFilters);
                  }}
                  className="px-2 py-0.5 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 rounded text-xs"
                >
                  Clear
                </button>
              </div>
            )}
          </div>

          {/* Stats */}
          <div className="text-zinc-400 text-sm space-y-1">
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-zinc-800/50 p-2 rounded">
                <div className="text-zinc-500">Loaded Nodes</div>
                <div className="text-white font-mono text-lg">{data.nodes.length.toLocaleString()}</div>
              </div>
              <div className="bg-zinc-800/50 p-2 rounded">
                <div className="text-zinc-500">Loaded Edges</div>
                <div className="text-white font-mono text-lg">{data.edges.length.toLocaleString()}</div>
              </div>
            </div>
            {data.stats && (
              <div className="mt-2 text-xs text-zinc-500">
                Total in database: {data.stats.totalNodes.toLocaleString()} cases, {data.stats.totalEdges.toLocaleString()} citations
              </div>
            )}
          </div>

          {/* Color Legend - Expanded Categories */}
          <div className="mt-3 pt-3 border-t border-zinc-700">
            <div className="text-xs text-zinc-500 mb-2">Court Hierarchy</div>
            <div className="space-y-2 text-xs">
              {/* Apex */}
              <div className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-[#fbbf24] shadow-sm shadow-yellow-500/50" />
                <span className="text-zinc-300 font-medium">High Court (HCA)</span>
              </div>
              {/* Federal */}
              <div className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-[#3b82f6] shadow-sm shadow-blue-500/50" />
                <span className="text-zinc-400">Federal Court</span>
              </div>
              {/* Supreme Courts */}
              <div className="pl-2 border-l border-zinc-700 space-y-1">
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-[#22c55e]" />
                  <span className="text-zinc-500">NSW Supreme</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-[#10b981]" />
                  <span className="text-zinc-500">VIC Supreme</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-[#14b8a6]" />
                  <span className="text-zinc-500">QLD Supreme</span>
                </div>
              </div>
              {/* Appeals */}
              <div className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-[#a855f7] shadow-sm shadow-purple-500/50" />
                <span className="text-zinc-400">Courts of Appeal</span>
              </div>
              {/* Specialized */}
              <div className="flex flex-wrap gap-2 mt-1">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-[#ec4899]" />
                  <span className="text-zinc-500">Family</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-[#ef4444]" />
                  <span className="text-zinc-500">Criminal</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-[#f97316]" />
                  <span className="text-zinc-500">Tribunal</span>
                </div>
              </div>
            </div>
          </div>

          {selectedNode && (
            <div className="mt-4 pt-4 border-t border-zinc-700 animate-in fade-in slide-in-from-top-2">
              <h3 className="text-cyan-400 font-mono font-bold text-sm">{selectedNode.label || selectedNode.id.slice(0, 40)}</h3>
              <p className="text-xs text-zinc-500 mt-1 truncate">{selectedNode.id}</p>
              <div className="flex flex-wrap gap-1 mt-2">
                {selectedNode.state && (
                  <span className="px-1.5 py-0.5 bg-cyan-500/20 text-cyan-400 rounded text-xs">{selectedNode.state}</span>
                )}
                {selectedNode.domain && (
                  <span className="px-1.5 py-0.5 bg-pink-500/20 text-pink-400 rounded text-xs">{selectedNode.domain}</span>
                )}
                {selectedNode.courtLevel && (
                  <span className="px-1.5 py-0.5 bg-yellow-500/20 text-yellow-400 rounded text-xs">{selectedNode.courtLevel}</span>
                )}
              </div>
              {selectedNode.court && (
                <p className="text-xs text-zinc-400 mt-2">Court: {selectedNode.court}</p>
              )}
              {selectedNode.date && (
                <p className="text-xs text-zinc-400">Date: {selectedNode.date}</p>
              )}
              <div className="mt-2 text-xs flex flex-col gap-1">
                <div className="flex justify-between">
                  <span className="text-zinc-400">Uncertainty:</span>
                  <span className={selectedNode.uncertainty > 0.7 ? "text-red-400" : "text-green-400"}>
                    {(selectedNode.uncertainty * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="w-full bg-zinc-800 h-1 mt-1 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${selectedNode.uncertainty > 0.7 ? 'bg-red-500' : 'bg-green-500'}`}
                    style={{ width: `${selectedNode.uncertainty * 100}%` }}
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center z-20 bg-zinc-950">
          <div className="text-cyan-500 animate-pulse font-mono">Loading Tensor Data...</div>
        </div>
      )}

      {/* 3D Scene */}
      <Canvas camera={{ position: [0, 0, 150], fov: 75 }}>
        <color attach="background" args={['#09090b']} /> {/* zinc-950 */}

        {/* Enhanced Lighting for vibrant tensor nodes */}
        <ambientLight intensity={1.2} />
        <pointLight position={[100, 100, 100]} intensity={2.0} color="#ffffff" />
        <pointLight position={[-100, -100, -100]} intensity={2.0} color="#ffffff" />
        <pointLight position={[0, 100, 0]} intensity={1.5} color="#ffffff" />

        {/* Controls */}
        <OrbitControls enableDamping dampingFactor={0.1} rotateSpeed={0.5} zoomSpeed={0.5} />

        {/* Content */}
        {!loading && (
          <>
            <ColoredNodes nodes={data.nodes} onNodeClick={setSelectedNode} />
            <Edges edges={data.edges} nodes={data.nodes} />
            
            {/* Selected Node Highlight */}
            {selectedNode && (
              <mesh position={[selectedNode.x, selectedNode.y, selectedNode.z]}>
                <sphereGeometry args={[selectedNode.size * 1.5, 16, 16]} />
                <meshBasicMaterial color="white" wireframe />
              </mesh>
            )}
          </>
        )}
      </Canvas>
    </div>
  );
}


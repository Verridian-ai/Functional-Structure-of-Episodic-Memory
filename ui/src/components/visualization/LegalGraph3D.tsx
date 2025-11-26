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

// --- Instanced Nodes Component (U4.1) ---
function InstancedNodes({ nodes, onNodeClick }: { nodes: Node[], onNodeClick: (node: Node) => void }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const tempObject = useMemo(() => new THREE.Object3D(), []);
  const colorObject = useMemo(() => new THREE.Color(), []);

  useEffect(() => {
    if (!meshRef.current) return;

    // Update instances
    nodes.forEach((node, i) => {
      const { x, y, z, size, color, uncertainty } = node;
      
      // Position & Scale
      tempObject.position.set(x, y, z);
      tempObject.scale.set(size, size, size);
      tempObject.updateMatrix();
      meshRef.current!.setMatrixAt(i, tempObject.matrix);
      
      // Color (Mix based on uncertainty for Heatmap U4.5)
      // Base color -> Red based on uncertainty
      colorObject.set(color);
      if (uncertainty > 0.5) {
          colorObject.lerp(new THREE.Color('red'), (uncertainty - 0.5) * 2);
      }
      
      meshRef.current!.setColorAt(i, colorObject);
    });

    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) meshRef.current.instanceColor.needsUpdate = true;
  }, [nodes, tempObject, colorObject]);

  const handleClick = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    const instanceId = e.instanceId;
    if (instanceId !== undefined) {
      onNodeClick(nodes[instanceId]);
    }
  };

  return (
    <instancedMesh
      ref={meshRef}
      args={[undefined, undefined, nodes.length]}
      onClick={handleClick}
      onPointerOver={() => document.body.style.cursor = 'pointer'}
      onPointerOut={() => document.body.style.cursor = 'auto'}
    >
      <sphereGeometry args={[1, 16, 16]} />
      <meshStandardMaterial attach="material" toneMapped={false} roughness={0.5} metalness={0.5} />
    </instancedMesh>
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
      <lineBasicMaterial attach="material" color="#ffffff" opacity={0.1} transparent />
    </lineSegments>
  );
}

// --- Main Visualizer Component ---
export default function LegalGraph3D() {
  const [data, setData] = useState<GraphData>({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch Data
    fetch('/api/graph')
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      });
  }, []);

  return (
    <div className="w-full h-full relative bg-zinc-950">
      {/* Overlay UI (U4.4) */}
      <div className="absolute top-4 left-4 z-10 pointer-events-none">
        <div className="bg-zinc-900/80 backdrop-blur-md border border-zinc-700 p-4 rounded-lg pointer-events-auto max-w-xs">
          <h2 className="text-white font-bold text-lg mb-2">TEM Manifold</h2>
          <div className="text-zinc-400 text-sm">
            <p>Interactive visualization of the Legal Space.</p>
            <p className="mt-2">Nodes: {data.nodes.length}</p>
            <p>Edges: {data.edges.length}</p>
          </div>
          
          {selectedNode && (
            <div className="mt-4 pt-4 border-t border-zinc-700 animate-in fade-in slide-in-from-top-2">
              <h3 className="text-cyan-400 font-mono font-bold">{selectedNode.label}</h3>
              <p className="text-xs text-zinc-500 mt-1">ID: {selectedNode.id}</p>
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
      <Canvas camera={{ position: [0, 0, 100], fov: 60 }}>
        <color attach="background" args={['#09090b']} /> {/* zinc-950 */}
        
        {/* Lighting */}
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        
        {/* Controls */}
        <OrbitControls enableDamping dampingFactor={0.1} rotateSpeed={0.5} zoomSpeed={0.5} />

        {/* Content */}
        {!loading && (
          <>
            <InstancedNodes nodes={data.nodes} onNodeClick={setSelectedNode} />
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


'use client';

import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import * as THREE from 'three';
import Image from 'next/image';

// --- Types & Constants ---
const PARTICLE_COUNT = 4000;
const BRAIN_SIZE = 2;

// 4-Color Palette
const COLORS = [
  new THREE.Color('#0088ff'), // Deep Blue
  new THREE.Color('#00f3ff'), // Electric Cyan
  new THREE.Color('#b026ff'), // Vivid Purple
  new THREE.Color('#ffffff'), // Pure White
];

// --- Audio Analyzer Hook ---
function useAudioAnalyzer() {
  const [audioData, setAudioData] = useState<Uint8Array | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const dataArrayRef = useRef<Uint8Array | null>(null);

  useEffect(() => {
    const initAudio = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(stream);
        const analyser = audioContext.createAnalyser();
        analyser.fftSize = 64; // Low FFT size for performance, we just need general volume
        source.connect(analyser);
        
        analyserRef.current = analyser;
        dataArrayRef.current = new Uint8Array(analyser.frequencyBinCount);
      } catch (err) {
        console.warn("Audio access denied or not supported:", err);
      }
    };

    // Initialize on first user interaction to satisfy browser autoplay policies
    const handleInteraction = () => {
      if (!analyserRef.current) initAudio();
      window.removeEventListener('click', handleInteraction);
    };

    window.addEventListener('click', handleInteraction);
    return () => window.removeEventListener('click', handleInteraction);
  }, []);

  // Removed incorrect useFrame from here. Data processing happens in BrainParticles component.

  return { analyserRef, dataArrayRef };
}

// --- Adaptive Settings ---
function useAdaptiveSettings() {
  const [particleCount, setParticleCount] = useState(PARTICLE_COUNT);
  const [enableBloom, setEnableBloom] = useState(true);

  useEffect(() => {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    if (isMobile) {
      setParticleCount(1500); // Reduce particles on mobile
      setEnableBloom(false); // Disable expensive post-processing
    } else {
      setParticleCount(4000);
      setEnableBloom(true);
    }
  }, []);

  return { particleCount, enableBloom };
}

// --- Brain Geometry Generator ---
function generateBrainPositions(count: number) {
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  
  for (let i = 0; i < count; i++) {
    // Random point in unit sphere
    const u = Math.random();
    const v = Math.random();
    const theta = 2 * Math.PI * u;
    const phi = Math.acos(2 * v - 1);
    
    let x = Math.sin(phi) * Math.cos(theta);
    let y = Math.sin(phi) * Math.sin(theta);
    let z = Math.cos(phi);
    
    // Shape deformation to look more like a brain (two hemispheres)
    // Flatten bottom, elongate front-to-back, separate hemispheres
    x *= 0.8; // Width
    y *= 1.2; // Length (front-to-back)
    z *= 0.9; // Height
    
    // Hemisphere separation along X
    x += (x > 0 ? 0.2 : -0.2);

    // Noise/Texture (Brain folds) - simplified as random perturbation
    const scale = 3.5 + Math.random() * 0.5; 
    
    positions[i * 3] = x * scale;
    positions[i * 3 + 1] = z * scale; // Swap Y and Z for better orientation in Three.js
    positions[i * 3 + 2] = y * scale;

    // Color: 4-Color Mix
    const color = COLORS[Math.floor(Math.random() * COLORS.length)];
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }
  
  return { positions, colors };
}

// --- Neural Connections Generator ---
function generateConnections(positions: Float32Array) {
  const connections: number[] = [];
  const maxDist = 0.8; // Connection threshold
  
  // Naive O(N^2) is too slow for 4000 particles. 
  // Optimized approach: Check random subset or spatial grid. 
  // For 'web' look, connecting to nearest neighbors is best.
  // We'll do a simplified random neighbor check for performance here.
  
  for (let i = 0; i < positions.length / 3; i++) {
    const x1 = positions[i * 3];
    const y1 = positions[i * 3 + 1];
    const z1 = positions[i * 3 + 2];
    
    // Check next 50 particles (local clustering often happens due to generation order or just random chance)
    // This is a visual approximation.
    for (let j = 1; j < 20; j++) {
      const targetIdx = (i + j) % (positions.length / 3);
      
      const x2 = positions[targetIdx * 3];
      const y2 = positions[targetIdx * 3 + 1];
      const z2 = positions[targetIdx * 3 + 2];
      
      const dist = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2) + Math.pow(z2 - z1, 2));
      
      if (dist < maxDist) {
        connections.push(x1, y1, z1);
        connections.push(x2, y2, z2);
      }
    }
  }
  
  return new Float32Array(connections);
}

// --- Main 3D Component ---
function BrainParticles({ analyserRef, dataArrayRef, particleCount }: { analyserRef: React.MutableRefObject<AnalyserNode | null>, dataArrayRef: React.MutableRefObject<Uint8Array | null>, particleCount: number }) {
  const pointsRef = useRef<THREE.Points>(null);
  const linesRef = useRef<THREE.LineSegments>(null);
  const groupRef = useRef<THREE.Group>(null);
  
  // Generate Geometry
  const { positions, colors } = useMemo(() => generateBrainPositions(particleCount), [particleCount]);
  const linePositions = useMemo(() => generateConnections(positions), [positions]);
  
  // Mouse interaction
  const { mouse, viewport } = useThree();
  const targetRotation = useRef(new THREE.Vector2(0, 0));

  useFrame((state, delta) => {
    if (!groupRef.current) return;

    // Audio Reactivity: Scale
    let scale = 1;
    if (analyserRef.current && dataArrayRef.current) {
      analyserRef.current.getByteFrequencyData(dataArrayRef.current);
      // Calculate average volume
      const avg = dataArrayRef.current.reduce((a, b) => a + b, 0) / dataArrayRef.current.length;
      // Map 0-255 to scale factor (e.g., 1.0 to 1.2)
      const targetScale = 1 + (avg / 255) * 0.3;
      scale = THREE.MathUtils.lerp(groupRef.current.scale.x, targetScale, 0.1);
    }

    groupRef.current.scale.set(scale, scale, scale);

    // Mouse Rotation (Eye Contact)
    // Convert mouse (-1 to 1) to rotation angles
    const xRot = -mouse.y * 0.5; // Look up/down
    const yRot = mouse.x * 0.5;  // Look left/right
    
    // Smooth interpolation
    groupRef.current.rotation.x = THREE.MathUtils.lerp(groupRef.current.rotation.x, xRot, 0.05);
    groupRef.current.rotation.y = THREE.MathUtils.lerp(groupRef.current.rotation.y, yRot, 0.05);
    
    // Idle floating animation
    groupRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.2;
    
    // Rotate particles slightly for "swarm" feel
    if (pointsRef.current) {
       pointsRef.current.rotation.y += 0.001;
    }
    // Sync lines with points rotation if desired, or keep them static relative to group
    if (linesRef.current && pointsRef.current) {
        linesRef.current.rotation.y = pointsRef.current.rotation.y;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Particles */}
      <points ref={pointsRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={positions.length / 3}
            array={positions}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            count={colors.length / 3}
            array={colors}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.06}
          vertexColors
          transparent
          opacity={0.8}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          sizeAttenuation={true}
        />
      </points>

      {/* Synapse Connections */}
      <lineSegments ref={linesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={linePositions.length / 3}
            array={linePositions}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial
          color="#0088ff"
          transparent
          opacity={0.15}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </lineSegments>
    </group>
  );
}

function CursorLight() {
  const lightRef = useRef<THREE.PointLight>(null);
  const { mouse, viewport } = useThree();

  useFrame(() => {
    if (lightRef.current) {
      // Map 2D mouse to 3D plane at z=2 (rough front of brain)
      const x = (mouse.x * viewport.width) / 2;
      const y = (mouse.y * viewport.height) / 2;
      
      // Smooth movement
      lightRef.current.position.x = THREE.MathUtils.lerp(lightRef.current.position.x, x, 0.1);
      lightRef.current.position.y = THREE.MathUtils.lerp(lightRef.current.position.y, y, 0.1);
      lightRef.current.position.z = 2; // Stay in front
    }
  });

  return (
    <pointLight
      ref={lightRef}
      distance={5}
      intensity={2}
      color="#0088ff"
    />
  );
}

// --- Main Exported Component ---
export function VerridianBrainUltimate() {
  const { analyserRef, dataArrayRef } = useAudioAnalyzer();
  const { particleCount, enableBloom } = useAdaptiveSettings();

  return (
    <div className="fixed inset-0 z-0 bg-black overflow-hidden">
      <Canvas dpr={[1, 2]} gl={{ antialias: false, toneMapping: THREE.NoToneMapping }}>
        <PerspectiveCamera makeDefault position={[0, 0, 12]} fov={45} />
        
        <color attach="background" args={['#000000']} />
        
        {/* Environment Lights */}
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={0.5} color="#ffffff" />
        
        <CursorLight />
        
        <BrainParticles analyserRef={analyserRef} dataArrayRef={dataArrayRef} particleCount={particleCount} />

        {/* Post Processing */}
        {enableBloom && (
          <EffectComposer multisampling={0}>
            <Bloom 
              luminanceThreshold={0.1} 
              mipmapBlur 
              intensity={1.5} 
              radius={0.6} 
            />
          </EffectComposer>
        )}
      </Canvas>

      {/* Overlay UI */}
      {/* Static Logo Overlay Removed as per request - Brain is the hero */}
      <div className="absolute inset-0 pointer-events-none flex flex-col items-center justify-center z-10">
         {/* Keeping empty container for structure if needed later, but content removed */}
      </div>
    </div>
  );
}


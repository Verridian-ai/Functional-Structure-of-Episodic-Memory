import React from 'react';
import LegalGraph3D from '@/components/visualization/LegalGraph3D';

export default function VisualizePage() {
  return (
    <main className="w-screen h-screen overflow-hidden bg-zinc-950">
      <LegalGraph3D />
    </main>
  );
}


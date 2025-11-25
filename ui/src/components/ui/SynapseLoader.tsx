import React from 'react';

export function SynapseLoader({ size = 'md', color = 'cyan' }: { size?: 'sm' | 'md' | 'lg', color?: 'cyan' | 'purple' }) {
  // Map sizes to pixel values
  const sizeMap = {
    sm: 24,
    md: 48,
    lg: 96
  };
  
  const px = sizeMap[size];
  
  const colorClass = color === 'cyan' ? 'bg-cyan-500' : 'bg-purple-500';
  const shadowClass = color === 'cyan' ? 'shadow-[0_0_10px_rgba(6,182,212,0.8)]' : 'shadow-[0_0_10px_rgba(168,85,247,0.8)]';

  return (
    <div className="relative flex items-center justify-center" style={{ width: px, height: px }}>
      <div className="absolute inset-0 flex items-center justify-center">
        {/* Central Core */}
        <div className={`w-[20%] h-[20%] rounded-full ${colorClass} ${shadowClass} animate-pulse`} />
        
        {/* Orbiting Synapses */}
        <div className="absolute w-full h-full animate-spin-slow opacity-70">
          <div className={`absolute top-0 left-1/2 -translate-x-1/2 w-[10%] h-[10%] rounded-full ${colorClass} blur-[1px]`} />
        </div>
        <div className="absolute w-[70%] h-[70%] animate-spin-reverse-slower opacity-60">
          <div className={`absolute bottom-0 left-1/2 -translate-x-1/2 w-[12%] h-[12%] rounded-full ${colorClass} blur-[1px]`} />
        </div>
        
        {/* Firing Lines (CSS only implementation for simplicity) */}
        <div className="absolute w-full h-full animate-ping opacity-20 rounded-full border border-cyan-400" />
      </div>
    </div>
  );
}


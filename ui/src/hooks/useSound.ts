import { useCallback, useEffect, useRef } from 'react';
import { useStore } from '@/lib/store';

type SoundType = 'click' | 'hover' | 'success' | 'error' | 'send';

const SOUND_PATHS: Record<SoundType, string> = {
  click: '/sounds/click.mp3',
  hover: '/sounds/hover.mp3',
  success: '/sounds/success.mp3',
  error: '/sounds/error.mp3',
  send: '/sounds/send.mp3',
};

export function useSound() {
  // We might want to check if sound is enabled in settings, assuming it exists in store
  // For now, we'll just play if called.
  
  const audioRefs = useRef<Record<string, HTMLAudioElement>>({});

  useEffect(() => {
    // Preload sounds
    Object.entries(SOUND_PATHS).forEach(([key, path]) => {
      const audio = new Audio(path);
      audio.volume = 0.2; // Low volume for subtlety
      audioRefs.current[key] = audio;
    });

    return () => {
      audioRefs.current = {};
    };
  }, []);

  const play = useCallback((type: SoundType) => {
    const audio = audioRefs.current[type];
    if (audio) {
      // Reset to start if already playing
      audio.currentTime = 0;
      audio.play().catch(err => {
        // Ignore errors (e.g. user didn't interact yet, or file missing)
        // console.warn('Audio play failed', err);
      });
    }
  }, []);

  return { play };
}


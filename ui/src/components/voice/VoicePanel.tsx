'use client';

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Mic, MicOff, Volume2, VolumeX, Settings2, X, AlertTriangle, ShieldCheck } from 'lucide-react';
import { useStore } from '@/lib/store';

// Permission state type
type PermissionState = 'prompt' | 'granted' | 'denied' | 'unknown';

// Web Speech API types
interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}

interface SpeechRecognitionResultList {
  length: number;
  item(index: number): SpeechRecognitionResult;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognitionResult {
  isFinal: boolean;
  length: number;
  item(index: number): SpeechRecognitionAlternative;
  [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start(): void;
  stop(): void;
  abort(): void;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
}

declare global {
  interface Window {
    SpeechRecognition?: new () => SpeechRecognition;
    webkitSpeechRecognition?: new () => SpeechRecognition;
  }
}

interface VoicePanelProps {
  onTranscript: (text: string) => void;
}

export function VoicePanel({ onTranscript }: VoicePanelProps) {
  const { voice, setVoice, settings, updateSettings } = useStore();
  const [audioLevel, setAudioLevel] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [showConsentDialog, setShowConsentDialog] = useState(false);
  const [micPermission, setMicPermission] = useState<PermissionState>('unknown');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const animationRef = useRef<number | null>(null);

  // Check microphone permission on mount
  useEffect(() => {
    const checkPermission = async () => {
      if (typeof navigator !== 'undefined' && navigator.permissions) {
        try {
          const result = await navigator.permissions.query({ name: 'microphone' as PermissionName });
          setMicPermission(result.state as PermissionState);
          result.onchange = () => setMicPermission(result.state as PermissionState);
        } catch {
          // Permissions API not fully supported
          setMicPermission('unknown');
        }
      }
    };
    checkPermission();
  }, []);

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
          let finalTranscript = '';
          let interimTranscript = '';

          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalTranscript += transcript;
            } else {
              interimTranscript += transcript;
            }
          }

          setVoice({ transcript: interimTranscript || finalTranscript });

          if (finalTranscript) {
            onTranscript(finalTranscript);
            setVoice({ isListening: false });
          }
        };

        recognition.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setVoice({ isListening: false, transcript: '' });
        };

        recognition.onend = () => {
          if (voice.isListening) {
            // Restart if still supposed to be listening
            try {
              recognition.start();
            } catch (e) {
              setVoice({ isListening: false });
            }
          }
        };

        recognitionRef.current = recognition;
      }
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const startAudioVisualization = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      audioContextRef.current = new AudioContext();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;

      const bufferLength = analyserRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const updateLevel = () => {
        if (analyserRef.current) {
          analyserRef.current.getByteFrequencyData(dataArray);
          const average = dataArray.reduce((a, b) => a + b) / bufferLength;
          setAudioLevel(average / 255);
        }
        animationRef.current = requestAnimationFrame(updateLevel);
      };

      updateLevel();
      setMicPermission('granted');
      setErrorMessage(null);
    } catch (e) {
      console.error('Failed to access microphone:', e);
      setMicPermission('denied');
      setErrorMessage('Microphone access was denied. Please enable it in your browser settings.');
      setVoice({ isListening: false });
    }
  }, [setVoice]);

  const stopAudioVisualization = useCallback(() => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    setAudioLevel(0);
  }, []);

  // Handle listening state changes
  useEffect(() => {
    if (voice.isListening) {
      try {
        recognitionRef.current?.start();
        startAudioVisualization();
      } catch (e) {
        console.error('Failed to start recognition:', e);
      }
    } else {
      recognitionRef.current?.stop();
      stopAudioVisualization();
    }
  }, [voice.isListening, startAudioVisualization, stopAudioVisualization]);

  // Request microphone permission with consent
  const requestMicrophoneAccess = useCallback(async () => {
    setShowConsentDialog(false);
    setErrorMessage(null);
    setVoice({ isListening: true, transcript: '' });
  }, [setVoice]);

  const toggleListening = useCallback(() => {
    if (voice.isListening) {
      // Stop listening
      setVoice({ isListening: false, transcript: '' });
    } else {
      // Check if we need to show consent dialog
      if (micPermission === 'prompt' || micPermission === 'unknown') {
        setShowConsentDialog(true);
      } else if (micPermission === 'denied') {
        setErrorMessage('Microphone access was previously denied. Please enable it in your browser settings.');
      } else {
        // Permission already granted
        setVoice({ isListening: true, transcript: '' });
      }
    }
  }, [voice.isListening, micPermission, setVoice]);

  if (!settings.voiceEnabled) return null;

  return (
    <>
      {/* Microphone Permission Consent Dialog */}
      {showConsentDialog && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-labelledby="consent-title">
          <div className="w-full max-w-md bg-zinc-900 rounded-2xl border border-cyan-500/30 p-6 shadow-2xl shadow-cyan-500/10">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-full bg-cyan-500/20 flex items-center justify-center">
                <Mic className="w-6 h-6 text-cyan-400" />
              </div>
              <div>
                <h3 id="consent-title" className="text-lg font-semibold text-white">Microphone Access Required</h3>
                <p className="text-sm text-zinc-400">For voice input feature</p>
              </div>
            </div>

            <div className="bg-zinc-800/50 rounded-xl p-4 mb-4 space-y-2">
              <div className="flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-zinc-300">Your voice data is processed locally in your browser</p>
              </div>
              <div className="flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-zinc-300">No audio recordings are stored or transmitted</p>
              </div>
              <div className="flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-zinc-300">You can revoke access at any time in browser settings</p>
              </div>
            </div>

            <p className="text-sm text-zinc-400 mb-6">
              Clicking &ldquo;Allow&rdquo; will prompt your browser to request microphone permission.
            </p>

            <div className="flex gap-3">
              <button
                onClick={() => setShowConsentDialog(false)}
                className="flex-1 px-4 py-3 rounded-xl border border-zinc-700 text-zinc-300 hover:bg-zinc-800 transition"
              >
                Cancel
              </button>
              <button
                onClick={requestMicrophoneAccess}
                className="flex-1 px-4 py-3 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-medium transition"
              >
                Allow Microphone
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Error Message Toast */}
      {errorMessage && (
        <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 max-w-md">
          <div className="flex items-center gap-3 px-4 py-3 bg-red-900/90 border border-red-700 rounded-xl shadow-lg">
            <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <p className="text-sm text-white">{errorMessage}</p>
            <button
              onClick={() => setErrorMessage(null)}
              className="p-1 hover:bg-red-800 rounded transition"
              aria-label="Dismiss error"
            >
              <X className="w-4 h-4 text-red-300" />
            </button>
          </div>
        </div>
      )}

      {/* Floating Voice Button - Mobile optimized positioning */}
      {voice.isListening && (
        <div className="fixed bottom-24 sm:bottom-32 left-1/2 -translate-x-1/2 z-40">
          <div className="relative">
            {/* Animated rings */}
            <div
              className="absolute inset-0 rounded-full bg-red-500/20 animate-ping"
              style={{ transform: `scale(${1 + audioLevel * 0.5})` }}
            />
            <div
              className="absolute inset-0 rounded-full bg-red-500/30"
              style={{ transform: `scale(${1 + audioLevel * 0.3})` }}
            />

            {/* Main button - Touch-friendly */}
            <button
              onClick={toggleListening}
              className="relative w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-red-500 to-pink-600 flex items-center justify-center shadow-lg shadow-red-500/30 hover:shadow-red-500/50 active:shadow-red-500/50 transition touch-target"
            >
              <Mic className="w-6 h-6 sm:w-8 sm:h-8 text-white" />
            </button>
          </div>

          {/* Transcript display - Mobile optimized width */}
          {voice.transcript && (
            <div className="absolute top-full mt-3 sm:mt-4 left-1/2 -translate-x-1/2 w-[calc(100vw-2rem)] sm:w-80 max-w-80 p-3 sm:p-4 bg-black/80 backdrop-blur-xl border border-cyan-500/30 rounded-xl shadow-xl shadow-cyan-500/10">
              <div className="flex items-center gap-2 mb-1.5 sm:mb-2">
                <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                <span className="text-[10px] sm:text-xs text-cyan-300">Listening...</span>
              </div>
              <p className="text-sm sm:text-base text-white">{voice.transcript}</p>
            </div>
          )}
        </div>
      )}

      {/* Voice Settings Modal - Mobile optimized */}
      {showSettings && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-end sm:items-center justify-center p-0 sm:p-4">
          <div className="w-full sm:max-w-md bg-zinc-900 rounded-t-2xl sm:rounded-2xl border-t sm:border border-zinc-800 p-4 sm:p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4 sm:mb-6">
              <h3 className="text-base sm:text-lg font-semibold text-white">Voice Settings</h3>
              <button
                onClick={() => setShowSettings(false)}
                className="p-2 hover:bg-zinc-800 active:bg-zinc-800 rounded-lg transition touch-target"
              >
                <X className="w-5 h-5 text-zinc-400" />
              </button>
            </div>

            <div className="space-y-3 sm:space-y-4">
              <div>
                <label className="block text-xs sm:text-sm font-medium text-white mb-1.5 sm:mb-2">Language</label>
                <select className="w-full p-2.5 sm:p-3 bg-zinc-800 border border-zinc-700 rounded-lg sm:rounded-xl text-sm sm:text-base text-white focus:outline-none focus:border-cyan-500 touch-target">
                  <option value="en-US">English (US)</option>
                  <option value="en-GB">English (UK)</option>
                  <option value="en-AU">English (Australia)</option>
                </select>
              </div>

              <div className="flex items-center justify-between p-3 sm:p-4 bg-zinc-800 rounded-lg sm:rounded-xl">
                <div className="flex-1 pr-3">
                  <div className="font-medium text-sm sm:text-base text-white">Auto-send on pause</div>
                  <div className="text-xs sm:text-sm text-zinc-400">Send message when you stop speaking</div>
                </div>
                <button
                  onClick={() => updateSettings({ voiceAutoSend: !settings.voiceAutoSend })}
                  className={`flex-shrink-0 w-11 sm:w-12 h-6 rounded-full transition-colors touch-target ${settings.voiceAutoSend ? 'bg-cyan-600' : 'bg-zinc-600'}`}
                >
                  <div className={`w-5 h-5 bg-white rounded-full transition-transform ${settings.voiceAutoSend ? 'translate-x-5 sm:translate-x-6' : 'translate-x-0.5 sm:translate-x-1'}`} />
                </button>
              </div>

              <div className="flex items-center justify-between p-3 sm:p-4 bg-zinc-800 rounded-lg sm:rounded-xl">
                <div className="flex-1 pr-3">
                  <div className="font-medium text-sm sm:text-base text-white">Voice response</div>
                  <div className="text-xs sm:text-sm text-zinc-400">AI speaks responses aloud</div>
                </div>
                <button className="flex-shrink-0 w-11 sm:w-12 h-6 rounded-full bg-zinc-600 touch-target">
                  <div className="w-5 h-5 bg-white rounded-full translate-x-0.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// Text-to-Speech utility
export function speakText(text: string, voice?: SpeechSynthesisVoice) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    if (voice) {
      utterance.voice = voice;
    }
    speechSynthesis.speak(utterance);
  }
}

// Hook for available voices
export function useVoices() {
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

  useEffect(() => {
    const loadVoices = () => {
      setVoices(speechSynthesis.getVoices());
    };

    loadVoices();
    speechSynthesis.onvoiceschanged = loadVoices;

    return () => {
      speechSynthesis.onvoiceschanged = null;
    };
  }, []);

  return voices;
}

'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Mic, MicOff, Volume2, VolumeX, Settings2, X } from 'lucide-react';
import { useStore } from '@/lib/store';

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
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationRef = useRef<number | null>(null);

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
  }, [voice.isListening]);

  const startAudioVisualization = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
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
    } catch (e) {
      console.error('Failed to access microphone:', e);
    }
  };

  const stopAudioVisualization = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    setAudioLevel(0);
  };

  const toggleListening = () => {
    setVoice({ isListening: !voice.isListening, transcript: '' });
  };

  if (!settings.voiceEnabled) return null;

  return (
    <>
      {/* Floating Voice Button */}
      {voice.isListening && (
        <div className="fixed bottom-32 left-1/2 -translate-x-1/2 z-40">
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

            {/* Main button */}
            <button
              onClick={toggleListening}
              className="relative w-20 h-20 rounded-full bg-gradient-to-br from-red-500 to-pink-600 flex items-center justify-center shadow-lg shadow-red-500/30 hover:shadow-red-500/50 transition"
            >
              <Mic className="w-8 h-8 text-white" />
            </button>
          </div>

          {/* Transcript display */}
          {voice.transcript && (
            <div className="absolute top-full mt-4 left-1/2 -translate-x-1/2 w-80 p-4 bg-black/80 backdrop-blur-xl border border-cyan-500/30 rounded-xl shadow-xl shadow-cyan-500/10">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                <span className="text-xs text-cyan-300">Listening...</span>
              </div>
              <p className="text-white">{voice.transcript}</p>
            </div>
          )}
        </div>
      )}

      {/* Voice Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-zinc-900 rounded-2xl border border-zinc-800 p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-white">Voice Settings</h3>
              <button
                onClick={() => setShowSettings(false)}
                className="p-2 hover:bg-zinc-800 rounded-lg transition"
              >
                <X className="w-5 h-5 text-zinc-400" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white mb-2">Language</label>
                <select className="w-full p-3 bg-zinc-800 border border-zinc-700 rounded-xl text-white focus:outline-none focus:border-cyan-500">
                  <option value="en-US">English (US)</option>
                  <option value="en-GB">English (UK)</option>
                  <option value="en-AU">English (Australia)</option>
                </select>
              </div>

              <div className="flex items-center justify-between p-4 bg-zinc-800 rounded-xl">
                <div>
                  <div className="font-medium text-white">Auto-send on pause</div>
                  <div className="text-sm text-zinc-400">Send message when you stop speaking</div>
                </div>
                <button 
                  onClick={() => updateSettings({ voiceAutoSend: !settings.voiceAutoSend })}
                  className={`w-12 h-6 rounded-full transition-colors ${settings.voiceAutoSend ? 'bg-cyan-600' : 'bg-zinc-600'}`}
                >
                  <div className={`w-5 h-5 bg-white rounded-full transition-transform ${settings.voiceAutoSend ? 'translate-x-6' : 'translate-x-1'}`} />
                </button>
              </div>

              <div className="flex items-center justify-between p-4 bg-zinc-800 rounded-xl">
                <div>
                  <div className="font-medium text-white">Voice response</div>
                  <div className="text-sm text-zinc-400">AI speaks responses aloud</div>
                </div>
                <button className="w-12 h-6 rounded-full bg-zinc-600">
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

"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Mic, MicOff, Volume2, VolumeX } from "lucide-react"

interface WebRTCAudioProps {
  onAudioData?: (audioData: Blob) => void
  onTranscription?: (text: string) => void
  isListening?: boolean
}

export function WebRTCAudio({ onAudioData, onTranscription, isListening = false }: WebRTCAudioProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [audioLevel, setAudioLevel] = useState(0)

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const animationFrameRef = useRef<number>()

  const initializeAudio = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100,
        },
      })

      streamRef.current = stream

      // Setup audio context for visualization
      audioContextRef.current = new AudioContext()
      analyserRef.current = audioContextRef.current.createAnalyser()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      source.connect(analyserRef.current)

      // Setup media recorder
      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: "audio/webm;codecs=opus",
      })

      const audioChunks: Blob[] = []

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" })
        onAudioData?.(audioBlob)

        // Mock transcription for demo
        setTimeout(() => {
          onTranscription?.("Patient says: I've been experiencing chest pain for the past hour...")
        }, 1000)
      }

      return true
    } catch (error) {
      console.error("Failed to initialize audio:", error)
      return false
    }
  }

  const monitorAudioLevel = () => {
    if (!analyserRef.current) return

    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount)
    analyserRef.current.getByteFrequencyData(dataArray)

    const average = dataArray.reduce((a, b) => a + b) / dataArray.length
    setAudioLevel(average / 255)

    animationFrameRef.current = requestAnimationFrame(monitorAudioLevel)
  }

  const startRecording = async () => {
    const initialized = await initializeAudio()
    if (!initialized || !mediaRecorderRef.current) return

    mediaRecorderRef.current.start(100) // Collect data every 100ms
    setIsRecording(true)
    monitorAudioLevel()
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)

      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }

  const toggleMute = () => {
    if (streamRef.current) {
      streamRef.current.getAudioTracks().forEach((track) => {
        track.enabled = isMuted
      })
      setIsMuted(!isMuted)
    }
  }

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop())
      }
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [])

  return (
    <div className="flex items-center gap-3">
      <Button
        variant={isRecording ? "destructive" : "default"}
        size="sm"
        onClick={isRecording ? stopRecording : startRecording}
        className="relative"
      >
        {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
        {isRecording && <div className="absolute -inset-1 rounded-full border-2 border-destructive animate-pulse" />}
      </Button>

      {isRecording && (
        <div className="flex items-center gap-1">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className={`w-1 h-4 rounded-full transition-colors ${audioLevel > i * 0.2 ? "bg-primary" : "bg-muted"}`}
            />
          ))}
        </div>
      )}

      <Button variant="outline" size="sm" onClick={toggleMute} disabled={!isRecording}>
        {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
      </Button>

      {isListening && (
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
          AI Listening...
        </div>
      )}
    </div>
  )
}

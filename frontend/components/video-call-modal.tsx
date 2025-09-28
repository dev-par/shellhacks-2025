"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogClose,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Mic,
  MicOff,
  Video,
  VideoOff,
  Phone,
  Settings,
  Users,
  MessageSquare,
  Volume2,
  X,
} from "lucide-react";
import { VisuallyHidden } from "@radix-ui/react-visually-hidden";
import { apiClient } from "../lib/api-client";

interface VideoCallModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface TranscriptEntry {
  id: string;
  speaker: string;
  text: string;
  timestamp: string;
  agentType?: string;
}

const mockParticipants = [
  { id: "1", name: "Sarah Chen", avatar: "/placeholder-user.jpg" },
  { id: "2", name: "Marcus Johnson", avatar: "/placeholder-user.jpg" },
];

const mockTranscript: TranscriptEntry[] = [
  {
    id: "1",
    speaker: "Sarah Chen",
    text: "Good morning everyone, thanks for joining the call today.",
    timestamp: "09:00:15",
  },
  {
    id: "2",
    speaker: "Marcus Johnson",
    text: "Morning Sarah! Ready to discuss the quarterly results.",
    timestamp: "09:00:22",
  },
];

export function VideoCallModal({ isOpen, onClose }: VideoCallModalProps) {
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOff, setIsVideoOff] = useState(false);
  const [transcript, setTranscript] =
    useState<TranscriptEntry[]>(mockTranscript);
  const [isInCall, setIsInCall] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [agentResponse, setAgentResponse] = useState<string>("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentAgentType, setCurrentAgentType] = useState<
    "doctor" | "nurse" | "emergency_room_agent"
  >("emergency_room_agent");

  // Simulate real-time transcription
  useEffect(() => {
    if (!isInCall) return;

    const interval = setInterval(() => {
      const newMessages = [
        "The user engagement has increased by 23% this quarter.",
        "Our mobile app downloads are up significantly.",
        "I think we should focus on the retention metrics next.",
        "The conversion rate from the new landing page looks promising.",
        "Should we schedule a follow-up meeting for next week?",
      ];

      const speakers = ["Sarah Chen", "Marcus Johnson", "Elena Rodriguez"];
      const randomMessage =
        newMessages[Math.floor(Math.random() * newMessages.length)];
      const randomSpeaker =
        speakers[Math.floor(Math.random() * speakers.length)];

      const newEntry: TranscriptEntry = {
        id: Date.now().toString(),
        speaker: randomSpeaker,
        text: randomMessage,
        timestamp: new Date().toLocaleTimeString("en-US", {
          hour12: false,
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        }),
      };

      setTranscript((prev) => [...prev, newEntry]);
    }, 8000);

    return () => clearInterval(interval);
  }, [isInCall]);

  const handleJoinCall = () => setIsInCall(true);
  const handleEndCall = () => {
    setIsInCall(false);
    onClose();
  };

  // Agent communication functions
  const sendMessageToAgent = async (message: string) => {
    try {
      setIsProcessing(true);
      const response = await apiClient.sendMessage(message);

      if (response.status === "success") {
        setAgentResponse(response.response);

        // Add agent response to transcript
        const agentEntry: TranscriptEntry = {
          id: Date.now().toString(),
          speaker: "Emergency Room Agent",
          text: response.response,
          timestamp: new Date().toLocaleTimeString("en-US", {
            hour12: false,
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          }),
        };
        setTranscript((prev) => [...prev, agentEntry]);
      }
    } catch (error) {
      console.error("Agent communication error:", error);
      setAgentResponse("Sorry, I couldn't process that request.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSpeechToText = async () => {
    try {
      setIsListening(true);
      // TODO: Implement actual speech-to-text
      // For now, simulate with a mock message
      const mockMessage =
        "Patient is complaining of chest pain and shortness of breath";

      // Add user speech to transcript
      const userEntry: TranscriptEntry = {
        id: Date.now().toString(),
        speaker: "Trainee",
        text: mockMessage,
        timestamp: new Date().toLocaleTimeString("en-US", {
          hour12: false,
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        }),
      };
      setTranscript((prev) => [...prev, userEntry]);

      // Send to agent
      await sendMessageToAgent(mockMessage);
    } catch (error) {
      console.error("Speech-to-text error:", error);
    } finally {
      setIsListening(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-7xl w-full h-[95vh] p-0 bg-card border-border flex rounded-2xl overflow-hidden">
        {/* Main Video Area */}
        <VisuallyHidden>
          <DialogTitle>Video Call</DialogTitle>
        </VisuallyHidden>
        <div className="flex-1 flex flex-col bg-background">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                <span className="text-sm font-medium text-foreground">
                  {isInCall ? "Live Meeting" : "Ready to Join"}
                </span>
              </div>
              <Badge variant="secondary" className="text-xs">
                <Users className="w-3 h-3 mr-1" />
                {mockParticipants.length} participants
              </Badge>
            </div>

            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm">
                <Settings className="w-4 h-4" />
              </Button>
              <Button variant="ghost" size="sm">
                <MessageSquare className="w-4 h-4" />
              </Button>
              <DialogClose asChild>
                <Button variant="ghost" size="icon">
                  <X className="w-4 h-4" />
                </Button>
              </DialogClose>
            </div>
          </div>

          {/* Video Grid */}
          <div className="flex-1 p-6 flex items-center justify-center">
            {!isInCall ? (
              <div className="text-center space-y-6">
                <div className="w-24 h-24 bg-muted rounded-full flex items-center justify-center mx-auto">
                  <Video className="w-12 h-12 text-muted-foreground" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-foreground">
                    Ready to join?
                  </h3>
                  <p className="text-muted-foreground">
                    Click join to start your video conference with real-time
                    transcription
                  </p>
                </div>
                <Button
                  onClick={handleJoinCall}
                  size="lg"
                  className="bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  Join Call
                </Button>
              </div>
            ) : (
              <div className="w-full h-full grid grid-cols-1 grid-rows-2 gap-4">
                {mockParticipants.slice(0, 2).map((p) => (
                  <div
                    key={p.id}
                    className="aspect-square bg-muted rounded-lg relative overflow-hidden border border-black/10 border-2"
                  >
                    <img
                      src={p.avatar}
                      alt={p.name}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute bottom-2 left-2 bg-black/70 text-white px-2 py-1 rounded text-xs">
                      {p.name}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Controls */}
          {isInCall && (
            <div className="p-4 border-t border-border bg-card">
              <div className="flex items-center justify-center gap-4">
                <Button
                  variant={isListening ? "destructive" : "secondary"}
                  size="lg"
                  onClick={handleSpeechToText}
                  disabled={isProcessing}
                  className="rounded-full w-12 h-12"
                >
                  {isListening ? (
                    <MicOff className="w-5 h-5" />
                  ) : (
                    <Mic className="w-5 h-5" />
                  )}
                </Button>

                <Button
                  variant={isVideoOff ? "destructive" : "secondary"}
                  size="lg"
                  onClick={() => setIsVideoOff(!isVideoOff)}
                  className="rounded-full w-12 h-12"
                >
                  {isVideoOff ? (
                    <VideoOff className="w-5 h-5" />
                  ) : (
                    <Video className="w-5 h-5" />
                  )}
                </Button>

                <Button
                  variant="destructive"
                  size="lg"
                  onClick={handleEndCall}
                  className="rounded-full w-12 h-12"
                >
                  <Phone className="w-5 h-5" />
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Transcription Sidebar */}
        <div className="w-80 bg-card border-l border-border flex flex-col">
          <div className="p-4 border-b border-border">
            <div className="flex items-center gap-2">
              <Volume2 className="w-5 h-5 text-primary" />
              <h3 className="font-semibold text-foreground">
                Live Transcription
              </h3>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Real-time speech-to-text
            </p>
          </div>

          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {transcript.map((entry) => (
                <div key={entry.id} className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-primary">
                      {entry.speaker}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {entry.timestamp}
                    </span>
                  </div>
                  <p className="text-sm text-foreground leading-relaxed">
                    {entry.text}
                  </p>
                </div>
              ))}

              {isInCall && (
                <div className="space-y-2">
                  {isListening && (
                    <div className="flex items-center gap-2 text-primary">
                      <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
                      <span className="text-xs">Listening...</span>
                    </div>
                  )}
                  {isProcessing && (
                    <div className="flex items-center gap-2 text-blue-500">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                      <span className="text-xs">Agent processing...</span>
                    </div>
                  )}
                  {agentResponse && (
                    <div className="p-2 bg-blue-50 rounded text-xs text-blue-700">
                      <strong>Agent:</strong> {agentResponse}
                    </div>
                  )}
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="p-4 border-t border-border">
            <div className="text-xs text-muted-foreground text-center">
              Transcription powered by AI
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

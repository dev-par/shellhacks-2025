"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Header } from "@/components/header";
import { AnimatedBackground } from "@/components/animated-background";
import { WebRTCAudio } from "@/components/webrtc-audio";
import {
  Send,
  ArrowLeft,
  Clock,
  User,
  Stethoscope,
  Heart,
  Thermometer,
  Activity,
  CheckCircle,
  Volume2,
  VolumeX,
} from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

interface Message {
  id: string;
  type: "user" | "patient" | "system";
  content: string;
  timestamp: Date;
  audioUrl?: string;
}

interface PatientData {
  name: string;
  age: number;
  gender: string;
  chiefComplaint: string;
  vitals: {
    heartRate: number;
    bloodPressure: string;
    temperature: number;
    respiratoryRate: number;
    oxygenSaturation: number;
  };
  allergies: string[];
  medications: string[];
  medicalHistory: string[];
}

const scenarioData = {
  "emergency-triage": {
    1: {
      title: "Multi-Vehicle Accident Victims",
      description: "Triage multiple trauma patients from a highway accident",
      duration: 8,
      patient: {
        name: "Sarah Johnson",
        age: 34,
        gender: "Female",
        chiefComplaint:
          "Motor vehicle accident with chest pain and difficulty breathing",
        vitals: {
          heartRate: 110,
          bloodPressure: "90/60",
          temperature: 98.2,
          respiratoryRate: 24,
          oxygenSaturation: 92,
        },
        allergies: ["Penicillin"],
        medications: ["Birth control pills"],
        medicalHistory: ["Asthma", "Previous appendectomy"],
      },
      initialMessage:
        "Doctor, I was in a car accident about 30 minutes ago. My chest really hurts and I'm having trouble breathing. The airbag hit me pretty hard.",
    },
  },
};

function SimulationContent() {
  const params = useParams();
  const moduleId = params.moduleId as string;
  const scenarioId = Number.parseInt(params.scenarioId as string);

  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [isActive, setIsActive] = useState(true);
  const [currentPhase, setCurrentPhase] = useState<
    "assessment" | "diagnosis" | "treatment"
  >("assessment");
  const [audioEnabled, setAudioEnabled] = useState(true);
  const [isListening, setIsListening] = useState(false);
  const [lastTranscription, setLastTranscription] = useState("");

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<NodeJS.Timeout>();

  // Use a safe any-cast to index into scenarioData to avoid complex TS index typing for numeric keys
  const scenario = (scenarioData as any)[moduleId]?.[String(scenarioId)];

  useEffect(() => {
    if (scenario && messages.length === 0) {
      const initialMessage: Message = {
        id: "1",
        type: "patient",
        content: scenario.initialMessage,
        timestamp: new Date(),
      };
      setMessages([initialMessage]);
    }
  }, [scenario]);

  useEffect(() => {
    if (isActive) {
      timerRef.current = setInterval(() => {
        setTimeElapsed((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isActive]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAudioData = async (audioBlob: Blob) => {
    console.log("[v0] Received audio data:", audioBlob.size, "bytes");
    setIsSpeaking(true);
    setTimeout(() => {
      setIsSpeaking(false);
    }, 2000);
  };

  const handleTranscription = (text: string) => {
    console.log("[v0] Received transcription:", text);
    setLastTranscription(text);
    setIsListening(false);
    setInputMessage(text);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setLastTranscription("");

    setTimeout(() => {
      const responses = [
        "The pain is getting worse, especially when I try to take a deep breath. It feels like something is pressing on my chest.",
        "I think I hit my head too, but I'm more worried about my breathing. Should I be concerned?",
        "The paramedics gave me some oxygen in the ambulance, but I still feel short of breath.",
        "I have asthma, and this feels different from my usual attacks. Much more painful.",
        "My chest hurts right here [points to left side]. It's a sharp, stabbing pain.",
        "Doctor, I'm getting dizzy now. Is that normal? The pain is really intense.",
        "I can't seem to catch my breath properly. It's scaring me.",
      ];

      const randomResponse =
        responses[Math.floor(Math.random() * responses.length)];

      const patientMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "patient",
        content: randomResponse,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, patientMessage]);

      if (audioEnabled) {
        setIsSpeaking(true);
        setTimeout(() => setIsSpeaking(false), 3000);
      }
    }, 1500);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  const progress = scenario
    ? (timeElapsed / (scenario.duration * 60)) * 100
    : 0;

  if (!scenario) {
    return (
      <div className="min-h-screen bg-background relative">
        <AnimatedBackground />
        <div className="relative z-10">
          <Header />
          <div className="container mx-auto px-4 py-20">
            <div className="max-w-md mx-auto text-center">
              <h1 className="text-2xl font-bold mb-4">Scenario Not Found</h1>
              <Link href="/modules">
                <Button className="text-black">Back to Modules</Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background relative">
      <AnimatedBackground />
      <div className="relative z-10">
        <Header />

        <div className="border-b border-border bg-card">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Link
                  href={`/modules/${moduleId}`}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <ArrowLeft className="w-5 h-5" />
                </Link>
                <div>
                  <h1 className="text-xl font-semibold">{scenario.title}</h1>
                  <p className="text-sm text-muted-foreground">
                    {scenario.description}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm font-mono">
                    {formatTime(timeElapsed)}
                  </span>
                </div>
                <div className="w-32">
                  <Progress value={progress} className="h-2" />
                </div>
                <Badge
                  variant={
                    currentPhase === "assessment" ? "default" : "secondary"
                  }
                >
                  {currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}
                </Badge>
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-4 py-6">
          <div className="grid lg:grid-cols-4 gap-6 h-[calc(100vh-200px)]">
            <div className="lg:col-span-1">
              <Card className="h-full">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <User className="w-5 h-5 mr-2" />
                    Patient Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-medium">{scenario.patient.name}</h4>
                    <p className="text-sm text-muted-foreground">
                      {scenario.patient.age} years old,{" "}
                      {scenario.patient.gender}
                    </p>
                  </div>

                  <div>
                    <h5 className="font-medium text-sm mb-2">
                      Chief Complaint
                    </h5>
                    <p className="text-sm text-muted-foreground">
                      {scenario.patient.chiefComplaint}
                    </p>
                  </div>

                  <div>
                    <h5 className="font-medium text-sm mb-2 flex items-center">
                      <Activity className="w-4 h-4 mr-1" />
                      Vital Signs
                    </h5>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="flex items-center">
                          <Heart className="w-3 h-3 mr-1 text-red-500" />
                          HR:
                        </span>
                        <span>{scenario.patient.vitals.heartRate} bpm</span>
                      </div>
                      <div className="flex justify-between">
                        <span>BP:</span>
                        <span>
                          {scenario.patient.vitals.bloodPressure} mmHg
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="flex items-center">
                          <Thermometer className="w-3 h-3 mr-1 text-blue-500" />
                          Temp:
                        </span>
                        <span>{scenario.patient.vitals.temperature}°F</span>
                      </div>
                      <div className="flex justify-between">
                        <span>RR:</span>
                        <span>
                          {scenario.patient.vitals.respiratoryRate}/min
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>O2 Sat:</span>
                        <span className="text-yellow-600">
                          {scenario.patient.vitals.oxygenSaturation}%
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h5 className="font-medium text-sm mb-2">Allergies</h5>
                    <div className="flex flex-wrap gap-1">
                      {scenario.patient.allergies.map(
                        (allergy: string, idx: number) => (
                          <Badge
                            key={`allergy-${idx}`}
                            variant="destructive"
                            className="text-xs"
                          >
                            {allergy}
                          </Badge>
                        )
                      )}
                    </div>
                  </div>

                  <div>
                    <h5 className="font-medium text-sm mb-2">
                      Current Medications
                    </h5>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {scenario.patient.medications.map(
                        (med: string, idx: number) => (
                          <li key={`med-${idx}`}>• {med}</li>
                        )
                      )}
                    </ul>
                  </div>

                  <div>
                    <h5 className="font-medium text-sm mb-2">
                      Medical History
                    </h5>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {scenario.patient.medicalHistory.map(
                        (history: string, idx: number) => (
                          <li key={`history-${idx}`}>• {history}</li>
                        )
                      )}
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="lg:col-span-3">
              <Card className="h-full flex flex-col">
                <CardHeader className="flex-shrink-0">
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center">
                      <Stethoscope className="w-5 h-5 mr-2" />
                      Patient Interaction
                    </CardTitle>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setAudioEnabled(!audioEnabled)}
                      >
                        {audioEnabled ? (
                          <Volume2 className="w-4 h-4" />
                        ) : (
                          <VolumeX className="w-4 h-4" />
                        )}
                      </Button>
                      {isSpeaking && (
                        <Badge variant="secondary" className="animate-pulse">
                          Patient Speaking...
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="flex-1 flex flex-col">
                  <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                    {messages.map((message) => (
                      <div
                        key={message.id}
                        className={`flex ${
                          message.type === "user"
                            ? "justify-end"
                            : "justify-start"
                        }`}
                      >
                        <div
                          className={`max-w-[80%] rounded-lg px-4 py-2 ${
                            message.type === "user"
                              ? "bg-primary text-primary-foreground"
                              : message.type === "patient"
                              ? "bg-muted"
                              : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
                          }`}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-medium">
                              {message.type === "user"
                                ? "You"
                                : message.type === "patient"
                                ? scenario.patient.name
                                : "System"}
                            </span>
                            <span className="text-xs opacity-70">
                              {message.timestamp.toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                            </span>
                          </div>
                          <p className="text-sm">{message.content}</p>
                        </div>
                      </div>
                    ))}
                    <div ref={messagesEndRef} />
                  </div>

                  <div className="flex-shrink-0 border-t border-border pt-4">
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 relative">
                        <Input
                          value={inputMessage}
                          onChange={(e) => setInputMessage(e.target.value)}
                          placeholder="Type your response or question..."
                          onKeyPress={(e) =>
                            e.key === "Enter" && handleSendMessage()
                          }
                          className="pr-12"
                        />
                        <Button
                          size="sm"
                          className="absolute right-1 top-1 h-8 w-8 p-0"
                          onClick={handleSendMessage}
                          disabled={!inputMessage.trim()}
                        >
                          <Send className="w-4 h-4" />
                        </Button>
                      </div>

                      <WebRTCAudio
                        onAudioData={handleAudioData}
                        onTranscription={handleTranscription}
                        isListening={isListening}
                      />
                    </div>

                    <div className="flex items-center justify-between mt-3 text-xs text-muted-foreground">
                      <span>
                        {lastTranscription
                          ? `Transcribed: "${lastTranscription.substring(
                              0,
                              50
                            )}..."`
                          : "Use voice input or type your message"}
                      </span>
                      <div className="flex items-center space-x-4">
                        <span className="flex items-center">
                          <CheckCircle className="w-3 h-3 mr-1 text-success" />
                          Assessment Phase
                        </span>
                        <span>Next: Diagnosis</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function SimulationPage() {
  return <SimulationContent />;
}

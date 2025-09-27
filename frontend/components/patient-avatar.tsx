"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { User, Activity, AlertTriangle } from "lucide-react"

interface PatientAvatarProps {
  name: string
  age: number
  gender: string
  isActive: boolean
  isSpeaking: boolean
  emotionalState: "calm" | "anxious" | "pain" | "distressed"
  vitals: {
    heartRate: number
    oxygenSaturation: number
  }
}

export function PatientAvatar({ name, age, gender, isActive, isSpeaking, emotionalState, vitals }: PatientAvatarProps) {
  const [pulseAnimation, setPulseAnimation] = useState(false)

  useEffect(() => {
    if (isSpeaking) {
      setPulseAnimation(true)
      const timer = setTimeout(() => setPulseAnimation(false), 2000)
      return () => clearTimeout(timer)
    }
  }, [isSpeaking])

  const getEmotionalStateColor = () => {
    switch (emotionalState) {
      case "calm":
        return "bg-green-100 border-green-300"
      case "anxious":
        return "bg-yellow-100 border-yellow-300"
      case "pain":
        return "bg-orange-100 border-orange-300"
      case "distressed":
        return "bg-red-100 border-red-300"
      default:
        return "bg-gray-100 border-gray-300"
    }
  }

  const getVitalStatus = () => {
    const hrNormal = vitals.heartRate >= 60 && vitals.heartRate <= 100
    const o2Normal = vitals.oxygenSaturation >= 95

    if (!hrNormal || !o2Normal) return "critical"
    return "stable"
  }

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <div className="flex items-center space-x-4">
          {/* Avatar */}
          <div
            className={`relative w-16 h-16 rounded-full border-2 ${getEmotionalStateColor()} ${
              pulseAnimation ? "animate-pulse" : ""
            } ${isSpeaking ? "ring-2 ring-primary ring-offset-2" : ""}`}
          >
            <div className="w-full h-full rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
              <User className="w-8 h-8 text-white" />
            </div>

            {/* Speaking indicator */}
            {isSpeaking && (
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-primary rounded-full flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
              </div>
            )}

            {/* Activity indicator */}
            <div
              className={`absolute -top-1 -right-1 w-4 h-4 rounded-full ${isActive ? "bg-green-500" : "bg-gray-400"}`}
            >
              <Activity className="w-3 h-3 text-white m-0.5" />
            </div>
          </div>

          {/* Patient Info */}
          <div className="flex-1">
            <h3 className="font-semibold text-lg">{name}</h3>
            <p className="text-muted-foreground">
              {age} years old, {gender}
            </p>

            <div className="flex items-center space-x-2 mt-2">
              <Badge variant={emotionalState === "calm" ? "secondary" : "destructive"}>
                {emotionalState.charAt(0).toUpperCase() + emotionalState.slice(1)}
              </Badge>

              <Badge variant={getVitalStatus() === "stable" ? "secondary" : "destructive"}>
                {getVitalStatus() === "stable" ? "Stable" : "Critical"}
              </Badge>

              {getVitalStatus() === "critical" && <AlertTriangle className="w-4 h-4 text-destructive" />}
            </div>
          </div>
        </div>

        {/* Quick Vitals */}
        <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Heart Rate:</span>
            <span className={vitals.heartRate > 100 || vitals.heartRate < 60 ? "text-destructive font-medium" : ""}>
              {vitals.heartRate} bpm
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">O2 Sat:</span>
            <span className={vitals.oxygenSaturation < 95 ? "text-destructive font-medium" : ""}>
              {vitals.oxygenSaturation}%
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

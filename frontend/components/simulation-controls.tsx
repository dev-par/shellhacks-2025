"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Play, Pause, Square, RotateCcw, Settings, HelpCircle, AlertTriangle } from "lucide-react"

interface SimulationControlsProps {
  isActive: boolean
  onToggleActive: () => void
  onReset: () => void
  onEndSimulation: () => void
  timeElapsed: number
  maxDuration: number
  currentPhase: "assessment" | "diagnosis" | "treatment"
  onPhaseChange: (phase: "assessment" | "diagnosis" | "treatment") => void
}

export function SimulationControls({
  isActive,
  onToggleActive,
  onReset,
  onEndSimulation,
  timeElapsed,
  maxDuration,
  currentPhase,
  onPhaseChange,
}: SimulationControlsProps) {
  const [showHelp, setShowHelp] = useState(false)

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  const progress = (timeElapsed / (maxDuration * 60)) * 100
  const isOvertime = timeElapsed > maxDuration * 60

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center">
            <Settings className="w-5 h-5 mr-2" />
            Simulation Controls
          </span>
          <Button variant="ghost" size="sm" onClick={() => setShowHelp(!showHelp)}>
            <HelpCircle className="w-4 h-4" />
          </Button>
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Timer and Progress */}
        <div className="text-center">
          <div className={`text-2xl font-mono font-bold ${isOvertime ? "text-destructive" : ""}`}>
            {formatTime(timeElapsed)}
          </div>
          <div className="text-sm text-muted-foreground">Target: {formatTime(maxDuration * 60)}</div>
          <div className="w-full bg-muted rounded-full h-2 mt-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${isOvertime ? "bg-destructive" : "bg-primary"}`}
              style={{ width: `${Math.min(progress, 100)}%` }}
            />
          </div>
        </div>

        {/* Phase Indicators */}
        <div className="space-y-2">
          <div className="text-sm font-medium">Current Phase:</div>
          <div className="flex space-x-2">
            {(["assessment", "diagnosis", "treatment"] as const).map((phase) => (
              <Badge
                key={phase}
                variant={currentPhase === phase ? "default" : "secondary"}
                className="cursor-pointer"
                onClick={() => onPhaseChange(phase)}
              >
                {phase.charAt(0).toUpperCase() + phase.slice(1)}
              </Badge>
            ))}
          </div>
        </div>

        {/* Control Buttons */}
        <div className="flex space-x-2">
          <Button variant={isActive ? "destructive" : "default"} size="sm" onClick={onToggleActive} className="flex-1">
            {isActive ? (
              <>
                <Pause className="w-4 h-4 mr-2" />
                Pause
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Resume
              </>
            )}
          </Button>

          <Button variant="outline" size="sm" onClick={onReset}>
            <RotateCcw className="w-4 h-4" />
          </Button>

          <Button variant="destructive" size="sm" onClick={onEndSimulation}>
            <Square className="w-4 h-4" />
          </Button>
        </div>

        {/* Status Indicators */}
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span>Status:</span>
            <Badge variant={isActive ? "default" : "secondary"}>{isActive ? "Active" : "Paused"}</Badge>
          </div>

          {isOvertime && (
            <div className="flex items-center text-destructive">
              <AlertTriangle className="w-4 h-4 mr-2" />
              <span>Simulation overtime</span>
            </div>
          )}
        </div>

        {/* Help Panel */}
        {showHelp && (
          <div className="border-t border-border pt-4 space-y-2 text-sm">
            <div className="font-medium">Quick Tips:</div>
            <ul className="space-y-1 text-muted-foreground">
              <li>• Use voice or text to interact with the patient</li>
              <li>• Check vital signs and patient history in the left panel</li>
              <li>• Progress through Assessment → Diagnosis → Treatment</li>
              <li>• Ask open-ended questions to gather information</li>
              <li>• Consider differential diagnoses based on symptoms</li>
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

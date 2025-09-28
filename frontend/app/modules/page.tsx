"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Header } from "@/components/header"
import { Play, Lock } from "lucide-react"
import Link from "next/link"

const trainingModules = [
  {
    id: "emergency-triage",
    title: "Emergency Department Triage",
    description:
      "Learn to quickly assess and prioritize patients in emergency situations using standardized triage protocols.",
    category: "Emergency Medicine",
    context:
      "You are working in a busy emergency department when multiple patients arrive simultaneously. Practice making rapid triage decisions to prioritize care based on severity and available resources.",
    isLocked: false,
  },
  {
    id: "patient-communication",
    title: "Difficult Patient Conversations",
    description:
      "Master the art of communicating with challenging patients and delivering difficult news with empathy.",
    category: "Communication",
    context:
      "Navigate complex conversations with patients who are anxious, angry, or receiving difficult diagnoses. Practice maintaining professionalism while showing compassion.",
    isLocked: false,
  },
  {
    id: "diagnostic-reasoning",
    title: "Clinical Diagnostic Reasoning",
    description: "Develop systematic approaches to differential diagnosis and clinical decision-making.",
    category: "Diagnostics",
    context:
      "Work through complex cases where symptoms could indicate multiple conditions. Practice systematic diagnostic thinking and evidence-based decision making.",
    isLocked: false,
  },
  {
    id: "pediatric-care",
    title: "Pediatric Patient Care",
    description: "Specialized training for treating young patients and communicating with families.",
    category: "Pediatrics",
    context:
      "Treat pediatric patients while managing both the child's needs and parental concerns. Practice age-appropriate communication and examination techniques.",
    isLocked: true,
  },
  {
    id: "surgical-consultation",
    title: "Pre-Surgical Consultations",
    description: "Learn to conduct thorough pre-operative assessments and patient consultations.",
    category: "Surgery",
    context:
      "Conduct comprehensive pre-surgical evaluations, explain procedures to patients, and assess surgical risks while addressing patient concerns.",
    isLocked: true,
  },
  {
    id: "mental-health",
    title: "Mental Health Screening",
    description: "Develop skills in identifying and addressing mental health concerns in primary care.",
    category: "Mental Health",
    context:
      "Screen patients for mental health conditions during routine visits. Practice sensitive questioning techniques and appropriate referral decisions.",
    isLocked: true,
  },
]

export default function ModulesPage() {
  const [selectedCategory, setSelectedCategory] = useState("All")

  const categories = [
    "All",
    "Emergency Medicine",
    "Communication",
    "Diagnostics",
    "Pediatrics",
    "Surgery",
    "Mental Health",
  ]

  const filteredModules =
    selectedCategory === "All"
      ? trainingModules
      : trainingModules.filter((module) => module.category === selectedCategory)

  return (
    <div className="min-h-screen relative">
      <Header />

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2 gradient-text">Training Modules</h1>
          <p className="text-muted-foreground">
            Choose from our comprehensive library of medical simulation training modules
          </p>
        </div>

        <div className="flex flex-wrap gap-2 mb-8">
          {categories.map((category) => (
            <Button
              key={category}
              variant={selectedCategory === category ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCategory(category)}
              className={
                selectedCategory === category
                  ? "bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700 hover:from-blue-600 hover:via-purple-700 hover:to-blue-800"
                  : "backdrop-blur-sm border-primary/30"
              }
            >
              {category}
            </Button>
          ))}
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredModules.map((module) => (
            <Card key={module.id} className="backdrop-blur-sm bg-card/80 border-border/30">
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="secondary" className="backdrop-blur-sm">
                    {module.category}
                  </Badge>
                  {module.isLocked && <Lock className="w-4 h-4 text-muted-foreground" />}
                </div>
                <CardTitle className="text-lg gradient-text-alt">{module.title}</CardTitle>
                <p className="text-sm text-muted-foreground mb-3">{module.description}</p>
                <div className="bg-muted/30 p-3 rounded-md backdrop-blur-sm">
                  <p className="text-xs text-muted-foreground font-medium mb-1">Training Context:</p>
                  <p className="text-xs text-foreground/80">{module.context}</p>
                </div>
              </CardHeader>

              <CardContent>
                <Link href={module.isLocked ? "#" : `/modules/${module.id}`}>
                  <Button
                    className={
                      module.isLocked
                        ? "w-full"
                        : "w-full bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700 hover:from-blue-600 hover:via-purple-700 hover:to-blue-800"
                    }
                    disabled={module.isLocked}
                  >
                    {module.isLocked ? (
                      <>
                        <Lock className="w-4 h-4 mr-2" />
                        Upgrade to Access
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4 mr-2" />
                        Start Training
                      </>
                    )}
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}

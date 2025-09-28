"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Header } from "@/components/header"
import { AnimatedBackground } from "@/components/animated-background"
import { Play, ArrowLeft, CheckCircle, Lock } from "lucide-react"
import Link from "next/link"
import { useParams } from "next/navigation"

const moduleData = {
  "emergency-triage": {
    id: "emergency-triage",
    title: "Emergency Department Triage",
    description:
      "Master the critical skills of emergency department triage through realistic patient scenarios. Learn to quickly assess patient conditions, prioritize care based on severity, and make life-saving decisions under pressure.",
    category: "Emergency Medicine",
    context:
      "You are working in a busy emergency department when multiple patients arrive simultaneously. Practice making rapid triage decisions to prioritize care based on severity and available resources.",
    objectives: [
      "Understand triage protocols and priority levels",
      "Assess patient vital signs and symptoms quickly",
      "Make critical decisions under time pressure",
      "Communicate effectively with medical team",
      "Document triage decisions accurately",
    ],
    scenario: {
      title: "Multi-Patient Emergency Triage",
      description:
        "Multiple patients have arrived at the emergency department simultaneously following a multi-vehicle accident. You must quickly assess each patient and determine treatment priority.",
      briefing:
        "A highway accident has resulted in 6 patients arriving within minutes of each other. Resources are limited and you must make rapid triage decisions to ensure the most critical patients receive immediate care.",
    },
  },
  "patient-communication": {
    id: "patient-communication",
    title: "Difficult Patient Conversations",
    description:
      "Master the art of communicating with challenging patients and delivering difficult news with empathy.",
    category: "Communication",
    context:
      "Navigate complex conversations with patients who are anxious, angry, or receiving difficult diagnoses. Practice maintaining professionalism while showing compassion.",
    objectives: [
      "Practice active listening techniques",
      "Deliver difficult news with empathy",
      "De-escalate tense situations",
      "Maintain professional boundaries",
      "Provide emotional support appropriately",
    ],
    scenario: {
      title: "Breaking Bad News",
      description:
        "You must inform a patient about a serious diagnosis while managing their emotional response and providing appropriate support.",
      briefing:
        "A 45-year-old patient has returned for test results. The diagnosis is serious and will significantly impact their life. Practice delivering this news with compassion while addressing their concerns.",
    },
  },
  "diagnostic-reasoning": {
    id: "diagnostic-reasoning",
    title: "Clinical Diagnostic Reasoning",
    description: "Develop systematic approaches to differential diagnosis and clinical decision-making.",
    category: "Diagnostics",
    context:
      "Work through complex cases where symptoms could indicate multiple conditions. Practice systematic diagnostic thinking and evidence-based decision making.",
    objectives: [
      "Apply systematic diagnostic reasoning",
      "Generate appropriate differential diagnoses",
      "Order relevant diagnostic tests",
      "Interpret clinical findings accurately",
      "Make evidence-based treatment decisions",
    ],
    scenario: {
      title: "Complex Diagnostic Challenge",
      description:
        "A patient presents with multiple symptoms that could indicate several different conditions. Use systematic diagnostic reasoning to reach the correct diagnosis.",
      briefing:
        "A 38-year-old patient presents with fatigue, joint pain, and skin changes. Multiple conditions could explain these symptoms. Work through a systematic diagnostic approach.",
    },
  },
}

function ModuleDetailContent() {
  const params = useParams()
  const moduleId = params.id as string
  const module = moduleData[moduleId as keyof typeof moduleData]

  if (!module) {
    return (
      <div className="min-h-screen relative">
        <AnimatedBackground />
        <div className="relative z-10">
          <Header />
          <div className="container mx-auto px-4 py-20">
            <div className="max-w-md mx-auto text-center">
              <h1 className="text-2xl font-bold mb-4">Module Not Found</h1>
              <p className="text-muted-foreground mb-6">The requested training module could not be found.</p>
              <Link href="/modules">
                <Button>Back to Modules</Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen relative">
      <AnimatedBackground />
      <div className="relative z-10">
        <Header />

        <div className="container mx-auto px-4 py-8">
          <div className="mb-6">
            <Link href="/modules" className="inline-flex items-center text-muted-foreground hover:text-foreground mb-4">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Modules
            </Link>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              <div className="mb-6">
                <div className="flex items-center gap-4 mb-4">
                  <Badge variant="secondary" className="backdrop-blur-sm">
                    {module.category}
                  </Badge>
                </div>

                <h1 className="text-3xl font-bold mb-4">{module.title}</h1>
                <p className="text-muted-foreground text-lg leading-relaxed mb-6">{module.description}</p>

                <Card className="mb-6 backdrop-blur-sm bg-card/80 border-border/50">
                  <CardHeader>
                    <CardTitle>Training Context</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-foreground/90">{module.context}</p>
                  </CardContent>
                </Card>
              </div>

              {/* Learning Objectives */}
              <Card className="mb-6 backdrop-blur-sm bg-card/80 border-border/50">
                <CardHeader>
                  <CardTitle>Learning Objectives</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {module.objectives.map((objective, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="w-5 h-5 text-success mr-3 mt-0.5 flex-shrink-0" />
                        <span>{objective}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-sm bg-card/80 border-border/50">
                <CardHeader>
                  <CardTitle>Training Scenario</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 border border-border/50 rounded-lg backdrop-blur-sm">
                      <h4 className="font-medium mb-2">{module.scenario.title}</h4>
                      <p className="text-sm text-muted-foreground mb-3">{module.scenario.description}</p>
                      <div className="bg-muted/30 p-3 rounded-md backdrop-blur-sm">
                        <p className="text-xs font-medium text-foreground/80 mb-1">Scenario Briefing:</p>
                        <p className="text-xs text-foreground/70">{module.scenario.briefing}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <Card className="sticky top-8 backdrop-blur-sm bg-card/80 border-border/50">
                <CardHeader>
                  <CardTitle>Start Training</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm text-muted-foreground">
                    Ready to begin your medical simulation training? Click below to start the interactive scenario.
                  </p>

                  <Link href={`/simulation/${moduleId}/1`}>
                    <Button className="w-full" size="lg">
                      <Play className="w-4 h-4 mr-2" />
                      Begin Training
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function ModuleDetailPage() {
  return (
      <ModuleDetailContent />
  )
}

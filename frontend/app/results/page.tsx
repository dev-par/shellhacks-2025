"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Header } from "@/components/header"
import { AuthProvider, useAuth } from "@/components/auth-context"
import { AnimatedBackground } from "@/components/animated-background"
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts"
import { Trophy, Clock, Target, TrendingUp, Calendar, Award, Star, Activity, Lock } from "lucide-react"
import Link from "next/link"

const performanceData = [
  { month: "Jan", score: 78 },
  { month: "Feb", score: 82 },
  { month: "Mar", score: 85 },
  { month: "Apr", score: 88 },
  { month: "May", score: 92 },
  { month: "Jun", score: 95 },
]

const categoryData = [
  { name: "Emergency Medicine", score: 95, color: "#10b981" },
  { name: "Communication", score: 88, color: "#3b82f6" },
  { name: "Diagnostics", score: 92, color: "#8b5cf6" },
  { name: "Patient Care", score: 85, color: "#f59e0b" },
]

const recentSessions = [
  {
    id: 1,
    module: "Emergency Department Triage",
    date: "2025-01-15",
    duration: "12:34",
    score: 95,
    status: "completed",
  },
  {
    id: 2,
    module: "Difficult Patient Conversations",
    date: "2025-01-14",
    duration: "18:22",
    score: 88,
    status: "completed",
  },
  {
    id: 3,
    module: "Clinical Diagnostic Reasoning",
    date: "2025-01-12",
    duration: "25:15",
    score: 92,
    status: "completed",
  },
]

function ResultsContent() {
  const { user } = useAuth()
  const [selectedPeriod, setSelectedPeriod] = useState("6months")

  if (!user) {
    return (
      <div className="min-h-screen bg-background relative">
        <AnimatedBackground />
        <div className="relative z-10">
          <Header />
          <div className="container mx-auto px-4 py-20">
            <div className="max-w-md mx-auto text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <Lock className="w-8 h-8 text-primary" />
              </div>
              <h1 className="text-2xl font-bold mb-4">Authentication Required</h1>
              <p className="text-muted-foreground mb-6">Please sign in to view your training results and analytics.</p>
              <Link href="/login">
                <Button size="lg">Sign In to Continue</Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background relative">
      <AnimatedBackground />
      <div className="relative z-10">
        <Header />

        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Training Results & Analytics</h1>
            <p className="text-muted-foreground">
              Track your progress and performance across all medical training modules
            </p>
          </div>

          {/* Period Filter */}
          <div className="flex gap-2 mb-8">
            {[
              { key: "1month", label: "Last Month" },
              { key: "3months", label: "3 Months" },
              { key: "6months", label: "6 Months" },
              { key: "1year", label: "1 Year" },
            ].map((period) => (
              <Button
                key={period.key}
                variant={selectedPeriod === period.key ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedPeriod(period.key)}
              >
                {period.label}
              </Button>
            ))}
          </div>

          {/* Stats Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Overall Score</p>
                    <p className="text-2xl font-bold text-primary">92%</p>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                    <Trophy className="w-6 h-6 text-primary" />
                  </div>
                </div>
                <div className="mt-4">
                  <Progress value={92} className="h-2" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Training Hours</p>
                    <p className="text-2xl font-bold">24.5h</p>
                  </div>
                  <div className="w-12 h-12 bg-medical-accent/10 rounded-lg flex items-center justify-center">
                    <Clock className="w-6 h-6 text-medical-accent" />
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-2">+2.3h this week</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Modules Completed</p>
                    <p className="text-2xl font-bold">12</p>
                  </div>
                  <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center">
                    <Target className="w-6 h-6 text-success" />
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-2">3 this month</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Improvement</p>
                    <p className="text-2xl font-bold text-success">+15%</p>
                  </div>
                  <div className="w-12 h-12 bg-chart-5/10 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-chart-5" />
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-2">Since last month</p>
              </CardContent>
            </Card>
          </div>

          <div className="grid lg:grid-cols-2 gap-8 mb-8">
            {/* Performance Trend */}
            <Card>
              <CardHeader>
                <CardTitle>Performance Trend</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis domain={[70, 100]} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="score"
                      stroke="hsl(var(--primary))"
                      strokeWidth={3}
                      dot={{ fill: "hsl(var(--primary))", strokeWidth: 2, r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Category Performance */}
            <Card>
              <CardHeader>
                <CardTitle>Performance by Category</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {categoryData.map((category, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium">{category.name}</span>
                        <span className="text-sm text-muted-foreground">{category.score}%</span>
                      </div>
                      <Progress value={category.score} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Sessions */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Activity className="w-5 h-5 mr-2" />
                Recent Training Sessions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentSessions.map((session) => (
                  <div
                    key={session.id}
                    className="flex items-center justify-between p-4 border border-border rounded-lg"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                        <Award className="w-5 h-5 text-primary" />
                      </div>
                      <div>
                        <h4 className="font-medium">{session.module}</h4>
                        <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                          <span className="flex items-center">
                            <Calendar className="w-3 h-3 mr-1" />
                            {new Date(session.date).toLocaleDateString()}
                          </span>
                          <span className="flex items-center">
                            <Clock className="w-3 h-3 mr-1" />
                            {session.duration}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Badge
                        variant={session.score >= 90 ? "default" : session.score >= 80 ? "secondary" : "outline"}
                        className="flex items-center"
                      >
                        <Star className="w-3 h-3 mr-1" />
                        {session.score}%
                      </Badge>
                      <Badge variant="outline" className="capitalize">
                        {session.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Achievements */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Trophy className="w-5 h-5 mr-2" />
                Achievements & Milestones
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="flex items-center space-x-3 p-4 border border-border rounded-lg">
                  <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                    <Trophy className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="font-medium">First Perfect Score</h4>
                    <p className="text-sm text-muted-foreground">Emergency Triage</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3 p-4 border border-border rounded-lg">
                  <div className="w-10 h-10 bg-medical-accent/10 rounded-lg flex items-center justify-center">
                    <Clock className="w-5 h-5 text-medical-accent" />
                  </div>
                  <div>
                    <h4 className="font-medium">10 Hours Trained</h4>
                    <p className="text-sm text-muted-foreground">Dedication milestone</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3 p-4 border border-border rounded-lg">
                  <div className="w-10 h-10 bg-success/10 rounded-lg flex items-center justify-center">
                    <Target className="w-5 h-5 text-success" />
                  </div>
                  <div>
                    <h4 className="font-medium">Module Master</h4>
                    <p className="text-sm text-muted-foreground">5 modules completed</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default function ResultsPage() {
  return (
    <AuthProvider>
      <ResultsContent />
    </AuthProvider>
  )
}

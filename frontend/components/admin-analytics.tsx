"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { TrendingUp, TrendingDown, Users, BookOpen, Clock, Award } from "lucide-react"

const moduleCompletionData = [
  { name: "Emergency Triage", completed: 892, total: 1247, rate: 71.5 },
  { name: "Patient Communication", completed: 756, total: 1247, rate: 60.6 },
  { name: "Diagnostic Reasoning", completed: 634, total: 1247, rate: 50.8 },
  { name: "Pediatric Care", completed: 423, total: 1247, rate: 33.9 },
  { name: "Surgical Consultation", completed: 312, total: 1247, rate: 25.0 },
  { name: "Mental Health", completed: 567, total: 1247, rate: 45.5 },
]

const weeklyActivityData = [
  { day: "Mon", sessions: 145, users: 89 },
  { day: "Tue", sessions: 167, users: 102 },
  { day: "Wed", sessions: 189, users: 115 },
  { day: "Thu", sessions: 156, users: 94 },
  { day: "Fri", sessions: 134, users: 81 },
  { day: "Sat", sessions: 98, users: 62 },
  { day: "Sun", sessions: 87, users: 54 },
]

const performanceDistribution = [
  { name: "Excellent (90-100%)", value: 28, color: "#22c55e" },
  { name: "Good (80-89%)", value: 42, color: "#3b82f6" },
  { name: "Average (70-79%)", value: 23, color: "#f59e0b" },
  { name: "Below Average (<70%)", value: 7, color: "#ef4444" },
]

export function AdminAnalytics() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Analytics Dashboard</h2>
        <p className="text-muted-foreground">Comprehensive insights into platform usage and performance</p>
      </div>

      {/* Key Performance Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Weekly Active Users</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">892</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <TrendingUp className="w-3 h-3 mr-1 text-green-500" />
              <span className="text-green-500">+12.5%</span> from last week
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Session Duration</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24.3m</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <TrendingUp className="w-3 h-3 mr-1 text-green-500" />
              <span className="text-green-500">+3.2%</span> from last week
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Module Completion Rate</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">73.2%</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <TrendingDown className="w-3 h-3 mr-1 text-red-500" />
              <span className="text-red-500">-1.8%</span> from last week
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Score</CardTitle>
            <Award className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">87.3%</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <TrendingUp className="w-3 h-3 mr-1 text-green-500" />
              <span className="text-green-500">+2.1%</span> from last week
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Weekly Activity Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Weekly Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={weeklyActivityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="sessions" fill="#3b82f6" name="Sessions" />
                <Bar dataKey="users" fill="#10b981" name="Active Users" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Performance Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Performance Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={performanceDistribution}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, value }) => `${value}%`}
                >
                  {performanceDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {performanceDistribution.map((item, index) => (
                <div key={index} className="flex items-center justify-between text-sm">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: item.color }} />
                    <span>{item.name}</span>
                  </div>
                  <span className="font-medium">{item.value}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Module Completion Rates */}
      <Card>
        <CardHeader>
          <CardTitle>Module Completion Rates</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {moduleCompletionData.map((module, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium">{module.name}</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-muted-foreground">
                      {module.completed}/{module.total}
                    </span>
                    <Badge variant={module.rate >= 60 ? "default" : module.rate >= 40 ? "secondary" : "destructive"}>
                      {module.rate}%
                    </Badge>
                  </div>
                </div>
                <Progress value={module.rate} className="h-2" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

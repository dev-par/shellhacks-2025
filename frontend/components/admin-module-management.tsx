"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Plus, Edit, Trash2, Eye, Users, Clock, Star } from "lucide-react"

const mockModules = [
  {
    id: 1,
    title: "Emergency Department Triage",
    category: "Emergency Medicine",
    difficulty: "Intermediate",
    duration: 45,
    scenarios: 8,
    participants: 1247,
    rating: 4.8,
    isActive: true,
    lastUpdated: "2024-01-15",
  },
  {
    id: 2,
    title: "Difficult Patient Conversations",
    category: "Communication",
    difficulty: "Advanced",
    duration: 60,
    scenarios: 12,
    participants: 892,
    rating: 4.9,
    isActive: true,
    lastUpdated: "2024-01-10",
  },
  {
    id: 3,
    title: "Clinical Diagnostic Reasoning",
    category: "Diagnostics",
    difficulty: "Advanced",
    duration: 90,
    scenarios: 15,
    participants: 654,
    rating: 4.7,
    isActive: true,
    lastUpdated: "2023-12-20",
  },
  {
    id: 4,
    title: "Pediatric Patient Care",
    category: "Pediatrics",
    difficulty: "Intermediate",
    duration: 75,
    scenarios: 10,
    participants: 423,
    rating: 4.6,
    isActive: false,
    lastUpdated: "2023-11-15",
  },
]

export function AdminModuleManagement() {
  const [modules, setModules] = useState(mockModules)

  const toggleModuleStatus = (id: number) => {
    setModules(modules.map((module) => (module.id === id ? { ...module, isActive: !module.isActive } : module)))
  }

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case "Beginner":
        return <Badge variant="secondary">Beginner</Badge>
      case "Intermediate":
        return <Badge variant="default">Intermediate</Badge>
      case "Advanced":
        return <Badge variant="destructive">Advanced</Badge>
      default:
        return <Badge variant="outline">{difficulty}</Badge>
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">Module Management</h2>
          <p className="text-muted-foreground">Create and manage training modules</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Create Module
        </Button>
      </div>

      {/* Modules Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Modules</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{modules.length}</div>
            <p className="text-xs text-muted-foreground">{modules.filter((m) => m.isActive).length} active</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Scenarios</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{modules.reduce((sum, module) => sum + module.scenarios, 0)}</div>
            <p className="text-xs text-muted-foreground">Across all modules</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Rating</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(modules.reduce((sum, module) => sum + module.rating, 0) / modules.length).toFixed(1)}
            </div>
            <p className="text-xs text-muted-foreground">Based on user feedback</p>
          </CardContent>
        </Card>
      </div>

      {/* Modules Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Modules</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Module</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Difficulty</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead>Scenarios</TableHead>
                  <TableHead>Participants</TableHead>
                  <TableHead>Rating</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {modules.map((module) => (
                  <TableRow key={module.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{module.title}</div>
                        <div className="text-sm text-muted-foreground">Updated {module.lastUpdated}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{module.category}</Badge>
                    </TableCell>
                    <TableCell>{getDifficultyBadge(module.difficulty)}</TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-1 text-muted-foreground" />
                        {module.duration}m
                      </div>
                    </TableCell>
                    <TableCell>{module.scenarios}</TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <Users className="w-4 h-4 mr-1 text-muted-foreground" />
                        {module.participants.toLocaleString()}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <Star className="w-4 h-4 mr-1 text-yellow-500 fill-current" />
                        {module.rating}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Switch checked={module.isActive} onCheckedChange={() => toggleModuleStatus(module.id)} />
                        <span className="text-sm">{module.isActive ? "Active" : "Inactive"}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Button variant="ghost" size="sm">
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

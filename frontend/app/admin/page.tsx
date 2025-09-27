"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Header } from "@/components/header"
import { AuthProvider, useAuth } from "@/components/auth-context"
import { Users, Activity, TrendingUp, AlertTriangle, Clock, CheckCircle, Shield } from "lucide-react"
import Link from "next/link"
import { AdminUserManagement } from "@/components/admin-user-management"
import { AdminAnalytics } from "@/components/admin-analytics"
import { AdminModuleManagement } from "@/components/admin-module-management"
import { AdminSystemStatus } from "@/components/admin-system-status"

const mockStats = {
  totalUsers: 1247,
  activeUsers: 892,
  totalModules: 12,
  completedSessions: 5634,
  averageScore: 87.3,
  systemUptime: 99.8,
}

const recentActivity = [
  {
    id: 1,
    user: "Dr. Sarah Johnson",
    action: "Completed Emergency Triage module",
    timestamp: "2 minutes ago",
    score: 94,
  },
  {
    id: 2,
    user: "Dr. Michael Chen",
    action: "Started Pediatric Care module",
    timestamp: "5 minutes ago",
    score: null,
  },
  {
    id: 3,
    user: "Dr. Emily Rodriguez",
    action: "Failed Diagnostic Reasoning scenario",
    timestamp: "12 minutes ago",
    score: 67,
  },
  {
    id: 4,
    user: "Dr. James Wilson",
    action: "Completed Patient Communication module",
    timestamp: "18 minutes ago",
    score: 91,
  },
]

const systemAlerts = [
  {
    id: 1,
    type: "warning",
    message: "High server load detected - response times may be slower",
    timestamp: "15 minutes ago",
  },
  {
    id: 2,
    type: "info",
    message: "Scheduled maintenance window: Sunday 2:00 AM - 4:00 AM EST",
    timestamp: "2 hours ago",
  },
  {
    id: 3,
    type: "success",
    message: "Database backup completed successfully",
    timestamp: "6 hours ago",
  },
]

function AdminDashboardContent() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState("overview")

  if (!user || user.role !== "admin") {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-md mx-auto text-center">
            <div className="w-16 h-16 bg-destructive/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <Shield className="w-8 h-8 text-destructive" />
            </div>
            <h1 className="text-2xl font-bold mb-4">Access Denied</h1>
            <p className="text-muted-foreground mb-6">You need administrator privileges to access this page.</p>
            <Link href="/">
              <Button>Return Home</Button>
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-muted-foreground">Manage users, modules, and monitor system performance</p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="modules">Modules</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="system">System</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{mockStats.totalUsers.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    <span className="text-success">+12%</span> from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Users</CardTitle>
                  <Activity className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{mockStats.activeUsers.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    <span className="text-success">+8%</span> from last week
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Completed Sessions</CardTitle>
                  <CheckCircle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{mockStats.completedSessions.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    <span className="text-success">+23%</span> from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Average Score</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{mockStats.averageScore}%</div>
                  <p className="text-xs text-muted-foreground">
                    <span className="text-success">+2.1%</span> from last month
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              {/* Recent Activity */}
              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentActivity.map((activity) => (
                      <div key={activity.id} className="flex items-center justify-between">
                        <div className="flex-1">
                          <p className="text-sm font-medium">{activity.user}</p>
                          <p className="text-xs text-muted-foreground">{activity.action}</p>
                          <p className="text-xs text-muted-foreground">{activity.timestamp}</p>
                        </div>
                        {activity.score && (
                          <Badge
                            variant={
                              activity.score >= 80 ? "default" : activity.score >= 70 ? "secondary" : "destructive"
                            }
                          >
                            {activity.score}%
                          </Badge>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* System Alerts */}
              <Card>
                <CardHeader>
                  <CardTitle>System Alerts</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {systemAlerts.map((alert) => (
                      <div key={alert.id} className="flex items-start space-x-3">
                        <div className="flex-shrink-0 mt-1">
                          {alert.type === "warning" && <AlertTriangle className="w-4 h-4 text-yellow-500" />}
                          {alert.type === "info" && <Clock className="w-4 h-4 text-blue-500" />}
                          {alert.type === "success" && <CheckCircle className="w-4 h-4 text-green-500" />}
                        </div>
                        <div className="flex-1">
                          <p className="text-sm">{alert.message}</p>
                          <p className="text-xs text-muted-foreground">{alert.timestamp}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="users">
            <AdminUserManagement />
          </TabsContent>

          <TabsContent value="modules">
            <AdminModuleManagement />
          </TabsContent>

          <TabsContent value="analytics">
            <AdminAnalytics />
          </TabsContent>

          <TabsContent value="system">
            <AdminSystemStatus />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default function AdminDashboardPage() {
  return (
    <AuthProvider>
      <AdminDashboardContent />
    </AuthProvider>
  )
}

"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { Server, Database, Wifi, HardDrive, Activity, AlertTriangle, CheckCircle, RefreshCw } from "lucide-react"

const systemMetrics = {
  server: {
    status: "healthy",
    uptime: "99.8%",
    responseTime: "145ms",
    load: 67,
  },
  database: {
    status: "healthy",
    connections: 45,
    maxConnections: 100,
    queryTime: "23ms",
    storage: 78,
  },
  network: {
    status: "healthy",
    bandwidth: 89,
    latency: "12ms",
    packets: "99.9%",
  },
  storage: {
    status: "warning",
    used: 85,
    total: "500GB",
    backups: "healthy",
  },
}

const recentLogs = [
  {
    id: 1,
    timestamp: "2024-01-20 14:32:15",
    level: "info",
    service: "API",
    message: "User authentication successful",
  },
  {
    id: 2,
    timestamp: "2024-01-20 14:31:45",
    level: "warning",
    service: "Storage",
    message: "Disk usage above 80% threshold",
  },
  {
    id: 3,
    timestamp: "2024-01-20 14:30:22",
    level: "info",
    service: "Database",
    message: "Backup completed successfully",
  },
  {
    id: 4,
    timestamp: "2024-01-20 14:28:10",
    level: "error",
    service: "WebRTC",
    message: "Connection timeout for user session",
  },
  {
    id: 5,
    timestamp: "2024-01-20 14:25:33",
    level: "info",
    service: "AI",
    message: "Voice synthesis completed",
  },
]

export function AdminSystemStatus() {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case "healthy":
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case "warning":
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />
      case "error":
        return <AlertTriangle className="w-4 h-4 text-red-500" />
      default:
        return <Activity className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "healthy":
        return (
          <Badge variant="default" className="bg-green-100 text-green-800">
            Healthy
          </Badge>
        )
      case "warning":
        return (
          <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
            Warning
          </Badge>
        )
      case "error":
        return <Badge variant="destructive">Error</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  const getLogLevelBadge = (level: string) => {
    switch (level) {
      case "info":
        return (
          <Badge variant="outline" className="text-xs">
            INFO
          </Badge>
        )
      case "warning":
        return (
          <Badge variant="secondary" className="text-xs bg-yellow-100 text-yellow-800">
            WARN
          </Badge>
        )
      case "error":
        return (
          <Badge variant="destructive" className="text-xs">
            ERROR
          </Badge>
        )
      default:
        return (
          <Badge variant="outline" className="text-xs">
            {level.toUpperCase()}
          </Badge>
        )
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">System Status</h2>
          <p className="text-muted-foreground">Monitor system health and performance</p>
        </div>
        <Button variant="outline">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* System Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Server</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between mb-2">
              {getStatusIcon(systemMetrics.server.status)}
              {getStatusBadge(systemMetrics.server.status)}
            </div>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Uptime:</span>
                <span className="font-medium">{systemMetrics.server.uptime}</span>
              </div>
              <div className="flex justify-between">
                <span>Response:</span>
                <span className="font-medium">{systemMetrics.server.responseTime}</span>
              </div>
              <div className="mt-2">
                <div className="flex justify-between text-xs mb-1">
                  <span>Load</span>
                  <span>{systemMetrics.server.load}%</span>
                </div>
                <Progress value={systemMetrics.server.load} className="h-2" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Database</CardTitle>
            <Database className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between mb-2">
              {getStatusIcon(systemMetrics.database.status)}
              {getStatusBadge(systemMetrics.database.status)}
            </div>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Connections:</span>
                <span className="font-medium">
                  {systemMetrics.database.connections}/{systemMetrics.database.maxConnections}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Query Time:</span>
                <span className="font-medium">{systemMetrics.database.queryTime}</span>
              </div>
              <div className="mt-2">
                <div className="flex justify-between text-xs mb-1">
                  <span>Storage</span>
                  <span>{systemMetrics.database.storage}%</span>
                </div>
                <Progress value={systemMetrics.database.storage} className="h-2" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Network</CardTitle>
            <Wifi className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between mb-2">
              {getStatusIcon(systemMetrics.network.status)}
              {getStatusBadge(systemMetrics.network.status)}
            </div>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Latency:</span>
                <span className="font-medium">{systemMetrics.network.latency}</span>
              </div>
              <div className="flex justify-between">
                <span>Packets:</span>
                <span className="font-medium">{systemMetrics.network.packets}</span>
              </div>
              <div className="mt-2">
                <div className="flex justify-between text-xs mb-1">
                  <span>Bandwidth</span>
                  <span>{systemMetrics.network.bandwidth}%</span>
                </div>
                <Progress value={systemMetrics.network.bandwidth} className="h-2" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Storage</CardTitle>
            <HardDrive className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between mb-2">
              {getStatusIcon(systemMetrics.storage.status)}
              {getStatusBadge(systemMetrics.storage.status)}
            </div>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Total:</span>
                <span className="font-medium">{systemMetrics.storage.total}</span>
              </div>
              <div className="flex justify-between">
                <span>Backups:</span>
                <span className="font-medium text-green-600">{systemMetrics.storage.backups}</span>
              </div>
              <div className="mt-2">
                <div className="flex justify-between text-xs mb-1">
                  <span>Used</span>
                  <span>{systemMetrics.storage.used}%</span>
                </div>
                <Progress value={systemMetrics.storage.used} className="h-2" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Logs */}
      <Card>
        <CardHeader>
          <CardTitle>Recent System Logs</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recentLogs.map((log) => (
              <div key={log.id} className="flex items-start space-x-3 p-3 rounded-lg bg-muted/50">
                <div className="flex-shrink-0 mt-1">{getLogLevelBadge(log.level)}</div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">{log.service}</span>
                    <span className="text-xs text-muted-foreground">{log.timestamp}</span>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{log.message}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

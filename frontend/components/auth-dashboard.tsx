"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/lib/use-auth";
import { apiClient } from "../lib/api-client";
import { useEffect, useState } from "react";

export function AuthDashboard() {
  const { user, logout, getToken, isAuthenticated } = useAuth();
  const [backendStatus, setBackendStatus] = useState<string>("");
  const [protectedData, setProtectedData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      // Set up API client with token
      getToken().then((token) => {
        if (token) {
          apiClient.setToken(token);
        }
      });
    }
  }, [isAuthenticated, getToken]);

  const testBackendConnection = async () => {
    setLoading(true);
    try {
      const response = await apiClient.testConnection();
      setBackendStatus(`✅ Backend connected: ${response.message}`);
    } catch (error) {
      setBackendStatus(`❌ Backend error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const testProtectedEndpoint = async () => {
    setLoading(true);
    try {
      const response = await apiClient.getProtectedData();
      setProtectedData(response);
    } catch (error) {
      setProtectedData({
        error: `Protected endpoint error: ${error}`,
        message:
          "This endpoint requires authentication. Make sure you're logged in.",
      });
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Authentication Required</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Please log in to access this dashboard.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Welcome, {user?.name || user?.email}!</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-semibold">User Info:</h3>
            <pre className="bg-muted p-2 rounded text-sm overflow-auto">
              {JSON.stringify(user, null, 2)}
            </pre>
          </div>

          <div className="flex gap-2">
            <Button onClick={testBackendConnection} disabled={loading}>
              Test Backend Connection
            </Button>
            <Button onClick={testProtectedEndpoint} disabled={loading}>
              Test Protected Endpoint
            </Button>
            <Button onClick={logout} variant="outline">
              Logout
            </Button>
          </div>

          {backendStatus && (
            <div className="p-3 bg-muted rounded">
              <p className="text-sm">{backendStatus}</p>
            </div>
          )}

          {protectedData && (
            <div>
              <h3 className="font-semibold">Protected Endpoint Response:</h3>
              <pre className="bg-muted p-2 rounded text-sm overflow-auto">
                {JSON.stringify(protectedData, null, 2)}
              </pre>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

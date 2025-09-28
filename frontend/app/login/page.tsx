"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Header } from "@/components/header";

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is already authenticated
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/profile', {
          credentials: 'include' // Important: includes cookies
        });
        setIsAuthenticated(response.ok);
      } catch (error) {
        setIsAuthenticated(false);
      }
    };
    
    checkAuth();
  }, []);

  const handleLogin = () => {
    setIsLoading(true);
    // Redirect to your backend login endpoint
    window.location.href = 'http://localhost:5000/login';
  };

  return (
    <div className="min-h-screen">
      <Header />

      <div className="container mx-auto px-4 py-20">
        <div className="max-w-md mx-auto text-center">
          {!isAuthenticated && (
            <Button
              onClick={handleLogin}
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700"
            >
              {isLoading ? "Redirecting..." : "Sign In with Auth0"}
            </Button>
          )}

          {isAuthenticated && (
            <p className="text-green-600 mt-4">You are already logged in.</p>
          )}
        </div>
      </div>
    </div>
  );
}
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in (simple localStorage check)
    const storedUser = localStorage.getItem("mock-user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const login = async () => {
    // Mock login - just set a user and redirect
    const mockUser = {
      sub: "mock-user-123",
      email: "user@example.com",
      name: "Mock User",
      picture: "https://via.placeholder.com/150",
    };

    setUser(mockUser);
    setIsAuthenticated(true);
    localStorage.setItem("mock-user", JSON.stringify(mockUser));

    // Redirect to dashboard
    router.push("/");
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem("mock-user");
    router.push("/");
  };

  const getToken = async () => {
    // Return a mock token
    return "mock-token-123";
  };

  return {
    isAuthenticated,
    user,
    isLoading,
    login,
    logout,
    getToken,
  };
}

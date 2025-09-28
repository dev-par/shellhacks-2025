"use client"

import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link"

export function Header() {

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  // Check if user is already authenticated
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/profile', {
          credentials: 'include' 
        });
        setIsAuthenticated(response.ok);
      } catch (error) {
        setIsAuthenticated(false);
      }
    };
    
    checkAuth();
  }, []);

  const handleLogin = () => {
    // Redirect to your backend login endpoint
    window.location.href = 'http://localhost:5000/login';
  };

  return (
    <header className="border-b border-border/30 bg-white backdrop-blur">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <Link href="/" className="flex items-center space-x-2">
            <span className="font-bold text-xl gradient-text">RespondER</span>
          </Link>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            {!isAuthenticated ? (
              <div>
                <Button 
                  onClick={handleLogin}
                  variant="ghost" 
                  className="backdrop-blur-sm border border-black cursor-pointer"
                >
                  Sign In
                </Button>
                <Button onClick={handleLogin} className="bg-gradient-to-r from-[#60adecff] via-[#5A8FD8] to-[#3e4175ff] hover:from-[#60adecff] hover:via-[#5A8FD8] hover:to-[#3e4175ff] cursor-pointer">
                  Get Started
                </Button>
              </div>
            ) : isAuthenticated && (
              <Button 
                onClick={() => router.push('/modules')}
                variant="ghost" 
                className="backdrop-blur-sm border border-black cursor-pointer"
              >
                Training Modules
              </Button>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

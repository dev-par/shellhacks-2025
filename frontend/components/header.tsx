"use client";

import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/use-auth";
import { useRouter } from "next/navigation";
import Link from "next/link";

export function Header() {
  const { isAuthenticated, login, logout } = useAuth();
  const router = useRouter();

  const handleLogin = () => {
    login();
  };

  const handleLogout = () => {
    logout();
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
                <Button
                  onClick={handleLogin}
                  className="bg-gradient-to-r from-[#60adecff] via-[#5A8FD8] to-[#3e4175ff] hover:from-[#60adecff] hover:via-[#5A8FD8] hover:to-[#3e4175ff] cursor-pointer"
                >
                  Get Started
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Button
                  onClick={() => router.push("/modules")}
                  variant="ghost"
                  className="backdrop-blur-sm border border-black cursor-pointer"
                >
                  Training Modules
                </Button>
                <Button
                  onClick={handleLogout}
                  variant="outline"
                  className="cursor-pointer"
                >
                  Logout
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

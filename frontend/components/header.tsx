"use client"

import { Button } from "@/components/ui/button"
import Link from "next/link"

export function Header() {

  return (
    <header className="border-b border-border/30 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">MS</span>
            </div>
            <span className="font-bold text-xl gradient-text">MedSimPro</span>
          </Link>

          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/modules" className="text-muted-foreground hover:text-foreground transition-colors">
              Training Modules
            </Link>
            <Link href="/about" className="text-muted-foreground hover:text-foreground transition-colors">
              About
            </Link>
            <Link href="/contact" className="text-muted-foreground hover:text-foreground transition-colors">
              Contact
            </Link>
          </nav>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Link href="/login">
              <Button variant="ghost" className="backdrop-blur-sm">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700 hover:from-blue-600 hover:via-purple-700 hover:to-blue-800">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}

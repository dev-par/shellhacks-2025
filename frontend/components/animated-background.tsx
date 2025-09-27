"use client"

import { Heart } from "lucide-react"

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-blue-500/20 constant-heartbeat">
        <Heart className="w-40 h-40" fill="currentColor" />
      </div>

      <div className="absolute top-20 left-20 text-purple-500/25 constant-heartbeat" style={{ animationDelay: "0.2s" }}>
        <Heart className="w-16 h-16" fill="currentColor" />
      </div>

      <div className="absolute top-32 right-24 text-blue-400/30 pulse-heart" style={{ animationDelay: "0.4s" }}>
        <Heart className="w-12 h-12" fill="currentColor" />
      </div>

      <div
        className="absolute bottom-32 left-32 text-purple-400/20 constant-heartbeat"
        style={{ animationDelay: "0.6s" }}
      >
        <Heart className="w-20 h-20" fill="currentColor" />
      </div>

      <div className="absolute bottom-20 right-20 text-blue-600/25 pulse-heart" style={{ animationDelay: "0.8s" }}>
        <Heart className="w-14 h-14" fill="currentColor" />
      </div>

      <div
        className="absolute top-40 left-1/3 text-purple-600/30 constant-heartbeat"
        style={{ animationDelay: "1.0s" }}
      >
        <Heart className="w-8 h-8" fill="currentColor" />
      </div>

      <div className="absolute bottom-40 right-1/3 text-blue-500/20 pulse-heart" style={{ animationDelay: "1.2s" }}>
        <Heart className="w-18 h-18" fill="currentColor" />
      </div>

      <div
        className="absolute top-60 right-1/4 text-purple-500/25 constant-heartbeat"
        style={{ animationDelay: "1.4s" }}
      >
        <Heart className="w-10 h-10" fill="currentColor" />
      </div>

      <div className="absolute top-1/4 left-1/4 text-blue-400/15 pulse-heart" style={{ animationDelay: "1.6s" }}>
        <Heart className="w-6 h-6" fill="currentColor" />
      </div>

      <div
        className="absolute bottom-1/4 left-3/4 text-purple-400/20 constant-heartbeat"
        style={{ animationDelay: "1.8s" }}
      >
        <Heart className="w-12 h-12" fill="currentColor" />
      </div>

      <div className="absolute top-3/4 right-1/2 text-blue-600/25 pulse-heart" style={{ animationDelay: "2.0s" }}>
        <Heart className="w-8 h-8" fill="currentColor" />
      </div>

      <div
        className="absolute top-10 left-1/2 text-purple-600/15 constant-heartbeat"
        style={{ animationDelay: "2.2s" }}
      >
        <Heart className="w-4 h-4" fill="currentColor" />
      </div>
    </div>
  )
}

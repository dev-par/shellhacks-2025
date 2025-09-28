"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Header } from "@/components/header";
import { VideoCallModal } from "@/components/video-call-modal";
import { AuthDashboard } from "@/components/auth-dashboard";
import { useAuth } from "@/lib/use-auth";
import Link from "next/link";
import { useState } from "react";
import {
  ArrowRight,
  Brain,
  Mic,
  Users,
  Shield,
  Clock,
  Award,
} from "lucide-react";

export default function HomePage() {
  const { login, isAuthenticated, user } = useAuth();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleLogin = () => {
    login();
  };

  return (
    <div className="min-h-screen relative">
      <Header />

      {/* Auth Dashboard or Hero Section */}
      {isAuthenticated ? (
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <AuthDashboard />
            </div>
          </div>
        </section>
      ) : (
        <section className="relative py-20 lg:py-32 bg-gradient-to-r from-[#5A8FD8] via-[#a3c6e4] to-[#5A8FD8]">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <div className="inline-flex items-center px-3 py-1 rounded-full bg-primary/10 text-white text-sm font-medium mb-6 backdrop-blur-sm">
                <Brain className="w-4 h-4 mr-2" />
                AI-Powered Medical Training
              </div>

              <h1 className="text-4xl lg:text-6xl font-bold text-white mb-6">
                The most advanced platform for{" "}
                <span className="gradient-text">medical simulation</span>{" "}
                training
              </h1>

              <p className="text-xl text-muted-foreground text-balance mb-8 max-w-2xl mx-auto leading-relaxed">
                Empower early-career doctors with realistic AI voice
                simulations, real-time feedback, and comprehensive training
                modules designed by medical experts.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Button
                  onClick={handleLogin}
                  size="lg"
                  className="text-lg px-8 py-6 bg-gradient-to-r from-[#60adecff] via-[#5A8FD8] to-[#3e4175ff] hover:from-[#60adecff] hover:via-[#5A8FD8] hover:to-[#3e4175ff] cursor-pointer"
                >
                  Start Training
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
                <Button
                  onClick={() => setIsModalOpen(true)}
                  variant="outline"
                  size="lg"
                  className="text-lg px-8 py-6 bg-white backdrop-blur-sm border-primary/30 cursor-pointer"
                >
                  <Mic className="w-5 h-5 mr-2" />
                  Watch Demo
                </Button>
              </div>
            </div>
          </div>
          <VideoCallModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
          />
        </section>
      )}

      {/* Stats Section */}
      <section className="py-16 border-y bg-white border-border/30">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">
                95%
              </div>
              <div className="text-muted-foreground">Training Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">
                Various
              </div>
              <div className="text-muted-foreground">Medical Scenarios</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">
                24/7
              </div>
              <div className="text-muted-foreground">Available Training</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-r from-[#5A8FD8] via-[#a3c6e4] to-[#5A8FD8]">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4 gradient-text pb-4">
              Advanced Training Features
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Experience the future of medical education with our comprehensive
              AI-powered platform
            </p>
          </div>

          <div className="grid grid-cols-2 gap-8">
            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Mic className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">
                  Voice AI Simulation
                </h3>
                <p className="text-muted-foreground">
                  Realistic patient interactions with advanced voice AI that
                  responds naturally to your medical inquiries and decisions.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Users className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">
                  Expert-Designed Scenarios
                </h3>
                <p className="text-muted-foreground">
                  Training modules created by experienced medical professionals
                  covering diverse clinical situations.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Clock className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">
                  Flexible Learning
                </h3>
                <p className="text-muted-foreground">
                  Train at your own pace with 24/7 access to all modules and
                  personalized learning paths.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Award className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">
                  Progress Tracking
                </h3>
                <p className="text-muted-foreground">
                  Comprehensive analytics and progress reports to track your
                  improvement and identify areas for growth.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/30 py-6 bg-white">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <span className="font-bold text-xl gradient-text">RespondER</span>
            </div>
            <div className="text-muted-foreground text-sm">
              © 2025 RespondER. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

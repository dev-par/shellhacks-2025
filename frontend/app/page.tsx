import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Header } from "@/components/header"
import Link from "next/link"
import { ArrowRight, Brain, Mic, Users, Shield, Clock, Award } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen relative">
      <Header />

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6 backdrop-blur-sm">
              <Brain className="w-4 h-4 mr-2" />
              AI-Powered Medical Training
            </div>

            <h1 className="text-4xl lg:text-6xl font-bold text-balance mb-6">
              The most advanced platform for <span className="gradient-text">medical simulation</span> training
            </h1>

            <p className="text-xl text-muted-foreground text-balance mb-8 max-w-2xl mx-auto leading-relaxed">
              Empower early-career doctors with realistic AI voice simulations, real-time feedback, and comprehensive
              training modules designed by medical experts.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/signup">
                <Button
                  size="lg"
                  className="text-lg px-8 py-6 bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700 hover:from-blue-600 hover:via-purple-700 hover:to-blue-800"
                >
                  Start Training
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <Link href="/demo">
                <Button
                  variant="outline"
                  size="lg"
                  className="text-lg px-8 py-6 bg-transparent backdrop-blur-sm border-primary/30"
                >
                  <Mic className="w-5 h-5 mr-2" />
                  Watch Demo
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 border-t border-border/30">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">95%</div>
              <div className="text-muted-foreground">Training Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">50+</div>
              <div className="text-muted-foreground">Medical Scenarios</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">24/7</div>
              <div className="text-muted-foreground">Available Training</div>
            </div>
            <div className="text-center">
              <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">1000+</div>
              <div className="text-muted-foreground">Doctors Trained</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4 gradient-text">Advanced Training Features</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Experience the future of medical education with our comprehensive AI-powered platform
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Mic className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">Voice AI Simulation</h3>
                <p className="text-muted-foreground">
                  Realistic patient interactions with advanced voice AI that responds naturally to your medical
                  inquiries and decisions.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Brain className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">Real-time Analysis</h3>
                <p className="text-muted-foreground">
                  Get instant feedback on your diagnostic approach, communication skills, and clinical decision-making
                  process.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Users className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">Expert-Designed Scenarios</h3>
                <p className="text-muted-foreground">
                  Training modules created by experienced medical professionals covering diverse clinical situations.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Shield className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">HIPAA Compliant</h3>
                <p className="text-muted-foreground">
                  Enterprise-grade security ensuring all training data and interactions remain completely confidential.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Clock className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">Flexible Learning</h3>
                <p className="text-muted-foreground">
                  Train at your own pace with 24/7 access to all modules and personalized learning paths.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card/80 border-border/30 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm">
                  <Award className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 gradient-text-alt">Progress Tracking</h3>
                <p className="text-muted-foreground">
                  Comprehensive analytics and progress reports to track your improvement and identify areas for growth.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4 gradient-text">
            Ready to transform your medical training?
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of medical professionals who are advancing their skills with MedSimPro
          </p>
          <Link href="/signup">
            <Button
              size="lg"
              className="text-lg px-8 py-6 bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700 hover:from-blue-600 hover:via-purple-700 hover:to-blue-800"
            >
              Get Started Today
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/30 py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 via-purple-600 to-blue-700 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">MS</span>
              </div>
              <span className="font-bold text-xl gradient-text">MedSimPro</span>
            </div>
            <div className="text-muted-foreground text-sm">© 2025 MedSimPro. All rights reserved.</div>
          </div>
        </div>
      </footer>
    </div>
  )
}

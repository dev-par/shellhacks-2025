import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import { Suspense } from "react"
import { AuthProvider } from "@/components/auth-context"
import { AnimatedBackground } from "@/components/animated-background"
import "./globals.css"

export const metadata: Metadata = {
  title: "MedSimPro - AI-Powered Medical Training",
  description: "Advanced voice simulation platform for early-career doctors",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable} antialiased`}>
        <AuthProvider>
          <AnimatedBackground />
          <div className="relative z-10">
            <Suspense fallback={null}>{children}</Suspense>
          </div>
        </AuthProvider>
        <Analytics />
      </body>
    </html>
  )
}

"use client"

import type React from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import Image from "next/image"
import Link from "next/link"
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function SignInPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const router = useRouter()

  const handleSignIn = (e: React.FormEvent) => {
    e.preventDefault()
    // Simulate sign in
    router.push("/dashboard")
  }

  const handleGoogleSignIn = () => {
    // Simulate Google sign in
    router.push("/dashboard")
  }

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    setMousePosition({ x: e.clientX, y: e.clientY })
  }

  return (
    <div
      className="min-h-screen bg-background flex items-center justify-center p-4 relative overflow-hidden"
      onMouseMove={handleMouseMove}
    >
      {/* Mouse Glow Effect */}
      <div
        className="absolute pointer-events-none"
        style={{
          left: mousePosition.x,
          top: mousePosition.y,
          transform: "translate(-50%, -50%)",
          width: "300px",
          height: "300px",
          borderRadius: "50%",
          background: "radial-gradient(circle at center, hsl(var(--cyan-light)) 0%, transparent 70%)",
          opacity: 0.15,
          filter: "blur(80px)",
          transition: "transform 0.1s ease-out",
          zIndex: 0,
        }}
      />

      <div className="w-full max-w-md space-y-8 relative z-10">
        <div className="text-center">
          <div className="flex justify-center mb-8">
            <Image
              src="/images/clapperlabs-full-logo.png"
              alt="ClapperLabs"
              width={560}
              height={140}
              className="h-32 w-auto"
            />
          </div>
          <h1 className="text-3xl font-semibold text-foreground">Welcome back</h1>
          <p className="text-muted-foreground mt-2">Sign in to your ClapperLabs account</p>
        </div>

        <div className="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-8 space-y-6">
          <Button
            onClick={handleGoogleSignIn}
            variant="outline"
            className="w-full py-3 text-base font-medium border-border/50 hover:bg-card/80 bg-transparent"
          >
            <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            Continue with Google
          </Button>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <Separator className="w-full" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-2 text-muted-foreground">Or continue with email</span>
            </div>
          </div>

          <form onSubmit={handleSignIn} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-foreground">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-background/50 border-border/50 text-foreground placeholder:text-muted-foreground"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-foreground">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-background/50 border-border/50 text-foreground placeholder:text-muted-foreground"
                required
              />
            </div>
            <Button type="submit" className="w-full bg-primary text-primary-foreground hover:bg-primary/90 py-3">
              Sign In
            </Button>
          </form>

          <div className="text-center text-sm">
            <Link href="#" className="text-muted-foreground hover:text-primary">
              Forgot your password?
            </Link>
          </div>

          <div className="text-center text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link href="#" className="text-primary hover:text-primary/80 font-medium">
              Sign up
            </Link>
          </div>
        </div>

        <div className="text-center">
          <Link href="/" className="text-muted-foreground hover:text-foreground text-sm">
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  )
}

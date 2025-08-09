import React from "react"
import { Button } from "@/components/ui/button"
import { Header } from "./header"
import Link from "next/link"

export function HeroSection() {
  return (
    <section className="flex flex-col items-center text-center relative w-full h-screen overflow-hidden">
      {/* SVG Background with ClapperLabs colors */}
      <div className="absolute inset-0 z-0">
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 1920 1080"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="xMidYMid slice"
        >
          <g clipPath="url(#clip0_hero)">
            <mask
              id="mask0_hero"
              style={{ maskType: "alpha" }}
              maskUnits="userSpaceOnUse"
              x="0"
              y="0"
              width="1920"
              height="1080"
            >
              <rect x="0" y="0" width="1920" height="1080" fill="url(#paint0_linear_hero)" />
            </mask>
            <g mask="url(#mask0_hero)">
              {/* Grid pattern */}
              {[...Array(54)].map((_, i) => (
                <React.Fragment key={`row1-${i}`}>
                  {[...Array(31)].map((_, j) => (
                    <rect
                      key={`${i}-${j}`}
                      x={-20 + i * 36}
                      y={-20 + j * 36}
                      width="35.6"
                      height="35.6"
                      stroke="hsl(var(--foreground))"
                      strokeOpacity="0.08"
                      strokeWidth="0.4"
                      strokeDasharray="2 2"
                    />
                  ))}
                </React.Fragment>
              ))}

              {/* Accent squares with coral and cyan colors */}
              <rect x="800" y="200" width="36" height="36" fill="hsl(var(--coral))" fillOpacity="0.15" />
              <rect x="400" y="300" width="36" height="36" fill="hsl(var(--cyan))" fillOpacity="0.15" />
              <rect x="1200" y="250" width="36" height="36" fill="hsl(var(--coral))" fillOpacity="0.12" />
              <rect x="300" y="450" width="36" height="36" fill="hsl(var(--cyan))" fillOpacity="0.12" />
              <rect x="1400" y="400" width="36" height="36" fill="hsl(var(--coral))" fillOpacity="0.1" />
              <rect x="1100" y="600" width="36" height="36" fill="hsl(var(--cyan))" fillOpacity="0.1" />
            </g>

            {/* Gradient overlays with coral and cyan */}
            <g filter="url(#filter0_f_hero)">
              <ellipse cx="960" cy="300" rx="600" ry="400" fill="url(#paint1_radial_hero)" fillOpacity="0.3" />
            </g>

            <g filter="url(#filter1_f_hero)">
              <ellipse cx="960" cy="700" rx="800" ry="300" fill="url(#paint2_radial_hero)" fillOpacity="0.2" />
            </g>
          </g>

          <defs>
            <filter
              id="filter0_f_hero"
              x="60"
              y="-400"
              width="1800"
              height="1400"
              filterUnits="userSpaceOnUse"
              colorInterpolationFilters="sRGB"
            >
              <feFlood floodOpacity="0" result="BackgroundImageFix" />
              <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
              <feGaussianBlur stdDeviation="150" result="effect1_foregroundBlur_hero" />
            </filter>
            <filter
              id="filter1_f_hero"
              x="-140"
              y="100"
              width="2200"
              height="1200"
              filterUnits="userSpaceOnUse"
              colorInterpolationFilters="sRGB"
            >
              <feFlood floodOpacity="0" result="BackgroundImageFix" />
              <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
              <feGaussianBlur stdDeviation="150" result="effect1_foregroundBlur_hero" />
            </filter>
            <linearGradient id="paint0_linear_hero" x1="0" y1="0" x2="1920" y2="1080" gradientUnits="userSpaceOnUse">
              <stop stopColor="hsl(var(--foreground))" stopOpacity="0" />
              <stop offset="1" stopColor="hsl(var(--muted-foreground))" />
            </linearGradient>
            <radialGradient
              id="paint1_radial_hero"
              cx="0"
              cy="0"
              r="1"
              gradientUnits="userSpaceOnUse"
              gradientTransform="translate(960 300) scale(600 400)"
            >
              <stop stopColor="hsl(var(--coral))" />
              <stop offset="0.5" stopColor="hsl(var(--coral-light))" />
              <stop offset="1" stopColor="hsl(var(--primary))" stopOpacity="0" />
            </radialGradient>
            <radialGradient
              id="paint2_radial_hero"
              cx="0"
              cy="0"
              r="1"
              gradientUnits="userSpaceOnUse"
              gradientTransform="translate(960 700) scale(800 300)"
            >
              <stop stopColor="hsl(var(--cyan))" />
              <stop offset="0.5" stopColor="hsl(var(--cyan-light))" />
              <stop offset="1" stopColor="hsl(var(--secondary))" stopOpacity="0" />
            </radialGradient>
            <clipPath id="clip0_hero">
              <rect width="1920" height="1080" fill="white" />
            </clipPath>
          </defs>
        </svg>
      </div>

      {/* Header positioned at top of hero container */}
      <div className="absolute top-0 left-0 right-0 z-20">
        <Header />
      </div>

      <div className="relative z-10 flex flex-col items-center justify-center h-full space-y-8 px-4 max-w-4xl">
        <h1 className="text-foreground text-4xl md:text-6xl lg:text-7xl font-semibold leading-tight text-center">
          AI-Powered Vibe Editing
        </h1>
        <p className="text-muted-foreground text-lg md:text-xl lg:text-2xl font-medium leading-relaxed text-center max-w-3xl">
          Transform your photos and videos with simple chat commands. Just tell our AI what mood you want, and watch
          your content come to life.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mt-8">
          <Link href="/signin">
            <Button className="bg-primary text-primary-foreground hover:bg-primary/90 px-10 py-4 rounded-full font-medium text-lg shadow-lg">
              Start Editing
            </Button>
          </Link>
          <Link href="#features-section">
            <Button
              variant="outline"
              className="border-secondary text-secondary hover:bg-secondary hover:text-secondary-foreground px-10 py-4 rounded-full font-medium text-lg bg-transparent"
            >
              Watch Demo
            </Button>
          </Link>
        </div>
      </div>
    </section>
  )
}

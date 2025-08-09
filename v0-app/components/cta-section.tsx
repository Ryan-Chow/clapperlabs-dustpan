import { Button } from "@/components/ui/button"
import Link from "next/link"

export function CTASection() {
  return (
    <section className="w-full min-h-screen px-8 relative flex flex-col justify-center items-center overflow-visible">
      <div className="absolute inset-0">
        <svg
          className="w-full h-full"
          viewBox="0 0 1920 1080"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="xMidYMid slice"
        >
          <g filter="url(#filter0_f_cta)">
            <ellipse cx="960" cy="540" rx="670" ry="355" fill="url(#paint1_radial_cta)" fillOpacity="0.4" />
          </g>
          <defs>
            <filter
              id="filter0_f_cta"
              x="32"
              y="-73"
              width="1856"
              height="1226"
              filterUnits="userSpaceOnUse"
              colorInterpolationFilters="sRGB"
            >
              <feFlood floodOpacity="0" result="BackgroundImageFix" />
              <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
              <feGaussianBlur stdDeviation="129" result="effect1_foregroundBlur_cta" />
            </filter>
            <radialGradient
              id="paint1_radial_cta"
              cx="0"
              cy="0"
              r="1"
              gradientUnits="userSpaceOnUse"
              gradientTransform="translate(960 540) scale(670 355)"
            >
              <stop offset="0.1294" stopColor="hsl(var(--coral))" />
              <stop offset="0.2347" stopColor="hsl(var(--primary))" />
              <stop offset="0.3" stopColor="hsl(var(--primary))" stopOpacity="0" />
            </radialGradient>
          </defs>
        </svg>
      </div>
      <div className="relative z-10 flex flex-col justify-start items-center gap-12 max-w-5xl mx-auto text-center">
        <div className="flex flex-col justify-start items-center gap-6">
          <h2 className="text-foreground text-5xl md:text-7xl font-semibold leading-tight">Start Creating Today</h2>
          <p className="text-muted-foreground text-xl md:text-2xl font-medium leading-relaxed max-w-3xl">
            Join thousands of creators who are already transforming their photos and videos with AI-powered vibe
            editing. No experience required.
          </p>
        </div>
        <div className="flex flex-col sm:flex-row gap-6">
          <Link href="/signin">
            <Button
              className="px-12 py-4 bg-primary text-primary-foreground text-xl font-medium leading-6 rounded-full hover:bg-primary/90 transition-all duration-200"
              size="lg"
            >
              Start Free Trial
            </Button>
          </Link>
          <Link href="#features-section">
            <Button
              variant="outline"
              className="px-12 py-4 border-secondary text-secondary hover:bg-secondary hover:text-secondary-foreground text-xl font-medium leading-6 rounded-full transition-all duration-200 bg-transparent"
              size="lg"
            >
              Watch Demo
            </Button>
          </Link>
        </div>
      </div>
    </section>
  )
}

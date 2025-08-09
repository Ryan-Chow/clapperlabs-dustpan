import { HeroSection } from "@/components/hero-section"
import { BentoSection } from "@/components/bento-section"
import { PricingSection } from "@/components/pricing-section"
import { TestimonialSection } from "@/components/testimonial-section"
import { CTASection } from "@/components/cta-section"
import { FooterSection } from "@/components/footer-section"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      <HeroSection />
      <div id="features-section">
        <BentoSection />
      </div>
      <div id="pricing-section">
        <PricingSection />
      </div>
      <div id="examples-section">
        <TestimonialSection />
      </div>
      <CTASection />
      <FooterSection />
    </div>
  )
}

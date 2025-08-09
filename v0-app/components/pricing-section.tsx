"use client"

import { useState } from "react"
import { Check } from "lucide-react"
import { Button } from "@/components/ui/button"

export function PricingSection() {
  const [isAnnual, setIsAnnual] = useState(true)

  const pricingPlans = [
    {
      name: "Free",
      monthlyPrice: "$0",
      annualPrice: "$0",
      description: "Perfect for trying out vibe editing.",
      features: [
        "10 edits per month",
        "Basic photo editing",
        "Standard filters",
        "720p video exports",
        "Community support",
      ],
      buttonText: "Get Started",
      buttonClass: "bg-muted text-muted-foreground hover:bg-muted/80",
    },
    {
      name: "Creator",
      monthlyPrice: "$19",
      annualPrice: "$15",
      description: "For content creators and enthusiasts.",
      features: [
        "Unlimited photo edits",
        "100 video edits per month",
        "Advanced AI filters",
        "4K video exports",
        "Priority support",
        "Custom presets",
        "Batch processing",
      ],
      buttonText: "Start Creating",
      buttonClass: "bg-primary text-primary-foreground hover:bg-primary/90",
      popular: true,
    },
    {
      name: "Pro",
      monthlyPrice: "$49",
      annualPrice: "$39",
      description: "For professionals and agencies.",
      features: [
        "Everything in Creator",
        "Unlimited video edits",
        "API access",
        "White-label exports",
        "Team collaboration",
        "Advanced analytics",
        "Dedicated support",
      ],
      buttonText: "Go Pro",
      buttonClass: "bg-secondary text-secondary-foreground hover:bg-secondary/90",
    },
  ]

  return (
    <section className="w-full px-5 overflow-hidden flex flex-col justify-start items-center my-0 py-8 md:py-14">
      <div className="self-stretch relative flex flex-col justify-center items-center gap-2 py-0">
        <div className="flex flex-col justify-start items-center gap-4">
          <h2 className="text-center text-foreground text-4xl md:text-5xl font-semibold leading-tight md:leading-[40px]">
            Choose Your Creative Plan
          </h2>
          <p className="self-stretch text-center text-muted-foreground text-sm font-medium leading-tight">
            From casual editing to professional workflows, we have a plan that fits your creative needs.
          </p>
        </div>
        <div className="pt-4">
          <div className="p-0.5 bg-muted rounded-lg flex justify-start items-center gap-1 md:mt-0">
            <button
              onClick={() => setIsAnnual(true)}
              className={`pl-2 pr-1 py-1 flex justify-start items-start gap-2 rounded-md ${isAnnual ? "bg-accent shadow-sm" : ""}`}
            >
              <span
                className={`text-center text-sm font-medium leading-tight ${isAnnual ? "text-accent-foreground" : "text-muted-foreground"}`}
              >
                Annually
              </span>
            </button>
            <button
              onClick={() => setIsAnnual(false)}
              className={`px-2 py-1 flex justify-start items-start rounded-md ${!isAnnual ? "bg-accent shadow-sm" : ""}`}
            >
              <span
                className={`text-center text-sm font-medium leading-tight ${!isAnnual ? "text-accent-foreground" : "text-muted-foreground"}`}
              >
                Monthly
              </span>
            </button>
          </div>
        </div>
      </div>
      <div className="self-stretch px-5 flex flex-col md:flex-row justify-start items-start gap-4 md:gap-6 mt-6 max-w-[1100px] mx-auto">
        {pricingPlans.map((plan) => (
          <div
            key={plan.name}
            className={`flex-1 p-4 overflow-hidden rounded-xl flex flex-col justify-start items-start gap-6 ${
              plan.popular
                ? "bg-gradient-to-b from-primary/10 to-primary/5 border border-primary/20"
                : "bg-card/50 border border-border/50"
            }`}
          >
            <div className="self-stretch flex flex-col justify-start items-start gap-6">
              <div className="self-stretch flex flex-col justify-start items-start gap-8">
                <div className="w-full h-5 text-sm font-medium leading-tight text-foreground">
                  {plan.name}
                  {plan.popular && (
                    <div className="ml-2 px-2 overflow-hidden rounded-full justify-center items-center gap-2.5 inline-flex mt-0 py-0.5 bg-primary/20">
                      <div className="text-center text-primary text-xs font-normal leading-tight break-words">
                        Popular
                      </div>
                    </div>
                  )}
                </div>
                <div className="self-stretch flex flex-col justify-start items-start gap-1">
                  <div className="flex justify-start items-center gap-1.5">
                    <div className="relative h-10 flex items-center text-3xl font-medium leading-10 text-foreground">
                      <span className="invisible">{isAnnual ? plan.annualPrice : plan.monthlyPrice}</span>
                      <span
                        className="absolute inset-0 flex items-center transition-all duration-500"
                        style={{
                          opacity: isAnnual ? 1 : 0,
                          transform: `scale(${isAnnual ? 1 : 0.8})`,
                          filter: `blur(${isAnnual ? 0 : 4}px)`,
                        }}
                        aria-hidden={!isAnnual}
                      >
                        {plan.annualPrice}
                      </span>
                      <span
                        className="absolute inset-0 flex items-center transition-all duration-500"
                        style={{
                          opacity: !isAnnual ? 1 : 0,
                          transform: `scale(${!isAnnual ? 1 : 0.8})`,
                          filter: `blur(${!isAnnual ? 0 : 4}px)`,
                        }}
                        aria-hidden={isAnnual}
                      >
                        {plan.monthlyPrice}
                      </span>
                    </div>
                    <div className="text-center text-sm font-medium leading-tight text-muted-foreground">/month</div>
                  </div>
                  <div className="self-stretch text-sm font-medium leading-tight text-muted-foreground">
                    {plan.description}
                  </div>
                </div>
              </div>
              <Button
                className={`self-stretch px-5 py-2 rounded-full flex justify-center items-center ${plan.buttonClass}`}
              >
                <div className="px-1.5 flex justify-center items-center gap-2">
                  <span className="text-center text-sm font-medium leading-tight">{plan.buttonText}</span>
                </div>
              </Button>
            </div>
            <div className="self-stretch flex flex-col justify-start items-start gap-4">
              <div className="self-stretch text-sm font-medium leading-tight text-muted-foreground">
                {plan.name === "Free" ? "What's included:" : "Everything in Free +"}
              </div>
              <div className="self-stretch flex flex-col justify-start items-start gap-3">
                {plan.features.map((feature) => (
                  <div key={feature} className="self-stretch flex justify-start items-center gap-2">
                    <div className="w-4 h-4 flex items-center justify-center">
                      <Check className="w-full h-full text-primary" strokeWidth={2} />
                    </div>
                    <div className="leading-tight font-normal text-sm text-left text-muted-foreground">{feature}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

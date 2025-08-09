"use client"

import { Twitter, Instagram, Youtube } from "lucide-react"
import Image from "next/image"

export function FooterSection() {
  return (
    <footer className="w-full max-w-[1320px] mx-auto px-5 flex flex-col md:flex-row justify-between items-start gap-8 md:gap-0 py-10 md:py-[70px]">
      {/* Left Section: Logo, Description, Social Links */}
      <div className="flex flex-col justify-start items-start gap-8 p-4 md:p-8">
        <div className="flex items-center">
          <Image
            src="/images/clapperlabs-full-logo.png"
            alt="ClapperLabs"
            width={400}
            height={100}
            className="h-24 w-auto"
          />
        </div>
        <p className="text-foreground/90 text-sm font-medium leading-[18px] text-left">
          AI-powered vibe editing for photos and videos
        </p>
        <div className="flex justify-start items-start gap-3">
          <a href="#" aria-label="Twitter" className="w-4 h-4 flex items-center justify-center">
            <Twitter className="w-full h-full text-muted-foreground hover:text-primary transition-colors" />
          </a>
          <a href="#" aria-label="Instagram" className="w-4 h-4 flex items-center justify-center">
            <Instagram className="w-full h-full text-muted-foreground hover:text-primary transition-colors" />
          </a>
          <a href="#" aria-label="YouTube" className="w-4 h-4 flex items-center justify-center">
            <Youtube className="w-full h-full text-muted-foreground hover:text-primary transition-colors" />
          </a>
        </div>
      </div>
      {/* Right Section: Product, Company, Resources */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-8 md:gap-12 p-4 md:p-8 w-full md:w-auto">
        <div className="flex flex-col justify-start items-start gap-3">
          <h3 className="text-muted-foreground text-sm font-medium leading-5">Product</h3>
          <div className="flex flex-col justify-end items-start gap-2">
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Features
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Pricing
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              API
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Mobile App
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Desktop App
            </a>
          </div>
        </div>
        <div className="flex flex-col justify-start items-start gap-3">
          <h3 className="text-muted-foreground text-sm font-medium leading-5">Company</h3>
          <div className="flex flex-col justify-center items-start gap-2">
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              About us
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Blog
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Careers
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Press
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Contact
            </a>
          </div>
        </div>
        <div className="flex flex-col justify-start items-start gap-3">
          <h3 className="text-muted-foreground text-sm font-medium leading-5">Resources</h3>
          <div className="flex flex-col justify-center items-start gap-2">
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Help Center
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Tutorials
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Community
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Templates
            </a>
            <a href="#" className="text-foreground text-sm font-normal leading-5 hover:text-primary transition-colors">
              Privacy Policy
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

import Image from "next/image"

const testimonials = [
  {
    quote:
      "ClapperLabs transformed my Instagram game. I can now edit photos in seconds just by describing the vibe I want. It's like having a professional editor in my pocket.",
    name: "Sarah Chen",
    company: "Content Creator",
    avatar: "/placeholder.svg?height=48&width=48",
    type: "large-coral",
  },
  {
    quote:
      "The AI understands exactly what I mean when I say 'make it more cinematic' or 'add golden hour vibes'. Game changer for video content.",
    name: "Marcus Rodriguez",
    company: "YouTuber",
    avatar: "/placeholder.svg?height=36&width=36",
    type: "small-dark",
  },
  {
    quote:
      "As a wedding photographer, ClapperLabs helps me deliver consistent, beautiful edits to my clients faster than ever before.",
    name: "Emma Thompson",
    company: "Wedding Photographer",
    avatar: "/placeholder.svg?height=36&width=36",
    type: "small-dark",
  },
  {
    quote:
      "The batch processing feature saved me hours of work. I can edit an entire photoshoot with just a few chat commands.",
    name: "David Kim",
    company: "Fashion Photographer",
    avatar: "/placeholder.svg?height=36&width=36",
    type: "small-dark",
  },
  {
    quote: "My TikTok videos have never looked better. The AI knows exactly how to make content pop for social media.",
    name: "Zoe Martinez",
    company: "TikTok Creator",
    avatar: "/placeholder.svg?height=36&width=36",
    type: "small-dark",
  },
  {
    quote:
      "ClapperLabs democratized professional editing. Now anyone can create stunning visuals without years of Photoshop experience.",
    name: "Alex Johnson",
    company: "Creative Director",
    avatar: "/placeholder.svg?height=36&width=36",
    type: "small-dark",
  },
  {
    quote:
      "The mood transformation feature is incredible. I can take a regular photo and turn it into something that perfectly matches my brand aesthetic with just a simple description.",
    name: "Riley Park",
    company: "Brand Designer",
    avatar: "/placeholder.svg?height=48&width=48",
    type: "large-light",
  },
]

const TestimonialCard = ({ quote, name, company, avatar, type }) => {
  const isLargeCard = type.startsWith("large")
  const avatarSize = isLargeCard ? 48 : 36
  const avatarBorderRadius = isLargeCard ? "rounded-[41px]" : "rounded-[30.75px]"
  const padding = isLargeCard ? "p-6" : "p-[30px]"

  let cardClasses = `flex flex-col justify-between items-start overflow-hidden rounded-[10px] shadow-[0px_2px_4px_rgba(0,0,0,0.08)] relative ${padding}`
  let quoteClasses = ""
  let nameClasses = ""
  let companyClasses = ""
  const backgroundElements = null
  let cardHeight = ""
  const cardWidth = "w-full md:w-[384px]"

  if (type === "large-coral") {
    cardClasses += " bg-primary"
    quoteClasses += " text-primary-foreground text-2xl font-medium leading-8"
    nameClasses += " text-primary-foreground text-base font-normal leading-6"
    companyClasses += " text-primary-foreground/60 text-base font-normal leading-6"
    cardHeight = "h-[502px]"
  } else if (type === "large-light") {
    cardClasses += " bg-card/50 border border-border/50"
    quoteClasses += " text-foreground text-2xl font-medium leading-8"
    nameClasses += " text-foreground text-base font-normal leading-6"
    companyClasses += " text-muted-foreground text-base font-normal leading-6"
    cardHeight = "h-[502px]"
  } else {
    cardClasses += " bg-card/30 border border-border/30"
    quoteClasses += " text-foreground/80 text-[17px] font-normal leading-6"
    nameClasses += " text-foreground text-sm font-normal leading-[22px]"
    companyClasses += " text-muted-foreground text-sm font-normal leading-[22px]"
    cardHeight = "h-[244px]"
  }

  return (
    <div className={`${cardClasses} ${cardWidth} ${cardHeight}`}>
      {backgroundElements}
      <div className={`relative z-10 font-normal break-words ${quoteClasses}`}>{quote}</div>
      <div className="relative z-10 flex justify-start items-center gap-3">
        <Image
          src={avatar || "/placeholder.svg"}
          alt={`${name} avatar`}
          width={avatarSize}
          height={avatarSize}
          className={`w-${avatarSize / 4} h-${avatarSize / 4} ${avatarBorderRadius}`}
        />
        <div className="flex flex-col justify-start items-start gap-0.5">
          <div className={nameClasses}>{name}</div>
          <div className={companyClasses}>{company}</div>
        </div>
      </div>
    </div>
  )
}

export function TestimonialSection() {
  return (
    <section className="w-full px-5 overflow-hidden flex flex-col justify-start py-6 md:py-8 lg:py-14">
      <div className="self-stretch py-6 md:py-8 lg:py-14 flex flex-col justify-center items-center gap-2">
        <div className="flex flex-col justify-start items-center gap-4">
          <h2 className="text-center text-foreground text-3xl md:text-4xl lg:text-[40px] font-semibold leading-tight md:leading-tight lg:leading-[40px]">
            Loved by Creators Worldwide
          </h2>
          <p className="self-stretch text-center text-muted-foreground text-sm md:text-sm lg:text-base font-medium leading-[18.20px] md:leading-relaxed lg:leading-relaxed">
            {"See how photographers, content creators, and brands are transforming"} <br />{" "}
            {"their visual content with AI-powered vibe editing"}
          </p>
        </div>
      </div>
      <div className="w-full pt-0.5 pb-4 md:pb-6 lg:pb-10 flex flex-col md:flex-row justify-center items-start gap-4 md:gap-4 lg:gap-6 max-w-[1100px] mx-auto">
        <div className="flex-1 flex flex-col justify-start items-start gap-4 md:gap-4 lg:gap-6">
          <TestimonialCard {...testimonials[0]} />
          <TestimonialCard {...testimonials[1]} />
        </div>
        <div className="flex-1 flex flex-col justify-start items-start gap-4 md:gap-4 lg:gap-6">
          <TestimonialCard {...testimonials[2]} />
          <TestimonialCard {...testimonials[3]} />
          <TestimonialCard {...testimonials[4]} />
        </div>
        <div className="flex-1 flex flex-col justify-start items-start gap-4 md:gap-4 lg:gap-6">
          <TestimonialCard {...testimonials[5]} />
          <TestimonialCard {...testimonials[6]} />
        </div>
      </div>
    </section>
  )
}

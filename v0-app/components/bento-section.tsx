import { MessageSquare, Palette, Sparkles, Zap, ImageIcon, Video } from "lucide-react"

const BentoCard = ({ title, description, icon: Icon, gradient }) => (
  <div className="overflow-hidden rounded-2xl border border-border/50 flex flex-col justify-start items-start relative group hover:border-border transition-colors">
    {/* Background with blur effect */}
    <div
      className={`absolute inset-0 rounded-2xl ${gradient}`}
      style={{
        backdropFilter: "blur(4px)",
        WebkitBackdropFilter: "blur(4px)",
      }}
    />

    <div className="self-stretch p-6 flex flex-col justify-start items-start gap-4 relative z-10">
      <div className="w-12 h-12 rounded-xl bg-card/50 flex items-center justify-center">
        <Icon className="w-6 h-6 text-primary" />
      </div>
      <div className="self-stretch flex flex-col justify-start items-start gap-2">
        <h3 className="text-foreground text-xl font-semibold leading-tight">{title}</h3>
        <p className="text-muted-foreground text-base leading-relaxed">{description}</p>
      </div>
    </div>
  </div>
)

export function BentoSection() {
  const cards = [
    {
      title: "Chat-Based Editing",
      description:
        "Simply describe what you want: 'Make it more vibrant', 'Add vintage vibes', or 'Brighten the shadows'.",
      icon: MessageSquare,
      gradient: "bg-gradient-to-br from-primary/10 to-transparent",
    },
    {
      title: "Mood Transformation",
      description: "Transform the entire mood of your content with AI that understands aesthetic preferences.",
      icon: Palette,
      gradient: "bg-gradient-to-br from-secondary/10 to-transparent",
    },
    {
      title: "Smart Enhancements",
      description: "AI automatically detects and enhances key elements like lighting, color balance, and composition.",
      icon: Sparkles,
      gradient: "bg-gradient-to-br from-coral/10 to-transparent",
    },
    {
      title: "Lightning Fast",
      description: "Get professional-quality edits in seconds, not hours. Perfect for content creators on the go.",
      icon: Zap,
      gradient: "bg-gradient-to-br from-cyan/10 to-transparent",
    },
    {
      title: "Photo & Video Support",
      description: "Works seamlessly with both photos and videos. Edit your entire content library with one tool.",
      icon: ImageIcon,
      gradient: "bg-gradient-to-br from-primary/10 to-transparent",
    },
    {
      title: "Creative Filters",
      description: "Access hundreds of AI-generated filters and effects that adapt to your content automatically.",
      icon: Video,
      gradient: "bg-gradient-to-br from-secondary/10 to-transparent",
    },
  ]

  return (
    <section className="w-full min-h-screen px-8 flex flex-col justify-center items-center overflow-visible bg-transparent">
      <div className="w-full py-16 relative flex flex-col justify-start items-start gap-6">
        <div className="w-[547px] h-[938px] absolute top-[614px] left-[80px] origin-top-left rotate-[-33.39deg] bg-primary/5 blur-[130px] z-0" />
        <div className="self-stretch py-16 flex flex-col justify-center items-center gap-2 z-10">
          <div className="flex flex-col justify-start items-center gap-6">
            <h2 className="w-full max-w-4xl text-center text-foreground text-5xl md:text-7xl font-semibold leading-tight">
              Editing Made Effortless
            </h2>
            <p className="w-full max-w-3xl text-center text-muted-foreground text-xl md:text-2xl font-medium leading-relaxed">
              Experience the future of photo and video editing with AI that understands your creative vision.
            </p>
          </div>
        </div>
        <div className="self-stretch grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 z-10">
          {cards.map((card) => (
            <BentoCard key={card.title} {...card} />
          ))}
        </div>
      </div>
    </section>
  )
}

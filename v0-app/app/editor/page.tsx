"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ArrowLeft, Send, Download, Share } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import { useState } from "react"

export default function EditorPage() {
  const [message, setMessage] = useState("")
  const [chatHistory, setChatHistory] = useState([
    {
      type: "system",
      content: "Hi! I'm your AI editing assistant. Tell me what you'd like to do with your image!",
    },
  ])

  const handleSendMessage = () => {
    if (!message.trim()) return

    const newHistory = [
      ...chatHistory,
      { type: "user", content: message },
      { type: "assistant", content: "Great! I'll apply those changes to your image. Processing..." },
    ]

    setChatHistory(newHistory)
    setMessage("")

    // Simulate AI processing
    setTimeout(() => {
      setChatHistory([
        ...newHistory,
        {
          type: "assistant",
          content: "Done! I've enhanced the saturation and added a warm vintage feel to your image. How does it look?",
        },
      ])
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/30 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Image
              src="/images/clapperlabs-full-logo.png"
              alt="ClapperLabs"
              width={320}
              height={80}
              className="h-20 w-auto"
            />
            <span className="text-muted-foreground">•</span>
            <span className="text-foreground font-medium">Summer Vacation Photo</span>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" className="border-border/50 bg-transparent">
              <Share className="w-4 h-4 mr-2" />
              Share
            </Button>
            <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
              <Download className="w-4 h-4 mr-2" />
              Download
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Image Preview */}
        <div className="flex-1 p-6 flex items-center justify-center bg-muted/5">
          <div className="max-w-4xl w-full">
            <div className="relative aspect-video bg-card/30 border border-border/50 rounded-2xl overflow-hidden">
              <Image
                src="/placeholder.svg?height=600&width=800&text=Your+Image+Preview"
                alt="Image being edited"
                fill
                className="object-cover"
              />
            </div>
          </div>
        </div>

        {/* Chat Panel */}
        <div className="w-96 border-l border-border/50 bg-card/20 backdrop-blur-sm flex flex-col">
          {/* Chat Header */}
          <div className="p-4 border-b border-border/50">
            <h2 className="font-semibold text-foreground">AI Assistant</h2>
            <p className="text-sm text-muted-foreground">Tell me how you want to edit your image</p>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 p-4 space-y-4 overflow-y-auto">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[80%] p-3 rounded-2xl ${
                    msg.type === "user"
                      ? "bg-primary text-primary-foreground"
                      : msg.type === "system"
                        ? "bg-secondary/20 text-foreground border border-border/50"
                        : "bg-card/50 text-foreground border border-border/50"
                  }`}
                >
                  <p className="text-sm">{msg.content}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Chat Input */}
          <div className="p-4 border-t border-border/50">
            <div className="flex gap-2">
              <Input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="e.g., 'Make it more vibrant' or 'Add vintage vibes'"
                className="bg-background/50 border-border/50"
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              />
              <Button
                onClick={handleSendMessage}
                size="icon"
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
            <div className="mt-2 flex flex-wrap gap-2">
              {["Make it brighter", "Add warmth", "Vintage look", "More contrast"].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setMessage(suggestion)}
                  className="text-xs px-2 py-1 bg-card/50 border border-border/50 rounded-full text-muted-foreground hover:text-foreground hover:bg-card/80 transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

"use client"

import { Button } from "@/components/ui/button"
import { Plus, ImageIcon, Video, MoreHorizontal, Search } from "lucide-react"
import Image from "next/image"
import { useState } from "react"
import { useRouter } from "next/navigation"

// Mock project data
const mockProjects = [
  {
    id: 1,
    name: "Summer Vacation Photos",
    type: "photo",
    thumbnail: "/placeholder.svg?height=200&width=300&text=Summer+Photos",
    lastEdited: "2 hours ago",
    status: "completed",
  },
  {
    id: 2,
    name: "Product Launch Video",
    type: "video",
    thumbnail: "/placeholder.svg?height=200&width=300&text=Product+Video",
    lastEdited: "1 day ago",
    status: "in-progress",
  },
  {
    id: 3,
    name: "Portrait Session",
    type: "photo",
    thumbnail: "/placeholder.svg?height=200&width=300&text=Portraits",
    lastEdited: "3 days ago",
    status: "completed",
  },
]

export default function DashboardPage() {
  const [projects, setProjects] = useState(mockProjects)
  const [searchQuery, setSearchQuery] = useState("")
  const router = useRouter()

  const handleNewProject = () => {
    router.push("/upload")
  }

  const filteredProjects = projects.filter((project) => project.name.toLowerCase().includes(searchQuery.toLowerCase()))

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/30 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
          <div className="flex items-center">
            <Image
              src="/images/clapperlabs-full-logo.png"
              alt="ClapperLabs"
              width={320}
              height={80}
              className="h-20 w-auto"
            />
          </div>
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <input
                type="text"
                placeholder="Search projects..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 bg-background/50 border border-border/50 rounded-full text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 w-64"
              />
            </div>
            <Button
              onClick={handleNewProject}
              className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-full px-6"
            >
              <Plus className="w-4 h-4 mr-2" />
              New Project
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold text-foreground mb-2">Your Projects</h1>
          <p className="text-muted-foreground">Manage and edit your photos and videos with AI</p>
        </div>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {/* New Project Card */}
          <div
            onClick={handleNewProject}
            className="group cursor-pointer bg-card/30 border-2 border-dashed border-border/50 rounded-2xl p-8 flex flex-col items-center justify-center text-center hover:border-primary/50 hover:bg-card/50 transition-all duration-200 min-h-[280px]"
          >
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
              <Plus className="w-8 h-8 text-primary" />
            </div>
            <h3 className="text-lg font-medium text-foreground mb-2">Start New Project</h3>
            <p className="text-muted-foreground text-sm">Upload a photo or video to begin editing</p>
          </div>

          {/* Existing Projects */}
          {filteredProjects.map((project) => (
            <div
              key={project.id}
              className="group cursor-pointer bg-card/30 border border-border/50 rounded-2xl overflow-hidden hover:border-border hover:bg-card/50 transition-all duration-200"
            >
              <div className="relative aspect-video bg-muted/20">
                <Image src={project.thumbnail || "/placeholder.svg"} alt={project.name} fill className="object-cover" />
                <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Button variant="ghost" size="icon" className="bg-background/80 hover:bg-background">
                    <MoreHorizontal className="w-4 h-4" />
                  </Button>
                </div>
                <div className="absolute bottom-3 left-3">
                  <div className="flex items-center gap-1 bg-background/80 backdrop-blur-sm rounded-full px-2 py-1">
                    {project.type === "photo" ? (
                      <ImageIcon className="w-3 h-3 text-primary" />
                    ) : (
                      <Video className="w-3 h-3 text-secondary" />
                    )}
                    <span className="text-xs font-medium text-foreground capitalize">{project.type}</span>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-medium text-foreground mb-1 truncate">{project.name}</h3>
                <div className="flex items-center justify-between text-sm text-muted-foreground">
                  <span>{project.lastEdited}</span>
                  <span
                    className={`px-2 py-1 rounded-full text-xs ${
                      project.status === "completed" ? "bg-primary/10 text-primary" : "bg-secondary/10 text-secondary"
                    }`}
                  >
                    {project.status === "completed" ? "Completed" : "In Progress"}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredProjects.length === 0 && searchQuery && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No projects found matching "{searchQuery}"</p>
          </div>
        )}
      </main>
    </div>
  )
}

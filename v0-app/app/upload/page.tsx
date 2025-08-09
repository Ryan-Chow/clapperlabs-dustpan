"use client"

import type React from "react"

import { Button } from "@/components/ui/button"
import { Upload, ImageIcon, Video, ArrowLeft } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import { useState, useRef } from "react"
import { useRouter } from "next/navigation"

export default function UploadPage() {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const router = useRouter()

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFile(files[0])
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files[0]) {
      handleFile(files[0])
    }
  }

  const handleFile = (file: File) => {
    if (file.type.startsWith("image/") || file.type.startsWith("video/")) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      // Simulate upload and redirect to editor
      console.log("Uploading file:", selectedFile.name)
      // In a real app, you would upload the file here
      router.push("/editor")
    }
  }

  const openFileDialog = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="min-h-screen bg-background">
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
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-12">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-semibold text-foreground mb-4">Upload Your Content</h1>
          <p className="text-xl text-muted-foreground">
            Choose a photo or video to start your AI-powered vibe editing journey
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          {!selectedFile ? (
            <div
              className={`relative border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-200 ${
                dragActive ? "border-primary bg-primary/5" : "border-border/50 hover:border-border hover:bg-card/30"
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*,video/*"
                onChange={handleFileInput}
                className="hidden"
              />

              <div className="flex flex-col items-center gap-6">
                <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center">
                  <Upload className="w-10 h-10 text-primary" />
                </div>

                <div>
                  <h3 className="text-2xl font-medium text-foreground mb-2">Drop your files here</h3>
                  <p className="text-muted-foreground mb-6">
                    or{" "}
                    <button onClick={openFileDialog} className="text-primary hover:text-primary/80 font-medium">
                      browse to upload
                    </button>
                  </p>
                </div>

                <div className="flex items-center gap-8 text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <ImageIcon className="w-5 h-5" />
                    <span>Photos</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Video className="w-5 h-5" />
                    <span>Videos</span>
                  </div>
                </div>

                <p className="text-sm text-muted-foreground">Supports JPG, PNG, GIF, MP4, MOV up to 100MB</p>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Preview */}
              <div className="bg-card/30 border border-border/50 rounded-2xl p-6">
                <h3 className="text-lg font-medium text-foreground mb-4">Preview</h3>
                <div className="relative aspect-video bg-muted/20 rounded-xl overflow-hidden">
                  {selectedFile.type.startsWith("image/") ? (
                    <Image src={previewUrl! || "/placeholder.svg"} alt="Preview" fill className="object-cover" />
                  ) : (
                    <video src={previewUrl!} className="w-full h-full object-cover" controls />
                  )}
                </div>
                <div className="mt-4 flex items-center justify-between">
                  <div>
                    <p className="font-medium text-foreground">{selectedFile.name}</p>
                    <p className="text-sm text-muted-foreground">{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSelectedFile(null)
                      setPreviewUrl(null)
                    }}
                  >
                    Remove
                  </Button>
                </div>
              </div>

              {/* Upload Button */}
              <div className="flex justify-center">
                <Button
                  onClick={handleUpload}
                  className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 py-3"
                >
                  Start Editing
                </Button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

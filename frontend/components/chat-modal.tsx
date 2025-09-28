"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  text: string
  sender: "user" | "other"
  timestamp: Date
  senderName: string
  senderAvatar?: string
}

interface ChatModalProps {
  isOpen: boolean
  onClose: () => void
  recipientName: string
  recipientAvatar?: string
  currentUserName?: string
  currentUserAvatar?: string
}

export function ChatModal({
  isOpen,
  onClose,
  recipientName,
  recipientAvatar,
  currentUserName = "You",
  currentUserAvatar,
}: ChatModalProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hey! Are you here?",
      sender: "other",
      timestamp: new Date(Date.now() - 300000),
      senderName: recipientName,
      senderAvatar: recipientAvatar,
    },
    {
      id: "2",
      text: "Yeah...",
      sender: "user",
      timestamp: new Date(Date.now() - 240000),
      senderName: currentUserName,
      senderAvatar: currentUserAvatar,
    },
    {
      id: "3",
      text: "Great work on the slides! Love it! Just one more thing...",
      sender: "other",
      timestamp: new Date(Date.now() - 180000),
      senderName: recipientName,
      senderAvatar: recipientAvatar,
    },
  ])

  const [newMessage, setNewMessage] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  const handleSendMessage = () => {
    if (!newMessage.trim()) return

    const message: Message = {
      id: Date.now().toString(),
      text: newMessage,
      sender: "user",
      timestamp: new Date(),
      senderName: currentUserName,
      senderAvatar: currentUserAvatar,
    }

    setMessages((prev) => [...prev, message])
    setNewMessage("")
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    })
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md h-[600px] p-0 overflow-hidden chat-gradient">
        <div className="flex flex-col h-full">
          {/* Header */}
          <DialogHeader className="flex-row items-center justify-between p-4 pb-3 space-y-0 bg-white/20 backdrop-blur-sm border-b border-white/20">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={recipientAvatar || "/placeholder.svg"} alt={recipientName} />
                  <AvatarFallback className="bg-primary text-primary-foreground text-sm">
                    {recipientName.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
              </div>
              <div>
                <DialogTitle className="text-sm font-medium text-white">{recipientName}</DialogTitle>
                <p className="text-xs text-white/70">Online</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="h-8 w-8 p-0 text-white/70 hover:text-white hover:bg-white/10"
            >
              <X className="h-4 w-4" />
            </Button>
          </DialogHeader>

          {/* Messages */}
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn("flex gap-3 max-w-[85%]", message.sender === "user" ? "ml-auto flex-row-reverse" : "")}
                >
                  <Avatar className="h-6 w-6 flex-shrink-0">
                    <AvatarImage src={message.senderAvatar || "/placeholder.svg"} alt={message.senderName} />
                    <AvatarFallback className="bg-primary text-primary-foreground text-xs">
                      {message.senderName.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  <div className={cn("flex flex-col gap-1", message.sender === "user" ? "items-end" : "items-start")}>
                    <div className="flex items-center gap-2 text-xs text-white/60">
                      <span>{formatTime(message.timestamp)}</span>
                    </div>
                    <div
                      className={cn(
                        "rounded-2xl px-4 py-2 max-w-xs break-words",
                        message.sender === "user"
                          ? "bg-primary text-primary-foreground rounded-br-md"
                          : "bg-white/90 text-gray-800 rounded-bl-md",
                      )}
                    >
                      <p className="text-sm leading-relaxed">{message.text}</p>
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Input */}
          <div className="p-4 pt-2 bg-white/10 backdrop-blur-sm border-t border-white/20">
            <div className="flex gap-2">
              <Input
                ref={inputRef}
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter Message"
                className="flex-1 bg-white/90 border-white/30 text-gray-800 placeholder:text-gray-500 focus:bg-white focus:border-primary"
              />
              <Button
                onClick={handleSendMessage}
                disabled={!newMessage.trim()}
                size="sm"
                className="px-3 bg-primary hover:bg-primary/90 text-primary-foreground"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

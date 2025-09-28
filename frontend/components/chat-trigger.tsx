"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { MessageCircle } from "lucide-react"
import { ChatModal } from "./chat-modal"

interface ChatTriggerProps {
  recipientName: string
  recipientAvatar?: string
  currentUserName?: string
  currentUserAvatar?: string
  variant?: "default" | "floating"
}

export function ChatTrigger({
  recipientName,
  recipientAvatar,
  currentUserName,
  currentUserAvatar,
  variant = "default",
}: ChatTriggerProps) {
  const [isOpen, setIsOpen] = useState(false)

  if (variant === "floating") {
    return (
      <>
        <Button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg bg-primary hover:bg-primary/90 text-primary-foreground z-50"
          size="sm"
        >
          <MessageCircle className="h-6 w-6" />
        </Button>
        <ChatModal
          isOpen={isOpen}
          onClose={() => setIsOpen(false)}
          recipientName={recipientName}
          recipientAvatar={recipientAvatar}
          currentUserName={currentUserName}
          currentUserAvatar={currentUserAvatar}
        />
      </>
    )
  }

  return (
    <>
      <Button onClick={() => setIsOpen(true)} variant="outline" className="gap-2">
        <MessageCircle className="h-4 w-4" />
        Message {recipientName}
      </Button>
      <ChatModal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        recipientName={recipientName}
        recipientAvatar={recipientAvatar}
        currentUserName={currentUserName}
        currentUserAvatar={currentUserAvatar}
      />
    </>
  )
}

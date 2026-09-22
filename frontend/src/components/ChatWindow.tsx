import { useEffect, useRef } from "react";
import type { Message } from "../types/chat";
import { MessageBubble } from "./MessageBubble";

export function ChatWindow({ messages }: { messages: Message[] }) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="empty-state">
          <h1>AI Agent</h1>
          <p>Ask me anything. I can search the web, read files, and run code.</p>
        </div>
      )}
      {messages.map((m, i) => (
        <MessageBubble key={i} message={m} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
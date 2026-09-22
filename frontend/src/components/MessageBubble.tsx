import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Message } from "../types/chat";

export function MessageBubble({ message }: { message: Message }) {
  if (message.role === "tool") {
    return (
      <div className="tool-badge">
        🔧 <strong>{message.toolName}</strong> — {message.content}
      </div>
    );
  }

  const isUser = message.role === "user";

  return (
    <div className={`bubble ${isUser ? "user" : "assistant"}`}>
      {isUser ? (
        <p>{message.content}</p>
      ) : (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {message.content}
        </ReactMarkdown>
      )}
    </div>
  );
}
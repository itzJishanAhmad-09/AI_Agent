import { useState } from "react";
import { ChatWindow } from "./components/ChatWindow";
import { InputBar } from "./components/InputBar";
import { streamChat } from "./api/chat";
import type { Message } from "./types/chat";

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(text: string) {
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);

    let assistantContent = "";
    let assistantIndex = -1;

    setMessages((m) => {
      assistantIndex = m.length;
      return [...m, { role: "assistant", content: "" }];
    });

    try {
      for await (const event of streamChat(text)) {
        if (event.type === "text") {
          assistantContent += event.content;
          setMessages((m) => {
            const copy = [...m];
            copy[assistantIndex] = {
              role: "assistant",
              content: assistantContent,
            };
            return copy;
          });
        } else if (event.type === "tool_start") {
          setMessages((m) => [
            ...m,
            { role: "tool", toolName: event.tool, content: "running..." },
          ]);
        } else if (event.type === "tool_end") {
          setMessages((m) => {
            const copy = [...m];
            const lastTool = copy.map((x) => x.role).lastIndexOf("tool");
            if (lastTool >= 0) {
              copy[lastTool] = {
                role: "tool",
                toolName: event.tool,
                content: event.result,
              };
            }
            return copy;
          });
        } else if (event.type === "error") {
          setMessages((m) => [
            ...m,
            { role: "assistant", content: `Error: ${event.message}` },
          ]);
        }
      }
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Connection error: ${String(e)}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <ChatWindow messages={messages} />
      <InputBar onSend={handleSend} disabled={loading} />
    </div>
  );
}
"use client";

import { Bot, Send, User } from "lucide-react";
import { useState } from "react";

interface Message {
  role: "user" | "assistant";
  text: string;
}

export default function ChatBox() {
  const [input, setInput] = useState("");

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text: "Upload an outfit and I'll help you find similar pieces.",
    },
  ]);

  function sendMessage() {
    if (!input.trim()) return;

    const text = input;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text,
      },
      {
        role: "assistant",
        text: "Got it. We'll use your preference to refine the results.",
      },
    ]);

    setInput("");
  }

  return (
    <section className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03]">

      <div className="border-b border-white/10 p-5">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-black">
            <Bot size={18} />
          </div>

          <div>
            <p className="text-sm font-semibold">
              DripSearch AI
            </p>

            <p className="text-xs text-white/40">
              Your personal style assistant
            </p>
          </div>
        </div>
      </div>

      <div className="max-h-[350px] space-y-4 overflow-y-auto p-4">

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              message.role === "user"
                ? "flex-row-reverse"
                : ""
            }`}
          >
            <div className="mt-1 shrink-0">
              {message.role === "user" ? (
                <User size={15} className="text-white/40" />
              ) : (
                <Bot size={15} className="text-white/40" />
              )}
            </div>

            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
                message.role === "user"
                  ? "bg-white text-black"
                  : "bg-white/10 text-white/80"
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}
      </div>

      <div className="border-t border-white/10 p-3">
        <div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-black/40 p-2">

          <input
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
            placeholder="Ask about your results..."
            className="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none placeholder:text-white/30"
          />

          <button
            onClick={sendMessage}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-black transition hover:scale-105"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </section>
  );
}
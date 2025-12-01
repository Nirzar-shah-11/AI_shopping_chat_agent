import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    const userMsg = { sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: text }),
    });

    const data = await res.json();

    // Format product results or comparison text into readable chat format
    let botText = data.answer;

    if (data.products && Array.isArray(data.products) && data.products.length > 0) {
      botText += "\n\nHere are the results:\n";
      data.products.forEach((p, i) => {
        botText += `\n${i + 1}. ${p.name}`;
        if (p.price) botText += ` — ${p.price}`;
        if (p.description) botText += `\n   ${p.description}`;
      });
    }

    const botMsg = { sender: "bot", text: botText };
    setMessages((prev) => [...prev, botMsg]);
  };

  return (
    <div className="w-screen h-screen bg-gray-100 p-6">
      <h1 className="text-3xl text-black font-bold mb-4 text-center">AI Shopping Chat Agent</h1>
      <ChatWindow messages={messages} onSend={handleSend} />
    </div>
  );
}

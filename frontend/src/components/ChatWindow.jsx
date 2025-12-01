import React, { useState } from "react";

export default function ChatWindow({ messages, onSend }) {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div className="flex flex-col bg-white rounded-lg h-[85vh] p-4">
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4 border-b pb-4 flex flex-col gap-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-md max-w-[80%] whitespace-pre-line ${
              msg.sender === "user"
                ? "bg-blue-400 self-end"
                : "bg-gray-200 self-start"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="flex gap-2 border-t pt-3">
        <input
          className="flex-1 p-2 border rounded-md"
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-4 py-2 rounded-md"
        >
          Send
        </button>
      </div>

    </div>
  );
}

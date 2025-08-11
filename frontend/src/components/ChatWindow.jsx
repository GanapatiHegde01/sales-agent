import React, { useState } from "react";

export default function ChatWindow({ onSend, prefill }) {
  const [text, setText] = useState(prefill || "");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      await onSend(text.trim());
      setText("");
    } finally { setLoading(false); }
  };

  return (
    <div className="w-full">
      <div className="flex gap-2">
        <input value={text} onChange={(e)=>setText(e.target.value)} placeholder="Ask about products, offers or warranty..." className="flex-1 border p-2 rounded" />
        <button onClick={send} className="bg-blue-600 text-white px-3 py-2 rounded">{loading ? "..." : "Send"}</button>
      </div>
    </div>
  );
}

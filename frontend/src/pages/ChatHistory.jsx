import React, { useEffect, useState } from "react";
import { getHistory, deleteChat, clearAllChats } from "../services/chat";

export default function ChatHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const data = await getHistory(1, 50);
      setHistory(data.chats || []);
    } finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const onDelete = async (id) => {
    await deleteChat(id);
    load();
  };

  const onClear = async () => {
    if (!confirm("Clear all chat history?")) return;
    await clearAllChats();
    load();
  };

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Chat History</h2>
        <button onClick={onClear} className="text-red-600">Clear All</button>
      </div>

      {loading ? <div>Loading...</div> : (
        <div className="space-y-4">
          {history.length === 0 && <div>No chats yet.</div>}
          {history.map(c => (
            <div key={c.id} className="border p-3 rounded">
              <div className="text-sm text-gray-500">{new Date(c.created_at).toLocaleString()}</div>
              <div><strong>Q:</strong> {c.query}</div>
              <div className="mt-2"><strong>A:</strong> {c.response}</div>
              <div className="mt-2">
                <button onClick={()=>onDelete(c.id)} className="text-red-600 text-sm">Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

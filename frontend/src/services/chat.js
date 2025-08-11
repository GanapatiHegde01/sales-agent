import api from "./api";

export const sendMessage = async (message) => {
  const res = await api.post("/chat", { message });
  return res.data; // { reply, facts }
};

export const getHistory = async (page = 1, per_page = 20) => {
  const res = await api.get("/chat-history", { params: { page, per_page } });
  return res.data;
};

export const deleteChat = async (id) => {
  const res = await api.delete(`/chat-history/${id}`);
  return res.data;
};

export const clearAllChats = async () => {
  const res = await api.delete("/chat-history/clear");
  return res.data;
};

export const searchChatHistory = async (query, page = 1, per_page = 20) => {
  const res = await api.get("/chat-history/search", { params: { query, page, per_page } });
  return res.data;
};

import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { sendMessage, getHistory, deleteChat, searchChatHistory } from "../services/chat";

export default function Chat() {
  const location = useLocation();
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchTimeout, setSearchTimeout] = useState(null);

  useEffect(() => {
    if (location.state?.prefill) setText(location.state.prefill);
    loadHistory();
  }, [location]);

  const loadHistory = async () => {
    try {
      const data = await getHistory(1, 20);
      setHistory(data.chats || []);
    } catch (e) {
      console.error('Failed to load history:', e);
    }
  };

  const handleSearch = async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      setIsSearching(false);
      return;
    }
    
    try {
      setIsSearching(true);
      console.log('Searching for:', query);
      const data = await searchChatHistory(query);
      console.log('Search results:', data);
      setSearchResults(data.chats || []);
    } catch (e) {
      console.error('Search failed:', e);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  useEffect(() => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
    
    if (searchQuery.trim()) {
      const timeout = setTimeout(() => {
        handleSearch(searchQuery);
      }, 500);
      setSearchTimeout(timeout);
    } else {
      setSearchResults([]);
      setIsSearching(false);
    }
    
    return () => {
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
    };
  }, [searchQuery]);

  const onSend = async () => {
    if (!text.trim()) return;
    const userMessage = text.trim();
    setMessages(m => [...m, { role: "user", text: userMessage }]);
    setText("");
    setLoading(true);
    
    try {
      const data = await sendMessage(userMessage);
      setMessages(m => [...m, { role: "agent", text: data.reply }]);
      loadHistory(); // Refresh history
    } catch (e) {
      setMessages(m => [...m, { role: "agent", text: "Sorry, failed to get reply." }]);
    } finally {
      setLoading(false);
    }
  };

  const onDeleteHistory = async (id) => {
    try {
      await deleteChat(id);
      loadHistory();
    } catch (e) {
      console.error('Failed to delete chat:', e);
    }
  };

  const loadHistoryChat = (chat) => {
    setMessages([
      { role: "user", text: chat.query },
      { role: "agent", text: chat.response }
    ]);
  };

  return (
    <div className="flex h-[calc(100vh-120px)] gap-4">
      {/* Chat Area */}
      <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Inquiro AI Assistant</h2>
          <button 
            onClick={() => setShowHistory(!showHistory)}
            className="md:hidden bg-blue-600 text-white px-3 py-1 rounded text-sm"
          >
            {showHistory ? 'Hide' : 'Show'} History
          </button>
        </div>
        
        {/* Messages */}
        <div className="flex-1 p-4 overflow-y-auto space-y-3">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
              <p>👋 Hi! I'm your AI sales assistant.</p>
              <p>Ask me about products, offers, or warranties!</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-xs lg:max-w-2xl px-4 py-3 rounded-lg ${
                m.role === "user" 
                  ? "bg-blue-600 text-white" 
                  : "bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-600"
              }`}>
                <div className="text-sm leading-relaxed text-gray-800 dark:text-gray-200">
                  {m.text.split('\n').map((line, idx) => {
                    if (line.trim() === '') return <br key={idx} />;
                    
                    // Handle bullet points with *
                    if (line.trim().startsWith('* ')) {
                      const content = line.replace(/^\* /, '');
                      return (
                        <div key={idx} className="flex items-start mb-2">
                          <span className="text-primary-600 dark:text-primary-400 mr-2 mt-1">•</span>
                          <span dangerouslySetInnerHTML={{ __html: content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                        </div>
                      );
                    }
                    
                    // Handle regular text with **bold** formatting
                    return (
                      <div key={idx} className="mb-1" dangerouslySetInnerHTML={{ 
                        __html: line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
                      }} />
                    );
                  })}
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 px-4 py-2 rounded-lg">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Input */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex gap-2">
            <input 
              value={text} 
              onChange={(e) => setText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && onSend()}
              placeholder="Ask about products, offers, or warranties..."
              className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <button 
              onClick={onSend}
              disabled={loading || !text.trim()}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300"
            >
              {loading ? '...' : 'Send'}
            </button>
          </div>
        </div>
      </div>
      
      {/* History Sidebar */}
      <div className={`w-80 bg-white dark:bg-gray-800 rounded-lg shadow ${showHistory ? 'block' : 'hidden md:block'}`}>
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Chat History</h3>
          <div className="relative">
            <input
              type="text"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <svg className="absolute right-3 top-2.5 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        <div className="h-full overflow-y-auto p-4 space-y-3">
          {isSearching ? (
            <div className="flex items-center justify-center py-4">
              <div className="animate-spin w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full"></div>
              <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">Searching...</span>
            </div>
          ) : searchQuery ? (
            searchResults.length === 0 ? (
              <p className="text-gray-500 dark:text-gray-400 text-sm">No results found</p>
            ) : (
              searchResults.map(chat => (
                <div key={chat.id} className="border border-gray-200 dark:border-gray-600 rounded-lg p-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {new Date(chat.created_at).toLocaleDateString()}
                    </span>
                    <button 
                      onClick={(e) => { e.stopPropagation(); onDeleteHistory(chat.id); }}
                      className="text-red-500 hover:text-red-700 text-xs"
                    >
                      ×
                    </button>
                  </div>
                  <div onClick={() => loadHistoryChat(chat)}>
                    <p className="text-sm font-medium truncate text-gray-900 dark:text-white">{chat.query}</p>
                    <p className="text-xs text-gray-600 dark:text-gray-300 mt-1 line-clamp-2">{chat.response}</p>
                  </div>
                </div>
              ))
            )
          ) : history.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 text-sm">No chat history yet</p>
          ) : (
            history.map(chat => (
              <div key={chat.id} className="border border-gray-200 dark:border-gray-600 rounded-lg p-3 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {new Date(chat.created_at).toLocaleDateString()}
                  </span>
                  <button 
                    onClick={(e) => { e.stopPropagation(); onDeleteHistory(chat.id); }}
                    className="text-red-500 hover:text-red-700 text-xs"
                  >
                    ×
                  </button>
                </div>
                <div onClick={() => loadHistoryChat(chat)}>
                  <p className="text-sm font-medium truncate text-gray-900 dark:text-white">{chat.query}</p>
                  <p className="text-xs text-gray-600 dark:text-gray-300 mt-1 line-clamp-2">{chat.response}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

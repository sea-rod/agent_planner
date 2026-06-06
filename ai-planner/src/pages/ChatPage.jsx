import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router';
import { supabase } from '../supabaseClient';
import api from '../api';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: 'Good evening, Hehe. How may I refine your time today?',
      meta: 'You have 3 events tomorrow and 2 hours blocked for deep work.',
      time: 'just now',
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef(null);
  const textareaRef = useRef(null);
  const [user, setUser] = useState(null);
  const [threadId, setThreadId] = useState('');

  const navigate = useNavigate()

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user)
      supabase.from("calendar_tokens").select("user_id").eq("user_id",user.id).then((res) => {
        if (res.data) {
          navigate("/connector")
        }
      })
    });
    setThreadId(crypto.randomUUID());
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  // Handle textarea auto-resize
  const handleInput = (e) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    setIsTyping(true);
    if (!input.trim()) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: input,
      time: 'just now',
    };

    // const { data: { session } } = await supabase.auth.getSession();



    // const data = {
    //   "message":input,
    //   "thread_id":session.access_token
    // }

    const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    api.post("/agent-chat", {
      "message": input,
      "thread_id": threadId,
      "time_zone": userTimeZone
    }).then((res) => {
      const aiResponse = {
        id: Date.now() + 1,
        sender: 'ai',
        text: res.data.reply,
        action: "",
        time: 'just now',
      };

      setMessages((prev) => [...prev, aiResponse])
      setIsTyping(false);


    }).catch((err) => {

      console.log(err);
      const aiResponse = {
        id: Date.now() + 1,
        sender: 'ai',
        text: "Error please try again",
        action: "View suggested schedule →",
        time: 'just now',
      };

      setMessages((prev) => [...prev, aiResponse])
      setIsTyping(false);
    })




    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';


  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  return (
    <div className="bg-[#0F172A] text-[#FAFAFA] min-h-screen flex flex-col font-sans antialiased">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-[#0F172A]/95 backdrop-blur-md border-b border-[#C9A96E]/10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16 sm:h-20">
            <div className="flex items-center gap-2.5">
              <div className="text-2xl sm:text-3xl font-serif font-bold tracking-tight text-[#C9A96E]">Atelier</div>
              <span className="hidden xs:inline text-xs sm:text-sm text-[#94A3B8] font-light tracking-wider uppercase">Time Curator</span>
            </div>
            <Link to="/" className="text-[#94A3B8] hover:text-[#C9A96E] transition text-sm sm:text-base font-light">
              ← Dashboard
            </Link>
          </div>
        </div>
      </header>

      {/* Chat messages area */}
      <main className="flex-1 pt-20 pb-32 overflow-hidden flex flex-col">
        <div
          ref={chatContainerRef}
          className="flex-1 overflow-y-auto px-4 sm:px-6 pt-5 pb-6 max-w-4xl mx-auto w-full space-y-6 scroll-smooth"
        >
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex items-start gap-3 sm:gap-4 animate-fade-in ${msg.sender === 'user' ? 'justify-end' : ''}`}
            >
              {msg.sender === 'ai' && (
                <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-full bg-[#C9A96E]/20 flex-shrink-0 flex items-center justify-center text-xl sm:text-2xl">
                  🕰️
                </div>
              )}
              <div className={`${msg.sender === 'user'
                  ? 'bg-[#C9A96E]/90 text-[#0F172A] rounded-tr-none'
                  : 'bg-[#1E293B]/60 backdrop-blur-sm rounded-tl-none'
                } rounded-2xl px-4 py-3 sm:px-5 sm:py-4 max-w-[85%] sm:max-w-[72%] shadow-sm`}
              >
                {msg.sender === 'ai' && <p className="text-[#94A3B8] text-xs sm:text-sm mb-1">Atelier • {msg.time}</p>}
                <p className="text-sm sm:text-base leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                {msg.meta && <p className="mt-2 text-[#94A3B8] text-xs sm:text-sm italic font-light">{msg.meta}</p>}
                {msg.action && <p className="mt-2 text-[#C9A96E] text-sm font-medium cursor-pointer hover:underline">{msg.action}</p>}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex items-start gap-3 sm:gap-4 animate-fade-in">
              <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-full bg-[#C9A96E]/20 flex-shrink-0 flex items-center justify-center text-xl">🕰️</div>
              <div className="bg-[#1E293B]/60 backdrop-blur-sm rounded-2xl rounded-tl-none px-5 py-4">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-[#94A3B8] rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-[#94A3B8] rounded-full animate-bounce [animation-delay:0.2s]"></div>
                  <div className="w-2 h-2 bg-[#94A3B8] rounded-full animate-bounce [animation-delay:0.4s]"></div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Input area */}
      <footer className="fixed bottom-0 left-0 right-0 bg-[#0F172A]/95 backdrop-blur-lg border-t border-[#C9A96E]/10 py-4 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={sendMessage} className="flex items-end gap-2 sm:gap-3">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              rows="1"
              placeholder="Ask me anything about your schedule..."
              className="flex-1 min-h-[52px] resize-none bg-[#1E293B]/40 backdrop-blur-md border border-[#C9A96E]/20 rounded-2xl px-4 py-3 sm:px-5 sm:py-4 text-sm sm:text-base text-white placeholder-[#94A3B8] focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E] outline-none max-h-40 overflow-y-auto leading-relaxed transition-all"
            />
            <button
              type="submit"
              disabled={!input.trim()}
              className="bg-[#C9A96E] text-[#0F172A] p-3.5 sm:p-4 rounded-full hover:bg-[#D4B978] transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed w-12 h-12 sm:w-14 sm:h-14 flex items-center justify-center flex-shrink-0"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
          </form>
          <p className="text-center text-xs text-[#94A3B8] mt-3 opacity-80">
            Atelier may suggest calendar changes • Always confirm
          </p>
        </div>
      </footer>
    </div>
  );
};

export default ChatPage;
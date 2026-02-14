import { Link } from "react-router";
import { supabase } from "../supabaseClient";
import { useEffect, useState } from 'react';
import React from "react";
import logo from '../assets/vite.svg'

const Navbar = () => {
  const [user, setUser] = useState(null);
  const [isOpen, setIsOpen] = useState(false); // State for mobile menu toggle

  useEffect(() => {
    const checkUser = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      setUser(session?.user.aud);
    };
    checkUser();

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (event === 'SIGNED_IN' && session?.provider_token) {
        const { error } = await supabase.from('user_integrations').upsert({
          user_id: session.user.id,
          google_access_token: session.provider_token,
          google_refresh_token: session.provider_refresh_token,
          updated_at: new Date()
        },
          { onConflict: 'user_id' });
        if (error) console.error("Error syncing to DB:", error.message);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

const logout = async () => {
  try {
    // 'global' scope ensures the session is cleared across all tabs/windows
    const { error } = await supabase.auth.signOut({ scope: 'global' });
    
    if (error) {
      console.error("Logout error:", error.message);
      return;
    }

    window.location.assign("/"); 
  } catch (err) {
    console.error("Unexpected error during logout:", err);
  }
};
  const navLinks = ['Features', 'Craftsmanship', 'Exclusivity'];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0F172A]/95 backdrop-blur-md border-b border-[#C9A96E]/10">
      <div className="max-w-7xl mx-auto px-6 lg:px-10">
        <div className="flex justify-between items-center h-24">

          {/* Logo Section */}
          <div className="flex items-center space-x-3">
            <img src={logo} className="w-10 h-10 md:w-12 md:h-12" alt="Atelier Logo" />
            <span className="text-2xl md:text-3xl font-serif font-bold tracking-tight text-[#C9A96E]">
              Atelier
            </span>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-10">
            {navLinks.map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                className="text-[#94A3B8] hover:text-[#C9A96E] font-medium transition tracking-wide text-sm uppercase"
              >
                {item}
              </a>
            ))}
          </div>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <>
                <Link to="chat" className="bg-[#C9A96E] text-[#0F172A] px-6 py-4 rounded-full font-semibold hover:bg-[#D4B978] transition shadow-lg text-xs uppercase tracking-wider">
                  Chat to Schedule
                </Link>
                <button onClick={logout} className="text-[#94A3B8] hover:text-[#7B241C] transition font-semibold text-xs uppercase tracking-wider">
                  Logout
                </button>
              </>
            ) : (
              <Link to="auth" className="bg-[#C9A96E] text-[#0F172A] px-8 py-3 rounded-full font-semibold hover:bg-[#D4B978] transition shadow-lg text-xs uppercase tracking-wider">
                Begin Your Journey
              </Link>
            )}
          </div>

          {/* Mobile Menu Button (Hamburger) */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-[#C9A96E] focus:outline-none p-2"
            >
              <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Dropdown Menu */}
      <div className={`md:hidden bg-[#0F172A] border-b border-[#C9A96E]/10 transition-all duration-300 ease-in-out ${isOpen ? 'max-h-screen opacity-100 py-6' : 'max-h-0 opacity-0 overflow-hidden'}`}>
        <div className="px-6 space-y-4">
          {navLinks.map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              onClick={() => setIsOpen(false)}
              className="block text-[#94A3B8] hover:text-[#C9A96E] text-lg font-medium"
            >
              {item}
            </a>
          ))}
          <div className="pt-4 border-t border-[#C9A96E]/10">
            {user ? (
              <div className="flex flex-col space-y-4">
                <Link to="chat" onClick={() => setIsOpen(false)} className="bg-[#C9A96E] text-center text-[#0F172A] py-4 rounded-full font-bold uppercase text-sm">
                  Chat to Schedule
                </Link>
                <button onClick={logout} className="text-[#94A3B8] font-bold uppercase text-sm">
                  Logout
                </button>
              </div>
            ) : (
              <Link to="auth" onClick={() => setIsOpen(false)} className="block bg-[#C9A96E] text-center text-[#0F172A] py-4 rounded-full font-bold uppercase text-sm">
                Begin Your Journey
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
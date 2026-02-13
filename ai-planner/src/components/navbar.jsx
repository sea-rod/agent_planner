import { Link } from "react-router";
import { supabase } from "../supabaseClient";
import { useEffect, useState } from 'react';
import React from "react";


const Navbar = () => {
  const [user,setUser] = useState()
  useEffect(() => {
    const checkUser = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      setUser(session?.user.aud)
      // console.log(session);
      
      // console.log(session.provider_token);
      // console.log(session.provider_refresh_token);
      
      // await supabase.auth.signOut()
    };
    checkUser()

     const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      
      // 2. Check if we just signed in and have Google tokens
      if (event === 'SIGNED_IN' && session?.provider_token) {
        console.log("Detected Google Login, syncing tokens...");
        
        const { error } = await supabase.from('user_integrations').upsert({
          user_id: session.user.id,
          google_access_token: session.provider_token,
          google_refresh_token: session.provider_refresh_token,
          updated_at: new Date()
        });

        if (error) console.error("Error syncing to DB:", error.message);
        else console.log("Tokens synced successfully to user_integrations!");
      }
    });

    return () => subscription.unsubscribe();


  },[])





  
  const logout = async ()=>{
    console.log("logout");
    
    supabase.auth.signOut().then(res=>{
      window.location.href = "/"
    })
  }

  return (

  <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0F172A]/95 backdrop-blur-md border-b border-[#C9A96E]/10">
    <div className="max-w-7xl mx-auto px-6 lg:px-10">
      <div className="flex justify-between items-center h-24">
        <div className="text-3xl font-serif font-bold tracking-tight text-[#C9A96E]">
          Atelier
        </div>
        <div className="hidden md:flex items-center space-x-12">
          {['Features', 'Craftsmanship', 'Exclusivity'].map((item) => (
            <a key={item} href={`#${item.toLowerCase()}`} className="text-[#94A3B8] hover:text-[#C9A96E] font-medium transition tracking-wide">
              {item}
            </a>
          ))}
        </div>
        <div>
          {user?( <button onClick={logout} className="bg-[#C9A96E] text-[#0F172A] px-8 py-4 rounded-full font-semibold hover:bg-[#D4B978] transition shadow-lg hover:shadow-xl tracking-wide uppercase text-sm">
            logout
          </button>): (<Link to="auth" className="bg-[#C9A96E] text-[#0F172A] px-8 py-4 rounded-full font-semibold hover:bg-[#D4B978] transition shadow-lg hover:shadow-xl tracking-wide uppercase text-sm">
            Begin Your Journey
          </Link>)}
        </div>
      </div>
    </div>
  </nav>
);}

export default Navbar
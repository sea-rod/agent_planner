import React, { useState } from 'react';
import { Link } from 'react-router';

const GoogleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22.56 12.25C22.56 11.47 22.49 10.72 22.36 10H12V14.51H18.05C17.8 15.99 16.92 17.26 15.56 18.09V21.09H19.19C21.27 19.19 22.56 15.92 22.56 12.25Z" fill="#4285F4"/>
    <path d="M12 23C15.11 23 17.71 21.97 19.19 20.09L15.56 18.09C14.53 18.81 13.23 19.24 12 19.24C9.01 19.24 6.44 17.28 5.57 14.7H1.84V17.78C3.32 20.98 7.1 23 12 23Z" fill="#34A853"/>
    <path d="M5.57 14.7C5.37 14.13 5.26 13.53 5.26 12.92C5.26 12.31 5.37 11.71 5.57 11.14V8.06H1.84C1.2 9.46 0.8 11 0.8 12.92C0.8 14.84 1.2 16.38 1.84 17.78L5.57 14.7Z" fill="#FBBC05"/>
    <path d="M12 5.38C13.62 5.38 15.04 5.93 16.15 6.98L19.43 3.7C17.71 2.07 15.11 1 12 1C7.1 1 3.32 3.02 1.84 6.22L5.57 9.3C6.44 6.72 9.01 4.76 12 4.76V5.38Z" fill="#EA4335"/>
  </svg>
);

const InputField = ({ label, type, placeholder, id }) => (
  <div className="space-y-2">
    <label htmlFor={id} className="block text-sm font-medium text-[#94A3B8] tracking-wide">
      {label}
    </label>
    <input 
      type={type} 
      id={id} 
      required 
      placeholder={placeholder}
      className="w-full px-5 py-4 bg-[#0F172A] border border-[#C9A96E]/20 rounded-xl text-white placeholder-[#94A3B8]/50 focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E] outline-none transition"
    />
  </div>
);

const AuthPage = () => {
  const [activeTab, setActiveTab] = useState('login');

  const handleGoogleSignIn = () => {
    console.log("Redirecting to Google OAuth...");
  };

  return (
    <div className="bg-[#0F172A] min-h-screen flex flex-col font-sans text-[#FAFAFA] antialiased">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-[#0F172A]/90 backdrop-blur-md border-b border-[#C9A96E]/10">
        <div className="max-w-7xl mx-auto px-6 lg:px-10">
          <div className="flex justify-between items-center h-20">
            <button className="text-3xl font-serif font-bold tracking-tight text-[#C9A96E]">
              Atelier
            </button>
            <Link to='/' className="text-[#94A3B8] hover:text-[#C9A96E] transition text-sm font-light tracking-wide">
              ← Back to Home
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center pt-24 pb-16 px-5">
        <div className="w-full max-w-md animate-fade-up">
          <div className="text-center mb-10">
            <div className="inline-block mb-4 px-6 py-2 bg-[#C9A96E]/10 text-[#C9A96E] font-serif text-xl rounded-full tracking-widest border border-[#C9A96E]/20">
              Atelier
            </div>
            <h1 className="text-4xl font-serif font-bold text-white mb-2">
              {activeTab === 'login' ? 'Welcome' : 'Join Us'}
            </h1>
            <p className="text-[#94A3B8] font-light">
              Curate time with quiet elegance
            </p>
          </div>

          <div className="bg-[#1E293B]/30 backdrop-blur-md rounded-3xl border border-[#C9A96E]/10 shadow-2xl overflow-hidden">
            {/* Tabs */}
            <div className="flex border-b border-[#C9A96E]/10">
              <button 
                onClick={() => setActiveTab('login')}
                className={`flex-1 py-5 text-center font-medium text-lg transition-all ${activeTab === 'login' ? 'text-[#C9A96E] border-b-2 border-[#C9A96E]' : 'text-[#94A3B8]'}`}
              >
                Sign In
              </button>
              <button 
                onClick={() => setActiveTab('signup')}
                className={`flex-1 py-5 text-center font-medium text-lg transition-all ${activeTab === 'signup' ? 'text-[#C9A96E] border-b-2 border-[#C9A96E]' : 'text-[#94A3B8]'}`}
              >
                Create Account
              </button>
            </div>

            <div className="p-8 md:p-10">
              <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
                <button 
                  type="button"
                  onClick={handleGoogleSignIn}
                  className="w-full bg-white text-gray-800 py-4 rounded-full font-medium flex items-center justify-center gap-3 shadow-md hover:shadow-lg transition-transform hover:-translate-y-0.5"
                >
                  <GoogleIcon />
                  {activeTab === 'login' ? 'Continue with Google' : 'Sign up with Google'}
                </button>

                <div className="relative my-8">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-[#C9A96E]/20"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-4 bg-[#1e293b] text-[#94A3B8]">or email</span>
                  </div>
                </div>

                {activeTab === 'signup' && (
                  <InputField label="Full Name" type="text" placeholder="Victoria Moreau" id="name" />
                )}

                <InputField label="Email" type="email" placeholder="your@name.com" id="email" />
                <InputField label="Password" type="password" placeholder="••••••••" id="password" />

                <button 
                  type="submit"
                  className="w-full bg-[#C9A96E] text-[#0F172A] py-4 rounded-full font-serif font-bold text-lg hover:bg-[#D4B978] transition shadow-lg transform hover:-translate-y-0.5"
                >
                  {activeTab === 'login' ? 'Enter Atelier' : 'Begin Your Journey'}
                </button>

                <p className="text-center text-sm text-[#94A3B8]">
                  {activeTab === 'login' ? "New here? " : "Already a member? "}
                  <button 
                    type="button"
                    onClick={() => setActiveTab(activeTab === 'login' ? 'signup' : 'login')}
                    className="text-[#C9A96E] hover:underline font-medium"
                  >
                    {activeTab === 'login' ? "Create account" : "Sign in"}
                  </button>
                </p>
              </form>
            </div>
          </div>
          <p className="text-center text-[#94A3B8] text-sm mt-10">
            © 2026 Atelier - All times curated with discretion
          </p>
        </div>
      </main>
    </div>
  );
};

export default AuthPage;
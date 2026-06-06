import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router';
import { supabase } from '../supabaseClient';

const GoogleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22.56 12.25C22.56 11.47 22.49 10.72 22.36 10H12V14.51H18.05C17.8 15.99 16.92 17.26 15.56 18.09V21.09H19.19C21.27 19.19 22.56 15.92 22.56 12.25Z" fill="#4285F4" />
    <path d="M12 23C15.11 23 17.71 21.97 19.19 20.09L15.56 18.09C14.53 18.81 13.23 19.24 12 19.24C9.01 19.24 6.44 17.28 5.57 14.7H1.84V17.78C3.32 20.98 7.1 23 12 23Z" fill="#34A853" />
    <path d="M5.57 14.7C5.37 14.13 5.26 13.53 5.26 12.92C5.26 12.31 5.37 11.71 5.57 11.14V8.06H1.84C1.2 9.46 0.8 11 0.8 12.92C0.8 14.84 1.2 16.38 1.84 17.78L5.57 14.7Z" fill="#FBBC05" />
    <path d="M12 5.38C13.62 5.38 15.04 5.93 16.15 6.98L19.43 3.7C17.71 2.07 15.11 1 12 1C7.1 1 3.32 3.02 1.84 6.22L5.57 9.3C6.44 6.72 9.01 4.76 12 4.76V5.38Z" fill="#EA4335" />
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
  const [activeTab, setActiveTab] = useState('signup');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ email: '', password: '', confirmPassword: '', fullName: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGoogleSignIn = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          queryParams: { access_type: 'offline', prompt: 'consent' },
          redirectTo: `${window.location.origin}/connector`,
        },
      });
      if (error) throw error;
    } catch (error) {
      alert(error.message);
    }
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    if (activeTab === 'signup' && formData.password !== formData.confirmPassword) {
      alert('Passwords do not match.');
      return;
    }
    setLoading(true);
    try {
      if (activeTab === 'signup') {
        const { data, error } = await supabase.auth.signUp({
          email: formData.email,
          password: formData.password,
          options: { data: { full_name: formData.fullName } },
        });

        if (error) throw error;

        if (data?.user?.identities?.length === 0) {
          alert('An account with this email already exists. Please sign in.');
          return;
        }

        alert('Check your email for the confirmation link!');
      } else {
        const { error } = await supabase.auth.signInWithPassword({
          email: formData.email,
          password: formData.password,
        });
        if (error) throw error;
        navigate('/dashboard');
      }
    } catch (error) {
      console.log(error)
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#0F172A] min-h-screen flex flex-col font-sans text-[#FAFAFA] antialiased">
      <main className="flex-grow flex items-center justify-center pt-24 pb-16 px-5">
        <div className="w-full max-w-md">
          <p className="text-center font-serif text-3xl text-[#C9A96E] tracking-widest mb-1">ATELIER</p>
          <p className="text-center text-xs text-[#475569] tracking-widest uppercase mb-7">Your intelligent workspace</p>

          <div className="bg-[#1E293B]/60 backdrop-blur-md rounded-3xl border border-[#C9A96E]/10 shadow-2xl overflow-hidden">

            {/* Tab Bar */}
            <div className="flex border-b border-[#C9A96E]/12">
              {['login', 'signup'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`flex-1 py-4 text-xs font-medium tracking-widest uppercase transition relative
                    ${activeTab === tab ? 'text-[#C9A96E]' : 'text-[#64748B]'}`}
                >
                  {tab === 'login' ? 'Sign In' : 'Create Account'}
                  {activeTab === tab && (
                    <span className="absolute bottom-0 left-[10%] right-[10%] h-0.5 bg-[#C9A96E] rounded-t-sm" />
                  )}
                </button>
              ))}
            </div>

            <div className="p-8 md:p-10">
              <form className="space-y-6" onSubmit={handleAuth}>
                {/* Google Button */}
                <button
                  type="button"
                  onClick={handleGoogleSignIn}
                  disabled={loading}
                  className="w-full bg-white text-gray-800 py-4 rounded-full font-medium flex items-center justify-center gap-3 shadow-md hover:shadow-lg transition-transform hover:-translate-y-0.5 disabled:opacity-50"
                >
                  <GoogleIcon />
                  {activeTab === 'login' ? 'Continue with Google' : 'Sign up with Google'}
                </button>

                <div className="relative my-8">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-[#C9A96E]/20" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-4 bg-[#1e293b] text-[#94A3B8]">or email</span>
                  </div>
                </div>

                {/* Fields */}
                <div className="space-y-4">
                  {activeTab === 'signup' && (
                    <div className="space-y-2">
                      <label className="block text-xs font-medium text-[#94A3B8] tracking-wide">Full Name</label>
                      <input name="fullName" type="text" required placeholder="Victoria Moreau"
                        onChange={handleChange}
                        className="w-full px-5 py-4 bg-[#0F172A] border border-[#C9A96E]/20 rounded-xl text-white placeholder-[#94A3B8]/45 focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 outline-none transition" />
                    </div>
                  )}

                  <div className="space-y-2">
                    <label className="block text-xs font-medium text-[#94A3B8] tracking-wide">Email</label>
                    <input name="email" type="email" required placeholder="your@name.com"
                      onChange={handleChange}
                      className="w-full px-5 py-4 bg-[#0F172A] border border-[#C9A96E]/20 rounded-xl text-white placeholder-[#94A3B8]/45 focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 outline-none transition" />
                  </div>

                  <div className="space-y-2">
                    <label className="block text-xs font-medium text-[#94A3B8] tracking-wide">Password</label>
                    <input name="password" type="password" required placeholder="••••••••"
                      onChange={handleChange}
                      className="w-full px-5 py-4 bg-[#0F172A] border border-[#C9A96E]/20 rounded-xl text-white placeholder-[#94A3B8]/45 focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 outline-none transition" />
                  </div>

                  {activeTab === 'signup' && (
                    <div className="space-y-2">
                      <label className="block text-xs font-medium text-[#94A3B8] tracking-wide">Confirm Password</label>
                      <input name="confirmPassword" type="password" required placeholder="••••••••"
                        onChange={handleChange}
                        className="w-full px-5 py-4 bg-[#0F172A] border border-[#C9A96E]/20 rounded-xl text-white placeholder-[#94A3B8]/45 focus:border-[#C9A96E] focus:ring-1 focus:ring-[#C9A96E]/20 outline-none transition" />
                    </div>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-[#C9A96E] text-[#0F172A] py-4 rounded-full font-serif font-bold text-lg hover:bg-[#D4B978] transition shadow-lg transform hover:-translate-y-0.5 disabled:opacity-50"
                >
                  {loading ? 'Processing...' : activeTab === 'login' ? 'Enter Atelier' : 'Begin Your Journey'}
                </button>

                <p className="text-center text-sm text-[#64748B]">
                  {activeTab === 'login' ? (
                    <>No account?{' '}
                      <button type="button" onClick={() => setActiveTab('signup')} className="text-[#C9A96E] underline underline-offset-2">Create one</button>
                    </>
                  ) : (
                    <>Already have an account?{' '}
                      <button type="button" onClick={() => setActiveTab('login')} className="text-[#C9A96E] underline underline-offset-2">Sign in</button>
                    </>
                  )}
                </p>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AuthPage;
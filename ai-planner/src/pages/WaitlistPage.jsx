import React, { useState } from 'react';
import { Link } from 'react-router';
import { supabase } from '../supabaseClient';

const WaitlistPage = () => {
  const [email, setEmail] = useState('');
  const [persona, setPersona] = useState('');
  const [frustration, setFrustration] = useState('');
  const [urgency, setUrgency] = useState(3);
  const [submitted, setSubmitted] = useState(true);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const { error } = await supabase
      .from('waitlist')
      .insert([{ email, persona, frustration, urgency }]);

    setLoading(false);
    if (!error) {
      setSubmitted(true);
    } else {
      alert(error.message || "Something went wrong. Please try again.");
    }
  };

  if (submitted) {
    return (
      <div className="bg-[#0F172A] text-[#FAFAFA] min-h-screen flex items-center justify-center px-4 font-sans antialiased">
        <div className="max-w-md w-full text-center space-y-6 border border-[#C9A96E]/20 bg-[#1E293B]/40 backdrop-blur-md p-8 rounded-3xl shadow-xl">
          <div className="text-4xl">🕰️</div>
          <h2 className="text-2xl font-serif font-bold text-[#C9A96E]">You're on the list.</h2>
          <p className="text-[#94A3B8] text-base leading-relaxed text-justify">
            Your early-bird slot ($6/month for 3 months) is secure.

            We are spinning up dedicated agent contexts to keep processing speeds hyper-optimal. Want to test it out right now? Click "Try for Free" below to explore the application interface immediately.

            Watch your inbox for your unique access key and custom checkout link to lock in your early-bird rate when your slot is ready.
          </p>
          <Link to="/auth" className="border-2 border-[#C9A96E]/60 text-[#C9A96E] px-5 py-4 rounded-full text-ml font-semibold hover:bg-[#C9A96E]/10 transition tracking-wide">
            TRY FOR FREE
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#0F172A] text-[#FAFAFA] min-h-screen flex flex-col font-sans antialiased justify-center items-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-xl w-full space-y-8 bg-[#1E293B]/40 backdrop-blur-md border border-[#C9A96E]/10 p-6 sm:p-10 rounded-3xl shadow-xl">

        {/* Branding Title */}
        <div className="text-center">
          <div className="text-3xl sm:text-4xl font-serif font-bold tracking-tight text-[#C9A96E]">Atelier</div>
          <p className="mt-3 text-sm text-[#94A3B8] max-w-sm mx-auto leading-relaxed">
            To maintain optimal AI compute metrics, cohort launches are strictly capped. Secure early-bird pricing slot ($10/mo forever).
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <div className="space-y-4">

            {/* Email Field */}
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-[#94A3B8] mb-2">Email Address</label>
              <input
                type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full bg-[#0F172A]/60 border border-[#C9A96E]/20 rounded-xl px-4 py-3 text-sm text-white focus:border-[#C9A96E] outline-none transition-all"
              />
            </div>

            {/* Persona Dropdown */}
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-[#94A3B8] mb-2">What describes you best?</label>
              <select
                value={persona} onChange={(e) => setPersona(e.target.value)} required
                className="w-full bg-[#0F172A]/60 border border-[#C9A96E]/20 rounded-xl px-4 py-3 text-sm text-white focus:border-[#C9A96E] outline-none transition-all appearance-none"
              >
                <option value="" disabled>Select your role...</option>
                <option value="engineer">Software Engineer / Researcher</option>
                <option value="founder">Founder / Indie Hacker</option>
                <option value="manager">Project Manager / Director</option>
                <option value="student">Student</option>
              </select>
            </div>

            {/* Frustration Open Field */}
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-[#94A3B8] mb-2">Most frustrating part of managing your schedule?</label>
              <textarea
                rows="3" value={frustration} onChange={(e) => setFrustration(e.target.value)} required
                placeholder="Context switching, manual calendar blocking, etc..."
                className="w-full bg-[#0F172A]/60 border border-[#C9A96E]/20 rounded-xl px-4 py-3 text-sm text-white focus:border-[#C9A96E] outline-none transition-all resize-none"
              />
            </div>

            {/* Urgency Meter */}
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-[#94A3B8] mb-2">How critical is automating your calendar layout?</label>
              <div className="flex justify-between items-center gap-2 mt-2">
                {[1, 2, 3, 4, 5].map((num) => (
                  <button
                    type="button" key={num} onClick={() => setUrgency(num)}
                    className={`flex-1 py-2 text-sm font-medium rounded-xl border transition-all ${urgency === num
                      ? 'bg-[#C9A96E] border-[#C9A96E] text-[#0F172A]'
                      : 'bg-[#0F172A]/40 border-[#C9A96E]/10 text-[#94A3B8] hover:border-[#C9A96E]/30'
                      }`}
                  >
                    {num}
                  </button>
                ))}
              </div>
              <div className="flex justify-between text-[10px] text-[#94A3B8] uppercase tracking-wide mt-1.5 px-1">
                <span>Nice to have</span>
                <span>Desperate need</span>
              </div>
            </div>

          </div>

          {/* Submit Button */}
          <button
            type="submit" disabled={loading}
            className="w-full bg-[#C9A96E] text-[#0F172A] font-medium py-3.5 px-4 rounded-xl hover:bg-[#D4B978] transition shadow-lg disabled:opacity-50 tracking-wide text-sm uppercase"
          >
            {loading ? 'Securing Spot...' : 'Claim Early-Bird Access'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default WaitlistPage;
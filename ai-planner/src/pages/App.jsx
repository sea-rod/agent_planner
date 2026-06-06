import { Link } from 'react-router';
import FeatureCard from '../components/FeatureCard';


function App() {
  return (
    <div className="bg-[#FAFAFA] text-[#0F172A] antialiased font-sans">

      {/* Hero Section */}
      <section className="pt-40 pb-3 md:pt-40 md:pb-48 bg-gradient-to-br from-[#0F172A] via-[#1E293B] to-[#0F172A]">
        <div className="max-w-6xl mx-auto px-6 lg:px-10 text-center">
          <div className="inline-block mb-8 px-8 py-3 bg-[#C9A96E]/10 text-[#C9A96E] font-serif text-lg rounded-full tracking-widest uppercase animate-pulse border border-[#C9A96E]/20">
            Bespoke Intelligence • Google Calendar Foundation
          </div>
          <h1 className="text-6xl md:text-8xl font-serif font-bold leading-tight mb-10 text-white">
            Your time,<br /> <span className="text-[#C9A96E]">meticulously curated</span><br />
          </h1>
          <p className="text-2xl md:text-3xl text-[#94A3B8] max-w-4xl mx-auto mb-16 font-light leading-relaxed">
            An exquisite AI companion that anticipates, orchestrates, and refines your schedule.
            <span className='text-[#C9A96E] rounded-full text-2xl '> So you may focus on what truly matters.</span>
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-8">
            <Link to="/waitlist" className="bg-[#C9A96E] text-[#0F172A] px-10 py-5  rounded-full text-xl font-semibold hover:bg-[#D4B978] transition shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 tracking-wide uppercase">
              SUBSCRIBE NOW • $6/MO
            </Link>
            <Link to="/auth" className="border-2 border-[#C9A96E]/60 text-[#C9A96E] px-10 py-5 rounded-full text-xl font-semibold hover:bg-[#C9A96E]/10 transition tracking-wide">
              TRY FOR FREE
            </Link>
          </div>
          <p className="mt-10 text-[#94A3B8] text-lg font-light">Early Bird Special: $6/mo for your first 3 months.
            Limited to the first 50 members (Reg. $18/mo).
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-32 bg-[#0B1220]">
        <div className="max-w-5xl mx-auto px-6 lg:px-10">
          <div className="text-center mb-16">
            <p className="text-[11px] tracking-[0.2em] uppercase text-[#C9A96E] mb-4">Capabilities</p>
            <h2 className="font-serif text-5xl text-[#F1EDE4] mb-4 font-normal">Built for the way you actually work</h2>
            <p className="text-[15px] text-[#5A6A80] font-light max-w-lg mx-auto leading-relaxed">
              Five precision instruments, working in concert. Talk naturally and Atelier handles the rest.
            </p>
          </div>
          <div className="grid md:grid-cols-3 border border-[#C9A96E]/12 rounded-2xl overflow-hidden divide-x divide-y divide-[#C9A96E]/12">
            <FeatureCard number="01" icon="🗓" title="Multi-Mode Scheduling"
              description="Plan across days or weeks, set single reminders, delete events with confirmation, or query your calendar, all through natural conversation. One interface, four scheduling modes."
              status="Live" />
            <FeatureCard number="02" icon="🧠" title="Semantic Memory"
              description="Atelier learns your scheduling patterns, surfaces relevant past context, and suggests proactive improvements over time. Three dedicated Weaviate collections keep your preferences precise."
              status="Coming soon" />
            <FeatureCard number="03" icon="✋" title="Human-in-the-Loop"
              description="Nothing touches your calendar without your explicit approval. Every proposed schedule comes with tradeoff analysis, transparent reasoning, and space for iterative refinement."
              status="Live" />
            <FeatureCard number="04" icon="🔗" title="Google Calendar Sync"
              description="Real-time synchronisation with conflict detection, secure OAuth2 authentication, and full create, retrieve, and delete support. Your existing calendar, made intelligent."
              status="Live" />
            <FeatureCard number="05" icon="💬" title="Natural Language Interface"
              description='Say "next Tuesday" or "sometime in the next two weeks" Atelier parses it. Ambiguous requests prompt clarifying questions. Sessions persist across conversations.'
              status="Live" />
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;
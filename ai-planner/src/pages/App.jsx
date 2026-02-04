import { Link } from 'react-router';
import FeatureCard from '../components/FeatureCard';


function App() {
  return (
    <div className="bg-[#FAFAFA] text-[#0F172A] antialiased font-sans">

      {/* Hero Section */}
      <section className="pt-40 pb-32 md:pt-60 md:pb-48 bg-gradient-to-br from-[#0F172A] via-[#1E293B] to-[#0F172A]">
        <div className="max-w-6xl mx-auto px-6 lg:px-10 text-center">
          <div className="inline-block mb-8 px-8 py-3 bg-[#C9A96E]/10 text-[#C9A96E] font-serif text-lg rounded-full tracking-widest uppercase animate-pulse border border-[#C9A96E]/20">
            Bespoke Intelligence • Google Calendar Foundation
          </div>
          <h1 className="text-6xl md:text-8xl font-serif font-bold leading-tight mb-10 text-white">
            Time, <span className="text-[#C9A96E]">reimagined</span><br />with quiet luxury
          </h1>
          <p className="text-2xl md:text-3xl text-[#94A3B8] max-w-4xl mx-auto mb-16 font-light leading-relaxed">
            An exquisite AI companion that anticipates, orchestrates, and refines your schedule — so you may focus on what truly matters.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-8">
            <Link to="/auth" className="bg-[#C9A96E] text-[#0F172A] px-12 py-6 rounded-full text-xl font-semibold hover:bg-[#D4B978] transition shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 tracking-wide uppercase">
              Reserve Your Access
            </Link>
            <button className="border-2 border-[#C9A96E]/60 text-[#C9A96E] px-12 py-6 rounded-full text-xl font-semibold hover:bg-[#C9A96E]/10 transition tracking-wide">
              Experience the Craft
            </button>
          </div>
          <p className="mt-10 text-[#94A3B8] text-lg font-light">Exclusive preview • No commitment required</p>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-32 bg-[#FAFAFA]">
        <div className="max-w-7xl mx-auto px-6 lg:px-10">
          <div className="text-center mb-24">
            <h2 className="text-6xl font-serif font-bold mb-8 text-[#0F172A]">Mastery in Every Detail</h2>
            <p className="text-2xl text-[#94A3B8] max-w-4xl mx-auto font-light">Precision-crafted intelligence wrapped in effortless elegance.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            <FeatureCard 
              emoji="🗓️" 
              title="Temporal Artistry" 
              description="Multi-horizon planning, instantaneous reminders, intelligent curation — expressed through natural conversation." 
            />
            <FeatureCard 
              emoji="🧠" 
              title="Discerning Memory" 
              description="A mind that remembers your rhythms, anticipates your needs, and evolves with refined taste." 
            />
            <FeatureCard 
              emoji="✋" 
              title="Respectful Guardianship" 
              description="Every decision presented with clarity, deference, and graceful invitation for your discerning approval." 
            />
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;
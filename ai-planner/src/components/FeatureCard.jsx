
const FeatureCard = ({ emoji, title, description, span }) => (
  <div className={`bg-white/50 backdrop-blur-sm p-12 rounded-3xl border border-[#C9A96E]/10 shadow-xl hover:shadow-2xl transition-all duration-500 group ${span ? 'md:col-span-2 lg:col-span-1' : ''}`}>
    <div className="text-7xl mb-8 text-[#C9A96E]">{emoji}</div>
    <h3 className="text-4xl font-serif font-bold mb-6 text-[#0F172A]">{title}</h3>
    <p className="text-[#94A3B8] text-lg leading-relaxed">{description}</p>
  </div>
);

export default FeatureCard;
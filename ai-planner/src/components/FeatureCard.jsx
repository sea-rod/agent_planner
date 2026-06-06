const FeatureCard = ({ number, icon, title, description, status }) => (
  <div className="relative bg-[#0D1528] p-9 hover:bg-[#111d35] transition-colors duration-300">
    <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-[#C9A96E]/20 to-transparent" />
    <span className="block text-[11px] tracking-[0.15em] text-[#C9A96E]/40 font-serif mb-6">{number}</span>
    <div className="w-9 h-9 border border-[#C9A96E]/25 rounded-lg flex items-center justify-center mb-5 text-[#C9A96E] text-lg">
      {icon}
    </div>
    <h3 className="font-serif text-[1.1rem] text-[#E8DCC8] mb-2.5 font-normal">{title}</h3>
    <p className="text-[13.5px] text-[#4E5E73] leading-relaxed font-light">{description}</p>
    {status && (
      <span className="inline-block mt-4 text-[10px] tracking-widest uppercase text-[#C9A96E]/50 border border-[#C9A96E]/15 rounded px-1.5 py-0.5">
        {status}
      </span>
    )}
  </div>
);

export default FeatureCard;
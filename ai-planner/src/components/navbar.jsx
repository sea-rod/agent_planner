
const Navbar = () => {
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
          <button className="bg-[#C9A96E] text-[#0F172A] px-8 py-4 rounded-full font-semibold hover:bg-[#D4B978] transition shadow-lg hover:shadow-xl tracking-wide uppercase text-sm">
            Begin Your Journey
          </button>
        </div>
      </div>
    </div>
  </nav>
);}

export default Navbar
import { Link } from 'react-router';
import FeatureCard from '../components/FeatureCard';

/**
 * SEO STRATEGY APPLIED:
 * Primary keywords: "AI scheduling assistant", "AI calendar app", "natural language scheduling"
 * Secondary: "time blocking", "Google Calendar AI", "smart scheduler", "focus time", "meeting scheduler"
 * Long-tail: "AI calendar assistant for Google Calendar", "schedule meetings with natural language"
 * Techniques: semantic HTML5, heading hierarchy, keyword-rich copy, JSON-LD structured data,
 *              ARIA labels, descriptive link text, meta-optimised content sections
 */

// JSON-LD structured data — injected as a side-effect via a tiny helper
function StructuredData() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Atelier",
    "applicationCategory": "ProductivityApplication",
    "operatingSystem": "Web",
    "description":
      "Atelier is an AI scheduling assistant that connects to Google Calendar and lets you manage your time through natural language. Schedule meetings, block focus time, and automate calendar management without manual entry.",
    "offers": {
      "@type": "Offer",
      "price": "6.00",
      "priceCurrency": "USD",
      "priceValidUntil": "2025-12-31",
      "description": "Early bird plan — first 50 members at $6/mo for 3 months",
    },
    "featureList": [
      "Natural language scheduling",
      "Google Calendar sync",
      "AI time blocking",
      "Smart meeting scheduler",
      "Focus time protection",
      "Semantic calendar memory",
    ],
    "url": "https://myatelier.in",
    "sameAs": ["https://myatelier.in"],
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

function App() {
  return (
    <>
      {/* JSON-LD: helps Google & AI Overviews cite Atelier correctly */}
      <StructuredData />

      {/*
        Semantic landmark: <main> tells crawlers this is the primary content.
        id="main-content" supports skip-nav (accessibility + crawl efficiency).
      */}
      <main
        id="main-content"
        className="bg-[#FAFAFA] text-[#0F172A] antialiased font-sans"
      >

        {/* ── HERO ──────────────────────────────────────────────────────────
            H1 contains primary keyword phrase "AI scheduling assistant"
            and secondary phrase "Google Calendar". One H1 per page rule.
            The eyebrow badge reinforces "Google Calendar" + "AI" co-occurrence.
        ─────────────────────────────────────────────────────────────────── */}
        <section
          aria-labelledby="hero-heading"
          className="pt-40 pb-3 md:pt-40 md:pb-48 bg-gradient-to-br from-[#0F172A] via-[#1E293B] to-[#0F172A]"
        >
          <div className="max-w-6xl mx-auto px-6 lg:px-10 text-center">
            <p
              aria-label="Product category"
              className="inline-block mb-8 px-8 py-3 bg-[#C9A96E]/10 text-[#C9A96E] font-serif text-lg rounded-full tracking-widest uppercase animate-pulse border border-[#C9A96E]/20"
            >
              AI Scheduling Assistant · Google Calendar
            </p>

            {/* Primary H1 — contains the two highest-volume keywords */}
            <h1
              id="hero-heading"
              className="text-5xl sm:text-2xl md:text-7xl font-serif font-bold leading-tight mb-10 text-white"
            >
              Your AI calendar assistant,{' '}
              <span className="text-[#C9A96E]">meticulously curated</span>
            </h1>

            {/*
              Hero sub-copy: naturally embeds "natural language scheduling",
              "time management", "smart scheduler", "meeting scheduler",
              "focus time", "time blocking" — all high-volume intent terms.
            */}
            <p className="text-2xl md:text-3xl text-[#94A3B8] max-w-4xl mx-auto mb-6 font-light leading-relaxed">
              Atelier is a{' '}
              <strong className="text-white font-medium">
                smart scheduling assistant
              </strong>{' '}
              powered by AI. Manage your Google Calendar through plain English
              schedule meetings, protect focus time, and automate time blocking
              without touching a single form.
            </p>

            <p className="text-xl text-[#94A3B8] max-w-3xl mx-auto mb-16 font-light leading-relaxed">
              <span className="text-[#C9A96E]">
                Say "block two hours for deep work next Tuesday"
              </span>{' '}
              Atelier handles the rest. The AI time management assistant that
              works the way you think.
            </p>

            <div className="flex flex-col sm:flex-row justify-center gap-8">
              {/* Descriptive CTA text — better for SEO than generic "Click here" */}
              <Link
                to="/waitlist"
                aria-label="Subscribe to Atelier AI scheduling assistant — $6 per month early bird"
                className="bg-[#C9A96E] text-[#0F172A] px-10 py-5 rounded-full text-xl font-semibold hover:bg-[#D4B978] transition shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 tracking-wide uppercase"
              >
                Start Scheduling — $6/mo
              </Link>
              <Link
                to="/auth"
                aria-label="Try Atelier AI calendar assistant for free"
                className="border-2 border-[#C9A96E]/60 text-[#C9A96E] px-10 py-5 rounded-full text-xl font-semibold hover:bg-[#C9A96E]/10 transition tracking-wide"
              >
                Try for Free
              </Link>
            </div>

            <p className="mt-10 text-[#94A3B8] text-lg font-light">
              Early Bird Special: $6/mo for your first 3 months.{' '}
              <strong className="text-[#C9A96E] font-medium">
                Limited to the first 50 members
              </strong>{' '}
              (Regular price $18/mo).
            </p>
          </div>
        </section>

        {/* ── SOCIAL PROOF / KEYWORD BRIDGE ────────────────────────────────
            A short sentence-level section reinforcing long-tail phrases:
            "AI scheduling app", "calendar management", "productivity app".
            Crawlers weight copy near the top of the page more heavily.
        ─────────────────────────────────────────────────────────────────── */}
        <section
          aria-label="Who Atelier is for"
          className="py-12 bg-[#0B1220] border-b border-[#C9A96E]/10"
        >
          <div className="max-w-4xl mx-auto px-6 text-center">
            <p className="text-[#5A6A80] text-lg font-light leading-relaxed">
              The{' '}
              <strong className="text-[#94A3B8] font-medium">
                AI calendar app
              </strong>{' '}
              for knowledge workers, founders, and busy professionals who want
              intelligent{' '}
              <strong className="text-[#94A3B8] font-medium">
                calendar management
              </strong>{' '}
              without the overhead. Unlike Motion or Reclaim, Atelier generates
              your schedule from scratch not just rearranges what you already
              entered.
            </p>
          </div>
        </section>

        {/* ── FEATURES ──────────────────────────────────────────────────────
            H2 contains "natural language" + "scheduling" (high-intent pair).
            Each FeatureCard should render with an <h3> internally for
            correct heading hierarchy (H1 → H2 → H3).
            aria-labelledby ties the section to its heading for screen readers
            and structured crawl paths.
        ─────────────────────────────────────────────────────────────────── */}
        <section
          id="features"
          aria-labelledby="features-heading"
          className="py-32 bg-[#0B1220]"
        >
          <div className="max-w-5xl mx-auto px-6 lg:px-10">
            <header className="text-center mb-16">
              {/*
                Eyebrow: exact-match keyword "AI Scheduling Features"
                helps with category-level indexing.
              */}
              <p className="text-[11px] tracking-[0.2em] uppercase text-[#C9A96E] mb-4">
                AI Scheduling Features
              </p>

              {/* H2 — secondary heading, weaves in "natural language scheduling" */}
              <h2
                id="features-heading"
                className="font-serif text-5xl text-[#F1EDE4] mb-4 font-normal"
              >
                Natural language scheduling,{' '}
                <span className="text-[#C9A96E]">built for how you work</span>
              </h2>

              <p className="text-[15px] text-[#5A6A80] font-light max-w-lg mx-auto leading-relaxed">
                Five precision scheduling tools working in concert. Talk to
                Atelier the way you'd text a human assistant — it handles the
                calendar, conflicts, and confirmations.
              </p>
            </header>

            {/*
              FeatureCard receives a `headingLevel` prop hint (h3) so the
              component renders semantically correct heading hierarchy.
              Each title and description naturally contains target keywords.
            */}
            <div
              role="list"
              aria-label="Atelier AI scheduling features"
              className="grid md:grid-cols-3 border border-[#C9A96E]/12 rounded-2xl overflow-hidden divide-x divide-y divide-[#C9A96E]/12"
            >
              {/* Feature 01 — keyword: "multi-mode scheduling", "time management" */}
              <FeatureCard
                number="01"
                icon="🗓"
                title="Multi-Mode AI Scheduler"
                description="Plan across days or weeks, set single reminders, remove calendar events with confirmation, or query your schedule — all through plain English conversation. One AI scheduling assistant, four intelligent modes."
                status="Live"
              />

              {/* Feature 02 — keyword: "smart scheduler", "AI memory", "calendar patterns" */}
              <FeatureCard
                number="02"
                icon="🧠"
                title="Smart Scheduling Memory"
                description="Atelier learns your scheduling preferences and daily patterns, surfaces relevant past context, and proactively improves your calendar management over time. Gets smarter the more you use it."
                status="Coming soon"
              />

              {/* Feature 03 — keyword: "calendar management", "human-in-the-loop" */}
              <FeatureCard
                number="03"
                icon="✋"
                title="Human-in-the-Loop Control"
                description="Nothing touches your calendar without your explicit approval. Every proposed time block comes with tradeoff analysis, transparent reasoning, and space for refinement. You stay in control."
                status="Live"
              />

              {/* Feature 04 — keyword: "Google Calendar sync", "Google Calendar AI" */}
              <FeatureCard
                number="04"
                icon="🔗"
                title="Google Calendar Sync"
                description="Real-time sync with conflict detection, secure OAuth2 authentication, and full create, retrieve, and delete support. Your existing Google Calendar, made intelligent with AI scheduling."
                status="Live"
              />

              {/* Feature 05 — keyword: "natural language scheduling", "task scheduling" */}
              <FeatureCard
                number="05"
                icon="💬"
                title="Natural Language Interface"
                description='Say "next Tuesday" or "sometime in the next two weeks" — Atelier parses it precisely. Ambiguous requests trigger smart clarifying questions. Your session context persists across conversations.'
                status="Live"
              />
            </div>
          </div>
        </section>

        {/* ── SEO FOOTER CONTEXT BLOCK ──────────────────────────────────────
            A keyword-rich paragraph-level section that reinforces topical
            authority for "AI scheduling assistant", "time blocking app",
            "meeting scheduler", and "productivity app" — without being
            spammy. This also gives Google enough entity context to serve
            Atelier in AI Overviews for comparison queries.
        ─────────────────────────────────────────────────────────────────── */}
        <section
          aria-label="About Atelier AI scheduling assistant"
          className="py-20 bg-[#0F172A] border-t border-[#C9A96E]/10"
        >
          <div className="max-w-3xl mx-auto px-6 text-center">
            <h2 className="font-serif text-3xl text-[#F1EDE4] mb-6 font-normal">
              The AI scheduling assistant that thinks ahead
            </h2>
            <p className="text-[#5A6A80] text-base font-light leading-relaxed mb-4">
              Atelier is a{' '}
              <strong className="text-[#94A3B8] font-medium">
                natural language scheduling app
              </strong>{' '}
              for Google Calendar. Unlike traditional smart calendars that
              rearrange events you've already entered, Atelier generates your
              entire schedule from a plain-English description of your week —
              then asks for your approval before touching anything.
            </p>
            <p className="text-[#5A6A80] text-base font-light leading-relaxed mb-4">
              Use it as a{' '}
              <strong className="text-[#94A3B8] font-medium">
                time blocking app
              </strong>
              , a{' '}
              <strong className="text-[#94A3B8] font-medium">
                meeting scheduler
              </strong>
              , a focus time protector, or a full calendar management assistant.
              Early bird access is open now at $6/mo.
            </p>
            <p className="text-[#5A6A80] text-sm font-light leading-relaxed">
              Compatible with Google Calendar · Powered by LangGraph + Groq ·
              Built for productivity-focused professionals
            </p>
          </div>
        </section>

      </main>
    </>
  );
}

export default App;
import React from 'react';

// Color palette baked into constants for easy maintenance within the file
const COLORS = {
  primary: 'bg-[#0F172A]',
  primaryDark: 'bg-[#020617]',
  accent: 'text-[#C9A96E]',
  accentBg: 'bg-[#C9A96E]',
  accentBorder: 'border-[#C9A96E]/20',
  secondary: 'bg-[#1E293B]',
  muted: 'text-[#94A3B8]',
  light: 'text-[#FAFAFA]'
};

const Terms = () => {
  return (
    <div className={`min-h-screen font-sans ${COLORS.primary} ${COLORS.light} antialiased selection:bg-[#C9A96E]/30`}>
      {/* Import Fonts directly in the component via Style tag */}
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700;800&display=swap');
          .font-serif { font-family: 'Playfair Display', serif; }
          .font-sans { font-family: 'Inter', sans-serif; }
        `}
      </style>

      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0F172A]/95 backdrop-blur-md border-b border-[#C9A96E]/10">
        <div className="max-w-7xl mx-auto px-5 sm:px-6 lg:px-10">
          <div className="flex items-center justify-between h-20">
            <div className="text-2xl sm:text-3xl font-serif font-bold tracking-tight text-[#C9A96E]">
              Atelier
            </div>
            <div className="flex items-center gap-6">
              <a href="/" className="text-[#94A3B8] hover:text-[#C9A96E] transition text-sm sm:text-base font-light tracking-wide">
                ← Home
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-28 pb-24 px-5 sm:px-6 lg:px-10 max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-block mb-6 px-8 py-3 bg-[#C9A96E]/10 text-[#C9A96E] font-serif text-xl rounded-full tracking-widest border border-[#C9A96E]/20">
            Legal
          </div>
          <h1 className="text-5xl sm:text-6xl font-serif font-bold mb-6 text-white">
            Terms of Service
          </h1>
          <p className="text-[#94A3B8] text-lg sm:text-xl font-light">
            Last Updated: February 14, 2026
          </p>
        </div>

        {/* Intro Banner */}
        <div className="bg-[#1E293B]/40 backdrop-blur-md rounded-3xl border border-[#C9A96E]/10 p-8 sm:p-12 mb-16 text-center">
          <p className="text-xl sm:text-2xl text-white/90 leading-relaxed max-w-4xl mx-auto font-light">
            By accessing or using Atelier, you agree to be bound by these Terms. 
            Atelier is currently in <span className="text-[#C9A96E] font-medium">beta/MVP stage</span> — features and terms may evolve.
          </p>
        </div>

        {/* Content Sections */}
        <div className="space-y-16 sm:space-y-20">
          
          {/* Section 1: Description of Service */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">1. Description of Service</h2>
            <div className="space-y-8">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">1.1 What Atelier Does</h3>
                <p className="text-[#94A3B8] text-lg mb-4">Atelier is an AI-powered calendar assistant that helps you:</p>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li>Schedule events and reminders</li>
                  <li>Create multi-day time-blocked plans</li>
                  <li>Manage your Google Calendar through natural language</li>
                  <li>Learn your scheduling preferences for personalized suggestions</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">1.2 What Atelier Is</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">An AI assistant</strong>, not a human scheduler</li>
                  <li><strong className="text-white">A productivity tool</strong>, not a professional scheduling service</li>
                  <li><strong className="text-white">Beta/MVP software</strong>, actively under development</li>
                  <li><strong className="text-white">Free to use</strong> during the MVP phase (pricing may be introduced later)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">1.3 What Atelier Is NOT</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li>Not a replacement for critical time-sensitive systems</li>
                  <li>Not guaranteed to be error-free or always available</li>
                  <li>Not liable for missed appointments due to AI errors</li>
                  <li>Not a medical, legal, or professional advice service</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 2: Eligibility */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">2. Eligibility</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">2.1 Age Requirement</h3>
                <p className="text-[#94A3B8] text-lg">You must be at least 18 years old to use Atelier. By using the Service, you represent and warrant that you are of legal age.</p>
              </div>
              
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">2.2 Google Account Requirement</h3>
                <p className="text-[#94A3B8] text-lg">You must have a valid Google account and grant Atelier permission to access your Google Calendar.</p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">2.3 Prohibited Users</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You may not use the Service if:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You are under 18 years of age</li>
                  <li>You are prohibited by law from receiving services from India or your jurisdiction</li>
                  <li>Your account has been previously terminated for violating these Terms</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 3: Account Registration and Security */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">3. Account Registration and Security</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">3.1 Account Creation</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You create an account by signing in with Google OAuth</li>
                  <li>You are responsible for maintaining the confidentiality of your account credentials</li>
                  <li>You are responsible for all activities that occur under your account</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">3.2 Account Security</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You agree to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Notify us immediately of any unauthorized access to your account</li>
                  <li>Use a strong, unique password for your Google account</li>
                  <li>Not share your account credentials with others</li>
                  <li>Log out from shared or public computers</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">3.3 Account Termination by You</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You may delete your account at any time by:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Contacting us at <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:underline">seam22rodr3@gmail.com</a></li>
                  <li>Revoking Atelier's access via Google Account Settings</li>
                  <li>Upon deletion, your data will be removed within 30 days (see Privacy Policy)</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 4: Google Calendar Access - HIGHLIGHTED */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">4. Google Calendar Access and Permissions</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">4.1 Required Permissions</h3>
                <p className="text-[#94A3B8] text-lg mb-3">By using Atelier, you grant us permission to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Read</strong> your Google Calendar events</li>
                  <li><strong className="text-white">Create</strong> new calendar events when you confirm our suggestions</li>
                  <li><strong className="text-white">Modify</strong> or <strong className="text-white">delete</strong> events when you request changes</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">4.2 Scope of Access</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>We only access your <strong className="text-white">primary Google Calendar</strong></li>
                  <li>We do not access other Google services (Gmail, Drive, etc.) unless explicitly stated</li>
                  <li>You can revoke access at any time via <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">Google Account Settings</a></li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">4.3 Your Responsibilities</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You are responsible for:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Reviewing AI suggestions before confirming calendar changes</li>
                  <li>Verifying that scheduled events are correct</li>
                  <li>Ensuring important events are not accidentally deleted</li>
                  <li>Maintaining backups of critical calendar information</li>
                </ul>
              </div>

              <div className="bg-[#C9A96E]/10 rounded-2xl p-8 border border-[#C9A96E]/30">
                <h3 className="text-2xl font-serif font-semibold mb-4 text-[#C9A96E]">4.4 Human-in-the-Loop Confirmation</h3>
                <ul className="list-disc pl-6 space-y-3 text-white text-lg">
                  <li>Atelier will <strong>never</strong> create, modify, or delete calendar events without your explicit confirmation</li>
                  <li>You must approve all suggested changes</li>
                  <li>You are in full control of your calendar at all times</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 5: Acceptable Use Policy */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">5. Acceptable Use Policy</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">5.1 Permitted Uses</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You may use Atelier for:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Personal scheduling and time management</li>
                  <li>Professional work scheduling (individual use)</li>
                  <li>Educational planning and study schedules</li>
                  <li>Any lawful purpose consistent with these Terms</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">5.2 Prohibited Uses</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You may NOT use Atelier to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Violate any laws or regulations</li>
                  <li>Harass, abuse, or harm others</li>
                  <li>Impersonate others or provide false information</li>
                  <li>Attempt to gain unauthorized access to the Service or other users' accounts</li>
                  <li>Use automated tools (bots, scrapers) to access the Service</li>
                  <li>Reverse engineer, decompile, or disassemble the Service</li>
                  <li>Transmit viruses, malware, or harmful code</li>
                  <li>Overload or interfere with the Service's infrastructure</li>
                  <li>Use the Service for any commercial purpose without authorization</li>
                  <li>Share explicit, violent, or illegal content with the AI</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">5.3 AI Misuse</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You may NOT:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Attempt to "jailbreak" or bypass the AI's safety guidelines</li>
                  <li>Use the AI to generate spam or malicious content</li>
                  <li>Exploit vulnerabilities in the AI system</li>
                  <li>Use the Service to train competing AI models</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">5.4 Enforcement</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We reserve the right to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Investigate violations of these Terms</li>
                  <li>Remove content that violates these Terms</li>
                  <li>Suspend or terminate accounts that violate these Terms</li>
                  <li>Report illegal activities to law enforcement</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 6: Intellectual Property Rights */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">6. Intellectual Property Rights</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.1 Our Intellectual Property</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>The Atelier platform, including its code, design, and AI models, is owned by us or our licensors</li>
                  <li>Our trademarks, logos, and branding are protected by intellectual property laws</li>
                  <li>You may not use our intellectual property without written permission</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.2 Your Content</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You retain ownership of your calendar data and messages</li>
                  <li>By using the Service, you grant us a limited license to:
                    <ul className="list-circle pl-6 mt-2 space-y-1">
                      <li>Process your data to provide the Service</li>
                      <li>Store anonymized summaries for personalization</li>
                      <li>Use aggregated, anonymized data to improve the Service</li>
                    </ul>
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.3 Open Source</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Atelier's source code is available at <a href="https://github.com/sea-rod/agent_planner" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">https://github.com/sea-rod/agent_planner</a></li>
                  <li>The code is licensed under the Apache License 2.0</li>
                  <li>You may use, modify, and distribute the code per the Apache 2.0 license</li>
                  <li>This does not grant rights to our branding, trademarks, or hosted service</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.4 Third-Party Services</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>We use third-party services (Google Calendar API, Groq, Weaviate, etc.)</li>
                  <li>These services have their own terms and licenses</li>
                  <li>You agree to comply with the terms of these third-party services</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 7: AI-Generated Content and Accuracy */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">7. AI-Generated Content and Accuracy</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">7.1 AI Limitations</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Atelier uses AI (large language models) which are not perfect</li>
                  <li>AI suggestions may contain errors, inaccuracies, or misunderstandings</li>
                  <li>The AI cannot guarantee optimal scheduling decisions</li>
                  <li>The AI's understanding is limited to the information you provide</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">7.2 No Warranty of Accuracy</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We do not warrant that:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>The AI will correctly interpret all requests</li>
                  <li>Suggested schedules will meet your expectations</li>
                  <li>Time calculations will always be accurate</li>
                  <li>Conflict detection will catch all scheduling conflicts</li>
                </ul>
              </div>

              <div className="bg-yellow-900/20 border border-yellow-600/30 rounded-2xl p-6">
                <h3 className="text-2xl font-serif font-semibold mb-4 text-yellow-400">7.3 Your Responsibility to Verify</h3>
                <p className="text-white text-lg mb-3">You agree to:</p>
                <ul className="list-disc pl-6 space-y-2 text-white text-lg">
                  <li><strong>Always review</strong> AI-generated schedules before confirming</li>
                  <li><strong>Double-check</strong> important events and times</li>
                  <li><strong>Not rely solely</strong> on Atelier for critical time-sensitive tasks</li>
                  <li><strong>Maintain backup</strong> scheduling methods for essential appointments</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">7.4 No Professional Advice</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Atelier does not provide medical, legal, financial, or professional advice</li>
                  <li>AI suggestions are for informational purposes only</li>
                  <li>Consult qualified professionals for specialized advice</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 8: Service Availability and Modifications */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">8. Service Availability and Modifications</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">8.1 Service Availability</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We strive to provide reliable service but do not guarantee 100% uptime. The Service may be temporarily unavailable due to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Maintenance and updates</li>
                  <li>Technical issues or outages</li>
                  <li>Third-party service disruptions (Google API, Groq, etc.)</li>
                  <li>Force majeure events</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">8.2 Beta/MVP Status</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Atelier is currently in <strong className="text-white">beta/MVP stage</strong></li>
                  <li>Features may change, be added, or removed without notice</li>
                  <li>We may reset data or make breaking changes during development</li>
                  <li>Service stability may vary as we test and improve</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">8.3 Modifications to Service</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We reserve the right to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Modify, suspend, or discontinue any part of the Service at any time</li>
                  <li>Change features, functionality, or pricing (with notice)</li>
                  <li>Update these Terms as the Service evolves</li>
                  <li>Impose usage limits or restrictions</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">8.4 Notice of Changes</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>We will notify you of significant changes via email or in-app notification</li>
                  <li>Continued use after changes constitutes acceptance of the new Terms</li>
                  <li>If you disagree with changes, you may terminate your account</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 9: Pricing and Payment */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">9. Pricing and Payment</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">9.1 Current Pricing</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Atelier is currently <strong className="text-white">free to use</strong> during the MVP phase</li>
                  <li>We reserve the right to introduce paid plans in the future</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">9.2 Future Paid Plans</h3>
                <p className="text-[#94A3B8] text-lg mb-3">If we introduce paid plans:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>We will provide advance notice (minimum 30 days)</li>
                  <li>Existing users may be grandfathered into free or discounted plans</li>
                  <li>You may choose to continue using the Service under the new pricing or terminate your account</li>
                  <li>All paid plans will be clearly communicated before charging</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">9.3 No Refunds for Free Service</h3>
                <p className="text-[#94A3B8] text-lg">Since the Service is currently free, no refunds are applicable.</p>
              </div>
            </div>
          </section>

          {/* Section 10: Limitation of Liability - CRITICAL */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">10. Limitation of Liability</h2>
            
            <div className="bg-red-900/20 border border-red-600/30 rounded-2xl p-8 mb-8">
              <h3 className="text-2xl font-serif font-semibold mb-4 text-red-400">10.1 Disclaimer of Warranties</h3>
              <p className="text-white text-lg mb-4">THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO:</p>
              <ul className="list-disc pl-6 space-y-2 text-white text-lg">
                <li>Warranties of merchantability</li>
                <li>Fitness for a particular purpose</li>
                <li>Non-infringement</li>
                <li>Accuracy, reliability, or completeness</li>
              </ul>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">10.2 Limitation of Liability</h3>
                <p className="text-[#94A3B8] text-lg mb-4">TO THE MAXIMUM EXTENT PERMITTED BY LAW:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>WE ARE NOT LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES</li>
                  <li>THIS INCLUDES DAMAGES FOR LOST PROFITS, DATA LOSS, OR BUSINESS INTERRUPTION</li>
                  <li className="text-white font-semibold">OUR TOTAL LIABILITY TO YOU SHALL NOT EXCEED ₹1,000 (One Thousand Indian Rupees) OR THE AMOUNT YOU PAID IN THE LAST 12 MONTHS, WHICHEVER IS GREATER</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">10.3 Specific Limitations</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We are not liable for:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Missed appointments</strong> due to AI errors, misunderstandings, or technical failures</li>
                  <li><strong className="text-white">Calendar conflicts</strong> that the AI failed to detect</li>
                  <li><strong className="text-white">Data loss</strong> due to service outages, bugs, or third-party failures</li>
                  <li><strong className="text-white">Scheduling errors</strong> resulting from unclear or ambiguous requests</li>
                  <li><strong className="text-white">Harm</strong> resulting from reliance on AI-generated content</li>
                  <li><strong className="text-white">Third-party actions</strong> (Google API changes, Groq outages, etc.)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">10.4 MVP-Specific Disclaimer</h3>
                <p className="text-[#94A3B8] text-lg mb-3">As an MVP/beta service:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Bugs and errors are expected</li>
                  <li>Data handling practices may change</li>
                  <li>Service stability is not guaranteed</li>
                  <li>You use the Service at your own risk</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">10.5 Exceptions</h3>
                <p className="text-[#94A3B8] text-lg">Some jurisdictions do not allow the exclusion of certain warranties or limitations of liability. In such cases, the above limitations may not apply to you, and liability will be limited to the maximum extent permitted by law.</p>
              </div>
            </div>
          </section>

          {/* Section 11: Indemnification */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">11. Indemnification</h2>
            <p className="text-[#94A3B8] text-lg mb-4">You agree to indemnify, defend, and hold harmless Atelier, its developers, and affiliates from any claims, damages, losses, liabilities, and expenses (including legal fees) arising from:</p>
            <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
              <li>Your use or misuse of the Service</li>
              <li>Your violation of these Terms</li>
              <li>Your violation of any third-party rights</li>
              <li>Your violation of applicable laws or regulations</li>
              <li>Content you submit or actions you take using the Service</li>
            </ul>
          </section>

          {/* Section 12: Privacy and Data Protection */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">12. Privacy and Data Protection</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">12.1 Privacy Policy</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Your use of the Service is also governed by our Privacy Policy</li>
                  <li>We do NOT store full message transcripts—only anonymized summaries</li>
                  <li>See our Privacy Policy for details on data collection, use, and storage</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">12.2 Data Processing</h3>
                <p className="text-[#94A3B8] text-lg mb-3">By using the Service, you consent to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Processing of your calendar data to provide scheduling services</li>
                  <li>Storage of anonymized summaries for personalization</li>
                  <li>Transfer of data to third-party services (Google, Groq, Weaviate, Cohere) as described in the Privacy Policy</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">12.3 Data Security</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>We implement industry-standard security measures</li>
                  <li>However, no system is 100% secure</li>
                  <li>You acknowledge the inherent risks of transmitting data over the internet</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 13: Third-Party Services and Links */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">13. Third-Party Services and Links</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">13.1 Third-Party Services</h3>
                <p className="text-[#94A3B8] text-lg mb-3">Atelier integrates with:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Google Calendar API</strong> (calendar access)</li>
                  <li><strong className="text-white">Groq</strong> (AI language processing)</li>
                  <li><strong className="text-white">Weaviate</strong> (vector database)</li>
                  <li><strong className="text-white">Cohere</strong> (text embeddings)</li>
                </ul>
                <p className="text-[#94A3B8] text-lg mt-3">You agree to comply with the terms of service of these third-party providers.</p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">13.2 Third-Party Links</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>The Service may contain links to third-party websites</li>
                  <li>We are not responsible for the content or practices of third-party websites</li>
                  <li>Your use of third-party websites is at your own risk</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">13.3 No Endorsement</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Links to third-party services do not imply endorsement</li>
                  <li>We are not responsible for third-party actions or content</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 14: Termination */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">14. Termination</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">14.1 Termination by You</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You may terminate your account at any time by:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Contacting us at <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:underline">seam22rodr3@gmail.com</a></li>
                  <li>Revoking Google Calendar access</li>
                  <li>Your data will be deleted within 30 days per our Privacy Policy</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">14.2 Termination by Us</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We may suspend or terminate your account if:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You violate these Terms</li>
                  <li>You engage in prohibited activities</li>
                  <li>You misuse the Service</li>
                  <li>Required by law or legal process</li>
                  <li>We discontinue the Service</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">14.3 Effect of Termination</h3>
                <p className="text-[#94A3B8] text-lg mb-3">Upon termination:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Your access to the Service will be revoked</li>
                  <li>Your data will be deleted per our Privacy Policy</li>
                  <li>Sections that should survive termination (e.g., liability limitations, indemnification) will remain in effect</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">14.4 No Refunds</h3>
                <p className="text-[#94A3B8] text-lg">Since the Service is currently free, no refunds are applicable upon termination.</p>
              </div>
            </div>
          </section>

          {/* Section 15: Dispute Resolution */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">15. Dispute Resolution</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">15.1 Governing Law</h3>
                <p className="text-[#94A3B8] text-lg">These Terms are governed by the laws of India, without regard to conflict of law principles.</p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">15.2 Jurisdiction</h3>
                <p className="text-[#94A3B8] text-lg">You agree to submit to the exclusive jurisdiction of the courts in Goa, India for resolution of any disputes.</p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">15.3 Informal Resolution</h3>
                <p className="text-[#94A3B8] text-lg mb-3">Before filing a legal claim, you agree to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Contact us at <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:underline">seam22rodr3@gmail.com</a> to resolve the dispute informally</li>
                  <li>Provide a detailed description of the dispute</li>
                  <li>Allow 30 days for us to attempt resolution</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">15.4 Arbitration (Optional)</h3>
                <p className="text-[#94A3B8] text-lg">If informal resolution fails, disputes may be resolved through binding arbitration in Goa, India, under the Indian Arbitration and Conciliation Act, 1996.</p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">15.5 Class Action Waiver</h3>
                <p className="text-[#94A3B8] text-lg">You agree to resolve disputes individually and waive any right to participate in class action lawsuits.</p>
              </div>
            </div>
          </section>

          {/* Section 16: Miscellaneous */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">16. Miscellaneous</h2>
            <div className="space-y-6 text-[#94A3B8] text-lg">
              <div>
                <h3 className="text-xl font-semibold mb-3 text-white">16.1 Entire Agreement</h3>
                <p>These Terms, together with our Privacy Policy, constitute the entire agreement between you and Atelier regarding the Service.</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-3 text-white">16.2 Severability</h3>
                <p>If any provision of these Terms is found to be invalid or unenforceable, the remaining provisions will remain in full force and effect.</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-3 text-white">16.3 Waiver</h3>
                <p>Our failure to enforce any provision of these Terms does not constitute a waiver of that provision.</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-3 text-white">16.4 Assignment</h3>
                <p>You may not assign or transfer these Terms without our written consent. We may assign or transfer these Terms at any time.</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-3 text-white">16.5 Force Majeure</h3>
                <p>We are not liable for delays or failures due to events beyond our reasonable control (e.g., natural disasters, wars, pandemics, internet outages).</p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-3 text-white">16.6 Feedback</h3>
                <p className="mb-3">If you provide feedback or suggestions about the Service:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>We may use your feedback without compensation or attribution</li>
                  <li>You grant us a perpetual, irrevocable license to use your feedback</li>
                  <li>Feedback does not create any confidentiality obligations</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-3 text-white">16.7 Language</h3>
                <p>These Terms are written in English. Translations may be provided for convenience, but the English version controls in case of conflicts.</p>
              </div>
            </div>
          </section>

          {/* Section 17: Open Source and Contributions */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">17. Open Source and Contributions</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">17.1 Open Source Code</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Atelier's source code is available under the Apache License 2.0</li>
                  <li>You may view the code at <a href="https://github.com/sea-rod/agent_planner" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">https://github.com/sea-rod/agent_planner</a></li>
                  <li>Contributions are welcome via pull requests</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">17.2 Contributor License</h3>
                <p className="text-[#94A3B8] text-lg mb-3">By contributing code, you:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Grant us a license to use your contribution under the Apache 2.0 license</li>
                  <li>Represent that you have the right to grant this license</li>
                  <li>Agree that your contribution may be included in the hosted Service</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">17.3 Hosted Service vs. Code</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>The <strong className="text-white">code</strong> is open source (Apache 2.0)</li>
                  <li>The <strong className="text-white">hosted service</strong> (atelier.vercel.app) is subject to these Terms</li>
                  <li>You may self-host the code, but this does not grant rights to our branding or hosted infrastructure</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 18: Contact Information */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">18. Contact Information</h2>
            <p className="text-[#94A3B8] text-lg mb-4">For questions, concerns, or notices regarding these Terms:</p>
            <div className="bg-[#1E293B]/40 rounded-2xl p-6 border border-[#C9A96E]/20">
              <p className="text-lg mb-2"><strong className="text-white">Email:</strong> <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:underline">seam22rodr3@gmail.com</a></p>
              <p className="text-lg mb-2"><strong className="text-white">GitHub:</strong> <a href="https://github.com/sea-rod/agent_planner/issues" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">https://github.com/sea-rod/agent_planner/issues</a></p>
              <p className="text-lg"><strong className="text-white">Response Time:</strong> <span className="text-[#94A3B8]">We aim to respond within 72 hours</span></p>
            </div>
          </section>

          {/* Section 19: Updates to Terms */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">19. Updates to Terms</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">19.1 Notification of Changes</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We may update these Terms from time to time. When we do:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>We will update the "Last Updated" date at the top</li>
                  <li>We will notify you via email or in-app notification for significant changes</li>
                  <li>You will be given at least 7 days' notice before changes take effect</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">19.2 Acceptance of Changes</h3>
                <p className="text-[#94A3B8] text-lg">By continuing to use the Service after changes take effect, you agree to the updated Terms. If you disagree, you must stop using the Service and delete your account.</p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">19.3 Version History</h3>
                <p className="text-[#94A3B8] text-lg">Previous versions of these Terms are available upon request.</p>
              </div>
            </div>
          </section>

          {/* Section 20: Special Provisions for Beta/MVP Users */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">20. Special Provisions for Beta/MVP Users</h2>
            <p className="text-[#94A3B8] text-lg mb-6">As an early user of Atelier's beta/MVP:</p>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">20.1 Acknowledgment of Beta Status</h3>
                <p className="text-[#94A3B8] text-lg mb-3">You acknowledge that:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>The Service is experimental and under active development</li>
                  <li>Features may change or be removed without notice</li>
                  <li>Bugs and errors are expected</li>
                  <li>Service interruptions may occur</li>
                  <li>Data handling practices may evolve</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">20.2 Feedback Encouraged</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Your feedback helps us improve the Service</li>
                  <li>You are encouraged to report bugs, suggest features, and provide honest feedback</li>
                  <li>We may use your feedback without compensation</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">20.3 Grandfathering (Future Paid Plans)</h3>
                <p className="text-[#94A3B8] text-lg mb-3">If we introduce paid plans, beta users may receive:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Discounted pricing</li>
                  <li>Early adopter benefits</li>
                  <li>Grandfathered features</li>
                  <li>However, this is not guaranteed</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">20.4 Service Discontinuation</h3>
                <p className="text-[#94A3B8] text-lg">We reserve the right to discontinue the beta Service at any time with reasonable notice (minimum 30 days).</p>
              </div>
            </div>
          </section>

          {/* Table Section */}
          <section className="mt-20">
            <h2 className="text-4xl font-serif font-bold mb-10 text-[#C9A96E] text-center">
              Quick Reference Summary
            </h2>
            <div className="overflow-x-auto rounded-2xl border border-[#C9A96E]/10 bg-[#1E293B]/30 backdrop-blur-sm">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#C9A96E]/10">
                    <th className="px-6 py-5 font-serif text-lg text-[#C9A96E]">Topic</th>
                    <th className="px-6 py-5 font-serif text-lg text-[#C9A96E]">Key Point</th>
                  </tr>
                </thead>
                <tbody className="text-[#94A3B8]">
                  {[
                    { label: "Age Requirement", point: "Must be 18+" },
                    { label: "Service Status", point: "Beta/MVP (expect changes)", bg: true },
                    { label: "Current Pricing", point: "Free (may introduce paid plans later)" },
                    { label: "AI Accuracy", point: "Not guaranteed — always verify", bg: true },
                    { label: "Data Storage", point: "Only summaries stored, not full messages" },
                    { label: "Liability", point: "Limited to ₹1,000 or amount paid", bg: true },
                    { label: "Google Access", point: "Read, write, delete with your confirmation" },
                    { label: "Human-in-the-Loop", point: "No changes without your approval", bg: true },
                    { label: "Open Source", point: "Code is Apache 2.0, service has separate terms" },
                    { label: "Termination", point: "You can delete account anytime", bg: true },
                    { label: "Governing Law", point: "India (Goa jurisdiction)" },
                    { label: "Contact", point: "seam22rodr3@gmail.com", bg: true },
                  ].map((row, idx) => (
                    <tr key={idx} className={`border-t border-[#C9A96E]/5 ${row.bg ? 'bg-[#1E293B]/20' : ''}`}>
                      <td className="px-6 py-5 font-medium text-white/80">{row.label}</td>
                      <td className="px-6 py-5">{row.point}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="text-center text-sm text-[#94A3B8] mt-6 italic">
              This is a simplified summary. The full Terms above govern your use of Atelier.
            </p>
          </section>

          {/* Final Acknowledgment */}
          <section className="mt-20 text-center">
            <div className="bg-[#C9A96E]/10 rounded-3xl p-10 sm:p-16 border border-[#C9A96E]/20">
              <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">
                Acknowledgment and Acceptance
              </h2>
              <p className="text-xl sm:text-2xl text-white/90 max-w-4xl mx-auto leading-relaxed font-light mb-8">
                BY CLICKING "ACCEPT," SIGNING UP, OR USING THE SERVICE, YOU ACKNOWLEDGE THAT:
              </p>
              <ul className="text-left max-w-3xl mx-auto space-y-3 text-lg text-white/80">
                <li>1. You have read and understood these Terms</li>
                <li>2. You agree to be bound by these Terms</li>
                <li>3. You are at least 18 years old</li>
                <li>4. You have the authority to enter into this agreement</li>
                <li>5. You understand the Service is in beta/MVP stage</li>
                <li>6. You agree to the limitations of liability and disclaimers</li>
                <li>7. You will use the Service responsibly and in accordance with these Terms</li>
              </ul>
              <p className="mt-10 text-[#94A3B8] text-lg">
                Thank you for using Atelier.<br/>
                <span className="text-[#C9A96E] font-medium">Crafted with care in Goa, India.</span>
              </p>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-[#0F172A]/95 border-t border-[#C9A96E]/10 py-12 text-center text-[#94A3B8]">
        <div className="max-w-7xl mx-auto px-6">
          <p className="text-lg mb-4 font-serif italic text-white/80">Atelier – Where time meets timeless elegance</p>
          <div className="flex justify-center gap-6 mb-4 text-sm">
            <a href="/privacy" className="hover:text-[#C9A96E] transition">Privacy Policy</a>
            <a href="/terms" className="hover:text-[#C9A96E] transition">Terms of Service</a>
            <a href="https://github.com/sea-rod/agent_planner" target="_blank" rel="noopener noreferrer" className="hover:text-[#C9A96E] transition">GitHub</a>
          </div>
          <p className="text-sm opacity-70">
            © 2026 Atelier. All rights reserved.<br/>
            Contact: <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:text-[#D4B978] transition">seam22rodr3@gmail.com</a>
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Terms;

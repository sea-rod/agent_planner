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

const Privacy = () => {
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
            Privacy Policy
          </h1>
          <p className="text-[#94A3B8] text-lg sm:text-xl font-light">
            Last Updated: February 14, 2026
          </p>
        </div>

        {/* Intro Banner */}
        <div className="bg-[#1E293B]/40 backdrop-blur-md rounded-3xl border border-[#C9A96E]/10 p-8 sm:p-12 mb-16 text-center">
          <p className="text-xl sm:text-2xl text-white/90 leading-relaxed max-w-4xl mx-auto font-light">
            We are committed to protecting your privacy and being transparent about how we handle your data. 
            We do <span className="text-[#C9A96E] font-medium">NOT store your full messages</span> — only anonymized summaries.
          </p>
        </div>

        {/* Content Sections */}
        <div className="space-y-16 sm:space-y-20">
          
          {/* Section 1: Information We Collect */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">1. Information We Collect</h2>
            <div className="space-y-8">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">1.1 Information You Provide</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Account Information:</strong> Email address and name when you sign up via Google OAuth</li>
                  <li><strong className="text-white">Calendar Data:</strong> Events, titles, descriptions, dates, times, and locations from your Google Calendar</li>
                  <li><strong className="text-white">Conversation Summaries:</strong> We do NOT store your full messages. Only anonymized summaries and preferences are stored in our vector database for personalization</li>
                  <li><strong className="text-white">User Preferences:</strong> Scheduling preferences and patterns learned from your interactions</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">1.2 Automatically Collected Information</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Authentication Tokens:</strong> Google OAuth tokens to access your calendar</li>
                  <li><strong className="text-white">Usage Data:</strong> How you interact with the app (timestamps, features used)</li>
                  <li><strong className="text-white">Technical Data:</strong> Browser type, device information, IP address (for security purposes)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">1.3 Information from Third Parties</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Google Calendar API:</strong> We access your calendar events when you grant us permission</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 2: How We Use Your Information */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">2. How We Use Your Information</h2>
            <p className="text-[#94A3B8] text-lg mb-6">We use your information to:</p>
            <div className="space-y-8">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">2.1 Core Functionality</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Schedule Management:</strong> Read your calendar to find free slots and check for conflicts</li>
                  <li><strong className="text-white">Event Creation:</strong> Create calendar events when you confirm our AI's suggestions</li>
                  <li><strong className="text-white">Event Deletion:</strong> Remove events from your calendar when you request it</li>
                  <li><strong className="text-white">Intelligent Planning:</strong> Learn your scheduling patterns to provide personalized recommendations</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">2.2 Service Improvement</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Memory System:</strong> Store anonymized summaries of your preferences and patterns to improve future suggestions</li>
                  <li><strong className="text-white">Conversation Context:</strong> Your full messages are processed in real-time but NOT stored permanently. Only summaries are kept</li>
                  <li><strong className="text-white">Performance Optimization:</strong> Analyze usage patterns to improve our AI assistant</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">2.3 Communication</h3>
                <ul className="list-disc pl-6 space-y-3 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Service Updates:</strong> Notify you about changes to our service</li>
                  <li><strong className="text-white">Support:</strong> Respond to your questions and troubleshoot issues</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 3: Google Calendar Access */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">3. Google Calendar Access</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">3.1 What We Access</h3>
                <p className="text-[#94A3B8] text-lg mb-3">When you connect your Google Calendar, we request permission to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Read</strong> your calendar events (titles, dates, times, descriptions)</li>
                  <li><strong className="text-white">Write</strong> new events when you confirm our suggestions</li>
                  <li><strong className="text-white">Modify</strong> or delete events when you request changes</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">3.2 How We Use Google Calendar Data</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Calendar data is accessed in real-time when you interact with Atelier</li>
                  <li>We analyze your schedule to find free time slots</li>
                  <li>We check for conflicts before suggesting new events</li>
                  <li>We store event metadata (but not full event details) to learn your scheduling patterns</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">3.3 Google Calendar Data Retention</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>We do <strong className="text-white">not</strong> permanently store the full content of your calendar events</li>
                  <li>We only cache minimal event metadata (summary, start/end times) temporarily for conversation context</li>
                  <li>Scheduling patterns (e.g., "user prefers morning workouts") are stored in anonymized form</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">3.4 Your Control</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You can revoke Atelier's access to your Google Calendar at any time via <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">Google Account Settings</a></li>
                  <li>Revoking access will stop all calendar operations but will not delete your conversation summaries</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 4: How We Store Your Data - HIGHLIGHTED */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">4. How We Store Your Data</h2>
            
            <div className="bg-[#C9A96E]/10 rounded-2xl p-8 border border-[#C9A96E]/30 mb-8">
              <h3 className="text-2xl font-serif font-semibold mb-6 text-[#C9A96E]">4.1 What We Store vs. What We Don't Store</h3>
              <div className="grid md:grid-cols-2 gap-8">
                <div className="bg-red-900/20 rounded-xl p-6 border border-red-600/30">
                  <h4 className="text-xl font-semibold mb-4 text-red-400">❌ We DO NOT Store:</h4>
                  <ul className="space-y-2 text-white text-base">
                    <li>• Full text of your messages to the AI</li>
                    <li>• Complete conversation transcripts</li>
                    <li>• Your raw calendar event descriptions</li>
                  </ul>
                </div>
                
                <div className="bg-green-900/20 rounded-xl p-6 border border-green-600/30">
                  <h4 className="text-xl font-semibold mb-4 text-green-400">✅ We DO Store:</h4>
                  <ul className="space-y-2 text-white text-base">
                    <li>• Anonymized summaries of your preferences</li>
                    <li>• Scheduling patterns</li>
                    <li>• Semantic embeddings (mathematical representations)</li>
                    <li>• Event metadata (start/end times, conflict info)</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">4.2 Data Storage Locations</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Authentication:</strong> Supabase (US-based cloud infrastructure)</li>
                  <li><strong className="text-white">Conversation Summaries:</strong> Weaviate vector database (cloud-hosted) - stores only embeddings and summaries</li>
                  <li><strong className="text-white">Calendar Tokens:</strong> Encrypted in Supabase database</li>
                  <li><strong className="text-white">Application Logs:</strong> Render.com/Railway.app servers (US-based)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">4.3 Data Security Measures</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Encryption in Transit:</strong> All data transmitted via HTTPS/TLS</li>
                  <li><strong className="text-white">Encryption at Rest:</strong> Database encryption for stored data</li>
                  <li><strong className="text-white">Access Controls:</strong> Only authorized systems can access your data</li>
                  <li><strong className="text-white">Token Security:</strong> Google OAuth tokens are encrypted and never exposed to client-side code</li>
                  <li><strong className="text-white">Message Privacy:</strong> Your full messages are processed in-memory and discarded after generating responses</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">4.4 Data Retention</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Account Data:</strong> Retained until you delete your account</li>
                  <li><strong className="text-white">Conversation Summaries:</strong> Retained for 90 days, then automatically deleted</li>
                  <li><strong className="text-white">Scheduling Patterns:</strong> Retained to improve service; anonymized after 180 days</li>
                  <li><strong className="text-white">Authentication Tokens:</strong> Refreshed automatically; old tokens expire within 1 hour</li>
                  <li><strong className="text-white">Full Messages:</strong> NOT stored - deleted immediately after processing</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 5: Data Sharing and Disclosure */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">5. Data Sharing and Disclosure</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">5.1 We Do NOT Sell Your Data</h3>
                <p className="text-[#94A3B8] text-lg">We will never sell, rent, or trade your personal information to third parties.</p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">5.2 Third-Party Services We Use</h3>
                <p className="text-[#94A3B8] text-lg mb-4">We share limited data with trusted service providers:</p>
                
                <div className="overflow-x-auto rounded-2xl border border-[#C9A96E]/10 bg-[#1E293B]/30 backdrop-blur-sm">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="bg-[#C9A96E]/10">
                        <th className="px-4 py-4 font-serif text-base text-[#C9A96E]">Service</th>
                        <th className="px-4 py-4 font-serif text-base text-[#C9A96E]">Purpose</th>
                        <th className="px-4 py-4 font-serif text-base text-[#C9A96E]">Data Shared</th>
                        <th className="px-4 py-4 font-serif text-base text-[#C9A96E]">Stored?</th>
                      </tr>
                    </thead>
                    <tbody className="text-[#94A3B8] text-sm">
                      {[
                        { service: "Google Calendar API", purpose: "Calendar integration", data: "Your calendar events", stored: "Yes (in your Google account)" },
                        { service: "Supabase", purpose: "Authentication & database", data: "Email, user ID, encrypted tokens", stored: "Yes", bg: true },
                        { service: "Weaviate", purpose: "Vector database", data: "Summaries & embeddings (anonymized)", stored: "Yes" },
                        { service: "Groq", purpose: "AI language model", data: "Messages in real-time", stored: "NO", bg: true, highlight: true },
                        { service: "Cohere", purpose: "Text embeddings", data: "Summary text", stored: "NO", highlight: true },
                        { service: "Vercel/Render", purpose: "Hosting", data: "Technical logs (IP, metadata)", stored: "Yes (temporary)", bg: true },
                      ].map((row, idx) => (
                        <tr key={idx} className={`border-t border-[#C9A96E]/5 ${row.bg ? 'bg-[#1E293B]/20' : ''}`}>
                          <td className="px-4 py-4 font-medium text-white/80">{row.service}</td>
                          <td className="px-4 py-4">{row.purpose}</td>
                          <td className="px-4 py-4">{row.data}</td>
                          <td className={`px-4 py-4 font-semibold ${row.highlight ? 'text-green-400' : ''}`}>{row.stored}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                
                <p className="text-[#94A3B8] text-lg mt-6">
                  <strong className="text-white">Important:</strong> Your full messages are sent to Groq for real-time AI processing but are NOT stored or used for training by Groq (per their privacy policy).
                </p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">5.3 Legal Disclosure</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We may disclose your information if required by law or to:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Comply with legal processes (subpoenas, court orders)</li>
                  <li>Protect our rights and safety</li>
                  <li>Prevent fraud or security threats</li>
                  <li>Enforce our Terms of Service</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 6: Your Rights and Choices */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">6. Your Rights and Choices</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.1 Access and Portability</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You can request a copy of your stored summaries and preferences at any time</li>
                  <li>Contact us at <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:underline">seam22rodr3@gmail.com</a> to request your data export</li>
                  <li>Note: We cannot provide full message transcripts as they are not stored</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.2 Correction and Deletion</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You can update your account information in the app settings</li>
                  <li>You can delete your account and all associated data by contacting us</li>
                  <li>Upon account deletion, we will remove all personal data within 30 days</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.3 Opt-Out of AI Memory</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>You can request that we disable learning from your interactions</li>
                  <li>This will make the assistant less personalized but fully functional</li>
                  <li>We will delete all stored summaries and preferences upon request</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">6.4 Revoke Calendar Access</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Revoke access via <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">Google Account Permissions</a></li>
                  <li>This immediately stops all calendar operations</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 7-9: Children, International, Changes */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">7. Children's Privacy</h2>
            <p className="text-[#94A3B8] text-lg">
              Atelier is not intended for users under 18 years of age. We do not knowingly collect personal information from children. If you believe a child has provided us with personal data, please contact us immediately.
            </p>
          </section>

          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">8. International Users</h2>
            <p className="text-[#94A3B8] text-lg mb-4">
              Atelier is operated from India. If you are accessing our service from outside India, please be aware that your information may be transferred to, stored, and processed in India or other countries where our service providers operate.
            </p>
            <p className="text-[#94A3B8] text-lg">
              By using Atelier, you consent to the transfer of your information to countries outside your country of residence, which may have different data protection laws.
            </p>
          </section>

          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">9. Changes to This Privacy Policy</h2>
            <p className="text-[#94A3B8] text-lg mb-4">We may update this Privacy Policy from time to time. When we make changes:</p>
            <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
              <li>We will update the "Last Updated" date at the top</li>
              <li>For significant changes, we will notify you via email or in-app notification</li>
              <li>Your continued use of Atelier after changes constitutes acceptance of the updated policy</li>
            </ul>
            <p className="text-[#94A3B8] text-lg mt-4">We encourage you to review this Privacy Policy periodically.</p>
          </section>

          {/* Section 10: AI and Automated Decision-Making */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">10. AI and Automated Decision-Making</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">10.1 How Our AI Works</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Atelier uses AI (large language models) to understand your requests and suggest schedules</li>
                  <li>The AI analyzes your calendar, stored preferences, and conversation summaries</li>
                  <li><strong className="text-white">Human-in-the-Loop:</strong> Our AI never makes calendar changes without your explicit approval</li>
                </ul>
              </div>

              <div className="bg-[#C9A96E]/10 rounded-2xl p-6 border border-[#C9A96E]/30">
                <h3 className="text-2xl font-serif font-semibold mb-4 text-[#C9A96E]">10.2 AI Data Processing</h3>
                <ul className="list-disc pl-6 space-y-3 text-white text-lg">
                  <li>Your messages are sent to Groq's API for real-time language processing</li>
                  <li>Groq does not store or train on your data (per their privacy policy)</li>
                  <li>We use Weaviate to store embeddings (mathematical representations) and summaries of conversations for memory</li>
                  <li className="font-semibold"><strong>Your full messages are NOT stored anywhere</strong> - only anonymized summaries and patterns</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">10.3 Accuracy Disclaimer</h3>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>AI suggestions are not perfect and may contain errors</li>
                  <li>Always review AI-generated schedules before confirming</li>
                  <li>We are not liable for scheduling mistakes due to AI misunderstandings</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 11: Data Minimization Principle */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">11. Data Minimization Principle</h2>
            <p className="text-[#94A3B8] text-lg mb-4">We follow the principle of data minimization:</p>
            <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
              <li>We only collect data necessary for the service to function</li>
              <li>We do not store full conversation transcripts</li>
              <li>We anonymize and summarize data where possible</li>
              <li>We automatically delete old data according to our retention policy</li>
            </ul>
            <p className="text-[#94A3B8] text-lg mt-4">
              This approach ensures maximum privacy while still providing personalized service.
            </p>
          </section>

          {/* Section 12: Data Breach Notification */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">12. Data Breach Notification</h2>
            <p className="text-[#94A3B8] text-lg mb-4">In the unlikely event of a data breach that affects your personal information:</p>
            <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
              <li>We will notify you within 72 hours via email</li>
              <li>We will provide details about the breach and steps you should take</li>
              <li>We will work with authorities to investigate and remediate the issue</li>
            </ul>
            <p className="text-[#94A3B8] text-lg mt-6">
              Given that we do not store full message content, the exposure in any breach is limited to:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg mt-3">
              <li>Account information (email, name)</li>
              <li>Anonymized preference summaries</li>
              <li>Calendar event metadata (not full calendar contents)</li>
            </ul>
          </section>

          {/* Section 13: Contact Us */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">13. Contact Us</h2>
            <p className="text-[#94A3B8] text-lg mb-4">If you have questions, concerns, or requests regarding this Privacy Policy or your data:</p>
            <div className="bg-[#1E293B]/40 rounded-2xl p-6 border border-[#C9A96E]/20">
              <p className="text-lg mb-2"><strong className="text-white">Email:</strong> <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:underline">seam22rodr3@gmail.com</a></p>
              <p className="text-lg mb-2"><strong className="text-white">GitHub Issues:</strong> <a href="https://github.com/sea-rod/agent_planner/issues" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">https://github.com/sea-rod/agent_planner/issues</a></p>
              <p className="text-lg"><strong className="text-white">Response Time:</strong> <span className="text-[#94A3B8]">We aim to respond within 72 hours</span></p>
            </div>
          </section>

          {/* Section 14: Compliance and Certifications */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">14. Compliance and Certifications</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">14.1 GDPR Compliance (EU Users)</h3>
                <p className="text-[#94A3B8] text-lg mb-3">If you are in the European Union, you have additional rights under GDPR:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Right to Access:</strong> Request a copy of your stored summaries and preferences</li>
                  <li><strong className="text-white">Right to Rectification:</strong> Correct inaccurate data</li>
                  <li><strong className="text-white">Right to Erasure:</strong> Request deletion of your data</li>
                  <li><strong className="text-white">Right to Restrict Processing:</strong> Limit how we use your data</li>
                  <li><strong className="text-white">Right to Data Portability:</strong> Receive your data in a structured format</li>
                  <li><strong className="text-white">Right to Object:</strong> Object to our processing of your data</li>
                </ul>
                <p className="text-[#94A3B8] text-lg mt-4">
                  To exercise these rights, contact us at <a href="mailto:seam22rodr3@gmail.com" className="text-[#C9A96E] hover:underline">seam22rodr3@gmail.com</a>.
                </p>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">14.2 CCPA Compliance (California Users)</h3>
                <p className="text-[#94A3B8] text-lg mb-3">If you are a California resident, you have rights under the California Consumer Privacy Act:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li>Right to know what personal information we collect</li>
                  <li>Right to delete personal information</li>
                  <li>Right to opt-out of data sales (we do not sell data)</li>
                  <li>Right to non-discrimination for exercising your rights</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-serif font-semibold mb-4 text-white">14.3 Data Processing Lawful Basis (GDPR)</h3>
                <p className="text-[#94A3B8] text-lg mb-3">We process your data based on:</p>
                <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
                  <li><strong className="text-white">Consent:</strong> You explicitly authorize Google Calendar access</li>
                  <li><strong className="text-white">Contract:</strong> Processing necessary to provide the service</li>
                  <li><strong className="text-white">Legitimate Interest:</strong> Improving service quality through anonymized learning</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Section 15: MVP Disclaimer */}
          <section>
            <div className="bg-yellow-900/20 border border-yellow-600/30 rounded-2xl p-8">
              <h2 className="text-4xl font-serif font-bold mb-6 text-yellow-400">15. MVP Disclaimer</h2>
              <p className="text-white text-lg mb-4"><strong>Important Notice:</strong> Atelier is currently in <strong>beta/MVP stage</strong>. This means:</p>
              <ul className="list-disc pl-6 space-y-2 text-white text-lg">
                <li>Features and data handling practices may change as we improve the service</li>
                <li>We are actively testing and may experience technical issues</li>
                <li>Your feedback helps us build a better product</li>
                <li>We will notify users of major changes to data handling</li>
              </ul>
              <p className="text-white text-lg mt-6">
                Despite being an MVP, we take your privacy seriously and follow industry best practices for data protection, including not storing your full messages.
              </p>
            </div>
          </section>

          {/* Section 16: Open Source */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">16. Open Source</h2>
            <p className="text-[#94A3B8] text-lg mb-4">
              Atelier's source code is available at <a href="https://github.com/sea-rod/agent_planner" target="_blank" rel="noopener noreferrer" className="text-[#C9A96E] hover:underline">https://github.com/sea-rod/agent_planner</a>. 
              You can review how we handle your data by examining the codebase, including:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
              <li>How messages are processed in real-time</li>
              <li>How summaries are generated and stored</li>
              <li>What data is actually persisted in our databases</li>
            </ul>
          </section>

          {/* Section 17: Transparency Commitment */}
          <section>
            <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">17. Transparency Commitment</h2>
            <p className="text-[#94A3B8] text-lg mb-4">To maintain trust, we commit to:</p>
            <ul className="list-disc pl-6 space-y-2 text-[#94A3B8] text-lg">
              <li>Being transparent about what data we collect and store</li>
              <li>Never storing full message transcripts</li>
              <li>Only using anonymized summaries for personalization</li>
              <li>Giving you control over your data</li>
              <li>Responding promptly to privacy concerns</li>
            </ul>
          </section>

          {/* Final Acknowledgment */}
          <section className="mt-20 text-center">
            <div className="bg-[#C9A96E]/10 rounded-3xl p-10 sm:p-16 border border-[#C9A96E]/20">
              <h2 className="text-4xl font-serif font-bold mb-8 text-[#C9A96E]">
                Acknowledgment
              </h2>
              <p className="text-xl sm:text-2xl text-white/90 max-w-4xl mx-auto leading-relaxed font-light">
                By using Atelier, you acknowledge that you have read and understood this Privacy Policy and agree to its terms.
              </p>
              <p className="mt-10 text-[#94A3B8] text-lg">
                Thank you for trusting Atelier with your schedule!<br/>
                <span className="text-[#C9A96E] font-medium">Last reviewed: February 14, 2026</span>
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

export default Privacy;

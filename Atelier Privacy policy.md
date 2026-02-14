# Privacy Policy for Atelier

**Last Updated: February 14, 2026**

## Introduction

Welcome to Atelier ("we," "our," or "us"). We are committed to protecting your privacy and being transparent about how we handle your data. This Privacy Policy explains what information we collect, how we use it, and your rights regarding your data.

By using Atelier, you agree to the collection and use of information in accordance with this policy.

---

## 1. Information We Collect

### 1.1 Information You Provide
- **Account Information**: Email address and name when you sign up via Google OAuth
- **Calendar Data**: Events, titles, descriptions, dates, times, and locations from your Google Calendar
- **Conversation Summaries**: We do NOT store your full messages. Only anonymized summaries and preferences are stored in our vector database for personalization
- **User Preferences**: Scheduling preferences and patterns learned from your interactions

### 1.2 Automatically Collected Information
- **Authentication Tokens**: Google OAuth tokens to access your calendar
- **Usage Data**: How you interact with the app (timestamps, features used)
- **Technical Data**: Browser type, device information, IP address (for security purposes)

### 1.3 Information from Third Parties
- **Google Calendar API**: We access your calendar events when you grant us permission

---

## 2. How We Use Your Information

We use your information to:

### 2.1 Core Functionality
- **Schedule Management**: Read your calendar to find free slots and check for conflicts
- **Event Creation**: Create calendar events when you confirm our AI's suggestions
- **Event Deletion**: Remove events from your calendar when you request it
- **Intelligent Planning**: Learn your scheduling patterns to provide personalized recommendations

### 2.2 Service Improvement
- **Memory System**: Store anonymized summaries of your preferences and patterns to improve future suggestions
- **Conversation Context**: Your full messages are processed in real-time but NOT stored permanently. Only summaries are kept
- **Performance Optimization**: Analyze usage patterns to improve our AI assistant

### 2.3 Communication
- **Service Updates**: Notify you about changes to our service
- **Support**: Respond to your questions and troubleshoot issues

---

## 3. Google Calendar Access

### 3.1 What We Access
When you connect your Google Calendar, we request permission to:
- **Read** your calendar events (titles, dates, times, descriptions)
- **Write** new events when you confirm our suggestions
- **Modify** or delete events when you request changes

### 3.2 How We Use Google Calendar Data
- Calendar data is accessed in real-time when you interact with Atelier
- We analyze your schedule to find free time slots
- We check for conflicts before suggesting new events
- We store event metadata (but not full event details) to learn your scheduling patterns

### 3.3 Google Calendar Data Retention
- We do **not** permanently store the full content of your calendar events
- We only cache minimal event metadata (summary, start/end times) temporarily for conversation context
- Scheduling patterns (e.g., "user prefers morning workouts") are stored in anonymized form

### 3.4 Your Control
- You can revoke Atelier's access to your Google Calendar at any time via [Google Account Settings](https://myaccount.google.com/permissions)
- Revoking access will stop all calendar operations but will not delete your conversation summaries

---

## 4. How We Store Your Data

### 4.1 What We Store vs. What We Don't Store

**We DO NOT Store:**
- ❌ Full text of your messages to the AI
- ❌ Complete conversation transcripts
- ❌ Your raw calendar event descriptions

**We DO Store:**
- ✅ Anonymized summaries of your preferences (e.g., "prefers morning meetings")
- ✅ Scheduling patterns (e.g., "typically works out at 6 PM")
- ✅ Semantic embeddings (mathematical representations) of conversation context
- ✅ Event metadata (start/end times, conflict information)

### 4.2 Data Storage Locations
- **Authentication**: Supabase (US-based cloud infrastructure)
- **Conversation Summaries**: Weaviate vector database (cloud-hosted) - stores only embeddings and summaries
- **Calendar Tokens**: Encrypted in Supabase database
- **Application Logs**: Render.com/Railway.app servers (US-based)

### 4.3 Data Security Measures
- **Encryption in Transit**: All data transmitted via HTTPS/TLS
- **Encryption at Rest**: Database encryption for stored data
- **Access Controls**: Only authorized systems can access your data
- **Token Security**: Google OAuth tokens are encrypted and never exposed to client-side code
- **Message Privacy**: Your full messages are processed in-memory and discarded after generating responses

### 4.4 Data Retention
- **Account Data**: Retained until you delete your account
- **Conversation Summaries**: Retained for 90 days, then automatically deleted
- **Scheduling Patterns**: Retained to improve service; anonymized after 180 days
- **Authentication Tokens**: Refreshed automatically; old tokens expire within 1 hour
- **Full Messages**: NOT stored - deleted immediately after processing

---

## 5. Data Sharing and Disclosure

### 5.1 We Do NOT Sell Your Data
We will never sell, rent, or trade your personal information to third parties.

### 5.2 Third-Party Services We Use
We share limited data with trusted service providers:

| Service | Purpose | Data Shared | Data Stored by Them? |
|---------|---------|-------------|----------------------|
| **Google Calendar API** | Calendar integration | Your calendar events (per your authorization) | Yes (in your Google account) |
| **Supabase** | Authentication & database | Email, user ID, encrypted tokens | Yes |
| **Weaviate** | Vector database for AI memory | Conversation summaries & embeddings (anonymized) | Yes |
| **Groq** | AI language model | Your messages in real-time for processing | **NO** - Not stored by Groq |
| **Cohere** | Text embeddings | Summary text for semantic search | **NO** - Not stored by Cohere |
| **Vercel/Render** | Hosting infrastructure | Technical logs (IP addresses, request metadata) | Yes (temporary logs) |

**Important**: Your full messages are sent to Groq for real-time AI processing but are NOT stored or used for training by Groq (per their privacy policy).

### 5.3 Legal Disclosure
We may disclose your information if required by law or to:
- Comply with legal processes (subpoenas, court orders)
- Protect our rights and safety
- Prevent fraud or security threats
- Enforce our Terms of Service

---

## 6. Your Rights and Choices

### 6.1 Access and Portability
- You can request a copy of your stored summaries and preferences at any time
- Contact us at seam22rodr3@gmail.com to request your data export
- Note: We cannot provide full message transcripts as they are not stored

### 6.2 Correction and Deletion
- You can update your account information in the app settings
- You can delete your account and all associated data by contacting us
- Upon account deletion, we will remove all personal data within 30 days

### 6.3 Opt-Out of AI Memory
- You can request that we disable learning from your interactions
- This will make the assistant less personalized but fully functional
- We will delete all stored summaries and preferences upon request

### 6.4 Revoke Calendar Access
- Revoke access via [Google Account Permissions](https://myaccount.google.com/permissions)
- This immediately stops all calendar operations

---

## 7. Children's Privacy

Atelier is not intended for users under 18 years of age. We do not knowingly collect personal information from children. If you believe a child has provided us with personal data, please contact us immediately.

---

## 8. International Users

Atelier is operated from India. If you are accessing our service from outside India, please be aware that your information may be transferred to, stored, and processed in India or other countries where our service providers operate.

By using Atelier, you consent to the transfer of your information to countries outside your country of residence, which may have different data protection laws.

---

## 9. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. When we make changes:
- We will update the "Last Updated" date at the top
- For significant changes, we will notify you via email or in-app notification
- Your continued use of Atelier after changes constitutes acceptance of the updated policy

We encourage you to review this Privacy Policy periodically.

---

## 10. AI and Automated Decision-Making

### 10.1 How Our AI Works
- Atelier uses AI (large language models) to understand your requests and suggest schedules
- The AI analyzes your calendar, stored preferences, and conversation summaries
- **Human-in-the-Loop**: Our AI never makes calendar changes without your explicit approval

### 10.2 AI Data Processing
- Your messages are sent to Groq's API for real-time language processing
- Groq does not store or train on your data (per their privacy policy)
- We use Weaviate to store embeddings (mathematical representations) and summaries of conversations for memory
- **Your full messages are NOT stored anywhere** - only anonymized summaries and patterns

### 10.3 Accuracy Disclaimer
- AI suggestions are not perfect and may contain errors
- Always review AI-generated schedules before confirming
- We are not liable for scheduling mistakes due to AI misunderstandings

---

## 11. Data Minimization Principle

We follow the principle of data minimization:
- We only collect data necessary for the service to function
- We do not store full conversation transcripts
- We anonymize and summarize data where possible
- We automatically delete old data according to our retention policy

This approach ensures maximum privacy while still providing personalized service.

---

## 12. Data Breach Notification

In the unlikely event of a data breach that affects your personal information:
- We will notify you within 72 hours via email
- We will provide details about the breach and steps you should take
- We will work with authorities to investigate and remediate the issue

Given that we do not store full message content, the exposure in any breach is limited to:
- Account information (email, name)
- Anonymized preference summaries
- Calendar event metadata (not full calendar contents)

---

## 13. Contact Us

If you have questions, concerns, or requests regarding this Privacy Policy or your data:

**Email**: seam22rodr3@gmail.com  
**GitHub Issues**: [https://github.com/sea-rod/agent_planner/issues](https://github.com/sea-rod/agent_planner/issues)  
**Response Time**: We aim to respond within 72 hours

---

## 14. Compliance and Certifications

### 14.1 GDPR Compliance (EU Users)
If you are in the European Union, you have additional rights under GDPR:
- **Right to Access**: Request a copy of your stored summaries and preferences
- **Right to Rectification**: Correct inaccurate data
- **Right to Erasure**: Request deletion of your data
- **Right to Restrict Processing**: Limit how we use your data
- **Right to Data Portability**: Receive your data in a structured format
- **Right to Object**: Object to our processing of your data

To exercise these rights, contact us at seam22rodr3@gmail.com.

### 14.2 CCPA Compliance (California Users)
If you are a California resident, you have rights under the California Consumer Privacy Act:
- Right to know what personal information we collect
- Right to delete personal information
- Right to opt-out of data sales (we do not sell data)
- Right to non-discrimination for exercising your rights

### 14.3 Data Processing Lawful Basis (GDPR)
We process your data based on:
- **Consent**: You explicitly authorize Google Calendar access
- **Contract**: Processing necessary to provide the service
- **Legitimate Interest**: Improving service quality through anonymized learning

---

## 15. MVP Disclaimer

**Important Notice**: Atelier is currently in **beta/MVP stage**. This means:
- Features and data handling practices may change as we improve the service
- We are actively testing and may experience technical issues
- Your feedback helps us build a better product
- We will notify users of major changes to data handling

Despite being an MVP, we take your privacy seriously and follow industry best practices for data protection, including not storing your full messages.

---

## 16. Open Source

Atelier's source code is available at [https://github.com/sea-rod/agent_planner](https://github.com/sea-rod/agent_planner). You can review how we handle your data by examining the codebase, including:
- How messages are processed in real-time
- How summaries are generated and stored
- What data is actually persisted in our databases

---

## 17. Transparency Commitment

To maintain trust, we commit to:
- Being transparent about what data we collect and store
- Never storing full message transcripts
- Only using anonymized summaries for personalization
- Giving you control over your data
- Responding promptly to privacy concerns

---

## Acknowledgment

By using Atelier, you acknowledge that you have read and understood this Privacy Policy and agree to its terms.

---

**Thank you for trusting Atelier with your schedule!**

*This privacy policy was last reviewed and updated on February 14, 2026.*
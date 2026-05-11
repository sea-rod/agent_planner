import { useState } from "react";
import { Link } from "react-router";

const providers = [
  {
    id: "google",
    name: "Google Calendar",
    shortName: "Google",
    desc: "Gmail, Workspace, and all Google account calendars.",
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05" />
        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
      </svg>
    ),
    iconBg: "bg-blue-500/10",
  },
  {
    id: "outlook",
    name: "Outlook / Microsoft 365",
    shortName: "Outlook",
    desc: "Personal Outlook, Hotmail, and Microsoft 365 organizational accounts.",
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
        <path d="M7 2H21a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1z" fill="#0078D4" />
        <path d="M22 8l-10 7L2 8V7l10 7 10-7v1z" fill="#50D9FF" opacity="0.7" />
        <path d="M2 3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3z" fill="#28A8E8" />
        <rect x="4" y="9" width="6" height="8" rx="1" fill="#0078D4" opacity="0.4" />
      </svg>
    ),
    iconBg: "bg-sky-500/10",
  },
  {
    id: "apple",
    name: "Apple Calendar",
    shortName: "Apple",
    desc: "iCloud, macOS, and iOS calendar via CalDAV. Works with your Apple ID.",
    icon: (
      <svg width="20" height="22" viewBox="0 0 814 1000" fill="white" opacity="0.85">
        <path d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76 0-103.7 40.8-165.9 40.8s-105-37.3-165.8-120.5c-69.7-95.2-119.5-254.8-119.5-405.8 0-209.6 135.8-319.9 270-319.9 70.3 0 128.9 46.4 172.3 46.4 41.6 0 106.7-49 187.3-49 30.1 0 108.2 2.6 168.9 80.4zm-126.7-81.5c-20.1 23.7-53.3 41.6-86.6 41.6-4.5 0-9-.6-13.5-1.3-1.3-3.2-1.9-6.5-1.9-9.7 0-28.9 14.8-58.4 36.1-77.7 26.5-22.7 61.6-37.5 94.3-38.8 1.3 3.8 1.9 7.7 1.9 11.5 0 27.7-12.9 57.8-30.3 74.4z" />
      </svg>
    ),
    iconBg: "bg-white/5",
  },
  {
    id: "yahoo",
    name: "Yahoo Calendar",
    shortName: "Yahoo",
    desc: "Yahoo Mail and Yahoo account calendars via CalDAV protocol.",
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
        <path d="M7 3l5 8.5L17 3h4l-8 13v5h-4v-5L1 3h6z" fill="#7209B7" opacity="0.9" />
      </svg>
    ),
    iconBg: "bg-purple-500/10",
  },
];

function StatusBadge({ state }) {
  if (state === "connected")
    return (
      <span className="text-[10px] font-light tracking-widest uppercase px-3 py-1 rounded-full text-emerald-400 border border-emerald-400/30 bg-emerald-400/5">
        Connected
      </span>
    );
  if (state === "connecting")
    return (
      <span className="text-[10px] font-light tracking-widest uppercase px-3 py-1 rounded-full text-[#C9A96E] border border-[#C9A96E]/25 bg-[#C9A96E]/10">
        Connecting…
      </span>
    );
  return (
    <span className="text-[10px] font-light tracking-widest uppercase px-3 py-1 rounded-full text-slate-400 border border-slate-400/25 bg-slate-400/5">
      Available
    </span>
  );
}

function ConnectorCard({ provider, state, onConnect }) {
  const isConnected = state === "connected";
  const isConnecting = state === "connecting";

  return (
    <div
      onClick={() => !isConnected && !isConnecting && onConnect(provider.id)}
      className={[
        "group relative rounded-2xl p-6 border transition-all duration-300 overflow-hidden",
        isConnected
          ? "bg-[#C9A96E]/5 border-[#C9A96E]/50 cursor-default"
          : isConnecting
          ? "bg-white/[0.03] border-[#C9A96E]/40 animate-pulse cursor-wait"
          : "bg-white/[0.03] border-[#C9A96E]/15 cursor-pointer hover:-translate-y-0.5 hover:border-[#C9A96E]/45 hover:bg-white/[0.05]",
      ].join(" ")}
    >
      {/* inner glow on hover */}
      {!isConnected && !isConnecting && (
        <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none rounded-2xl bg-[radial-gradient(ellipse_80%_50%_at_50%_0%,rgba(201,169,110,0.06),transparent)]" />
      )}

      {/* top row */}
      <div className="flex items-start justify-between mb-4">
        <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${provider.iconBg}`}>
          {provider.icon}
        </div>
        <StatusBadge state={state} />
      </div>

      {/* name + desc */}
      <p className="font-serif text-[19px] font-light text-white mb-1">
        {provider.name}
      </p>
      <p className="text-xs font-light text-slate-400 leading-relaxed mb-5">
        {provider.desc}
      </p>

      {/* CTA button */}
      <button
        onClick={(e) => {
          e.stopPropagation();
          if (!isConnected && !isConnecting) onConnect(provider.id);
        }}
        disabled={isConnected || isConnecting}
        className={[
          "w-full py-2.5 rounded-lg text-[11px] tracking-widest uppercase transition-all duration-200",
          isConnected
            ? "bg-emerald-400/5 border border-emerald-400/20 text-emerald-400 cursor-default"
            : isConnecting
            ? "bg-[#C9A96E]/10 border border-[#C9A96E]/20 text-[#C9A96E] cursor-wait"
            : "bg-[#C9A96E]/10 border border-[#C9A96E]/20 text-[#C9A96E] hover:bg-[#C9A96E]/20 hover:text-[#D4B978]",
        ].join(" ")}
      >
        {isConnected
          ? `✓ ${provider.shortName} connected`
          : isConnecting
          ? "Authenticating…"
          : `Connect ${provider.shortName}`}
      </button>
    </div>
  );
}

export default function Connector() {
  const [connectionStates, setConnectionStates] = useState(
    Object.fromEntries(providers.map((p) => [p.id, "idle"]))
  );

  const handleConnect = (providerId) => {
    setConnectionStates((prev) => ({ ...prev, [providerId]: "connecting" }));
    // Replace with your actual OAuth redirect / popup logic
    setTimeout(() => {
      setConnectionStates((prev) => ({ ...prev, [providerId]: "connected" }));
    }, 1800);
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-[#0F172A] via-[#1E293B] to-[#0F172A] px-6 py-16 text-white overflow-hidden">

      {/* top gold rule */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#C9A96E]/30 to-transparent" />

      {/* ambient glow */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_60%_40%_at_50%_0%,rgba(201,169,110,0.08),transparent)]" />

      <div className="relative z-10 max-w-2xl mx-auto">

        {/* step pill */}
        <span className="inline-block mb-6 px-5 py-1.5 rounded-full border border-[#C9A96E]/25 bg-[#C9A96E]/10 text-[#C9A96E] text-[10px] tracking-[0.2em] uppercase font-light">
          Step 2 of 3 · Calendar Access
        </span>

        {/* heading */}
        <h1 className="font-serif text-4xl md:text-5xl font-light leading-tight mb-3">
          Connect your{" "}
          <span className="text-[#C9A96E] italic">calendar</span>
        </h1>
        <p className="text-sm font-light text-slate-400 leading-relaxed mb-10 max-w-md">
          Atelier works in harmony with your existing calendar. Choose your provider
          and grant read access — your events remain entirely yours.
        </p>

        {/* permission note */}
        {/* <div className="flex gap-3 items-start mb-8 px-4 py-3.5 rounded-xl border border-[#C9A96E]/15 bg-[#C9A96E]/[0.04]">
          <span className="text-[#C9A96E] text-base mt-0.5 shrink-0">🔒</span>
          <p className="text-xs font-light text-slate-400 leading-relaxed m-0">
            We request{" "}
            <span className="text-slate-300">read-only</span>{" "}
            access to view and organize your schedule. We never modify, delete, or share your calendar data.
          </p>
        </div> */}

        {/* provider grid */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          {providers.map((provider) => (
            <ConnectorCard
              key={provider.id}
              provider={provider}
              state={connectionStates[provider.id]}
              onConnect={handleConnect}
            />
          ))}
        </div>

        {/* divider */}
        <div className="h-px bg-gradient-to-r from-transparent via-[#C9A96E]/20 to-transparent mb-8" />

        {/* footer trust line */}
        <div className="flex items-center justify-center gap-2 text-[11px] font-light text-slate-500">
          <span className="text-[#C9A96E] text-xs">🔒</span>
          <span>OAuth 2.0 · End-to-end encrypted · Revocable at any time</span>
        </div>

        {/* skip */}
        <Link
          to="/chat"
          className="block text-center mt-5 text-[20px] font-light tracking-widest text-slate-500/200 hover:text-slate-400 transition-colors duration-200 no-underline"
        >
          Skip for now - I'll connect later →
        </Link>
      </div>
    </div>
  );
}
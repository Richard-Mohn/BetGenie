const features = [
  {
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      </svg>
    ),
    title: "Player Impact Score",
    description:
      "A proprietary 0–100 score that measures how a player's personal circumstances will affect tonight's game. Physical, emotional, psychological, and situational — all weighted and time-decayed.",
    highlight: "67.6/100",
    highlightLabel: "Ja Morant (gun incident)",
    color: "text-[var(--accent-light)]",
    bgColor: "bg-[var(--accent)]/10",
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    title: "Real-Time News Intelligence",
    description:
      "Our AI scans social media, news outlets, court records, and team reports 24/7. When something happens in a player's life, BetGenie catches it hours before the market adjusts.",
    highlight: "4 hrs",
    highlightLabel: "avg. lead time vs market",
    color: "text-[var(--blue)]",
    bgColor: "bg-[var(--blue)]/10",
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
    title: "Adjusted Stat Projections",
    description:
      "We don't just flag issues — we quantify them. See exactly how many points, assists, or rebounds a player is projected to gain or lose based on their current Impact Score.",
    highlight: "-0.8 PPG",
    highlightLabel: "Morant adjusted projection",
    color: "text-[var(--yellow)]",
    bgColor: "bg-[var(--yellow)]/10",
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
      </svg>
    ),
    title: "Sentiment Analysis Engine",
    description:
      "Purpose-built NLP that classifies news articles, social posts, and public records into 16 event categories — then scores severity, direction, and confidence for each.",
    highlight: "16",
    highlightLabel: "event categories tracked",
    color: "text-[var(--green)]",
    bgColor: "bg-[var(--green)]/10",
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
      </svg>
    ),
    title: "Smart Parlay Builder",
    description:
      "Build smarter parlays with AI-powered correlation analysis. We flag same-game risks, weak legs, and suggest replacements — then score your whole parlay's confidence.",
    highlight: "+1294",
    highlightLabel: "sample optimized payout",
    color: "text-purple-400",
    bgColor: "bg-purple-500/10",
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    title: "Time Decay Modeling",
    description:
      "Not all events affect players the same way over time. Our half-life decay model ensures a DUI from last month weighs less than one from yesterday — just like reality.",
    highlight: "60 day",
    highlightLabel: "event tracking window",
    color: "text-rose-400",
    bgColor: "bg-rose-500/10",
  },
];

export default function Features() {
  return (
    <section id="features" className="py-20 md:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-20">
          <span className="text-sm font-semibold text-[var(--accent-light)] uppercase tracking-wider">
            Features
          </span>
          <h2 className="mt-3 text-3xl sm:text-4xl lg:text-5xl font-bold text-white">
            Intelligence the Market{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
              Can&apos;t See
            </span>
          </h2>
          <p className="mt-4 text-lg text-gray-400">
            Every sportsbook analyzes stats. BetGenie analyzes the human behind the stats —
            and finds the edge that doesn&apos;t show up in a box score.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="gradient-border p-6 md:p-8 rounded-2xl hover:translate-y-[-4px] transition-all duration-300 group"
            >
              <div
                className={`w-12 h-12 rounded-xl ${feature.bgColor} flex items-center justify-center ${feature.color} mb-5 group-hover:scale-110 transition-transform`}
              >
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed mb-4">
                {feature.description}
              </p>
              <div className="pt-4 border-t border-[var(--border)]">
                <span className={`text-2xl font-bold ${feature.color}`}>
                  {feature.highlight}
                </span>
                <span className="block text-xs text-gray-500 mt-1">
                  {feature.highlightLabel}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

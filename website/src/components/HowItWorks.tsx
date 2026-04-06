const steps = [
  {
    number: "01",
    title: "AI Scans Everything",
    description:
      "Our engine monitors social media, news, court records, team reports, and thousands of other sources — 24/7 — looking for events that could affect player performance.",
    details: [
      "Twitter/X, Instagram, TikTok mentions",
      "Google News & local beat reporters",
      "Court records & legal filings",
      "Team press conferences & injury reports",
    ],
    visual: (
      <div className="space-y-2">
        {["ESPN: Ja Morant shows gun on IG Live", "AP: NBA launches investigation into Morant", "TMZ: Morant deactivates social media"].map(
          (headline, i) => (
            <div
              key={i}
              className="flex items-center gap-3 bg-white/5 rounded-lg p-3 border border-[var(--border)]"
            >
              <div className="w-2 h-2 rounded-full bg-[var(--red)] animate-pulse flex-shrink-0" />
              <span className="text-sm text-gray-300 truncate">
                {headline}
              </span>
            </div>
          )
        )}
      </div>
    ),
  },
  {
    number: "02",
    title: "Classify & Score Events",
    description:
      "Each event is classified into one of 16 categories, scored for severity and sentiment, then mapped to the physical, emotional, psychological, or situational component it affects most.",
    details: [
      "16 event categories (legal, family, trade, etc.)",
      "Severity scoring: 0.0 to 1.0 scale",
      "Sentiment analysis: -1.0 to +1.0",
      "Confidence scoring with source verification",
    ],
    visual: (
      <div className="bg-white/5 rounded-lg p-4 border border-[var(--border)] font-mono text-xs">
        <div className="text-gray-500 mb-2">// Event Classification</div>
        <div className="text-[var(--accent-light)]">
          category:{" "}
          <span className="text-[var(--red)]">&quot;legal_arrest&quot;</span>
        </div>
        <div className="text-[var(--accent-light)]">
          severity: <span className="text-[var(--yellow)]">0.85</span>
        </div>
        <div className="text-[var(--accent-light)]">
          sentiment: <span className="text-[var(--red)]">-0.92</span>
        </div>
        <div className="text-[var(--accent-light)]">
          affects:{" "}
          <span className="text-[var(--blue)]">
            [emotional, psychological]
          </span>
        </div>
        <div className="text-[var(--accent-light)]">
          confidence: <span className="text-[var(--green)]">0.95</span>
        </div>
      </div>
    ),
  },
  {
    number: "03",
    title: "Calculate Impact Score",
    description:
      "All active events are combined using weighted formulas with time-decay modeling. Recent events hit harder; old events fade away naturally — just like in real life.",
    details: [
      "Physical (30%) + Emotional (25%)",
      "Psychological (25%) + Situational (20%)",
      "Half-life decay: events fade over 7–60 days",
      "Baseline 75 = no effect; below 70 = flagged",
    ],
    visual: (
      <div className="bg-white/5 rounded-lg p-4 border border-[var(--border)]">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm text-gray-400">Player Impact Score</span>
          <span className="text-2xl font-bold text-[var(--yellow)]">67.6</span>
        </div>
        <div className="space-y-2">
          {[
            { label: "Physical", score: 75, color: "bg-[var(--green)]" },
            { label: "Emotional", score: 57, color: "bg-[var(--yellow)]" },
            { label: "Psychological", score: 64, color: "bg-[var(--yellow)]" },
            { label: "Situational", score: 75, color: "bg-[var(--green)]" },
          ].map((bar) => (
            <div key={bar.label} className="flex items-center gap-3">
              <span className="text-xs text-gray-500 w-24">{bar.label}</span>
              <div className="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden">
                <div
                  className={`h-full ${bar.color} rounded-full`}
                  style={{ width: `${bar.score}%` }}
                />
              </div>
              <span className="text-xs text-gray-400 w-8 text-right">
                {bar.score}
              </span>
            </div>
          ))}
        </div>
      </div>
    ),
  },
  {
    number: "04",
    title: "Generate Betting Edge",
    description:
      "The Impact Score becomes a performance multiplier. We project adjusted stats, compare them to sportsbook prop lines, and deliver actionable OVER/UNDER recommendations with confidence ratings.",
    details: [
      "Adjusted stat projections (PPG, APG, RPG)",
      "OVER/UNDER recommendations with % confidence",
      "Parlay builder with correlation warnings",
      "Real-time alerts when PIS drops below threshold",
    ],
    visual: (
      <div className="bg-[var(--red)]/10 border border-[var(--red)]/20 rounded-lg p-4">
        <div className="text-xs text-[var(--red)] font-semibold uppercase tracking-wider mb-2">
          BetGenie Recommendation
        </div>
        <div className="text-white font-semibold mb-1">
          Ja Morant UNDER 25.5 Points
        </div>
        <div className="text-sm text-gray-400">
          Projected: 25.4 pts · Edge: +0.1 · Confidence: 69%
        </div>
        <div className="mt-3 pt-3 border-t border-[var(--border)] text-xs text-gray-500">
          Baseline 26.2 PPG × 0.970 multiplier = 25.4 projected
        </div>
      </div>
    ),
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 md:py-32 bg-[var(--surface)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-20">
          <span className="text-sm font-semibold text-[var(--accent-light)] uppercase tracking-wider">
            How It Works
          </span>
          <h2 className="mt-3 text-3xl sm:text-4xl lg:text-5xl font-bold text-white">
            From News to{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
              Betting Edge
            </span>{" "}
            in Seconds
          </h2>
          <p className="mt-4 text-lg text-gray-400">
            Our pipeline turns unstructured real-world events into quantified
            betting intelligence — automatically.
          </p>
        </div>

        {/* Steps */}
        <div className="space-y-16 md:space-y-24">
          {steps.map((step, index) => (
            <div
              key={step.number}
              className={`grid md:grid-cols-2 gap-8 md:gap-16 items-center ${
                index % 2 === 1 ? "md:[direction:rtl]" : ""
              }`}
            >
              {/* Text */}
              <div className={index % 2 === 1 ? "md:[direction:ltr]" : ""}>
                <div className="flex items-center gap-4 mb-4">
                  <span className="text-5xl font-black text-[var(--accent)]/20">
                    {step.number}
                  </span>
                  <h3 className="text-2xl md:text-3xl font-bold text-white">
                    {step.title}
                  </h3>
                </div>
                <p className="text-gray-400 leading-relaxed mb-6">
                  {step.description}
                </p>
                <ul className="space-y-2">
                  {step.details.map((detail, i) => (
                    <li key={i} className="flex items-center gap-3 text-sm">
                      <svg
                        className="w-4 h-4 text-[var(--accent-light)] flex-shrink-0"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span className="text-gray-300">{detail}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Visual */}
              <div className={index % 2 === 1 ? "md:[direction:ltr]" : ""}>
                {step.visual}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

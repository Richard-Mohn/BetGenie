const stats = [
  { value: "7.7", label: "PIS Gap Detected", sublabel: "Morant vs SGA — same night" },
  { value: "98.8%", label: "Directional Accuracy", sublabel: "Morant historical validation" },
  { value: "<0.3", label: "PPG Error Margin", sublabel: "Projected 25.4 · Actual 25.1" },
  { value: "0", label: "Competitors", sublabel: "in personal factor analysis" },
];

export default function SocialProof() {
  return (
    <section className="py-16 md:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className="text-center p-6 rounded-2xl bg-[var(--surface)] border border-[var(--border)]"
            >
              <div className="text-3xl sm:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
                {stat.value}
              </div>
              <div className="text-sm text-white font-medium mt-2">
                {stat.label}
              </div>
              <div className="text-xs text-gray-500 mt-1">{stat.sublabel}</div>
            </div>
          ))}
        </div>

        {/* Quote / Thesis Statement */}
        <div className="mt-16 text-center max-w-4xl mx-auto">
          <div className="gradient-border rounded-2xl p-8 md:p-12">
            <svg
              className="w-10 h-10 text-[var(--accent)]/40 mx-auto mb-4"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
            </svg>
            <blockquote className="text-xl md:text-2xl text-white font-medium leading-relaxed">
              Every player is a person first. Their personal circumstances
              directly impact performance — and no one is systematically
              tracking, scoring, and monetizing that insight.{" "}
              <span className="text-[var(--accent-light)]">Until now.</span>
            </blockquote>
            <div className="mt-6 text-sm text-gray-400">
              The BetGenie Thesis — Validated by Proof of Concept, March 2026
            </div>
          </div>
        </div>

        {/* Trust Signals */}
        <div className="mt-16 flex flex-wrap items-center justify-center gap-8 md:gap-12 text-gray-600">
          {[
            "NBA Data Verified",
            "Real Player Events",
            "Open-Source AI Engine",
            "Responsible Gambling",
          ].map((label) => (
            <div
              key={label}
              className="flex items-center gap-2 text-sm"
            >
              <svg
                className="w-4 h-4 text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                />
              </svg>
              <span>{label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

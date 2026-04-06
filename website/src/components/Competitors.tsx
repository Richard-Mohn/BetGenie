const competitors = [
  { name: "Action Network", stats: true, personalFactors: false, ai: false, parlayAI: false },
  { name: "PrizePicks", stats: true, personalFactors: false, ai: false, parlayAI: false },
  { name: "Unabated", stats: true, personalFactors: false, ai: false, parlayAI: false },
  { name: "Swish Analytics", stats: true, personalFactors: false, ai: true, parlayAI: false },
  { name: "OddsJam", stats: true, personalFactors: false, ai: false, parlayAI: false },
  { name: "Dimers.com", stats: true, personalFactors: false, ai: true, parlayAI: false },
];

function Check() {
  return (
    <svg className="w-5 h-5 text-[var(--green)]" fill="currentColor" viewBox="0 0 20 20">
      <path
        fillRule="evenodd"
        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function Cross() {
  return (
    <svg className="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
      <path
        fillRule="evenodd"
        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
        clipRule="evenodd"
      />
    </svg>
  );
}

export default function Competitors() {
  return (
    <section className="py-20 md:py-32 bg-[var(--surface)]">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <span className="text-sm font-semibold text-[var(--accent-light)] uppercase tracking-wider">
            Why BetGenie
          </span>
          <h2 className="mt-3 text-3xl sm:text-4xl font-bold text-white">
            Nobody Else{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
              Does This
            </span>
          </h2>
          <p className="mt-4 text-lg text-gray-400">
            We analyzed every major competitor. The result: zero platforms
            track personal life factors for sports betting.
          </p>
        </div>

        {/* Comparison Table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-[var(--border)]">
                <th className="text-left py-4 px-4 text-sm text-gray-400 font-medium">
                  Platform
                </th>
                <th className="text-center py-4 px-4 text-sm text-gray-400 font-medium">
                  Stats Analysis
                </th>
                <th className="text-center py-4 px-4 text-sm text-gray-400 font-medium">
                  <span className="text-[var(--accent-light)]">
                    Personal Factor Analysis
                  </span>
                </th>
                <th className="text-center py-4 px-4 text-sm text-gray-400 font-medium">
                  AI/ML Models
                </th>
                <th className="text-center py-4 px-4 text-sm text-gray-400 font-medium">
                  Smart Parlay Builder
                </th>
              </tr>
            </thead>
            <tbody>
              {competitors.map((comp) => (
                <tr
                  key={comp.name}
                  className="border-b border-[var(--border)] hover:bg-white/[0.02] transition-colors"
                >
                  <td className="py-4 px-4 text-sm text-gray-300">
                    {comp.name}
                  </td>
                  <td className="py-4 px-4 text-center">
                    <div className="flex justify-center">
                      {comp.stats ? <Check /> : <Cross />}
                    </div>
                  </td>
                  <td className="py-4 px-4 text-center">
                    <div className="flex justify-center">
                      {comp.personalFactors ? <Check /> : <Cross />}
                    </div>
                  </td>
                  <td className="py-4 px-4 text-center">
                    <div className="flex justify-center">
                      {comp.ai ? <Check /> : <Cross />}
                    </div>
                  </td>
                  <td className="py-4 px-4 text-center">
                    <div className="flex justify-center">
                      {comp.parlayAI ? <Check /> : <Cross />}
                    </div>
                  </td>
                </tr>
              ))}

              {/* BetGenie row - highlighted */}
              <tr className="bg-[var(--accent)]/5 border-b border-[var(--accent)]/20">
                <td className="py-4 px-4">
                  <span className="text-sm font-semibold text-white">
                    BetGenie
                  </span>
                  <span className="ml-2 text-xs text-[var(--accent-light)] bg-[var(--accent)]/10 px-2 py-0.5 rounded-full">
                    New
                  </span>
                </td>
                <td className="py-4 px-4 text-center">
                  <div className="flex justify-center"><Check /></div>
                </td>
                <td className="py-4 px-4 text-center">
                  <div className="flex justify-center"><Check /></div>
                </td>
                <td className="py-4 px-4 text-center">
                  <div className="flex justify-center"><Check /></div>
                </td>
                <td className="py-4 px-4 text-center">
                  <div className="flex justify-center"><Check /></div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p className="text-center text-sm text-gray-500 mt-6">
          Based on public feature reviews as of March 2026.
          &quot;Personal Factor Analysis&quot; = systematic tracking and scoring
          of players&apos; personal life events for betting intelligence.
        </p>
      </div>
    </section>
  );
}

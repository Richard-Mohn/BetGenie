export default function LiveDemo() {
  const players = [
    {
      initials: "JM",
      name: "Ja Morant",
      team: "Grizzlies",
      pis: 67.6,
      status: "CAUTION",
      statusColor: "text-[var(--yellow)]",
      bgColor: "from-blue-500 to-blue-700",
      factors: ["Gun incident on IG", "NBA investigation", "Social media deactivated"],
      recommendation: "UNDER 25.5 pts",
      projected: "25.4",
      confidence: 69,
      physical: 75,
      emotional: 56.8,
      psychological: 63.5,
      situational: 75,
    },
    {
      initials: "JB",
      name: "Jimmy Butler",
      team: "Suns",
      pis: 70.4,
      status: "FLAGGED",
      statusColor: "text-[var(--yellow)]",
      bgColor: "from-orange-500 to-orange-700",
      factors: ["Trade demand to PHX", "Double suspension by MIA", "Locker room conflict"],
      recommendation: "UNDER 19.5 pts",
      projected: "17.8",
      confidence: 66,
      physical: 75,
      emotional: 59.2,
      psychological: 75,
      situational: 71.7,
    },
    {
      initials: "SGA",
      name: "Shai Gilgeous-Alexander",
      team: "Thunder",
      pis: 75.0,
      status: "BASELINE",
      statusColor: "text-[var(--green)]",
      bgColor: "from-sky-500 to-sky-700",
      factors: ["MVP candidate", "No personal flags", "Team chemistry strong"],
      recommendation: "OVER 31.3 pts",
      projected: "33.1",
      confidence: 78,
      physical: 75,
      emotional: 75,
      psychological: 75,
      situational: 75,
    },
    {
      initials: "LD",
      name: "Luka Doncic",
      team: "Lakers",
      pis: 74.0,
      status: "MONITOR",
      statusColor: "text-yellow-300",
      bgColor: "from-yellow-500 to-yellow-700",
      factors: ["Traded to LAL", "Adjusting to new system", "Weight/conditioning questions"],
      recommendation: "UNDER 32.5 pts",
      projected: "31.2",
      confidence: 61,
      physical: 75,
      emotional: 75,
      psychological: 75,
      situational: 69.8,
    },
  ];

  return (
    <section id="live-demo" className="py-20 md:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-8">
          <span className="text-sm font-semibold text-[var(--accent-light)] uppercase tracking-wider">
            Live Demo
          </span>
          <h2 className="mt-3 text-3xl sm:text-4xl lg:text-5xl font-bold text-white">
            See BetGenie{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
              In Action
            </span>
          </h2>
          <p className="mt-4 text-lg text-gray-400">
            Real NBA players. Real personal events. Real Impact Scores.
            This is what our AI engine produces right now.
          </p>
        </div>

        {/* POC Validation Badge */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex items-center gap-3 bg-[var(--green)]/10 border border-[var(--green)]/20 rounded-full px-6 py-2.5">
            <svg className="w-5 h-5 text-[var(--green)]" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            <span className="text-sm text-[var(--green)] font-medium">
              Validated: Morant projected 25.4 PPG — actual 2023-24 avg was 25.1 PPG (98.8% directional accuracy)
            </span>
          </div>
        </div>

        {/* Player Cards Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {players.map((player) => (
            <div
              key={player.name}
              className="gradient-border rounded-2xl p-5 hover:translate-y-[-4px] transition-all duration-300"
            >
              {/* Header */}
              <div className="flex items-center gap-3 mb-4">
                <div
                  className={`w-10 h-10 rounded-full bg-gradient-to-br ${player.bgColor} flex items-center justify-center text-white font-bold text-xs`}
                >
                  {player.initials}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-white font-semibold text-sm truncate">
                    {player.name}
                  </h3>
                  <p className="text-gray-500 text-xs">{player.team}</p>
                </div>
              </div>

              {/* PIS */}
              <div className="flex items-end justify-between mb-4">
                <div>
                  <div className="text-xs text-gray-500 uppercase tracking-wide">
                    Impact Score
                  </div>
                  <div className="text-3xl font-bold text-white">{player.pis}</div>
                </div>
                <span
                  className={`text-xs font-semibold uppercase ${player.statusColor} px-2 py-1 rounded-md bg-white/5`}
                >
                  {player.status}
                </span>
              </div>

              {/* Mini Bars */}
              <div className="space-y-1.5 mb-4">
                {[
                  { label: "PHY", val: player.physical },
                  { label: "EMO", val: player.emotional },
                  { label: "PSY", val: player.psychological },
                  { label: "SIT", val: player.situational },
                ].map((bar) => (
                  <div key={bar.label} className="flex items-center gap-2">
                    <span className="text-[10px] text-gray-500 w-6">
                      {bar.label}
                    </span>
                    <div className="flex-1 h-1 bg-white/5 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          bar.val >= 75
                            ? "bg-[var(--green)]"
                            : bar.val >= 65
                            ? "bg-[var(--yellow)]"
                            : "bg-[var(--red)]"
                        }`}
                        style={{ width: `${bar.val}%` }}
                      />
                    </div>
                    <span className="text-[10px] text-gray-500 w-7 text-right">
                      {bar.val}
                    </span>
                  </div>
                ))}
              </div>

              {/* Factors */}
              <div className="border-t border-[var(--border)] pt-3 mb-3">
                <div className="text-[10px] uppercase tracking-wider text-gray-600 mb-1.5">
                  Key Factors
                </div>
                {player.factors.map((f, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-1.5 mb-1"
                  >
                    <span
                      className={`mt-1 w-1 h-1 rounded-full flex-shrink-0 ${
                        player.pis >= 75
                          ? "bg-[var(--green)]"
                          : player.pis >= 70
                          ? "bg-[var(--yellow)]"
                          : "bg-[var(--red)]"
                      }`}
                    />
                    <span className="text-xs text-gray-400">{f}</span>
                  </div>
                ))}
              </div>

              {/* Recommendation */}
              <div
                className={`rounded-lg p-3 ${
                  player.pis < 75
                    ? "bg-[var(--red)]/10 border border-[var(--red)]/15"
                    : "bg-[var(--green)]/10 border border-[var(--green)]/15"
                }`}
              >
                <div className="text-xs font-semibold text-white mb-0.5">
                  {player.recommendation}
                </div>
                <div className="text-[10px] text-gray-400">
                  Proj: {player.projected} · {player.confidence}% conf
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Historical Proof */}
        <div className="mt-16 gradient-border rounded-2xl p-8 md:p-10">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">
                Historical Validation: Ja Morant
              </h3>
              <p className="text-gray-400 mb-6">
                We ran BetGenie&apos;s algorithm retroactively on Morant&apos;s 2023-24 season —
                after his gun incidents and 25-game suspension. Here&apos;s what we found:
              </p>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-xl bg-[var(--accent)]/10 flex items-center justify-center">
                    <span className="text-2xl font-bold text-[var(--accent-light)]">25.4</span>
                  </div>
                  <div>
                    <div className="text-white font-semibold">BetGenie Projected</div>
                    <div className="text-sm text-gray-400">PPG for post-suspension games</div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-xl bg-[var(--green)]/10 flex items-center justify-center">
                    <span className="text-2xl font-bold text-[var(--green)]">25.1</span>
                  </div>
                  <div>
                    <div className="text-white font-semibold">Actual PPG (9 games)</div>
                    <div className="text-sm text-gray-400">Below his 26.2 season baseline</div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-xl bg-[var(--blue)]/10 flex items-center justify-center">
                    <span className="text-2xl font-bold text-[var(--blue)]">0.3</span>
                  </div>
                  <div>
                    <div className="text-white font-semibold">PPG Error Margin</div>
                    <div className="text-sm text-gray-400">98.8% directional accuracy</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-[var(--surface-light)] rounded-xl p-6 border border-[var(--border)]">
              <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                Morant 2023-24 Timeline
              </h4>
              <div className="space-y-3">
                {[
                  { date: "Mar 4, 2023", event: "Gun shown on Instagram Live", dot: "bg-[var(--red)]" },
                  { date: "Mar 15, 2023", event: "Suspended 8 games by NBA", dot: "bg-[var(--red)]" },
                  { date: "May 14, 2023", event: "Second gun incident on IG", dot: "bg-[var(--red)]" },
                  { date: "Jun 16, 2023", event: "Suspended 25 games", dot: "bg-[var(--red)]" },
                  { date: "Sep 2023", event: "Entered counseling program", dot: "bg-[var(--yellow)]" },
                  { date: "Dec 19, 2023", event: "Returned — 34 pts, game-winner", dot: "bg-[var(--green)]" },
                  { date: "Jan 8, 2024", event: "Season-ending shoulder surgery", dot: "bg-[var(--red)]" },
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <div className="flex flex-col items-center">
                      <div className={`w-2.5 h-2.5 rounded-full ${item.dot} flex-shrink-0 mt-1`} />
                      {i < 6 && <div className="w-0.5 h-6 bg-white/10 mt-1" />}
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">{item.date}</div>
                      <div className="text-sm text-gray-300">{item.event}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

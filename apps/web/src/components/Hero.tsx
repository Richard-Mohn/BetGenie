export default function Hero() {
  return (
    <section className="relative gradient-hero min-h-screen flex items-center pt-20">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[var(--accent)]/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left: Copy */}
          <div className="text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[var(--accent)]/10 border border-[var(--accent)]/20 mb-6">
              <span className="w-2 h-2 rounded-full bg-[var(--green)] animate-pulse" />
              <span className="text-sm text-[var(--accent-light)] font-medium">
                AI Engine v0.1 — Proof of Concept Live
              </span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight tracking-tight">
              The Edge{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
                Nobody Else
              </span>{" "}
              Sees
            </h1>

            <p className="mt-6 text-lg sm:text-xl text-gray-400 leading-relaxed max-w-xl mx-auto lg:mx-0">
              BetGenie is the first AI platform that analyzes{" "}
              <span className="text-white font-medium">
                the whole player
              </span>{" "}
              — personal life, emotions, psychology — to predict performance
              and find prop betting edges the market misses.
            </p>

            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <a
                href="#waitlist"
                className="px-8 py-4 text-base font-semibold text-white gradient-accent rounded-full hover:opacity-90 transition-all shadow-xl pulse-glow"
              >
                Join the Waitlist — It&apos;s Free
              </a>
              <a
                href="#live-demo"
                className="px-8 py-4 text-base font-semibold text-gray-300 bg-white/5 border border-[var(--border)] rounded-full hover:bg-white/10 hover:text-white transition-all"
              >
                See Live Demo
              </a>
            </div>

            <div className="mt-10 flex items-center gap-6 justify-center lg:justify-start text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 text-[var(--green)]" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>No credit card</span>
              </div>
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 text-[var(--green)]" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>Free tier forever</span>
              </div>
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 text-[var(--green)]" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>NBA, NFL, MLB</span>
              </div>
            </div>
          </div>

          {/* Right: Player Impact Score Card */}
          <div className="relative">
            <div className="gradient-border p-6 sm:p-8 rounded-2xl glow-accent">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center text-white font-bold text-lg">
                    JM
                  </div>
                  <div>
                    <h3 className="text-white font-semibold text-lg">Ja Morant</h3>
                    <p className="text-gray-400 text-sm">PG · Memphis Grizzlies</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-[var(--yellow)]">67.6</div>
                  <div className="text-xs text-[var(--yellow)] font-medium uppercase tracking-wide">Caution</div>
                </div>
              </div>

              {/* Score Bars */}
              <div className="space-y-3 mb-6">
                {[
                  { label: "Physical", score: 75.0, color: "bg-[var(--green)]", width: "75%" },
                  { label: "Emotional", score: 56.8, color: "bg-[var(--yellow)]", width: "56.8%" },
                  { label: "Psychological", score: 63.5, color: "bg-[var(--yellow)]", width: "63.5%" },
                  { label: "Situational", score: 75.0, color: "bg-[var(--green)]", width: "75%" },
                ].map((item) => (
                  <div key={item.label}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-400">{item.label}</span>
                      <span className="text-white font-medium">{item.score}</span>
                    </div>
                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${item.color} rounded-full score-bar-fill`}
                        style={{ "--bar-width": item.width } as React.CSSProperties}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {/* Active Factors */}
              <div className="border-t border-[var(--border)] pt-4 mb-4">
                <h4 className="text-xs uppercase tracking-wider text-gray-500 mb-3">Active Factors</h4>
                <div className="space-y-2">
                  <div className="flex items-start gap-2">
                    <span className="text-[var(--red)] mt-0.5">●</span>
                    <span className="text-sm text-gray-300">Gun shown on Instagram Live — HIGH impact</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <span className="text-[var(--red)] mt-0.5">●</span>
                    <span className="text-sm text-gray-300">Under NBA investigation — media scrutiny</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <span className="text-[var(--yellow)] mt-0.5">●</span>
                    <span className="text-sm text-gray-300">Deactivated social media — &quot;stepping away&quot;</span>
                  </div>
                </div>
              </div>

              {/* Recommendation */}
              <div className="bg-[var(--red)]/10 border border-[var(--red)]/20 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[var(--red)] font-bold text-sm">RECOMMENDATION</span>
                </div>
                <p className="text-white font-semibold">
                  UNDER 25.5 Points{" "}
                  <span className="text-gray-400 font-normal">· Projected 25.4 · 69% confidence</span>
                </p>
              </div>
            </div>

            {/* Floating comparison card */}
            <div className="absolute -bottom-4 -left-4 sm:-left-8 bg-[var(--surface-light)] border border-[var(--border)] rounded-xl p-4 shadow-2xl max-w-[240px]">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-orange-500 to-orange-700 flex items-center justify-center text-white font-bold text-xs">
                  SGA
                </div>
                <div>
                  <p className="text-white text-sm font-medium">SGA</p>
                  <p className="text-gray-500 text-xs">Same Night</p>
                </div>
                <div className="ml-auto text-xl font-bold text-[var(--green)]">75.3</div>
              </div>
              <p className="text-xs text-gray-400">
                Clean record · No flags · <span className="text-[var(--green)]">OVER 31.3 pts</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

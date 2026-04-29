const tiers = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    description: "Get started with basic Impact Scores",
    features: [
      "3 player lookups per day",
      "Basic Impact Score (overall only)",
      "1 game analysis per day",
      "Community access",
    ],
    cta: "Get Started Free",
    ctaStyle:
      "bg-white/5 border border-[var(--border)] text-white hover:bg-white/10",
    popular: false,
  },
  {
    name: "Pro",
    price: "$29.99",
    period: "/month",
    yearlyPrice: "$249/yr (save 31%)",
    description: "Full Impact Scores + prop recommendations",
    features: [
      "Unlimited player lookups",
      "Full 4-component PIS breakdown",
      "All game analysis, every night",
      "Prop recommendations with confidence %",
      "Email alerts when PIS drops below 70",
      "Bet tracker & performance history",
      "Ad-free experience",
    ],
    cta: "Join Waitlist — Pro",
    ctaStyle:
      "gradient-accent text-white hover:opacity-90 shadow-lg",
    popular: true,
  },
  {
    name: "Elite",
    price: "$79.99",
    period: "/month",
    yearlyPrice: "$699/yr (save 27%)",
    description: "Smart Parlay Builder + backtesting",
    features: [
      "Everything in Pro",
      "Smart Parlay Builder (AI-optimized)",
      "SMS & push alerts (real-time)",
      "Historical backtesting access",
      "Advanced filters & custom watchlists",
      "Bankroll management tools",
      "Priority data refresh",
      "Dedicated support",
    ],
    cta: "Join Waitlist — Elite",
    ctaStyle:
      "bg-white/5 border border-[var(--accent)]/30 text-white hover:bg-[var(--accent)]/10",
    popular: false,
  },
  {
    name: "API",
    price: "$199",
    period: "/month+",
    description: "For developers, sharps & media",
    features: [
      "REST API access to all endpoints",
      "Webhooks for real-time PIS changes",
      "Bulk data exports (CSV, JSON)",
      "Custom integrations support",
      "Usage-based pricing above threshold",
      "SLA & dedicated support",
    ],
    cta: "Contact Sales",
    ctaStyle:
      "bg-white/5 border border-[var(--border)] text-white hover:bg-white/10",
    popular: false,
  },
];

export default function Pricing() {
  return (
    <section id="pricing" className="py-20 md:py-32 bg-[var(--surface)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="text-sm font-semibold text-[var(--accent-light)] uppercase tracking-wider">
            Pricing
          </span>
          <h2 className="mt-3 text-3xl sm:text-4xl lg:text-5xl font-bold text-white">
            Start Free.{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
              Win More.
            </span>
          </h2>
          <p className="mt-4 text-lg text-gray-400">
            At 55% hit rate, Pro pays for itself in your first week of betting.
          </p>
        </div>

        {/* Plans Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {tiers.map((tier) => (
            <div
              key={tier.name}
              className={`relative rounded-2xl p-6 transition-all duration-300 hover:translate-y-[-4px] ${
                tier.popular
                  ? "gradient-border glow-accent"
                  : "bg-[var(--surface-light)] border border-[var(--border)]"
              }`}
            >
              {tier.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 gradient-accent rounded-full text-xs font-semibold text-white shadow-lg">
                  Most Popular
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-lg font-semibold text-white mb-1">
                  {tier.name}
                </h3>
                <p className="text-sm text-gray-400">{tier.description}</p>
              </div>

              <div className="mb-6">
                <span className="text-4xl font-bold text-white">
                  {tier.price}
                </span>
                <span className="text-gray-400 text-sm">{tier.period}</span>
                {tier.yearlyPrice && (
                  <div className="text-xs text-[var(--green)] mt-1">
                    {tier.yearlyPrice}
                  </div>
                )}
              </div>

              <ul className="space-y-3 mb-8">
                {tier.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-2.5">
                    <svg
                      className="w-4 h-4 text-[var(--accent-light)] flex-shrink-0 mt-0.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span className="text-sm text-gray-300">{feature}</span>
                  </li>
                ))}
              </ul>

              <a
                href="#waitlist"
                className={`block w-full text-center py-3 rounded-full text-sm font-semibold transition-all ${tier.ctaStyle}`}
              >
                {tier.cta}
              </a>
            </div>
          ))}
        </div>

        {/* Bottom Note */}
        <p className="text-center text-sm text-gray-500 mt-8">
          All plans include our responsible gambling toolkit.
          Cancel anytime. No long-term contracts.
        </p>
      </div>
    </section>
  );
}

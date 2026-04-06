"use client";

import { useState } from "react";

const faqs = [
  {
    question: "Is BetGenie a sportsbook?",
    answer:
      "No. BetGenie is an analytics and intelligence platform — we never take bets, hold funds, or set odds. We provide data-driven recommendations that you can use on your preferred sportsbook (DraftKings, FanDuel, BetMGM, etc.). Think of us as the smartest research assistant you've ever had.",
  },
  {
    question: "How is this different from Action Network or PrizePicks?",
    answer:
      "Every existing platform focuses on statistics — historical averages, line movements, odds comparisons. BetGenie is the first platform that systematically analyzes players' personal lives (legal issues, family events, mental health, team dynamics) and quantifies how those factors impact tonight's game. No one else does this.",
  },
  {
    question: "What sports do you cover?",
    answer:
      "We're launching with NBA coverage (500+ players). NFL and MLB will follow within 6 months. Our AI engine is sport-agnostic — the Player Impact Score model works across any sport where personal factors affect performance.",
  },
  {
    question: "How accurate is the Player Impact Score?",
    answer:
      "In our proof-of-concept with real NBA data, we projected Ja Morant's post-suspension PPG within 0.3 points of his actual average (25.4 projected vs 25.1 actual). Our target production accuracy is 58%+ hit rate on flagged props — at standard -110 odds, that's a profitable edge.",
  },
  {
    question: "Where does BetGenie get its data?",
    answer:
      "We aggregate publicly available information from 30+ source categories: social media (Twitter/X, Instagram), news outlets (ESPN, local beat reporters), court records, team press conferences, injury reports, and more. We never access private information — everything we use is already public.",
  },
  {
    question: "Is this ethical? You're profiting from players' personal struggles.",
    answer:
      "BetGenie analyzes public information about public figures — the same information sports journalists report on daily. We don't surveil, hack, or invade privacy. Our system actually promotes responsible gambling by helping bettors make informed decisions rather than emotional ones. We also flag when users might be chasing losses.",
  },
  {
    question: "When will BetGenie launch?",
    answer:
      "We're currently in proof-of-concept phase with a working AI engine. The free tier (basic Impact Score lookups) is targeted for Q3 2026. Join the waitlist to get early access and help shape the product.",
  },
  {
    question: "Can I use BetGenie's data in my own models?",
    answer:
      "Yes! Our API tier ($199/month) provides REST API access to Player Impact Scores, event classifications, and prop recommendations. You can integrate BetGenie data directly into your spreadsheets, scripts, or custom models.",
  },
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section id="faq" className="py-20 md:py-32">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <span className="text-sm font-semibold text-[var(--accent-light)] uppercase tracking-wider">
            FAQ
          </span>
          <h2 className="mt-3 text-3xl sm:text-4xl font-bold text-white">
            Questions? We&apos;ve Got Answers.
          </h2>
        </div>

        {/* Accordion */}
        <div className="space-y-3">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="rounded-xl border border-[var(--border)] bg-[var(--surface)] overflow-hidden"
            >
              <button
                onClick={() =>
                  setOpenIndex(openIndex === index ? null : index)
                }
                className="w-full flex items-center justify-between p-5 text-left hover:bg-white/[0.02] transition-colors"
              >
                <span className="text-white font-medium pr-4">
                  {faq.question}
                </span>
                <svg
                  className={`w-5 h-5 text-gray-400 flex-shrink-0 transition-transform duration-200 ${
                    openIndex === index ? "rotate-180" : ""
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
              <div
                className={`transition-all duration-300 ease-in-out ${
                  openIndex === index
                    ? "max-h-96 opacity-100"
                    : "max-h-0 opacity-0"
                } overflow-hidden`}
              >
                <div className="px-5 pb-5 text-sm text-gray-400 leading-relaxed">
                  {faq.answer}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

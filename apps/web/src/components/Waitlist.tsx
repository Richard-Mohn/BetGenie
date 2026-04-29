"use client";

import { useState } from "react";

export default function Waitlist() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubmitted(true);
    }
  };

  return (
    <section id="waitlist" className="py-20 md:py-32 bg-[var(--surface)]">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="gradient-border rounded-2xl p-8 md:p-16 glow-accent">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[var(--accent)]/10 border border-[var(--accent)]/20 mb-6">
            <span className="w-2 h-2 rounded-full bg-[var(--green)] animate-pulse" />
            <span className="text-sm text-[var(--accent-light)] font-medium">
              Early Access — Limited Spots
            </span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4">
            Get the Edge{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--accent)] to-[var(--accent-light)]">
              Before Everyone Else
            </span>
          </h2>

          <p className="text-lg text-gray-400 max-w-2xl mx-auto mb-8">
            Join the waitlist for early access to BetGenie. Free tier users get
            3 player lookups per day — forever. Early supporters get priority
            access to Pro features.
          </p>

          {submitted ? (
            <div className="bg-[var(--green)]/10 border border-[var(--green)]/20 rounded-xl p-6 max-w-md mx-auto">
              <svg
                className="w-12 h-12 text-[var(--green)] mx-auto mb-3"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
              <h3 className="text-white font-semibold text-lg mb-1">
                You&apos;re on the list!
              </h3>
              <p className="text-sm text-gray-400">
                We&apos;ll notify you when BetGenie launches. Check{" "}
                <span className="text-white">{email}</span> for a
                confirmation.
              </p>
            </div>
          ) : (
            <form
              onSubmit={handleSubmit}
              className="flex flex-col sm:flex-row gap-3 max-w-lg mx-auto"
            >
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email address"
                required
                className="flex-1 px-5 py-3.5 rounded-full bg-white/5 border border-[var(--border)] text-white placeholder:text-gray-500 focus:outline-none focus:border-[var(--accent)] focus:ring-1 focus:ring-[var(--accent)] text-sm"
              />
              <button
                type="submit"
                className="px-8 py-3.5 gradient-accent text-white font-semibold rounded-full hover:opacity-90 transition-opacity shadow-lg text-sm whitespace-nowrap"
              >
                Join Waitlist
              </button>
            </form>
          )}

          <div className="mt-6 flex items-center justify-center gap-6 text-xs text-gray-500">
            <span>No spam, ever</span>
            <span>·</span>
            <span>Unsubscribe anytime</span>
            <span>·</span>
            <span>Free tier forever</span>
          </div>
        </div>
      </div>
    </section>
  );
}

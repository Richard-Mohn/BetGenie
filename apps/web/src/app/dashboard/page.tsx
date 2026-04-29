"use client";

import React, { useState, useEffect } from 'react';

interface GuaranteedPick {
  player_name: string;
  team: string;
  prop_type: string;
  line: number;
  direction: string;
  odds: number;
  ai_confidence: number;
  impact_score: number;
  projected_value: number;
  edge: number;
  quality: string;
  conservative_win_rate: number;
  key_factors: string[];
  recommended_bet?: {
    recommended_amount: number;
    percentage_of_bankroll: number;
    expected_value: number;
  };
}

interface GuaranteedParlay {
  picks: GuaranteedPick[];
  combined_odds: number;
  payout_multiplier: number;
  monte_carlo_probability: number;
  conservative_probability: number;
  expected_value: number;
  recommended_bet?: {
    recommended_amount: number;
    percentage_of_bankroll: number;
  };
  warnings?: string[];
}

export default function Dashboard() {
  const [bankroll] = useState(500);
  const [riskProfile, setRiskProfile] = useState('moderate');
  const [picks, setPicks] = useState<GuaranteedPick[]>([]);
  const [parlay, setParlay] = useState<GuaranteedParlay | null>(null);
  const [loading, setLoading] = useState(true);

  // Mock data - in production, this would come from the Python backend
  useEffect(() => {
    const loadData = () => {
      const mockPicks: GuaranteedPick[] = [
        {
          player_name: "LeBron James",
          team: "Los Angeles Lakers",
          prop_type: "points",
          line: 23.5,
          direction: "OVER",
          odds: -110,
          ai_confidence: 78,
          impact_score: 85,
          projected_value: 26.2,
          edge: 2.7,
          quality: "strong",
          conservative_win_rate: 0.70,
          key_factors: ["Home game", "Well rested", "Matchup advantage"],
          recommended_bet: {
            recommended_amount: 8.50,
            percentage_of_bankroll: 1.70,
            expected_value: 0.142,
          },
        },
        {
          player_name: "Shai Gilgeous-Alexander",
          team: "Oklahoma City Thunder",
          prop_type: "points",
          line: 31.5,
          direction: "UNDER",
          odds: -105,
          ai_confidence: 82,
          impact_score: 88,
          projected_value: 28.5,
          edge: 3.0,
          quality: "lock",
          conservative_win_rate: 0.74,
          key_factors: ["Elite defense", "Slow pace game", "Fatigue factor"],
          recommended_bet: {
            recommended_amount: 10.00,
            percentage_of_bankroll: 2.00,
            expected_value: 0.190,
          },
        },
        {
          player_name: "Victor Wembanyama",
          team: "San Antonio Spurs",
          prop_type: "rebounds",
          line: 10.5,
          direction: "OVER",
          odds: -110,
          ai_confidence: 75,
          impact_score: 82,
          projected_value: 12.8,
          edge: 2.3,
          quality: "strong",
          conservative_win_rate: 0.68,
          key_factors: ["Size advantage", "Weak rebounding opponent"],
          recommended_bet: {
            recommended_amount: 7.50,
            percentage_of_bankroll: 1.50,
            expected_value: 0.136,
          },
        },
      ];

      const mockParlay: GuaranteedParlay = {
        picks: mockPicks.slice(0, 2),
        combined_odds: +175,
        payout_multiplier: 2.75,
        monte_carlo_probability: 0.64,
        conservative_probability: 0.52,
        expected_value: 0.76,
        recommended_bet: {
          recommended_amount: 5.00,
          percentage_of_bankroll: 1.00,
        },
        warnings: [],
      };

      setPicks(mockPicks);
      setParlay(mockParlay);
      setLoading(false);
    };

    loadData();
  }, []);

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'lock': return 'bg-green-500';
      case 'strong': return 'bg-blue-500';
      case 'moderate': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getQualityIcon = (quality: string) => {
    switch (quality) {
      case 'lock': return '🔒';
      case 'strong': return '💪';
      case 'moderate': return '⚡';
      default: return '❓';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-2xl">Loading BetGenie Intelligence...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen gradient-hero">
      {/* Header */}
      <header className="backdrop-blur-xl bg-surface-light/50 border-b border-border px-6 py-4 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-accent glow-text">BetGenie 🎯</h1>
            <p className="text-gray-400 text-sm">AI-Powered Basketball Intelligence</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm text-gray-400">Bankroll</div>
              <div className="text-xl font-bold text-green">${bankroll.toFixed(2)}</div>
            </div>
            <select
              value={riskProfile}
              onChange={(e) => setRiskProfile(e.target.value)}
              className="bg-surface border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-accent transition-all"
              title="Risk Profile"
              aria-label="Risk Profile"
            >
              <option value="conservative">Conservative</option>
              <option value="moderate">Moderate</option>
              <option value="aggressive">Aggressive</option>
            </select>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="gradient-border p-4">
            <div className="text-gray-400 text-sm">Guaranteed Picks</div>
            <div className="text-3xl font-bold text-accent">{picks.length}</div>
          </div>
          <div className="gradient-border p-4">
            <div className="text-gray-400 text-sm">Avg Confidence</div>
            <div className="text-3xl font-bold text-green">
              {(picks.reduce((sum, p) => sum + p.ai_confidence, 0) / picks.length).toFixed(0)}%
            </div>
          </div>
          <div className="gradient-border p-4">
            <div className="text-gray-400 text-sm">Total Exposure</div>
            <div className="text-3xl font-bold text-yellow">
              ${picks.reduce((sum, p) => sum + (p.recommended_bet?.recommended_amount || 0), 0).toFixed(2)}
            </div>
          </div>
          <div className="gradient-border p-4">
            <div className="text-gray-400 text-sm">Risk Profile</div>
            <div className="text-3xl font-bold text-blue capitalize">{riskProfile}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Guaranteed Picks */}
          <div className="lg:col-span-2">
            <div className="gradient-border">
              <div className="px-6 py-4 border-b border-border backdrop-blur-sm">
                <h2 className="text-xl font-bold">🔒 Guaranteed Picks (70%+ Confidence)</h2>
                <p className="text-gray-400 text-sm">Quality over quantity. Bankroll protection first.</p>
              </div>
              <div className="p-6 space-y-4">
                {picks.map((pick, index) => (
                  <div key={index} className={`bg-surface-light/50 backdrop-blur-sm rounded-lg p-4 border border-border hover:border-accent transition-all duration-300 animate-fade-in-up animate-delay-${Math.min(index + 1, 5)}`}>
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-2xl">{getQualityIcon(pick.quality)}</span>
                          <h3 className="text-lg font-bold">{pick.player_name}</h3>
                          <span className={`px-2 py-1 rounded text-xs font-bold ${getQualityColor(pick.quality)}`}>
                            {pick.quality.toUpperCase()}
                          </span>
                        </div>
                        <div className="text-gray-400 text-sm">{pick.team}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-green">{pick.ai_confidence}%</div>
                        <div className="text-gray-400 text-xs">AI Confidence</div>
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4 mb-3">
                      <div className="bg-surface/50 backdrop-blur-sm rounded-lg p-2 text-center border border-border">
                        <div className="text-gray-400 text-xs">Bet</div>
                        <div className="font-bold">{pick.direction} {pick.line} {pick.prop_type}</div>
                      </div>
                      <div className="bg-surface/50 backdrop-blur-sm rounded-lg p-2 text-center border border-border">
                        <div className="text-gray-400 text-xs">Odds</div>
                        <div className="font-bold">{pick.odds > 0 ? '+' : ''}{pick.odds}</div>
                      </div>
                      <div className="bg-surface/50 backdrop-blur-sm rounded-lg p-2 text-center border border-border">
                        <div className="text-gray-400 text-xs">Edge</div>
                        <div className="font-bold text-green">+{pick.edge}</div>
                      </div>
                    </div>

                    <div className="mb-3">
                      <div className="text-gray-400 text-xs mb-1">Key Factors</div>
                      <div className="flex flex-wrap gap-2">
                        {pick.key_factors.map((factor, i) => (
                          <span key={i} className="bg-accent/20 text-accent-light px-2 py-1 rounded text-xs border border-accent/30">
                            {factor}
                          </span>
                        ))}
                      </div>
                    </div>

                    {pick.recommended_bet && (
                      <div className="bg-green/10 backdrop-blur-sm border border-green/30 rounded-lg p-3">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="text-green text-sm font-bold">💰 Recommended Bet</div>
                            <div className="text-gray-400 text-xs">
                              ${pick.recommended_bet.recommended_amount.toFixed(2)} ({pick.recommended_bet.percentage_of_bankroll}% of bankroll)
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-green font-bold">EV: {pick.recommended_bet.expected_value.toFixed(3)}</div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Parlay & Bankroll */}
          <div className="space-y-6">
            {/* Parlay Recommendation */}
            {parlay && (
              <div className="gradient-border">
                <div className="px-6 py-4 border-b border-border backdrop-blur-sm">
                  <h2 className="text-xl font-bold">🎯 Optimized Parlay</h2>
                  <p className="text-gray-400 text-sm">2-Leg parlay with guaranteed picks</p>
                </div>
                <div className="p-6">
                  <div className="text-center mb-4">
                    <div className="text-4xl font-bold text-accent glow-text">{parlay.combined_odds > 0 ? '+' : ''}{parlay.combined_odds}</div>
                    <div className="text-gray-400 text-sm">Combined Odds</div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-surface/50 backdrop-blur-sm rounded-lg p-3 text-center border border-border">
                      <div className="text-gray-400 text-xs">Payout</div>
                      <div className="text-xl font-bold text-green">{parlay.payout_multiplier.toFixed(2)}x</div>
                    </div>
                    <div className="bg-surface/50 backdrop-blur-sm rounded-lg p-3 text-center border border-border">
                      <div className="text-gray-400 text-xs">MC Win Rate</div>
                      <div className="text-xl font-bold text-accent">{(parlay.monte_carlo_probability * 100).toFixed(0)}%</div>
                    </div>
                  </div>

                  <div className="space-y-2 mb-4">
                    {parlay.picks.map((pick, i) => (
                      <div key={i} className="bg-surface/50 backdrop-blur-sm rounded-lg p-2 text-sm border border-border">
                        <span className="font-bold">{i + 1}.</span> {pick.player_name} {pick.direction[0].toUpperCase()}{pick.line} ({pick.ai_confidence}%)
                      </div>
                    ))}
                  </div>

                  {parlay.recommended_bet && (
                    <div className="bg-green/10 backdrop-blur-sm border border-green/30 rounded-lg p-3">
                      <div className="text-center">
                        <div className="text-green text-sm font-bold">💰 Bet ${parlay.recommended_bet.recommended_amount.toFixed(2)}</div>
                        <div className="text-gray-400 text-xs">{parlay.recommended_bet.percentage_of_bankroll}% of bankroll</div>
                      </div>
                    </div>
                  )}

                  {parlay.warnings && parlay.warnings.length > 0 && (
                    <div className="mt-4 bg-yellow/10 backdrop-blur-sm border border-yellow/30 rounded-lg p-3">
                      {parlay.warnings.map((warning, i) => (
                        <div key={i} className="text-yellow text-xs">⚠️ {warning}</div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Bankroll Summary */}
            <div className="gradient-border">
              <div className="px-6 py-4 border-b border-border backdrop-blur-sm">
                <h2 className="text-xl font-bold">💵 Bankroll Summary</h2>
              </div>
              <div className="p-6">
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Total Bankroll</span>
                    <span className="font-bold">${bankroll.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Total Exposure</span>
                    <span className="font-bold text-yellow">
                      ${picks.reduce((sum, p) => sum + (p.recommended_bet?.recommended_amount || 0), 0).toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Remaining</span>
                    <span className="font-bold text-green">
                      ${(bankroll - picks.reduce((sum, p) => sum + (p.recommended_bet?.recommended_amount || 0), 0)).toFixed(2)}
                    </span>
                  </div>
                  <div className="border-t border-border pt-3">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Risk Profile</span>
                      <span className="font-bold capitalize text-blue">{riskProfile}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Max Bet</span>
                      <span className="font-bold">
                        {riskProfile === 'conservative' ? '1%' : riskProfile === 'moderate' ? '2%' : '3%'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 gradient-border p-4">
          <p className="text-gray-400 text-sm text-center">
            ⚠️ BetGenie provides analysis and recommendations only. Gambling involves risk. Never bet more than you can afford to lose. 
            Past performance does not guarantee future results. Please gamble responsibly.
          </p>
        </div>
      </main>
    </div>
  );
}

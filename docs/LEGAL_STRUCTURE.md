# BetGenie — Legal Structure & International Expansion

**Document Purpose**: Define the legal framework for BetGenie to operate legally in the US while preparing for international expansion.

**Key Principle**: Separate the "Data/Analytics" business (legal everywhere) from the "Betting Execution" business (regulated).

---

## Executive Summary

**The Problem**: US gambling laws are complex, state-by-state, and restrict access to international betting exchanges like Betfair.

**The Solution**: A two-entity structure:
1. **US Entity (Mohn Empire)**: SaaS/Data Analytics platform — 100% legal in all states
2. **International Entity (Future)**: Execution layer for non-US markets — accesses Betfair/Pinnacle

**Why This Works**:
- Selling sports betting intelligence/data is legal in all 50 states
- Only the actual bet placement requires gambling licenses
- Modular architecture allows easy swap of execution APIs
- Banking separation (US bank for SaaS, international bank for gambling)

---

## Entity Structure

### Entity 1: Mohn Empire (US-Based)

**Type**: LLC (Limited Liability Company)  
**Jurisdiction**: Virginia (or Delaware for corporate flexibility)  
**Purpose**: Software as a Service (SaaS) / Data Analytics Platform  
**Legal Status**: Software company, NOT a gambling operator

**What It Does**:
- Hosts the Next.js 16 dashboard
- Runs the AI analysis engine (Python)
- Provides "information services" to subscribers
- Sells access to BetGenie intelligence platform
- Does NOT place bets directly

**Revenue Model**:
- Subscription tiers (Basic, Pro, Enterprise)
- Monthly/annual subscriptions
- API access fees for developers
- No commission on bets (we don't place bets)

**Regulatory Burden**: MINIMAL
- Data/analytics is legal in all states
- No gambling license required
- Standard business registration
- Standard tax reporting

**Banking**:
- US business bank account (Chase, Bank of America, etc.)
- Payment processing: Stripe, PayPal
- No restrictions on banking

**Intellectual Property**:
- Owns all BetGenie code and algorithms
- Owns Player Impact Score methodology
- Trademarks: "BetGenie", "Player Impact Score", "PIS"

**Compliance**:
- Terms of Service (ToS)
- Privacy Policy (GDPR/CCPA compliant)
- Data security standards
- User authentication (OAuth/JWT)

---

### Entity 2: Mohn Empire International (Future - UK Ltd or UAE Freezone)

**Type**: Ltd (UK) or Freezone Company (UAE)  
**Jurisdiction**: United Kingdom or United Arab Emirates  
**Purpose**: Betting Execution Layer for non-US markets  
**Legal Status**: Gambling operator (requires license)

**What It Does**:
- Hosts the execution module (bet placement)
- Integrates with Betfair API (UK/Europe)
- Integrates with Pinnacle API (International)
- Integrates with Sporttrade API (US states where legal)
- Places bets for international users
- Handles gambling compliance

**Revenue Model**:
- Commission on bet execution (2-5%)
- Subscription for execution API access
- White-label solutions for other operators

**Regulatory Burden**: HIGH
- Gambling license in target jurisdiction
- AML/KYC compliance
- Responsible gambling requirements
- Regular audits and reporting

**Banking**:
- International EMI (Revolut Business, Airwallex)
- Multi-currency accounts (GBP, EUR, USD)
- Gambling-friendly payment processors

**Licensing Options**:
- **UK**: UK Gambling Commission (most respected, expensive)
- **Malta**: MGA license (EU-wide, moderate cost)
- **Gibraltar**: Similar to UK, slightly cheaper
- **UAE**: DIFC/ADGM (emerging hub, tax benefits)
- **Curacao**: Low-cost, less respected

**Recommended**: Start with UK Ltd + UK Gambling Commission (Phase 4+)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (Bettor)                             │
│  - Located in US or International                           │
│  - Subscribes to BetGenie SaaS                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Mohn Empire (US Entity)                         │
│              SaaS / Data Analytics Platform                  │
├─────────────────────────────────────────────────────────────┤
│  - Next.js 16 Dashboard                                     │
│  - AI Engine (Python)                                        │
│  - Player Impact Score                                      │
│  - Consensus Module                                         │
│  - Unified Confidence Score                                 │
│  - OpticOdds API Integration                                │
│  - Data Storage (US-based)                                  │
│  - User Authentication                                       │
│  - Subscription Management                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ User sees picks and recommendations
                     │ User clicks "Place Bet" button
                     │
                     ▼
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   US User       │    │ Intl User       │
│   (Legal State) │    │   (Non-US)      │
└────────┬────────┘    └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Sporttrade API │    │ Betfair API     │
│  (US Exchange)  │    │ (Intl Exchange) │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Mohn Empire Intl      │
         │ (Future UK Entity)    │
         │ - Execution Module    │
         │ - API Keys            │
         │ - Compliance          │
         └───────────────────────┘
```

---

## Modular Execution Layer

The execution layer is designed to be modular — it can swap APIs based on user location and legal requirements.

### Execution Interface

```python
class BettingExecutionInterface:
    """Abstract interface for betting execution."""
    
    def place_bet(self, bet_details: BetDetails) -> BetConfirmation:
        """Place a bet via the configured exchange."""
        pass
    
    def get_balance(self) -> float:
        """Get account balance."""
        pass
    
    def get_bet_status(self, bet_id: str) -> BetStatus:
        """Get status of a placed bet."""
        pass
```

### Implementations

1. **SporttradeExecution** (US states where legal)
2. **BetfairExecution** (UK/Europe/International)
3. **PinnacleExecution** (International)
4. **ProphetXExecution** (US sweepstakes model)

### Configuration

```python
# Based on user location and legal status
if user.location == "US" and user.state in LEGAL_SPORTTRADE_STATES:
    executor = SporttradeExecution(api_key=SPORTTRADE_KEY)
elif user.location == "UK":
    executor = BetfairExecution(api_key=BETFAIR_KEY)
elif user.location == "International":
    executor = PinnacleExecution(api_key=PINNACLE_KEY)
else:
    executor = None  # No legal execution available
```

---

## Banking & Financial Structure

### US Entity Banking

**Business Account**:
- Chase Business Complete Banking
- Bank of America Business Account
- Features: ACH transfers, wire transfers, debit card

**Payment Processing**:
- Stripe (subscriptions)
- PayPal (alternative)
- Wise (international transfers if needed)

**Taxation**:
- Pass-through entity (LLC)
- Income taxed at personal rate
- Self-employment tax
- State taxes (Virginia)

### International Entity Banking

**EMI Options**:
- Revolut Business (UK/Europe)
- Airwallex (Hong Kong/Global)
- Wise Business (Global)

**Multi-Currency**:
- GBP (UK operations)
- EUR (Europe)
- USD (US customers)
- AED (UAE operations)

**Payment Processing**:
- Gambling-specific processors
- Crypto (optional, for international)
- Bank wires for large amounts

**Taxation**:
- UK Ltd: 19% corporate tax
- UAE Freezone: 0% corporate tax
- May need to pay US taxes on US-source income

---

## Compliance Requirements

### US Entity (SaaS)

**Required**:
- Business registration (State)
- EIN (Employer Identification Number)
- Business bank account
- Terms of Service
- Privacy Policy
- Data security (SSL, encryption)

**Not Required**:
- Gambling license
- Gaming commission approval
- AML/KYC for users (basic identity verification only)

**Recommended**:
- D&B (Dun & Bradstreet) number
- Business insurance
- Trademark registration
- Patent protection (for PIS algorithm)

### International Entity (Gambling)

**Required**:
- Gambling license (UKGC, MGA, etc.)
- AML/KYC compliance program
- Responsible gambling tools
- Age verification (18+)
- Self-exclusion program
- Regular audits
- Financial reserves

**Data Protection**:
- GDPR compliance (Europe)
- Local data protection laws
- Data localization (some countries)

**Reporting**:
- Transaction reporting
- Suspicious activity reporting
- Financial reporting to regulators
- Responsible gambling metrics

---

## Phase-by-Phase Rollout

### Phase 1: US SaaS Launch (Immediate)

**Timeline**: Month 1-3

**Activities**:
1. Form US LLC (if not already formed)
2. Open US business bank account
3. Set up Stripe for payments
4. Launch BetGenie SaaS platform
5. Market as "sports betting intelligence"
6. No bet placement (information only)

**Legal Status**: 100% legal in all 50 states

**Revenue**: Subscription fees only

---

### Phase 2: US Exchange Integration (Month 4-6)

**Timeline**: Month 4-6

**Activities**:
1. Sign up for Sporttrade API
2. Integrate Sporttrade execution module
3. Enable bet placement for users in legal states
4. Add state-by-state geolocation
5. Implement responsible gambling tools

**Legal Status**: Legal in states where Sporttrade operates

**Revenue**: Subscriptions + optional execution fees

**Note**: US entity can handle this as "technology provider" to Sporttrade

---

### Phase 3: International Expansion Planning (Month 7-12)

**Timeline**: Month 7-12

**Activities**:
1. Consult with international gambling lawyers
2. Choose jurisdiction (UK recommended)
3. Prepare UK Gambling Commission application
4. Set up international banking (Revolut Business)
5. Draft international entity structure

**Legal Status**: Planning phase

**Revenue**: Still US-focused

---

### Phase 4: International Launch (Month 12-18)

**Timeline**: Month 12-18

**Activities**:
1. Form UK Ltd entity
2. Obtain UK Gambling Commission license
3. Integrate Betfair API
4. Integrate Pinnacle API
5. Launch international version
6. Hire international staff

**Legal Status**: Licensed gambling operator in UK/EU

**Revenue**: Subscriptions + execution commissions

---

## Risk Mitigation

### Legal Risks

**Risk**: US states classify BetGenie as illegal gambling  
**Mitigation**:
- Clear positioning as "data/analytics" only
- Terms of Service explicitly state we don't place bets
- No bet placement from US entity
- Legal review of ToS by gambling attorney

**Risk**: International license denied  
**Mitigation**:
- Start with UK (most straightforward)
- Have backup jurisdictions (Malta, Gibraltar)
- Partner with licensed operator initially

### Financial Risks

**Risk**: Payment processor blocks gambling-related business  
**Mitigation**:
- US entity: Position as SaaS (not gambling)
- International entity: Use gambling-friendly processors
- Maintain multiple payment options

**Risk**: Banking restrictions  
**Mitigation**:
- US entity: Standard business banking (no issue)
- International entity: Use EMIs familiar with gambling

### Operational Risks

**Risk**: API access revoked (Sporttrade, Betfair)  
**Mitigation**:
- Multiple API integrations (redundancy)
- Modular architecture (easy swap)
- Direct relationships with exchanges

**Risk**: User fraud/chargebacks  
**Mitigation**:
- KYC verification
- Two-factor authentication
- Transaction monitoring
- Clear refund policy

---

## Attorney Consultation Checklist

Before launch, consult with a gambling attorney to review:

- [ ] Entity structure (US LLC)
- [ ] Terms of Service (gambling disclaimers)
- [ ] Privacy Policy (data handling)
- [ ] State-by-state gambling law analysis
- [ ] Sporttrade integration legality
- [ ] International entity structure
- [ ] UK Gambling Commission requirements
- [ ] Tax implications (US and international)
- [ ] Intellectual property protection
- [ ] Employment law (international hiring)

---

## Next Steps

1. **Form US LLC** (if not already formed)
2. **Open US business bank account**
3. **Set up Stripe account**
4. **Draft Terms of Service** (with gambling disclaimers)
5. **Draft Privacy Policy**
6. **Consult with gambling attorney** (US-based)
7. **Apply for Sporttrade API access**
8. **Begin UK entity planning** (for Phase 4)

---

**Document Status**: Draft — Requires Attorney Review  
**Last Updated**: April 28, 2026  
**Next Review**: After attorney consultation

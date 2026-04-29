"use strict";
/**
 * BetGenie Firebase Functions
 *
 * Provides API endpoints for:
 * - Getting daily picks and parlays
 * - Fetching player data and odds
 * - News monitoring
 * - AI analysis results
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.placeBet = exports.askJarvis = exports.cleanupOldData = exports.generateDailyReport = exports.onNewsEvent = exports.onOddsUpdated = exports.onGameCreated = exports.api = void 0;
const functions = __importStar(require("firebase-functions"));
const admin = __importStar(require("firebase-admin"));
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
// Initialize Firebase Admin
admin.initializeApp();
const db = admin.firestore();
// Create Express app
const app = (0, express_1.default)();
app.use((0, cors_1.default)({ origin: true }));
app.use(express_1.default.json());
// ============================================================================
// API Routes
// ============================================================================
/**
 * GET /api/health
 * Health check endpoint
 */
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'betgenie-api',
        version: '1.0.0'
    });
});
/**
 * GET /api/picks/today
 * Get today's guaranteed picks
 */
app.get('/api/picks/today', async (req, res) => {
    try {
        const today = new Date().toISOString().split('T')[0];
        const picksSnapshot = await db
            .collection('picks')
            .where('date', '==', today)
            .where('quality', 'in', ['LOCK', 'STRONG'])
            .orderBy('ai_confidence', 'desc')
            .get();
        const picks = picksSnapshot.docs.map(doc => (Object.assign({ id: doc.id }, doc.data())));
        res.json({
            date: today,
            count: picks.length,
            picks
        });
    }
    catch (error) {
        console.error('Error fetching picks:', error);
        res.status(500).json({ error: 'Failed to fetch picks' });
    }
});
/**
 * GET /api/parlays/today
 * Get today's parlay recommendations
 */
app.get('/api/parlays/today', async (req, res) => {
    try {
        const today = new Date().toISOString().split('T')[0];
        const parlaysSnapshot = await db
            .collection('parlays')
            .where('date', '==', today)
            .orderBy('conservative_probability', 'desc')
            .get();
        const parlays = parlaysSnapshot.docs.map(doc => (Object.assign({ id: doc.id }, doc.data())));
        res.json({
            date: today,
            count: parlays.length,
            parlays
        });
    }
    catch (error) {
        console.error('Error fetching parlays:', error);
        res.status(500).json({ error: 'Failed to fetch parlays' });
    }
});
/**
 * GET /api/kickers/today
 * Get today's kicker bets (high payout opportunities)
 */
app.get('/api/kickers/today', async (req, res) => {
    try {
        const today = new Date().toISOString().split('T')[0];
        const kickersSnapshot = await db
            .collection('kicker_bets')
            .where('date', '==', today)
            .orderBy('odds', 'desc')
            .get();
        const kickers = kickersSnapshot.docs.map(doc => (Object.assign({ id: doc.id }, doc.data())));
        res.json({
            date: today,
            count: kickers.length,
            kickers
        });
    }
    catch (error) {
        console.error('Error fetching kickers:', error);
        res.status(500).json({ error: 'Failed to fetch kicker bets' });
    }
});
/**
 * GET /api/games/today
 * Get today's NBA games
 */
app.get('/api/games/today', async (req, res) => {
    try {
        const today = new Date().toISOString().split('T')[0];
        const gamesSnapshot = await db
            .collection('games')
            .where('date', '==', today)
            .orderBy('start_time')
            .get();
        const games = gamesSnapshot.docs.map(doc => (Object.assign({ id: doc.id }, doc.data())));
        res.json({
            date: today,
            count: games.length,
            games
        });
    }
    catch (error) {
        console.error('Error fetching games:', error);
        res.status(500).json({ error: 'Failed to fetch games' });
    }
});
/**
 * GET /api/players/:playerId
 * Get player details and stats
 */
app.get('/api/players/:playerId', async (req, res) => {
    try {
        const { playerId } = req.params;
        const playerDoc = await db.collection('players').doc(playerId).get();
        if (!playerDoc.exists) {
            res.status(404).json({ error: 'Player not found' });
            return;
        }
        // Get recent stats
        const statsSnapshot = await db
            .collection('player_stats')
            .where('player_id', '==', playerId)
            .orderBy('date', 'desc')
            .limit(10)
            .get();
        const stats = statsSnapshot.docs.map(doc => doc.data());
        // Get impact score
        const impactDoc = await db.collection('impact_scores').doc(playerId).get();
        const impactScore = impactDoc.exists ? impactDoc.data() : null;
        res.json({
            player: Object.assign({ id: playerDoc.id }, playerDoc.data()),
            recent_stats: stats,
            impact_score: impactScore
        });
    }
    catch (error) {
        console.error('Error fetching player:', error);
        res.status(500).json({ error: 'Failed to fetch player data' });
    }
});
/**
 * GET /api/news/recent
 * Get recent news events
 */
app.get('/api/news/recent', async (req, res) => {
    try {
        const daysBack = parseInt(req.query.days) || 7;
        const since = new Date();
        since.setDate(since.getDate() - daysBack);
        const newsSnapshot = await db
            .collection('news_events')
            .where('date', '>=', since.toISOString())
            .orderBy('date', 'desc')
            .get();
        const news = newsSnapshot.docs.map(doc => (Object.assign({ id: doc.id }, doc.data())));
        res.json({
            count: news.length,
            days_back: daysBack,
            news
        });
    }
    catch (error) {
        console.error('Error fetching news:', error);
        res.status(500).json({ error: 'Failed to fetch news' });
    }
});
/**
 * GET /api/report/today
 * Get full daily betting report
 */
app.get('/api/report/today', async (req, res) => {
    try {
        const today = new Date().toISOString().split('T')[0];
        const reportDoc = await db.collection('daily_reports').doc(today).get();
        if (!reportDoc.exists) {
            res.status(404).json({
                error: 'Report not found',
                message: 'Today\'s report has not been generated yet. Please check back later.'
            });
            return;
        }
        res.json(Object.assign({ date: today }, reportDoc.data()));
    }
    catch (error) {
        console.error('Error fetching report:', error);
        res.status(500).json({ error: 'Failed to fetch daily report' });
    }
});
/**
 * POST /api/jarvis/query
 * Jarvis AI intelligence query
 */
app.post('/api/jarvis/query', async (req, res) => {
    try {
        const { query } = req.body;
        if (!query) {
            res.status(400).json({ error: 'Query is required' });
            return;
        }
        // In production, this would call the Python AI engine
        // For now, return a mock response
        const mockResponse = {
            query,
            main_answer: "Based on today's analysis, I recommend focusing on the 4-leg parlay with the LeBron James kicker side bet. The main parlay has a 64.5% win probability and offers solid profit potential even without the kicker hitting.",
            confidence_score: 92,
            suggested_actions: [
                "Consider the 4-leg parlay for $20 stake",
                "Add $7.50 kicker side bet on LeBron OVER",
                "Monitor for any last-minute injury news"
            ],
            risk_assessment: "MODERATE - Main parlay provides downside protection",
            timestamp: new Date().toISOString()
        };
        res.json(mockResponse);
    }
    catch (error) {
        console.error('Error processing Jarvis query:', error);
        res.status(500).json({ error: 'Failed to process query' });
    }
});
/**
 * GET /api/dual-strategy/today
 * Get today's dual bet strategy (guaranteed + kicker)
 */
app.get('/api/dual-strategy/today', async (req, res) => {
    var _a, _b;
    try {
        const today = new Date().toISOString().split('T')[0];
        // Get the 4-leg parlay as main bet
        const parlaysSnapshot = await db
            .collection('parlays')
            .where('date', '==', today)
            .where('legs', '==', 4)
            .limit(1)
            .get();
        // Get a kicker bet
        const kickersSnapshot = await db
            .collection('kicker_bets')
            .where('date', '==', today)
            .orderBy('odds', 'desc')
            .limit(1)
            .get();
        const mainParlay = ((_a = parlaysSnapshot.docs[0]) === null || _a === void 0 ? void 0 : _a.data()) || null;
        const kickerBet = ((_b = kickersSnapshot.docs[0]) === null || _b === void 0 ? void 0 : _b.data()) || null;
        if (!mainParlay) {
            res.status(404).json({ error: 'No dual strategy available for today' });
            return;
        }
        // Calculate scenarios
        const mainStake = 20;
        const kickerStake = kickerBet ? 7.5 : 0;
        const totalStake = mainStake + kickerStake;
        const mainPayout = mainStake * mainParlay.payout_multiplier;
        const kickerPayout = kickerBet ? kickerStake * (kickerBet.odds / 100 + 1) : 0;
        res.json({
            date: today,
            strategy_name: "Dual Bet: Guaranteed + Kicker",
            main_parlay: Object.assign(Object.assign({}, mainParlay), { stake: mainStake, potential_payout: mainPayout }),
            kicker_bet: kickerBet ? Object.assign(Object.assign({}, kickerBet), { stake: kickerStake, potential_payout: kickerPayout }) : null,
            total_stake: totalStake,
            scenarios: {
                main_only_win: {
                    description: "Main parlay hits, kicker misses",
                    net_profit: mainPayout - totalStake
                },
                both_win: {
                    description: "Both main parlay AND kicker hit",
                    net_profit: mainPayout + kickerPayout - totalStake
                },
                both_lose: {
                    description: "Both miss",
                    net_profit: -totalStake
                }
            },
            recommendation: "RECOMMENDED - High EV with downside protection"
        });
    }
    catch (error) {
        console.error('Error fetching dual strategy:', error);
        res.status(500).json({ error: 'Failed to fetch dual bet strategy' });
    }
});
// Export the API as a Firebase Function
exports.api = functions.https.onRequest(app);
// ============================================================================
// Cloud Functions (Firestore Triggers)
// ============================================================================
/**
 * Trigger: When a new game is added, update related data
 */
exports.onGameCreated = functions.firestore
    .document('games/{gameId}')
    .onCreate(async (snap, context) => {
    const game = snap.data();
    console.log(`New game created: ${game.home_team} vs ${game.away_team}`);
    // Trigger odds aggregation for this game
    // This would call the Cloud Run service
    return null;
});
/**
 * Trigger: When new odds are added, run AI analysis
 */
exports.onOddsUpdated = functions.firestore
    .document('odds/{oddsId}')
    .onWrite(async (change, context) => {
    const odds = change.after.data();
    if (!odds)
        return null;
    console.log(`Odds updated for game: ${odds.game_id}`);
    // Trigger AI analysis
    // This would call the Cloud Run service
    return null;
});
/**
 * Trigger: When news event is detected, update player impact score
 */
exports.onNewsEvent = functions.firestore
    .document('news_events/{eventId}')
    .onCreate(async (snap, context) => {
    const event = snap.data();
    console.log(`News event detected: ${event.player_name} - ${event.event_category}`);
    // Update player impact score
    const playerId = event.player_name.toLowerCase().replace(/\s+/g, '_');
    const impactRef = db.collection('impact_scores').doc(playerId);
    await impactRef.set({
        player_name: event.player_name,
        recent_event: event,
        last_updated: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });
    return null;
});
/**
 * Scheduled Function: Generate daily report at 6 AM EST
 */
exports.generateDailyReport = functions.pubsub
    .schedule('0 6 * * *')
    .timeZone('America/New_York')
    .onRun(async (context) => {
    const today = new Date().toISOString().split('T')[0];
    console.log(`Generating daily report for ${today}`);
    // This would trigger the Python AI pipeline
    // For now, just log
    console.log('Daily report generation triggered');
    return null;
});
/**
 * Scheduled Function: Clean up old data (runs weekly)
 */
exports.cleanupOldData = functions.pubsub
    .schedule('0 0 * * 0')
    .timeZone('America/New_York')
    .onRun(async (context) => {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    // Delete old odds data
    const oldOdds = await db
        .collection('odds')
        .where('timestamp', '<', thirtyDaysAgo.toISOString())
        .limit(1000)
        .get();
    const batch = db.batch();
    oldOdds.docs.forEach(doc => {
        batch.delete(doc.ref);
    });
    await batch.commit();
    console.log(`Cleaned up ${oldOdds.size} old odds records`);
    return null;
});
// ============================================================================
// Callable Functions (for client SDK)
// ============================================================================
/**
 * Callable: Get Jarvis AI analysis for a specific query
 */
exports.askJarvis = functions.https.onCall(async (data, context) => {
    const { query } = data;
    if (!query) {
        throw new functions.https.HttpsError('invalid-argument', 'Query is required');
    }
    // In production, this would call the Python AI engine
    return {
        query,
        response: "Jarvis analysis would be generated here by the Python AI engine",
        timestamp: new Date().toISOString()
    };
});
/**
 * Callable: Place a bet (track user bets)
 */
exports.placeBet = functions.https.onCall(async (data, context) => {
    // Verify authentication
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
    }
    const userId = context.auth.uid;
    const { pick_id, amount, odds, type } = data;
    // Store bet in user's history
    const betRef = db.collection('users').doc(userId).collection('bets').doc();
    await betRef.set({
        pick_id,
        amount,
        odds,
        type,
        status: 'pending',
        placed_at: admin.firestore.FieldValue.serverTimestamp()
    });
    return { bet_id: betRef.id, status: 'placed' };
});
//# sourceMappingURL=index.js.map
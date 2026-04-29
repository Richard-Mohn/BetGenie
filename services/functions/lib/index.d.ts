/**
 * BetGenie Firebase Functions
 *
 * Provides API endpoints for:
 * - Getting daily picks and parlays
 * - Fetching player data and odds
 * - News monitoring
 * - AI analysis results
 */
import * as functions from 'firebase-functions';
export declare const api: functions.HttpsFunction;
/**
 * Trigger: When a new game is added, update related data
 */
export declare const onGameCreated: functions.CloudFunction<functions.firestore.QueryDocumentSnapshot>;
/**
 * Trigger: When new odds are added, run AI analysis
 */
export declare const onOddsUpdated: functions.CloudFunction<functions.Change<functions.firestore.DocumentSnapshot>>;
/**
 * Trigger: When news event is detected, update player impact score
 */
export declare const onNewsEvent: functions.CloudFunction<functions.firestore.QueryDocumentSnapshot>;
/**
 * Scheduled Function: Generate daily report at 6 AM EST
 */
export declare const generateDailyReport: functions.CloudFunction<unknown>;
/**
 * Scheduled Function: Clean up old data (runs weekly)
 */
export declare const cleanupOldData: functions.CloudFunction<unknown>;
/**
 * Callable: Get Jarvis AI analysis for a specific query
 */
export declare const askJarvis: functions.HttpsFunction & functions.Runnable<any>;
/**
 * Callable: Place a bet (track user bets)
 */
export declare const placeBet: functions.HttpsFunction & functions.Runnable<any>;
//# sourceMappingURL=index.d.ts.map
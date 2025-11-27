/**
 * Query Log Interceptor - Middleware for capturing ORM queries in Node.js applications.
 * 
 * Supports: Sequelize, Prisma, TypeORM
 * 
 * Features:
 * - Captures all queries with timing
 * - Groups queries by request
 * - Detects N+1 patterns in real-time
 * - Exports logs for analysis
 * 
 * Usage:
 *   const { QueryInterceptor, expressMiddleware } = require('./log_interceptor');
 *   app.use(expressMiddleware());
 */

const { AsyncLocalStorage } = require('async_hooks');

// Store for request-scoped query tracking
const asyncLocalStorage = new AsyncLocalStorage();

/**
 * Query log entry
 */
class QueryLog {
  constructor() {
    this.queries = [];
    this.startTime = Date.now();
  }

  add(query, params, duration) {
    this.queries.push({
      sql: query,
      params: params,
      duration: duration,
      timestamp: Date.now(),
      normalized: this.normalize(query)
    });
  }

  normalize(sql) {
    return sql
      .replace(/'(?:[^'\\]|\\.)*'/g, "'?'")
      .replace(/\b\d+(?:\.\d+)?\b/g, '?')
      .replace(/\$\d+/g, '?')
      .replace(/:\w+/g, '?')
      .toUpperCase()
      .trim();
  }

  getStats() {
    const totalTime = this.queries.reduce((sum, q) => sum + q.duration, 0);
    const queryCount = this.queries.length;
    
    // Detect N+1
    const normalized = {};
    this.queries.forEach(q => {
      normalized[q.normalized] = (normalized[q.normalized] || 0) + 1;
    });
    
    const nPlusOne = Object.entries(normalized)
      .filter(([_, count]) => count >= 3)
      .map(([sql, count]) => ({ sql: sql.substring(0, 100), count }));

    return {
      queryCount,
      totalTime,
      avgTime: queryCount > 0 ? totalTime / queryCount : 0,
      nPlusOne,
      slowQueries: this.queries
        .filter(q => q.duration > 100)
        .map(q => ({ sql: q.sql.substring(0, 200), duration: q.duration }))
    };
  }

  toJSON() {
    return {
      queries: this.queries,
      stats: this.getStats(),
      duration: Date.now() - this.startTime
    };
  }
}

/**
 * Main interceptor class
 */
class QueryInterceptor {
  static getStore() {
    return asyncLocalStorage.getStore();
  }

  static getCurrentLog() {
    const store = this.getStore();
    return store?.queryLog;
  }

  static logQuery(sql, params, duration) {
    const log = this.getCurrentLog();
    if (log) {
      log.add(sql, params, duration);
    }
  }

  /**
   * Wrap a function with query tracking
   */
  static async track(fn) {
    const queryLog = new QueryLog();
    return asyncLocalStorage.run({ queryLog }, async () => {
      try {
        return await fn();
      } finally {
        const stats = queryLog.getStats();
        if (stats.nPlusOne.length > 0) {
          console.warn('[QueryInterceptor] N+1 detected:', stats.nPlusOne);
        }
      }
    });
  }
}

/**
 * Express/Connect middleware
 */
function expressMiddleware(options = {}) {
  const {
    logAll = false,
    warnThreshold = 10,  // Warn if more than N queries per request
    slowThreshold = 100,  // Log queries slower than N ms
    onComplete = null     // Callback with query log
  } = options;

  return (req, res, next) => {
    const queryLog = new QueryLog();
    
    asyncLocalStorage.run({ queryLog }, () => {
      // Capture response end
      const originalEnd = res.end;
      res.end = function(...args) {
        const stats = queryLog.getStats();
        
        // Log warnings
        if (stats.queryCount > warnThreshold) {
          console.warn(`[QueryInterceptor] ${req.method} ${req.path}: ${stats.queryCount} queries (${stats.totalTime}ms)`);
        }
        
        if (stats.nPlusOne.length > 0) {
          console.warn(`[QueryInterceptor] N+1 detected in ${req.method} ${req.path}:`, stats.nPlusOne);
        }
        
        if (logAll) {
          console.log(`[QueryInterceptor] ${req.method} ${req.path}:`, JSON.stringify(stats, null, 2));
        }
        
        // Attach to response for debugging
        res.locals.queryLog = queryLog.toJSON();
        
        if (onComplete) {
          onComplete(req, res, queryLog.toJSON());
        }
        
        return originalEnd.apply(this, args);
      };
      
      next();
    });
  };
}

/**
 * Sequelize integration
 */
function sequelizeLogger(sequelize) {
  const originalQuery = sequelize.query.bind(sequelize);
  
  sequelize.query = async function(sql, options = {}) {
    const start = Date.now();
    try {
      const result = await originalQuery(sql, options);
      const duration = Date.now() - start;
      
      QueryInterceptor.logQuery(
        typeof sql === 'string' ? sql : sql.query,
        options.replacements || options.bind || [],
        duration
      );
      
      return result;
    } catch (error) {
      const duration = Date.now() - start;
      QueryInterceptor.logQuery(
        typeof sql === 'string' ? sql : sql.query,
        options.replacements || options.bind || [],
        duration
      );
      throw error;
    }
  };
  
  return sequelize;
}

/**
 * Prisma integration (using $extends)
 */
function prismaExtension() {
  return {
    query: {
      $allOperations({ operation, model, args, query }) {
        const start = Date.now();
        return query(args).then(result => {
          const duration = Date.now() - start;
          QueryInterceptor.logQuery(
            `${model}.${operation}`,
            JSON.stringify(args),
            duration
          );
          return result;
        });
      }
    }
  };
}

/**
 * TypeORM integration (using subscriber)
 */
class TypeORMQuerySubscriber {
  afterQuery(event) {
    if (event.query) {
      QueryInterceptor.logQuery(
        event.query,
        event.parameters || [],
        event.queryExecutionTime || 0
      );
    }
  }
}

/**
 * Export query logs to file
 */
async function exportLogs(queryLog, filepath) {
  const fs = require('fs').promises;
  const content = queryLog.queries
    .map(q => `${q.sql}`)
    .join('\n');
  await fs.writeFile(filepath, content);
}

/**
 * Analyze accumulated logs
 */
function analyzeSession(queryLogs) {
  const allQueries = queryLogs.flatMap(log => log.queries);
  const normalized = {};
  
  allQueries.forEach(q => {
    const key = q.normalized;
    if (!normalized[key]) {
      normalized[key] = { count: 0, totalTime: 0, example: q.sql };
    }
    normalized[key].count++;
    normalized[key].totalTime += q.duration;
  });
  
  return {
    totalQueries: allQueries.length,
    uniqueQueries: Object.keys(normalized).length,
    topByCount: Object.entries(normalized)
      .sort((a, b) => b[1].count - a[1].count)
      .slice(0, 10)
      .map(([sql, stats]) => ({ ...stats, sql: sql.substring(0, 100) })),
    topByTime: Object.entries(normalized)
      .sort((a, b) => b[1].totalTime - a[1].totalTime)
      .slice(0, 10)
      .map(([sql, stats]) => ({ ...stats, sql: sql.substring(0, 100) }))
  };
}

module.exports = {
  QueryInterceptor,
  QueryLog,
  expressMiddleware,
  sequelizeLogger,
  prismaExtension,
  TypeORMQuerySubscriber,
  exportLogs,
  analyzeSession
};

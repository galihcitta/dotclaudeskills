#!/usr/bin/env python3
"""
Query Analyzer - Detect common ORM anti-patterns from query logs.

Analyzes a log of SQL queries and identifies:
- N+1 query patterns
- Missing WHERE clauses on large tables
- SELECT * (over-fetching)
- Cartesian joins
- Repeated identical queries (missing caching)
- Sequential scans hints

Usage:
    python query_analyzer.py queries.log
    python query_analyzer.py --stdin < queries.log
    cat queries.log | python query_analyzer.py --stdin
"""

import sys
import re
import argparse
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass
class Query:
    """Represents a parsed SQL query."""
    raw: str
    normalized: str
    query_type: str  # SELECT, INSERT, UPDATE, DELETE
    tables: list[str]
    has_where: bool
    has_limit: bool
    has_join: bool
    selects_all: bool
    param_count: int


@dataclass
class Issue:
    """Represents a detected issue."""
    severity: str  # HIGH, MEDIUM, LOW
    category: str
    message: str
    queries: list[str]
    suggestion: str


def normalize_query(sql: str) -> str:
    """
    Normalize a query for comparison (replace literals with placeholders).
    """
    # Remove ORM prefixes
    sql = re.sub(r'^Executing \([^)]+\):\s*', '', sql)
    sql = re.sub(r'^Query:\s*', '', sql)
    
    # Normalize whitespace
    sql = ' '.join(sql.split())
    
    # Replace string literals
    sql = re.sub(r"'(?:[^'\\]|\\.)*'", "'?'", sql)
    
    # Replace numeric literals
    sql = re.sub(r'\b\d+(?:\.\d+)?\b', '?', sql)
    
    # Replace IN lists
    sql = re.sub(r'IN\s*\([^)]+\)', 'IN (?)', sql, flags=re.IGNORECASE)
    
    # Replace parameter placeholders
    sql = re.sub(r'\$\d+', '?', sql)
    sql = re.sub(r':\w+', '?', sql)
    sql = re.sub(r'%\(\w+\)s', '?', sql)
    sql = re.sub(r'%s', '?', sql)
    
    return sql.upper()


def parse_query(sql: str) -> Query:
    """
    Parse a SQL query and extract metadata.
    """
    normalized = normalize_query(sql)
    upper_sql = sql.upper()
    
    # Determine query type
    if upper_sql.strip().startswith('SELECT'):
        query_type = 'SELECT'
    elif upper_sql.strip().startswith('INSERT'):
        query_type = 'INSERT'
    elif upper_sql.strip().startswith('UPDATE'):
        query_type = 'UPDATE'
    elif upper_sql.strip().startswith('DELETE'):
        query_type = 'DELETE'
    else:
        query_type = 'OTHER'
    
    # Extract table names (simplified)
    tables = []
    table_pattern = r'(?:FROM|JOIN|INTO|UPDATE)\s+["\']?(\w+)["\']?'
    tables = re.findall(table_pattern, upper_sql)
    tables = list(set(tables))
    
    # Check for various patterns
    has_where = 'WHERE' in upper_sql
    has_limit = 'LIMIT' in upper_sql
    has_join = 'JOIN' in upper_sql
    selects_all = bool(re.search(r'SELECT\s+\*', upper_sql))
    
    # Count parameters
    param_count = len(re.findall(r'\$\d+|\?|:\w+|%\(\w+\)s|%s', sql))
    
    return Query(
        raw=sql,
        normalized=normalized,
        query_type=query_type,
        tables=tables,
        has_where=has_where,
        has_limit=has_limit,
        has_join=has_join,
        selects_all=selects_all,
        param_count=param_count
    )


def detect_n_plus_one(queries: list[Query]) -> Optional[Issue]:
    """
    Detect N+1 query patterns.
    
    Pattern: One query followed by N similar queries on a related table.
    """
    # Group consecutive similar queries
    normalized_groups = defaultdict(list)
    
    for i, q in enumerate(queries):
        normalized_groups[q.normalized].append((i, q))
    
    issues = []
    for normalized, occurrences in normalized_groups.items():
        if len(occurrences) >= 3:
            # Check if they're roughly consecutive
            indices = [i for i, _ in occurrences]
            if max(indices) - min(indices) <= len(occurrences) * 2:
                sample_queries = [q.raw for _, q in occurrences[:3]]
                issues.append(Issue(
                    severity='HIGH',
                    category='N+1 Query',
                    message=f'Detected {len(occurrences)} similar queries executed in sequence',
                    queries=sample_queries,
                    suggestion='Use eager loading (include/preload/prefetch_related) to fetch related data in one query'
                ))
    
    return issues if issues else None


def detect_missing_where(queries: list[Query]) -> list[Issue]:
    """
    Detect SELECT queries without WHERE clause (potential full table scans).
    """
    issues = []
    
    for q in queries:
        if q.query_type == 'SELECT' and not q.has_where and not q.has_limit:
            issues.append(Issue(
                severity='MEDIUM',
                category='Missing WHERE',
                message='SELECT query without WHERE clause may cause full table scan',
                queries=[q.raw],
                suggestion='Add WHERE clause or LIMIT to prevent scanning entire table'
            ))
    
    return issues


def detect_select_star(queries: list[Query]) -> list[Issue]:
    """
    Detect SELECT * queries (over-fetching).
    """
    issues = []
    
    select_star_queries = [q for q in queries if q.selects_all and q.query_type == 'SELECT']
    
    if select_star_queries:
        issues.append(Issue(
            severity='LOW',
            category='SELECT *',
            message=f'Found {len(select_star_queries)} queries using SELECT *',
            queries=[q.raw for q in select_star_queries[:3]],
            suggestion='Select only needed columns to reduce data transfer and memory usage'
        ))
    
    return issues


def detect_duplicate_queries(queries: list[Query]) -> list[Issue]:
    """
    Detect identical queries executed multiple times.
    """
    issues = []
    
    query_counts = defaultdict(list)
    for q in queries:
        query_counts[q.raw].append(q)
    
    for raw_query, occurrences in query_counts.items():
        if len(occurrences) >= 3:
            issues.append(Issue(
                severity='MEDIUM',
                category='Duplicate Query',
                message=f'Identical query executed {len(occurrences)} times',
                queries=[raw_query],
                suggestion='Consider caching the result or restructuring code to avoid repeated queries'
            ))
    
    return issues


def detect_cartesian_join(queries: list[Query]) -> list[Issue]:
    """
    Detect potential Cartesian joins (multiple tables without proper JOIN/WHERE).
    """
    issues = []
    
    for q in queries:
        if q.query_type == 'SELECT' and len(q.tables) > 1:
            # Check for comma-separated tables without JOIN keyword
            if not q.has_join and ',' in q.raw.upper().split('FROM')[1].split('WHERE')[0] if 'FROM' in q.raw.upper() else False:
                issues.append(Issue(
                    severity='HIGH',
                    category='Cartesian Join',
                    message='Possible Cartesian join detected (comma-separated tables)',
                    queries=[q.raw],
                    suggestion='Use explicit JOIN with ON clause to specify relationship'
                ))
    
    return issues


def analyze_queries(queries: list[Query]) -> list[Issue]:
    """
    Run all analyzers and collect issues.
    """
    all_issues = []
    
    # N+1 detection
    n_plus_one = detect_n_plus_one(queries)
    if n_plus_one:
        all_issues.extend(n_plus_one)
    
    # Other detections
    all_issues.extend(detect_missing_where(queries))
    all_issues.extend(detect_select_star(queries))
    all_issues.extend(detect_duplicate_queries(queries))
    all_issues.extend(detect_cartesian_join(queries))
    
    return all_issues


def format_report(issues: list[Issue], queries: list[Query]) -> str:
    """
    Format analysis results as a readable report.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("QUERY ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append(f"\nTotal queries analyzed: {len(queries)}")
    lines.append(f"Issues found: {len(issues)}")
    
    # Summary by severity
    severity_counts = defaultdict(int)
    for issue in issues:
        severity_counts[issue.severity] += 1
    
    if severity_counts:
        lines.append("\nSeverity breakdown:")
        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            if severity_counts[severity]:
                lines.append(f"  {severity}: {severity_counts[severity]}")
    
    # Group by category
    by_category = defaultdict(list)
    for issue in issues:
        by_category[issue.category].append(issue)
    
    lines.append("\n" + "-" * 60)
    
    for category, cat_issues in by_category.items():
        lines.append(f"\n📌 {category} ({len(cat_issues)} issue(s))")
        lines.append("-" * 40)
        
        for issue in cat_issues[:5]:  # Limit to 5 per category
            lines.append(f"\n  Severity: {issue.severity}")
            lines.append(f"  {issue.message}")
            lines.append(f"\n  Example query:")
            for q in issue.queries[:1]:
                # Truncate long queries
                q_display = q[:200] + "..." if len(q) > 200 else q
                lines.append(f"    {q_display}")
            lines.append(f"\n  💡 Suggestion: {issue.suggestion}")
    
    if not issues:
        lines.append("\n✅ No issues detected!")
    
    lines.append("\n" + "=" * 60)
    
    return '\n'.join(lines)


def parse_log_file(content: str) -> list[str]:
    """
    Parse a log file and extract SQL queries.
    Handles various log formats.
    """
    queries = []
    
    # Try to match common patterns
    patterns = [
        # Sequelize: Executing (default): SELECT ...
        r'Executing \([^)]+\):\s*(.+?)(?=Executing|\Z)',
        # Prisma: Query: SELECT ...
        r'Query:\s*(.+?)(?=Query:|\Z)',
        # Generic SQL statements
        r'((?:SELECT|INSERT|UPDATE|DELETE|WITH)\s+.+?;)',
        # Line by line (fallback)
        r'^(.+?)$'
    ]
    
    for pattern in patterns[:3]:  # Skip line-by-line fallback first
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        if matches:
            queries = [m.strip() for m in matches if m.strip()]
            break
    
    # Fallback: treat each line as a potential query
    if not queries:
        for line in content.split('\n'):
            line = line.strip()
            if line and any(line.upper().startswith(kw) for kw in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WITH']):
                queries.append(line)
    
    return queries


def main():
    parser = argparse.ArgumentParser(
        description='Analyze SQL query logs for performance anti-patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s queries.log
    %(prog)s --stdin < queries.log
    %(prog)s --json queries.log > report.json
        """
    )
    parser.add_argument('logfile', nargs='?', help='Query log file to analyze')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--min-severity', choices=['LOW', 'MEDIUM', 'HIGH'], 
                        default='LOW', help='Minimum severity to report')
    
    args = parser.parse_args()
    
    # Read input with proper error handling
    try:
        if args.stdin or not args.logfile:
            if sys.stdin.isatty() and not args.logfile:
                parser.print_help()
                sys.exit(1)
            content = sys.stdin.read()
        else:
            with open(args.logfile, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.logfile}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied: {args.logfile}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse and analyze
    raw_queries = parse_log_file(content)
    if not raw_queries:
        print("No SQL queries found in input.")
        sys.exit(1)
    
    parsed_queries = [parse_query(q) for q in raw_queries]
    issues = analyze_queries(parsed_queries)
    
    # Filter by severity
    severity_order = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
    min_level = severity_order[args.min_severity]
    issues = [i for i in issues if severity_order[i.severity] >= min_level]
    
    # Output
    if args.json:
        import json
        output = {
            'total_queries': len(parsed_queries),
            'issues': [
                {
                    'severity': i.severity,
                    'category': i.category,
                    'message': i.message,
                    'queries': i.queries,
                    'suggestion': i.suggestion
                }
                for i in issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_report(issues, parsed_queries))


if __name__ == '__main__':
    main()

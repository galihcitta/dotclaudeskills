#!/usr/bin/env python3
"""
EXPLAIN Parser - Parse and analyze database EXPLAIN output.

Supports PostgreSQL, MySQL, and SQLite EXPLAIN formats.
Highlights performance issues and suggests optimizations.

Usage:
    python explain_parser.py --postgres < explain_output.txt
    python explain_parser.py --mysql explain_output.json
    psql -c "EXPLAIN ANALYZE SELECT ..." | python explain_parser.py --postgres
"""

import sys
import re
import json
import argparse
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExplainNode:
    """Represents a node in the query plan."""
    node_type: str
    relation: Optional[str]
    cost: Optional[float]
    rows: Optional[int]
    actual_time: Optional[float]
    actual_rows: Optional[int]
    loops: Optional[int]
    children: list
    raw: str
    warnings: list


@dataclass 
class ExplainIssue:
    """Represents a detected issue in the plan."""
    severity: str  # HIGH, MEDIUM, LOW
    node_type: str
    message: str
    suggestion: str


def parse_postgres_explain(text: str) -> tuple[list[ExplainNode], list[ExplainIssue]]:
    """
    Parse PostgreSQL EXPLAIN ANALYZE output.
    """
    nodes = []
    issues = []
    
    lines = text.strip().split('\n')
    
    for line in lines:
        # Skip planning/execution time lines
        if line.strip().startswith(('Planning', 'Execution', 'Total runtime')):
            continue
        
        # Parse node pattern
        # Example: "Seq Scan on users  (cost=0.00..431.00 rows=10000 width=244) (actual time=0.015..3.123 rows=10000 loops=1)"
        node_match = re.match(
            r'^[\s\->]*([\w\s]+?)(?:\s+on\s+([\w\.]+))?\s*'
            r'\(cost=([\d.]+)\.\.([\d.]+)\s+rows=(\d+)\s+width=(\d+)\)'
            r'(?:\s*\(actual time=([\d.]+)\.\.([\d.]+)\s+rows=(\d+)\s+loops=(\d+)\))?',
            line
        )
        
        if node_match:
            node_type = node_match.group(1).strip()
            relation = node_match.group(2)
            startup_cost = float(node_match.group(3))
            total_cost = float(node_match.group(4))
            estimated_rows = int(node_match.group(5))
            
            actual_time = None
            actual_rows = None
            loops = None
            
            if node_match.group(7):
                actual_time = float(node_match.group(8))
                actual_rows = int(node_match.group(9))
                loops = int(node_match.group(10))
            
            node = ExplainNode(
                node_type=node_type,
                relation=relation,
                cost=total_cost,
                rows=estimated_rows,
                actual_time=actual_time,
                actual_rows=actual_rows,
                loops=loops,
                children=[],
                raw=line,
                warnings=[]
            )
            nodes.append(node)
            
            # Detect issues
            if 'Seq Scan' in node_type:
                issues.append(ExplainIssue(
                    severity='MEDIUM',
                    node_type=node_type,
                    message=f'Sequential scan on {relation or "table"}',
                    suggestion='Consider adding an index on filtered/joined columns'
                ))
            
            if actual_rows is not None and estimated_rows > 0:
                ratio = actual_rows / estimated_rows
                if ratio > 10 or ratio < 0.1:
                    issues.append(ExplainIssue(
                        severity='MEDIUM',
                        node_type=node_type,
                        message=f'Row estimate mismatch: estimated {estimated_rows}, actual {actual_rows}',
                        suggestion='Run ANALYZE on the table to update statistics'
                    ))
            
            if 'Nested Loop' in node_type and loops and loops > 100:
                issues.append(ExplainIssue(
                    severity='HIGH',
                    node_type=node_type,
                    message=f'Nested loop with {loops} iterations',
                    suggestion='Consider using a hash or merge join, or add an index'
                ))
        
        # Check for other warning patterns
        if 'Sort Method: external' in line:
            issues.append(ExplainIssue(
                severity='HIGH',
                node_type='Sort',
                message='Sort spilling to disk',
                suggestion='Increase work_mem or optimize query to reduce sort size'
            ))
        
        if 'Buffers: shared read' in line:
            # High buffer reads might indicate cache misses
            buffer_match = re.search(r'shared read=(\d+)', line)
            if buffer_match and int(buffer_match.group(1)) > 10000:
                issues.append(ExplainIssue(
                    severity='LOW',
                    node_type='Buffer',
                    message=f'High buffer reads: {buffer_match.group(1)} pages',
                    suggestion='Query may benefit from caching or index optimization'
                ))
    
    return nodes, issues


def parse_mysql_explain(text: str) -> tuple[list[ExplainNode], list[ExplainIssue]]:
    """
    Parse MySQL EXPLAIN output (JSON or tabular format).
    """
    nodes = []
    issues = []
    
    # Try JSON format first
    try:
        data = json.loads(text)
        if 'query_block' in data:
            return parse_mysql_explain_json(data)
    except json.JSONDecodeError:
        pass
    
    # Parse tabular format
    lines = text.strip().split('\n')
    
    for line in lines:
        # Skip header lines
        if 'select_type' in line.lower() or line.startswith('+'):
            continue
        
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) >= 10:
            # id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows, filtered, Extra
            table = parts[2] if len(parts) > 2 else None
            access_type = parts[4] if len(parts) > 4 else None
            key = parts[6] if len(parts) > 6 else None
            rows = int(parts[9]) if len(parts) > 9 and parts[9].isdigit() else None
            extra = parts[11] if len(parts) > 11 else ''
            
            node = ExplainNode(
                node_type=access_type or 'UNKNOWN',
                relation=table,
                cost=None,
                rows=rows,
                actual_time=None,
                actual_rows=None,
                loops=None,
                children=[],
                raw=line,
                warnings=[]
            )
            nodes.append(node)
            
            # Detect issues
            if access_type == 'ALL':
                issues.append(ExplainIssue(
                    severity='HIGH',
                    node_type='Full Table Scan',
                    message=f'Full table scan on {table}',
                    suggestion='Add an index on columns used in WHERE/JOIN'
                ))
            
            if access_type == 'index':
                issues.append(ExplainIssue(
                    severity='MEDIUM',
                    node_type='Full Index Scan',
                    message=f'Full index scan on {table}',
                    suggestion='Query may not be using index efficiently'
                ))
            
            if 'Using filesort' in extra:
                issues.append(ExplainIssue(
                    severity='MEDIUM',
                    node_type='Filesort',
                    message='Using filesort for ORDER BY',
                    suggestion='Add index that matches ORDER BY columns'
                ))
            
            if 'Using temporary' in extra:
                issues.append(ExplainIssue(
                    severity='MEDIUM',
                    node_type='Temporary Table',
                    message='Creating temporary table',
                    suggestion='Optimize query to avoid temporary tables'
                ))
    
    return nodes, issues


def parse_mysql_explain_json(data: dict) -> tuple[list[ExplainNode], list[ExplainIssue]]:
    """Parse MySQL EXPLAIN FORMAT=JSON output."""
    nodes = []
    issues = []
    
    def process_block(block, depth=0):
        if 'table' in block:
            table = block['table']
            node = ExplainNode(
                node_type=table.get('access_type', 'UNKNOWN'),
                relation=table.get('table_name'),
                cost=table.get('cost_info', {}).get('read_cost'),
                rows=table.get('rows_examined_per_scan'),
                actual_time=None,
                actual_rows=None,
                loops=None,
                children=[],
                raw=json.dumps(table, indent=2),
                warnings=[]
            )
            nodes.append(node)
            
            if table.get('access_type') == 'ALL':
                issues.append(ExplainIssue(
                    severity='HIGH',
                    node_type='Full Table Scan',
                    message=f"Full table scan on {table.get('table_name')}",
                    suggestion='Add an index on columns used in WHERE/JOIN'
                ))
        
        # Process nested blocks
        for key in ['nested_loop', 'query_block', 'ordering_operation', 'grouping_operation']:
            if key in block:
                items = block[key] if isinstance(block[key], list) else [block[key]]
                for item in items:
                    if isinstance(item, dict):
                        process_block(item, depth + 1)
    
    process_block(data.get('query_block', data))
    return nodes, issues


def format_report(nodes: list[ExplainNode], issues: list[ExplainIssue]) -> str:
    """Format analysis results as a readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("EXPLAIN ANALYSIS REPORT")
    lines.append("=" * 60)
    
    # Summary
    lines.append(f"\nNodes analyzed: {len(nodes)}")
    lines.append(f"Issues found: {len(issues)}")
    
    # Node summary
    if nodes:
        lines.append("\n📊 Query Plan Nodes:")
        lines.append("-" * 40)
        for i, node in enumerate(nodes, 1):
            info = f"{i}. {node.node_type}"
            if node.relation:
                info += f" on {node.relation}"
            if node.rows:
                info += f" (rows: {node.rows})"
            if node.actual_time:
                info += f" [{node.actual_time:.3f}ms]"
            lines.append(info)
    
    # Issues
    if issues:
        lines.append("\n⚠️  Issues Detected:")
        lines.append("-" * 40)
        
        for issue in sorted(issues, key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x.severity]):
            emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}[issue.severity]
            lines.append(f"\n{emoji} [{issue.severity}] {issue.node_type}")
            lines.append(f"   {issue.message}")
            lines.append(f"   💡 {issue.suggestion}")
    else:
        lines.append("\n✅ No significant issues detected!")
    
    lines.append("\n" + "=" * 60)
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Parse and analyze database EXPLAIN output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    psql -c "EXPLAIN ANALYZE SELECT * FROM users" | %(prog)s --postgres
    mysql -e "EXPLAIN FORMAT=JSON SELECT ..." | %(prog)s --mysql
    %(prog)s --postgres explain_output.txt
        """
    )
    parser.add_argument('file', nargs='?', help='EXPLAIN output file')
    parser.add_argument('--postgres', '-p', action='store_true', help='Parse PostgreSQL format')
    parser.add_argument('--mysql', '-m', action='store_true', help='Parse MySQL format')
    parser.add_argument('--sqlite', '-s', action='store_true', help='Parse SQLite format')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Require database type
    if not any([args.postgres, args.mysql, args.sqlite]):
        args.postgres = True  # Default to PostgreSQL
    
    # Read input with error handling
    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        else:
            if sys.stdin.isatty():
                parser.print_help()
                sys.exit(1)
            content = sys.stdin.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied: {args.file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not content or not content.strip():
        print("Error: No EXPLAIN output provided", file=sys.stderr)
        sys.exit(1)
    
    # Parse based on database type
    if args.postgres:
        nodes, issues = parse_postgres_explain(content)
    elif args.mysql:
        nodes, issues = parse_mysql_explain(content)
    else:
        print("SQLite parsing not yet implemented")
        sys.exit(1)
    
    # Output
    if args.json:
        output = {
            'nodes': [
                {
                    'type': n.node_type,
                    'relation': n.relation,
                    'cost': n.cost,
                    'rows': n.rows,
                    'actual_time': n.actual_time,
                    'actual_rows': n.actual_rows
                }
                for n in nodes
            ],
            'issues': [
                {
                    'severity': i.severity,
                    'type': i.node_type,
                    'message': i.message,
                    'suggestion': i.suggestion
                }
                for i in issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_report(nodes, issues))


if __name__ == '__main__':
    main()

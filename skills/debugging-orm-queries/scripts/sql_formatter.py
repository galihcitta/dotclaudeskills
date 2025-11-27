#!/usr/bin/env python3
"""
SQL Formatter - Pretty-print SQL queries for easier debugging.
Works with queries captured from any ORM.

Usage:
    python sql_formatter.py "SELECT * FROM users WHERE id = 1"
    echo "SELECT ..." | python sql_formatter.py
    python sql_formatter.py --file query.sql
"""

import sys
import re
import argparse
from typing import Optional


KEYWORDS = [
    'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN',
    'INNER JOIN', 'OUTER JOIN', 'FULL JOIN', 'CROSS JOIN', 'ON', 'GROUP BY',
    'HAVING', 'ORDER BY', 'LIMIT', 'OFFSET', 'INSERT INTO', 'VALUES', 'UPDATE',
    'SET', 'DELETE FROM', 'CREATE TABLE', 'ALTER TABLE', 'DROP TABLE', 'AS',
    'DISTINCT', 'UNION', 'UNION ALL', 'EXCEPT', 'INTERSECT', 'CASE', 'WHEN',
    'THEN', 'ELSE', 'END', 'IN', 'NOT IN', 'EXISTS', 'NOT EXISTS', 'BETWEEN',
    'LIKE', 'IS NULL', 'IS NOT NULL', 'ASC', 'DESC', 'NULLS FIRST', 'NULLS LAST',
    'WITH', 'RECURSIVE', 'RETURNING', 'CONFLICT', 'DO UPDATE', 'DO NOTHING'
]

NEWLINE_BEFORE = [
    'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'LEFT JOIN', 'RIGHT JOIN',
    'INNER JOIN', 'OUTER JOIN', 'FULL JOIN', 'CROSS JOIN', 'JOIN',
    'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT', 'OFFSET', 'SET', 'VALUES', 
    'UNION', 'UNION ALL', 'EXCEPT', 'INTERSECT', 'RETURNING', 'WITH'
]

INDENT_KEYWORDS = ['AND', 'OR', 'ON']


def format_sql(sql: str, indent: int = 2, uppercase: bool = True) -> str:
    """
    Format SQL query with proper indentation and line breaks.
    
    Args:
        sql: Raw SQL query string
        indent: Number of spaces for indentation
        uppercase: Whether to uppercase keywords
    
    Returns:
        Formatted SQL string
    """
    # Normalize whitespace
    sql = ' '.join(sql.split())
    
    # Remove ORM prefixes (e.g., "Executing (default): " from Sequelize)
    sql = re.sub(r'^Executing \([^)]+\):\s*', '', sql)
    sql = re.sub(r'^Query:\s*', '', sql)
    
    # Protect multi-word keywords by replacing spaces with placeholders
    multi_word_keywords = [
        'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN', 
        'FULL JOIN', 'CROSS JOIN', 'LEFT OUTER JOIN', 'RIGHT OUTER JOIN',
        'GROUP BY', 'ORDER BY', 'UNION ALL', 'IS NULL', 'IS NOT NULL',
        'NOT IN', 'NOT EXISTS', 'INSERT INTO', 'DELETE FROM', 'CREATE TABLE',
        'ALTER TABLE', 'DROP TABLE', 'NULLS FIRST', 'NULLS LAST',
        'DO UPDATE', 'DO NOTHING'
    ]
    
    placeholders = {}
    for i, kw in enumerate(multi_word_keywords):
        placeholder = f"__KW{i}__"
        placeholders[placeholder] = kw.upper()
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        sql = pattern.sub(placeholder, sql)
    
    # Uppercase single-word keywords
    if uppercase:
        single_keywords = [kw for kw in KEYWORDS if ' ' not in kw]
        for kw in single_keywords:
            pattern = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)
            sql = pattern.sub(kw, sql)
    
    # Restore multi-word keywords (now uppercased)
    for placeholder, kw in placeholders.items():
        sql = sql.replace(placeholder, kw)
    
    # Define where to add newlines
    newline_keywords = [
        'LEFT OUTER JOIN', 'RIGHT OUTER JOIN',
        'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN', 
        'FULL JOIN', 'CROSS JOIN',
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR',
        'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT', 'OFFSET', 
        'SET', 'VALUES', 'UNION ALL', 'UNION', 'EXCEPT', 
        'INTERSECT', 'RETURNING', 'WITH'
    ]
    
    # Add newlines before keywords (process longer ones first)
    for kw in sorted(newline_keywords, key=len, reverse=True):
        # Don't add newline if already at start of line
        pattern = re.compile(r'(?<!\n)\s+(' + re.escape(kw) + r')\b', re.IGNORECASE)
        sql = pattern.sub(r'\n\1', sql)
    
    # Indent continuation keywords
    lines = sql.split('\n')
    formatted_lines = []
    indent_str = ' ' * indent
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line starts with indent keyword
        first_word = line.split()[0] if line.split() else ''
        if first_word.upper() in INDENT_KEYWORDS:
            formatted_lines.append(indent_str + line)
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)


def extract_params(sql: str) -> tuple[str, list[str]]:
    """
    Extract parameter placeholders and their positions.
    
    Returns:
        Tuple of (sql_with_numbered_params, list_of_original_placeholders)
    """
    # Match various placeholder styles: $1, ?, :name, %(name)s
    placeholders = re.findall(r'\$\d+|\?|:\w+|%\(\w+\)s|%s', sql)
    return sql, placeholders


def highlight_sql(sql: str) -> str:
    """
    Add ANSI color codes for terminal output.
    """
    colors = {
        'keyword': '\033[94m',   # Blue
        'string': '\033[92m',    # Green
        'number': '\033[93m',    # Yellow
        'reset': '\033[0m'
    }
    
    # Highlight keywords
    for kw in KEYWORDS:
        pattern = re.compile(r'\b(' + kw.replace(' ', r'\s+') + r')\b', re.IGNORECASE)
        sql = pattern.sub(colors['keyword'] + r'\1' + colors['reset'], sql)
    
    # Highlight strings
    sql = re.sub(r"('(?:[^'\\]|\\.)*')", colors['string'] + r'\1' + colors['reset'], sql)
    
    # Highlight numbers
    sql = re.sub(r'\b(\d+(?:\.\d+)?)\b', colors['number'] + r'\1' + colors['reset'], sql)
    
    return sql


def main():
    parser = argparse.ArgumentParser(
        description='Format SQL queries for easier debugging',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s "SELECT * FROM users WHERE id = 1"
    %(prog)s --file query.sql
    %(prog)s --no-color "SELECT * FROM users"
    echo "SELECT * FROM users" | %(prog)s
        """
    )
    parser.add_argument('sql', nargs='?', help='SQL query to format')
    parser.add_argument('--file', '-f', help='Read SQL from file')
    parser.add_argument('--indent', '-i', type=int, default=2, help='Indentation spaces (default: 2)')
    parser.add_argument('--no-color', action='store_true', help='Disable color output')
    parser.add_argument('--lowercase', '-l', action='store_true', help='Keep keywords lowercase')
    parser.add_argument('--params', '-p', action='store_true', help='Show parameter positions')
    
    args = parser.parse_args()
    
    # Get SQL from various sources with error handling
    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8', errors='replace') as f:
                sql = f.read()
        elif args.sql:
            sql = args.sql
        elif not sys.stdin.isatty():
            sql = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied: {args.file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not sql or not sql.strip():
        print("Error: No SQL provided", file=sys.stderr)
        sys.exit(1)
    
    # Format the SQL
    formatted = format_sql(sql, indent=args.indent, uppercase=not args.lowercase)
    
    # Show parameter info if requested
    if args.params:
        _, placeholders = extract_params(formatted)
        if placeholders:
            print("Parameters:", placeholders)
            print("-" * 40)
    
    # Add colors if terminal supports it and not disabled
    if not args.no_color and sys.stdout.isatty():
        formatted = highlight_sql(formatted)
    
    print(formatted)


if __name__ == '__main__':
    main()

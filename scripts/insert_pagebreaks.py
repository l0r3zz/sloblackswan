#!/usr/bin/env python3
"""
Markdown Pagebreak Inserter
Inserts '{::pagebreak /}' before ## headers, excluding those inside code blocks.
"""
import argparse
import sys
from pathlib import Path

def insert_pagebreaks(content: str) -> str:
    lines = content.splitlines(keepends=True)
    result = []
    in_code_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        if not in_code_block and line.strip().startswith('##') and not line.strip().startswith('###'):
            if result and result[-1].strip() == '{::pagebreak /}':
                result.append(line)
            else:
                result.append('{::pagebreak /}\n')
                result.append(line)
        else:
            result.append(line)
    return ''.join(result)

def process_file(input_path: Path, output_path: Path = None, overwrite: bool = False) -> None:
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {input_path}: {e}", file=sys.stderr)
        sys.exit(1)
    modified_content = insert_pagebreaks(content)
    out_path = input_path if overwrite else (output_path or input_path.parent / f"{input_path.stem}_processed{input_path.suffix}")
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Successfully processed: {input_path}")
    except Exception as e:
        print(f"Error writing to {out_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=Path)
    parser.add_argument('-o', '--output', type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    process_file(args.input_file, args.output, args.overwrite)

if __name__ == '__main__':
    main()

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
    
    # Detect line ending style from the original content
    # Check the first line that has a line ending, or default to \n
    line_ending = '\n'
    for line in lines:
        if line.endswith('\r\n'):
            line_ending = '\r\n'
            break
        elif line.endswith('\r'):
            line_ending = '\r'
            break
        elif line.endswith('\n'):
            line_ending = '\n'
            break
    
    for i, line in enumerate(lines):
        # Check if line starts with ``` at column 0 (not indented)
        if line.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        # Check if line starts with exactly ## (level-2 header) at column 0
        # Must start with ## followed by a space or end of line (not ### or deeper)
        if not in_code_block and line.startswith('##') and (len(line) < 3 or line[2] != '#'):
            # Look back through blank lines to find the last non-blank line
            has_existing_pagebreak = False
            has_prior_content = False
            for j in range(len(result) - 1, -1, -1):
                last_line = result[j].strip()
                if last_line == '{::pagebreak /}':
                    has_existing_pagebreak = True
                    break
                elif last_line:  # Non-blank line that's not a pagebreak
                    has_prior_content = True
                    break
            
            # Skip pagebreak if this is the first header (no prior content)
            if has_existing_pagebreak:
                result.append(line)
            elif has_prior_content:
                # Insert pagebreak only if there's prior non-blank content
                result.append(f'{{::pagebreak /}}{line_ending}')
                result.append(line)
            else:
                # First header in document - no pagebreak needed
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

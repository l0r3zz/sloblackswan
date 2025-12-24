#!/usr/bin/env python3
"""
Markdown Pagebreak Inserter

Inserts '{::pagebreak /}' before ## headers, excluding those inside code blocks.
Code blocks are delimited by triple backticks (```).

Author: Geoff White
"""

import argparse
import sys
from pathlib import Path


def insert_pagebreaks(content: str) -> str:
    """
    Insert pagebreaks before ## headers, but not inside code blocks.

    Args:
        content: The markdown file content as a string

    Returns:
        Modified content with pagebreaks inserted
    """
    lines = content.splitlines(keepends=True)
    result = []
    in_code_block = False

    for i, line in enumerate(lines):
        # Check if this line toggles code block state
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        # Check if this is a ## header outside of a code block
        if not in_code_block and line.strip().startswith('##') and not line.strip().startswith('###'):
            # Check if previous line is already a pagebreak to avoid duplicates
            if result and result[-1].strip() == '{::pagebreak /}':
                result.append(line)
            else:
                # Insert pagebreak before the header
                result.append('{::pagebreak /}\n')
                result.append(line)
        else:
            result.append(line)

    return ''.join(result)


def process_file(input_path: Path, output_path: Path = None, overwrite: bool = False) -> None:
    """
    Process a markdown file to insert pagebreaks.

    Args:
        input_path: Path to input markdown file
        output_path: Path to output file (optional)
        overwrite: If True, overwrite the original file
    """
    # Read the input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Process the content
    modified_content = insert_pagebreaks(content)

    # Determine output path
    if overwrite:
        out_path = input_path
    elif output_path:
        out_path = output_path
    else:
        # Default: add _processed before the extension
        out_path = input_path.parent / f"{input_path.stem}_processed{input_path.suffix}"

    # Write the output file
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Successfully processed: {input_path}")
        print(f"Output written to: {out_path}")
    except Exception as e:
        print(f"Error writing to {out_path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Insert pagebreaks before ## headers in markdown files, excluding code blocks.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.md                    # Creates input_processed.md
  %(prog)s input.md -o output.md       # Creates output.md
  %(prog)s input.md --overwrite        # Overwrites input.md
        """
    )

    parser.add_argument('input_file', type=Path, help='Input markdown file')
    parser.add_argument('-o', '--output', type=Path, help='Output file path (default: input_processed.md)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite the input file')

    args = parser.parse_args()

    # Validate input file exists
    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Check for conflicting arguments
    if args.overwrite and args.output:
        print("Error: Cannot use both --overwrite and --output", file=sys.stderr)
        sys.exit(1)

    # Process the file
    process_file(args.input_file, args.output, args.overwrite)


if __name__ == '__main__':
    main()


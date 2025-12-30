# make sure you export MD_PATH, PDF_PATH, OUTPUT_DIR 
python scripts/build_book.py -s content -d SLOBLACKSWAN -v "v0.xx" -m MANIFEST.md
python scripts/insert_pagebreaks.py --overwrite $MD_PATH
doctoc ${MD_PATH} --title "## Table of Contents" --maxlevel 2 --maxlevel 2
python scripts/generate_pdf.py "$MD_PATH" "$PDF_PATH" "$OUTPUT_DIR"
python scripts/cleanup_markdown.py $MD_PATH

"""
Utility functions for text processing and file operations.
"""

import re
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

import os

# Default directory for Markdown files
DEFAULT_MD_DIR = Path(r"C:\Users\LangZheZR\Documents\road\FLOW")

# Path to the diary folder
DIARY_DIR = DEFAULT_MD_DIR / "diary"
def get_recent_diaries(n: int = 7):
    """Return a list of paths to the most recent n diary markdown files."""
    diary_files = sorted(
        [f for f in DIARY_DIR.glob("*.md") if re.match(r"\d{4}-\d{2}-\d{2}\.md", f.name)],
        key=lambda f: f.stem,
        reverse=True
    )
    return diary_files[:n]


def read_diary_content(n: int = 7):
    """Read the content of the most recent n diary files."""
    recent_files = get_recent_diaries(n)
    return {f.name: f.read_text(encoding="utf-8") for f in recent_files}


def update_today_diary(llm_text: str, section_title: str = "LLM Update"):
    """Append a new LLM-written block with timestamp to today's diary."""
    today_name = datetime.now().strftime("%Y-%m-%d") + ".md"
    today_file = DIARY_DIR / today_name

    if not today_file.exists():
        today_file.write_text(f"# {today_name}\n\n", encoding="utf-8")

    # Format header with time
    current_time = datetime.now().strftime("%H:%M")
    section_header = f"### {section_title} — {current_time}"

    # Compose new entry block
    new_block = (
        f"\n{section_header}\n"
        f"{llm_text.strip()}\n"
    )

    # Append to end of file
    with today_file.open("a", encoding="utf-8") as f:
        f.write(new_block)

if __name__ =="__main__":
    print(read_diary_content())
    update_today_diary("test text")

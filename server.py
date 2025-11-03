#!/usr/bin/env python3
"""
Knowledge Management MCP Server

This server provides tools for managing Markdown files and their summaries.
"""

from pathlib import Path
from typing import Optional
import re
from pathlib import Path
from typing import Optional
import json
import datetime
import os

from utils import *
from mcp.server.fastmcp import FastMCP



# Create the MCP server
mcp = FastMCP("Knowledge Management Server")

from datetime import datetime
import traceback

@mcp.tool()
def load_recent_diaries(n: int = 7):
    """Load content of the recent n diaries to understand the user's context."""
    try:
        diaries = read_diary_content(n)
        return {"status": "success", "count": len(diaries), "diaries": diaries}
    except FileNotFoundError as e:
        return {"status": "error", "message": f"Diary folder not found: {DIARY_DIR}", "error": str(e)}
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to load recent diaries.",
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


@mcp.tool()
def update_note(llm_input: str, section: str = "LLM Update"):
    """
    Use this function to update user's knowledge base.
    llm_input usually means the concise content user wants to record.
    section should be the descriptive llm_input content title.
    """
    try:
        update_today_diary(llm_input, "AI-update " + section)
        today_file = datetime.now().strftime("%Y-%m-%d") + ".md"
        return {"status": "success", "file": today_file}
    except FileNotFoundError as e:
        return {"status": "error", "message": f"Diary directory not found: {DIARY_DIR}", "error": str(e)}
    except PermissionError as e:
        return {"status": "error", "message": "Permission denied when writing to diary file.", "error": str(e)}
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to update today's diary.",
            "error": str(e),
            "traceback": traceback.format_exc(),
        }

# @mcp.tool()
# def list_md_summaries() -> str:
#     """
#     List all Markdown files with their summaries from the knowledge base.
#     Returns a formatted string with filenames and summaries.
#     """
#     return list_md_files()



# @mcp.tool()
# def read_md_file(file_name: str) -> str:
#     """
#     Read the full content of a specific Markdown file.
#     Automatically adds .md extension if not present.
#     """
#     return get_md_contents([file_name])


# @mcp.tool()
# def append_to_md_file(file_name: str, tag: str, content: str, version: str = "1.0") -> str:
#     """
#     Append formatted content to a Markdown file.
#     Includes timestamp, tag, and version information.
#     Keep content concise unless specifically instructed to be detailed or exact.
#     """
#     try:
#         append_to_md(file_name, tag, content, version)
#         log_change(change_type="append_md", file_involved=file_name, content=content)
#         return f"Successfully appended to {file_name}"
#     except ValueError as e:
#         return str(e)


# @mcp.tool()
# def update_md_summary(file_name: str, summary: str) -> str:
#     """
#     Update the summary for a specific Markdown file.
#     Keep summary concise unless specifically instructed to be detailed or exact.
#     """
#     try:
#         update_md_summaries(custom_summaries={file_name: summary})
#         log_change(change_type="update_summary", file_involved=file_name, content=summary)
#         return f"Successfully updated summary for {file_name}"
#     except Exception as e:
#         return f"Error updating summary: {str(e)}"


# @mcp.resource("md://{file_name}")
# def get_md_resource(file_name: str) -> str:
#     """
#     Resource to retrieve the content of a specific Markdown file.
#     """
#     return get_md_contents([file_name])


# # =========================
# # Instruction tools (minimal)
# # =========================

# @mcp.tool()
# def init_llm_instructions() -> str:
#     """
#     run this tool first before other tools to get understanding of following instructions 
#     Return the latest (bottom-most non-empty) '## instructions' section body.
#     """
#     return load_latest_instructions()


# @mcp.tool()
# def add_instruction_version(body: str, header_suffix: Optional[str] = None) -> str:
#     """
#     usually don't necessary, most time only need append new instruction with append_to_md_file
#     only use when specific instruct to update version of instructions
#     Append a new instructions version to the instruction markdown.
#     header_suffix optional (e.g., 'v1.0.1 - 2025-09-29'); defaults to today's date.
#     """
#     try:
#         append_instruction_version(body=body, header_suffix=header_suffix)
#         log_change(
#             change_type="append_instruction_version",
#             file_involved="knowledge management mcp instruction for llm .md",
#             content=(header_suffix or "date_default"),
#         )
#         return "Appended new instruction version."
#     except Exception as e:
#         return f"Error appending instruction version: {str(e)}"


if __name__ == "__main__":
    mcp.run()
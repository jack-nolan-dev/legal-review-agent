#!/usr/bin/env python3
"""MCP server that exposes the Legal Review Agent as a tool for Claude Desktop / Claude Code.

Usage:
    python mcp_server.py

In MCP mode, the tool doesn't call the Anthropic API itself. Instead, it returns
the legal knowledge base and analysis instructions as context — the Claude session
that called the tool does the reasoning. This means users don't need a separate
API key or credits; it works with their existing Claude Desktop or Claude Code subscription.
"""

from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from agent.prompt import build_system_prompt

MAX_QUESTION_LENGTH = 5000

mcp = MCPServer(
    "legal-review-agent",
    description="AI-powered legal risk classifier for small business decisions",
)


@mcp.tool()
def legal_review(
    question: str,
    state: str | None = None,
    business_type: str | None = None,
) -> str:
    """Evaluate a business decision for legal risk.

    Call this tool when a user asks whether a business action is legal, wants to
    know the legal risk of a decision, or needs to understand compliance requirements.

    The tool returns a legal analysis framework with a knowledge base. Use it to
    produce a structured GREEN/YELLOW/RED verdict with statute citations, compliant
    alternatives, and whether the user needs a real attorney.

    Args:
        question: A plain-English description of the business decision being considered.
                  Example: "Can I scrape Google reviews and put them on my client's website?"
        state: Optional US state abbreviation for state-specific analysis (e.g., "MA", "CA", "NY").
               When provided, the analysis prioritizes that state's laws alongside federal law.
        business_type: Optional business type for industry-specific context (e.g., "restaurant",
                       "web agency", "healthcare startup").
    """
    if len(question) > MAX_QUESTION_LENGTH:
        return f"Error: Question too long ({len(question)} chars). Maximum is {MAX_QUESTION_LENGTH}."

    system_prompt = build_system_prompt(state=state, business_type=business_type)

    return f"""LEGAL REVIEW REQUEST
====================

USER'S QUESTION: {question}

INSTRUCTIONS: Use the legal analysis framework and knowledge base below to answer
the user's question. Follow the response structure EXACTLY as specified — verdict,
why, compliant alternative, professional needed, sources.

{system_prompt}"""


if __name__ == "__main__":
    mcp.run()

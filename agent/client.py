"""Anthropic SDK wrapper for the legal review agent."""

from __future__ import annotations

import anthropic
from .prompt import build_system_prompt

MAX_QUESTION_LENGTH = 5000

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    """Return a reusable Anthropic client instance."""
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def query(
    question: str,
    state: str | None = None,
    business_type: str | None = None,
    model: str = "claude-sonnet-4-6",
) -> str:
    """Send a legal question to Claude and return the raw response text.

    Args:
        question: The user's plain-English business decision question.
        state: Optional US state for state-specific analysis.
        business_type: Optional business type for industry context.
        model: Claude model ID. Defaults to claude-sonnet-4-6.

    Returns:
        The full text response from Claude.

    Raises:
        ValueError: If the question exceeds MAX_QUESTION_LENGTH.
    """
    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError(f"Question too long ({len(question)} chars). Max is {MAX_QUESTION_LENGTH}.")

    client = _get_client()
    system_prompt = build_system_prompt(state=state, business_type=business_type)

    message = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {"role": "user", "content": question}
        ],
    )

    return message.content[0].text

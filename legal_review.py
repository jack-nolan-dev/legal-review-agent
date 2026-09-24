#!/usr/bin/env python3
"""Legal Review Agent — AI-powered legal risk classifier for small businesses.

Sends a plain-English business decision to Claude and returns a structured
GREEN/YELLOW/RED risk verdict with statute citations and compliant alternatives.

Usage:
    python legal_review.py "Can I record sales calls in Massachusetts?"
    python legal_review.py --state MA --business-type "web agency" "Can I scrape Google reviews?"
    python legal_review.py --interactive
"""

import json
import sys

import click
from dotenv import load_dotenv

from agent.client import query
from agent.formatter import format_json, format_response
from agent.prompt import build_system_prompt

load_dotenv()


@click.command()
@click.argument("question", required=False)
@click.option("--state", "-s", default=None, help="US state for state-specific analysis (e.g., MA, CA, NY)")
@click.option("--business-type", "-b", default=None, help='Business type for industry context (e.g., "restaurant", "web agency")')
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode — ask multiple questions in a REPL")
@click.option("--raw", "-r", is_flag=True, help="Output raw JSON instead of formatted text")
@click.option("--verbose", "-v", is_flag=True, help="Show the full system prompt sent to Claude")
@click.option("--model", "-m", default="claude-sonnet-4-6", help="Claude model ID (default: claude-sonnet-4-6)")
@click.option("--no-color", is_flag=True, help="Disable color output")
def main(question, state, business_type, interactive, raw, verbose, model, no_color):
    """Evaluate a business decision for legal risk.

    Pass a QUESTION as an argument, or use --interactive for a REPL.

    \b
    Examples:
        python legal_review.py "Can I scrape Google reviews for my client's site?"
        python legal_review.py --state MA "Can I record sales calls?"
        python legal_review.py --interactive --state CA --business-type "restaurant"
    """
    if verbose:
        prompt = build_system_prompt(state=state, business_type=business_type)
        click.echo(click.style("--- SYSTEM PROMPT ---", fg="cyan", bold=True))
        click.echo(prompt)
        click.echo(click.style("--- END SYSTEM PROMPT ---\n", fg="cyan", bold=True))

    if interactive:
        _run_interactive(state, business_type, raw, model, no_color)
    elif question:
        _run_single(question, state, business_type, raw, model, no_color)
    else:
        click.echo("Error: Provide a QUESTION argument or use --interactive mode.", err=True)
        click.echo("Run `python legal_review.py --help` for usage.", err=True)
        sys.exit(1)


def _run_single(question, state, business_type, raw, model, no_color):
    """Run a single question and print the result."""
    try:
        response = query(question, state=state, business_type=business_type, model=model)
    except Exception as e:
        _handle_error(e)
        return

    if raw:
        result = format_json(response)
        click.echo(json.dumps(result, indent=2))
    else:
        formatted = format_response(response, use_color=not no_color)
        click.echo()
        click.echo(formatted)
        click.echo()


def _run_interactive(state, business_type, raw, model, no_color):
    """Run an interactive REPL loop."""
    click.echo(click.style("\nLegal Review Agent — Interactive Mode", bold=True))
    click.echo("Type a business decision question and press Enter.")
    click.echo("Type 'quit' or 'exit' to leave.\n")

    if state:
        click.echo(f"  State: {state}")
    if business_type:
        click.echo(f"  Business type: {business_type}")
    click.echo()

    while True:
        try:
            question = click.prompt(click.style("Question", fg="cyan"), prompt_suffix=" > ")
        except (EOFError, KeyboardInterrupt):
            click.echo("\nGoodbye.")
            break

        if question.strip().lower() in ("quit", "exit", "q"):
            click.echo("Goodbye.")
            break

        if not question.strip():
            continue

        click.echo(click.style("\nAnalyzing...\n", dim=True))

        try:
            response = query(question, state=state, business_type=business_type, model=model)
        except Exception as e:
            _handle_error(e)
            continue

        if raw:
            result = format_json(response)
            click.echo(json.dumps(result, indent=2))
        else:
            formatted = format_response(response, use_color=not no_color)
            click.echo(formatted)

        click.echo("\n" + "─" * 60 + "\n")


def _handle_error(e):
    """Print a user-friendly error message."""
    error_str = str(e)
    if "api_key" in error_str.lower() or "authentication" in error_str.lower():
        click.echo(click.style(
            "Error: ANTHROPIC_API_KEY not set or invalid.\n"
            "Set it in your environment or in a .env file:\n"
            "  export ANTHROPIC_API_KEY=your-key-here",
            fg="red",
        ), err=True)
    else:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)


if __name__ == "__main__":
    main()

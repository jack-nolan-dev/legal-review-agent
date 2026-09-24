"""Parse and format the agent's response for terminal output."""


# ANSI color codes for terminal output
COLORS = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "reset": "\033[0m",
}


def _detect_verdict(text: str) -> str:
    """Detect the verdict level from the response text."""
    text_upper = text.upper()
    if "RED" in text_upper and "\U0001f534" in text:
        return "red"
    if "YELLOW" in text_upper and "\U0001f7e1" in text:
        return "yellow"
    if "GREEN" in text_upper and "\U0001f7e2" in text:
        return "green"
    # Fallback: check without emoji
    for line in text.split("\n"):
        line_upper = line.upper()
        if "RED" in line_upper and ("VERDICT" in line_upper or "DO NOT" in line_upper):
            return "red"
        if "YELLOW" in line_upper and ("VERDICT" in line_upper or "PROCEED" in line_upper):
            return "yellow"
        if "GREEN" in line_upper and ("VERDICT" in line_upper or "SAFE" in line_upper):
            return "green"
    return "unknown"


def format_response(text: str, use_color: bool = True) -> str:
    """Format the agent's response for terminal display.

    Adds color coding based on the verdict and cleans up formatting.

    Args:
        text: Raw response text from Claude.
        use_color: Whether to apply ANSI color codes.

    Returns:
        Formatted string ready for terminal output.
    """
    if not use_color:
        return text

    verdict = _detect_verdict(text)
    color = COLORS.get(verdict, "")
    reset = COLORS["reset"]
    bold = COLORS["bold"]
    dim = COLORS["dim"]

    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        # Color the verdict line
        if any(v in line.upper() for v in ["GREEN", "YELLOW", "RED"]) and any(
            e in line for e in ["\U0001f7e2", "\U0001f7e1", "\U0001f534"]
        ):
            formatted_lines.append(f"{bold}{color}{line}{reset}")
        # Bold section headers
        elif line.strip().startswith("**") and line.strip().endswith("**"):
            formatted_lines.append(f"{bold}{line}{reset}")
        elif line.strip().startswith("WHY:") or line.strip().startswith("**WHY"):
            formatted_lines.append(f"{bold}{line}{reset}")
        elif line.strip().startswith("COMPLIANT") or line.strip().startswith("**COMPLIANT"):
            formatted_lines.append(f"{bold}{line}{reset}")
        elif line.strip().startswith("NEEDS") or line.strip().startswith("**NEEDS"):
            formatted_lines.append(f"{bold}{line}{reset}")
        elif line.strip().startswith("Sources") or line.strip().startswith("**Sources"):
            formatted_lines.append(f"{dim}{line}{reset}")
        elif line.strip().startswith("- ") and formatted_lines and "Sources" in formatted_lines[-1]:
            formatted_lines.append(f"{dim}{line}{reset}")
        # Dim the disclaimer
        elif "not legal advice" in line.lower() or "consult a licensed" in line.lower():
            formatted_lines.append(f"{dim}{line}{reset}")
        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)


def parse_response(text: str) -> dict:
    """Parse the response into a structured dictionary.

    Args:
        text: Raw response text from Claude.

    Returns:
        Dictionary with keys: verdict, why, alternative, professional, sources, raw.
    """
    result = {
        "verdict": _detect_verdict(text),
        "raw": text,
        "why": "",
        "compliant_alternative": "",
        "needs_professional": "",
        "sources": [],
    }

    sections = text.split("\n")
    current_section = None

    for line in sections:
        line_stripped = line.strip()
        upper = line_stripped.upper()

        if "WHY:" in upper or "**WHY" in upper:
            current_section = "why"
            # Capture content after the header on the same line
            after = line_stripped.split(":", 1)[-1].strip().strip("*").strip()
            if after:
                result["why"] = after
            continue
        elif "COMPLIANT" in upper and ("ALTERNATIVE" in upper or "WAY" in upper):
            current_section = "alternative"
            continue
        elif "NEEDS" in upper and "PROFESSIONAL" in upper:
            current_section = "professional"
            after = line_stripped.split("?", 1)[-1].strip().strip("*").strip()
            if after:
                result["needs_professional"] = after
            continue
        elif "SOURCES" in upper or "SOURCE" in upper:
            current_section = "sources"
            continue
        elif any(v in upper for v in ["GREEN", "YELLOW", "RED"]) and any(
            e in line_stripped for e in ["\U0001f7e2", "\U0001f7e1", "\U0001f534"]
        ):
            current_section = None
            continue

        if current_section == "why" and line_stripped:
            result["why"] += (" " + line_stripped) if result["why"] else line_stripped
        elif current_section == "alternative" and line_stripped:
            result["compliant_alternative"] += (
                ("\n" + line_stripped) if result["compliant_alternative"] else line_stripped
            )
        elif current_section == "professional" and line_stripped:
            result["needs_professional"] += (
                (" " + line_stripped) if result["needs_professional"] else line_stripped
            )
        elif current_section == "sources" and line_stripped.startswith("- "):
            result["sources"].append(line_stripped[2:])

    return result

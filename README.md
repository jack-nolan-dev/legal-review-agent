# Legal Review Agent

An AI-powered legal risk classifier for small business decisions. Describe what you're about to do in plain English — get back a structured GREEN/YELLOW/RED verdict with statute citations, reasoning, and the compliant way to do it.

Works as a **CLI tool**, a **Claude Desktop tool** (MCP), or a **Claude Code tool** — so you can get a legal gut-check right inside the conversation where you're planning the decision.

Built for small business owners who can't afford to run every decision past a lawyer, but also can't afford to get it wrong.

> **This tool provides legal research, not legal advice.** It is not a substitute for a licensed attorney. Always consult a professional before acting on high-stakes decisions.

## How It Works

You ask a question. The agent classifies it into one of three risk levels:

- **GREEN** — Safe to proceed
- **YELLOW** — Proceed only with specific conditions
- **RED** — Do not proceed

Every verdict comes with the specific law behind it, a compliant alternative, and a call on whether you actually need a lawyer for this one.

## Example

```bash
$ python legal_review.py --state MA "Can I record sales calls with prospects?"
```

```
⚠️  This tool provides legal research, not legal advice. Consult a licensed attorney before acting.

🔴 RED — Do not proceed

WHY: Massachusetts is a strict all-party-consent wiretap state (M.G.L. c. 272 §99).
Recording any call — including sales calls — without explicit verbal consent from ALL
parties is a criminal offense, not just a civil matter. Commonwealth v. Hyde (2001)
upheld criminal conviction for secret recording even of police officers.

COMPLIANT ALTERNATIVE:
1. At the start of every call, say: "Just so you know, this call may be recorded for
   quality purposes. Is that okay with you?"
2. Wait for a spoken "yes" before proceeding
3. If they decline, do not record — take written notes instead
4. Store consent logs (date, time, caller, confirmation)

NEEDS A REAL PROFESSIONAL? No — the rule is clear-cut. Just follow the script above.

Sources:
- M.G.L. c. 272 §99 — Massachusetts wiretap statute
- Commonwealth v. Hyde, 434 Mass. 610 (2001)
```

## Installation

**Requirements:** Python 3.10+

```bash
# Clone the repo
git clone https://github.com/jack-nolan-dev/legal-review-agent.git
cd legal-review-agent

# Create a virtual environment and install dependencies
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**For CLI mode only** (MCP mode doesn't need an API key):

Get an API key from [console.anthropic.com](https://console.anthropic.com/) and set it:

```bash
# Option 1: environment variable
export ANTHROPIC_API_KEY=your-key-here

# Option 2: .env file (recommended — persists across sessions)
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

## Usage

### Single question
```bash
python legal_review.py "Can I scrape Google reviews and put them on my client's website?"
```

### With state context
```bash
python legal_review.py --state CA "Can I hire a freelancer to work 40hrs/week exclusively for me?"
```

### With business type
```bash
python legal_review.py --business-type "restaurant" "Do I need to post calorie counts on my menu?"
```

### Interactive mode
```bash
python legal_review.py --interactive --state MA
```

### Raw JSON output
```bash
python legal_review.py --raw "Can I send cold emails to local businesses?"
```

### See the full system prompt
```bash
python legal_review.py --verbose "question"
```

### Use a different model
```bash
# Use Opus for more complex analysis
python legal_review.py --model claude-opus-4-6 "complex multi-jurisdictional question"
```

## Use with Claude Desktop or Claude Code (MCP)

This is the easiest way to use the tool — no API key needed. It works as an [MCP server](https://modelcontextprotocol.io/), which means you can add it as a tool inside Claude Desktop or Claude Code. Then you just ask Claude to review a business decision and it calls the tool automatically.

**No API key required.** The tool provides the legal knowledge base and analysis framework to the Claude session that's already running — your existing Claude Desktop or Claude Code subscription does the reasoning.

### Setup (do this first)

```bash
git clone https://github.com/jack-nolan-dev/legal-review-agent.git
cd legal-review-agent
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Claude Desktop

Open your Claude Desktop config file:

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Add the `mcpServers` block (or add to it if one already exists):

```json
{
  "mcpServers": {
    "legal-review": {
      "command": "/absolute/path/to/legal-review-agent/.venv/bin/python",
      "args": ["/absolute/path/to/legal-review-agent/mcp_server.py"]
    }
  }
}
```

> Replace `/absolute/path/to/legal-review-agent` with the actual path where you cloned the repo. Use absolute paths, not `~`.

Restart Claude Desktop. Then just ask:

> "Use the legal-review tool to analyze: Can I scrape Google reviews and put them on my client's website?"

### Claude Code

```bash
claude mcp add legal-review -- /absolute/path/to/legal-review-agent/.venv/bin/python /absolute/path/to/legal-review-agent/mcp_server.py
```

Restart Claude Code, then ask about any legal question and it'll use the tool.

## Architecture

```
legal-review-agent/
├── legal_review.py          # CLI entry point (Click)
├── mcp_server.py            # MCP server for Claude Desktop / Claude Code
├── agent/
│   ├── prompt.py            # System prompt construction
│   ├── client.py            # Anthropic SDK wrapper
│   └── formatter.py         # Terminal output formatting
├── knowledge/
│   └── legal_base.md        # Core legal knowledge base
├── examples/
│   └── sample_queries.md    # 10 example queries with expected verdicts
├── pyproject.toml           # Package config
└── requirements.txt         # anthropic, click, python-dotenv, mcp
```

**How the prompt works:**

1. `prompt.py` loads the legal knowledge base from `knowledge/legal_base.md`
2. It constructs a system prompt that instructs Claude to analyze the question, identify the legal domain, cite real statutes, and return a structured verdict
3. Optional state and business-type context is injected into the prompt
4. `client.py` sends the question to Claude via the Anthropic SDK
5. `formatter.py` color-codes the terminal output based on the verdict

The knowledge base covers 12 legal areas common to small businesses: wiretapping, CAN-SPAM, TCPA, ROSCA, copyright, trademark, right of publicity, consumer protection (93A, UCL, etc.), entity/liability, contracts, data privacy, and employment classification.

## Legal Domains Covered

| Domain | Key Laws |
|--------|----------|
| Call Recording | 18 U.S.C. §2511, state wiretap statutes |
| Cold Email | CAN-SPAM Act (15 U.S.C. §7701) |
| Cold Calls | TCPA (47 U.S.C. §227), FTC TSR |
| Subscriptions | ROSCA (15 U.S.C. §8401), state auto-renewal laws |
| Copyright | 17 U.S.C. §101 et seq. |
| Trademark | Lanham Act (15 U.S.C. §1051) |
| Right of Publicity | State statutes (CA §3344, NY §50-51) |
| Consumer Protection | MA 93A, CA UCL, NY GBL §349 |
| Business Entity | State LLC/partnership law |
| Contracts | UCC, common law |
| Data Privacy | CCPA/CPRA, COPPA, state privacy laws |
| Employment | IRS classification, DOL tests, CA AB 5 |

## Limitations

- **Not legal advice.** This is a research tool, not a lawyer. The disclaimer is there for a reason.
- **Not a substitute for an attorney.** For entity formation, contracts, tax strategy, or anything with potential criminal liability — get a real professional.
- **Knowledge base is not exhaustive.** It covers common small-business scenarios, not every area of law.
- **No web search.** The tool cannot verify that statutes are current. It flags uncertainty when it's unsure about effective dates or recent amendments.
- **US-focused.** Federal + state law only. No international coverage.
- **Model limitations.** Claude can hallucinate citations. The prompt instructs it not to, and to flag uncertainty — but always verify citations independently before relying on them.

## Tech Stack

- **Python 3.10+**
- **[Anthropic SDK](https://docs.anthropic.com/en/docs/sdks)** — Claude API client
- **[Click](https://click.palletsprojects.com/)** — CLI framework
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — Environment variable loading
- **[MCP SDK](https://modelcontextprotocol.io/)** — Model Context Protocol server for Claude Desktop / Claude Code integration
- **Claude Sonnet 4.6** — Default model (swap to `claude-opus-4-6` via `--model` for deeper analysis)

## License

MIT — see [LICENSE](LICENSE).

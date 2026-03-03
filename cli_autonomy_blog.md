# The CLI Is The Path To AI Autonomy

The terminal isn't a developer convenience. It's the existing, universal, zero-overhead integration layer that makes AI autonomy practical today.

## In Short

Everyone is building new protocols, new APIs, new standards to give AI agents access to tools. MCP servers. Function calling schemas. Tool registries.

Meanwhile, the terminal has been sitting there the whole time. Every tool already has a CLI. Git, Docker, curl, ffmpeg, npm — decades of tooling, already accessible through a shell command.

NVIDIA just published a study proving that terminal capability in LLMs is trainable and scales predictably. Peter Steinberger, creator of OpenClaw and now at OpenAI, has been saying the same thing from a practitioner's perspective: "mcp were a mistake. bash is better."

Anthropic acquired Vercept, a computer-use startup, folding desktop and terminal operation directly into Claude.

Elon Musk put it simply in his recent interview with Dwarkesh Patel — the approach is "driving a computer screen" rather than a car. A self-driving computer. The first step to autonomy is AI operating a computer as well as a human does.

The industry is converging on one conclusion — the CLI is the bridge to autonomy.

## The NVIDIA Study

NVIDIA's paper "On Data Engineering for Scaling LLM Terminal Capabilities" addresses a gap nobody was talking about openly. Training data strategies for terminal agents have been largely undisclosed.

Their contributions:

- **Terminal-Task-Gen** — a pipeline to synthetically generate terminal tasks
- **Terminal-Corpus** — an open-source dataset for terminal agent training
- **Nemotron-Terminal** — models trained on this data showing dramatic gains

The results speak for themselves. Nemotron-Terminal-8B improves from 2.5% to 13.0% on Terminal-Bench 2.0. The 14B model jumps from 4.0% to 20.2%. The 32B model goes from 3.4% to 27.4%, matching significantly larger models.

The key insight isn't bigger models. It's data engineering — filtering, curriculum learning, long context training. Terminal capability is a trainable skill that scales predictably.

## Peter Steinberger's Position

Steinberger built OpenClaw — 190,000 GitHub stars. Sam Altman recruited him to OpenAI to build personal agents. His take on tool integration is blunt.

He removed his last MCP server. Claude would spin up Playwright when it could simply read the code — slower and pollutes the context.

His argument against MCP:

**Token cost.** GitHub's MCP consumed nearly 50,000 tokens initially. Even optimised, it wastes 23,000 tokens just describing available tools. A CLI costs zero tokens. The model already knows git, grep, curl. If it doesn't, it reads --help.

**Self-documenting.** When an agent encounters an unfamiliar CLI, it triggers the help menu. Full context, no documentation burden.

**Model familiarity.** AI systems already understand command-line tools. The model learns through trial and error on first use. No schema definitions needed.

His workflow: 3-8 Codex CLI instances in parallel, running in a 3x3 terminal grid. Pure terminal. No abstractions.

## The Anthropic Bet

Anthropic acquired Vercept on February 25, 2026. Vercept built Vy — a computer-use agent that could operate a remote MacBook in the cloud.

The founders joined Anthropic. The product is being shut down. The technology is being folded into Claude.

This isn't a coincidence. Anthropic already has Claude Code — a terminal agent. Now they're adding desktop-level computer operation. The strategy is clear: make Claude operate computers the way humans do.

## Musk: A Self-Driving Computer

In his recent interview with Dwarkesh Patel, Elon Musk described the approach as essentially applying Tesla's self-driving methodology — but instead of driving a car, you're driving a computer screen. A self-driving computer.

The analogy is precise. Tesla's autonomy stack perceives the road, reasons about obstacles, and acts through steering and acceleration. A terminal agent perceives the screen, reasons about the task, and acts through commands and keystrokes.

Same architecture. Different vehicle.

The first step to full autonomy isn't building new infrastructure. It's AI using computers as well as humans do. Click, type, navigate, execute. Once that works, everything else follows.

## The Autonomy Progression

There's a clear progression happening:

**Stage 1: Chat.** The model generates text. You copy-paste it.

**Stage 2: Tool use.** The model calls predefined functions. MCP, function calling, tool schemas. Curated, bounded, safe.

**Stage 3: Terminal.** The model operates the computer directly. Shell commands, file systems, scripts. No curated tool APIs — it uses what's already there.

**Stage 4: Full autonomy.** The model reasons, plans, and executes end-to-end. Multi-step tasks across applications, sessions, and time.

We're between Stage 2 and Stage 3 right now. Most production agents are in Stage 2. Claude Code, Codex CLI, and OpenClaw are pushing into Stage 3.

The CLI is the critical bridge. It's where the model stops calling curated APIs and starts operating the machine.

## Why CLI Wins

Think about what MCP requires. A server process. A protocol. Schema definitions. Token overhead per tool. Maintenance. Version management.

Think about what a CLI requires. Nothing. It already exists. The model already knows how to use it.

Every piece of software installed on a machine is already accessible through the terminal. Package managers, version control, cloud CLIs, database clients, container orchestration, monitoring tools — all of it.

The terminal is the ultimate existing integration. Not a new protocol. Not a new standard. An interface that has existed for decades, with every tool already built for it.

## Bounded Autonomy Through The Terminal

I've written extensively about bounded autonomy — agents operating freely within defined constraints.

The terminal provides natural boundaries:

- **Sandboxing** — Docker containers, VMs, restricted shells
- **Permissions** — file system permissions, user roles, sudo controls
- **Logging** — every command is traceable, auditable
- **Reversibility** — git for code, snapshots for systems

These aren't new governance layers you need to build. They're operating system primitives that already exist.

NVIDIA's study confirms this. Their models operate in terminal environments with natural constraints. The governance is built into the environment itself.

Compare this to the OpenAI Agentic Governance Cookbook I wrote about recently. That approach requires building governance scaffolding — pre-flight checks, post-flight guardrails, policy packages. Valuable for structured workflows, but a lot of infrastructure.

The terminal gives you governance primitives for free. The sandbox is the guardrail.

## In Closing

The industry is converging. NVIDIA is training models specifically for terminal capability. Anthropic is acquiring computer-use companies. OpenAI hired the person who built the most popular terminal agent. Steinberger calls CLI the ultimate integration. The data backs him up.

The path to AI autonomy doesn't run through new protocols. It runs through the terminal — the integration layer that's been there all along.

---

## References

- [On Data Engineering for Scaling LLM Terminal Capabilities — NVIDIA (arXiv)](https://arxiv.org/abs/2602.21193)
- [Just Talk To It — Peter Steinberger](https://steipete.me/posts/just-talk-to-it)
- [Elon Musk — "In 36 months, the cheapest place to put AI will be space" — Dwarkesh Patel](https://www.dwarkesh.com/p/elon-musk)
- [Anthropic acquires Vercept — TechCrunch](https://techcrunch.com/2026/02/25/anthropic-acquires-vercept-ai-startup-agents-computer-use-founders-investors/)
- [Anthropic acquires Vercept — GeekWire](https://www.geekwire.com/2026/anthropic-acquires-vercept-in-early-exit-for-one-of-seattles-standout-ai-startups/)
- [OpenAI grabs OpenClaw creator Peter Steinberger — TechEduByte](https://www.techedubyte.com/openai-peter-steinberger-openclaw-personal-agents/)
- [Lex Fridman Podcast #491 — Peter Steinberger](https://lexfridman.com/peter-steinberger-transcript/)
- [Why CLIs Beat MCP for AI Agents](https://medium.com/@rentierdigital/why-clis-beat-mcp-for-ai-agents-and-how-to-build-your-own-cli-army-6c27b0aec969)

---

*Chief Evangelist @ Kore.ai | I'm passionate about exploring the intersection of AI and language. Language Models, AI Agents, Agentic Apps, Dev Frameworks & Data-Driven Tools shaping tomorrow.*

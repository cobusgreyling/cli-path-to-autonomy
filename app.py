"""
Nemotron-Terminal Agent — Gradio Demo (Mock Mode)
Simulates the Nemotron-Terminal-8B structured JSON output format.
Shows the model's analysis → plan → commands → task_complete flow.
"""

import json
import time
import random

import gradio as gr

PORT = 7863

# ---------------------------------------------------------------------------
# Nemotron-Terminal output schema reference
# ---------------------------------------------------------------------------
# The model produces structured JSON:
# {
#   "analysis": "Analysis of the current terminal state...",
#   "plan": "Step-by-step plan for the next command...",
#   "commands": [
#     { "keystrokes": "ls -la\n", "duration": 0.1 }
#   ],
#   "task_complete": false
# }
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Mock scenarios — each is a multi-turn sequence of model responses
# ---------------------------------------------------------------------------

MOCK_SCENARIOS = {
    "List all files and show their sizes": {
        "description": "Directory listing with human-readable sizes",
        "turns": [
            {
                "model_response": {
                    "analysis": "The user wants to see all files in the current working directory with their sizes displayed in a human-readable format. I need to run a listing command that shows file sizes.",
                    "plan": "1. Use ls with -lah flags to list all files including hidden ones, with human-readable sizes.\n2. Report the results back to the user.",
                    "commands": [
                        {"keystrokes": "ls -lah\n", "duration": 0.3}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": "total 32K\ndrwxr-xr-x  5 user staff  160 Mar  4 10:22 .\ndrwxr-xr-x 12 user staff  384 Mar  4 09:15 ..\n-rw-r--r--  1 user staff  2.1K Mar  4 10:22 app.py\n-rw-r--r--  1 user staff   45  Mar  4 09:30 .env\n-rw-r--r--  1 user staff  512  Mar  4 10:00 requirements.txt\ndrwxr-xr-x  3 user staff   96  Mar  3 14:20 data/"
            },
            {
                "model_response": {
                    "analysis": "The ls command executed successfully. The directory contains 3 files (app.py at 2.1K, .env at 45 bytes, requirements.txt at 512 bytes) and 1 subdirectory (data/). Total size is 32K. The task is complete.",
                    "plan": "No further commands needed. Summarise findings for the user.",
                    "commands": [],
                    "task_complete": True
                },
                "simulated_terminal": None
            }
        ]
    },

    "Create a project with Python files": {
        "description": "Multi-step directory and file creation",
        "turns": [
            {
                "model_response": {
                    "analysis": "The user wants me to create a project directory structure with Python files. I need to first create the directory, then create the Python files inside it.",
                    "plan": "1. Create a directory called 'project' using mkdir.\n2. Create three empty Python files inside it using touch.\n3. Verify the structure with ls.",
                    "commands": [
                        {"keystrokes": "mkdir -p project\n", "duration": 0.1}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": ""
            },
            {
                "model_response": {
                    "analysis": "The project directory was created successfully (no error output). Now I need to create three Python files inside it.",
                    "plan": "1. Use touch to create main.py, utils.py, and config.py inside the project directory.\n2. Then verify the structure.",
                    "commands": [
                        {"keystrokes": "touch project/main.py project/utils.py project/config.py\n", "duration": 0.1}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": ""
            },
            {
                "model_response": {
                    "analysis": "Files created without errors. Let me verify the directory structure to confirm everything is in place.",
                    "plan": "1. Run ls -la on the project directory to verify all three files exist.",
                    "commands": [
                        {"keystrokes": "ls -la project/\n", "duration": 0.2}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": "total 0\ndrwxr-xr-x 5 user staff 160 Mar  4 10:25 .\ndrwxr-xr-x 6 user staff 192 Mar  4 10:25 ..\n-rw-r--r-- 1 user staff   0 Mar  4 10:25 config.py\n-rw-r--r-- 1 user staff   0 Mar  4 10:25 main.py\n-rw-r--r-- 1 user staff   0 Mar  4 10:25 utils.py"
            },
            {
                "model_response": {
                    "analysis": "All three Python files (main.py, utils.py, config.py) were successfully created inside the project/ directory. The directory structure is confirmed. Task is complete.",
                    "plan": "No further commands needed.",
                    "commands": [],
                    "task_complete": True
                },
                "simulated_terminal": None
            }
        ]
    },

    "Find .py files and count lines of code": {
        "description": "Chained find and wc commands",
        "turns": [
            {
                "model_response": {
                    "analysis": "The user wants to find all Python files and get a total line count. I need to use find to locate .py files, then pipe the results to wc to count lines.",
                    "plan": "1. Use find to locate all .py files recursively.\n2. Pipe the file list to xargs wc -l to count lines in each file and get a total.",
                    "commands": [
                        {"keystrokes": "find . -name '*.py' -type f\n", "duration": 0.5}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": "./app.py\n./project/main.py\n./project/utils.py\n./project/config.py\n./tests/test_app.py"
            },
            {
                "model_response": {
                    "analysis": "Found 5 Python files across the directory tree. Now I need to count the total lines across all of them using wc.",
                    "plan": "1. Use find piped to wc -l via xargs to get per-file and total line counts.",
                    "commands": [
                        {"keystrokes": "find . -name '*.py' -type f | sort | head -20\n", "duration": 0.3},
                        {"keystrokes": "wc -l ./app.py ./project/main.py ./project/utils.py ./project/config.py ./tests/test_app.py\n", "duration": 0.3}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": "  142 ./app.py\n    0 ./project/main.py\n   28 ./project/utils.py\n   15 ./project/config.py\n   67 ./tests/test_app.py\n  252 total"
            },
            {
                "model_response": {
                    "analysis": "Line count complete. Found 5 Python files with 252 total lines of code. The largest file is app.py at 142 lines, followed by test_app.py at 67 lines. Three project files have minimal content. Task complete.",
                    "plan": "No further commands needed. Report summary.",
                    "commands": [],
                    "task_complete": True
                },
                "simulated_terminal": None
            }
        ]
    },

    "Show system information": {
        "description": "System info gathering with multiple commands",
        "turns": [
            {
                "model_response": {
                    "analysis": "The user wants system information including OS details, hostname, and disk usage. I will gather this information using uname, whoami, and df commands.",
                    "plan": "1. Run uname -a for full OS/kernel info.\n2. Run whoami for the current user.\n3. Run df -h for disk usage in human-readable format.",
                    "commands": [
                        {"keystrokes": "uname -a\n", "duration": 0.1}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": "Darwin MacBook-Pro.local 24.3.0 Darwin Kernel Version 24.3.0: Thu Jan  2 20:24:16 PST 2025; root:xnu-11215.81.4~3/RELEASE_ARM64_T6030 arm64"
            },
            {
                "model_response": {
                    "analysis": "Got OS info — macOS Darwin on ARM64 (Apple Silicon). Now gathering user and disk info.",
                    "plan": "1. Run whoami for current user.\n2. Run df -h for disk usage.",
                    "commands": [
                        {"keystrokes": "whoami\n", "duration": 0.1},
                        {"keystrokes": "df -h /\n", "duration": 0.2}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": "cobusgreyling\nFilesystem     Size   Used  Avail Capacity  Mounted on\n/dev/disk3s1  460Gi  287Gi  148Gi    66%     /"
            },
            {
                "model_response": {
                    "analysis": "All system information collected. OS is macOS Darwin 24.3.0 on ARM64, user is cobusgreyling, disk is 66% full (287GB used of 460GB). Task complete.",
                    "plan": "No further commands needed.",
                    "commands": [],
                    "task_complete": True
                },
                "simulated_terminal": None
            }
        ]
    },

    "Attempt a blocked command (rm -rf)": {
        "description": "Demonstrates governance — model proposes rm, allowlist rejects it",
        "turns": [
            {
                "model_response": {
                    "analysis": "The user asked me to delete everything in the directory. I would need to use rm to remove files. However, rm is a destructive command that may not be in the allowed commands list.",
                    "plan": "1. Attempt to use rm -rf to remove all files as requested.",
                    "commands": [
                        {"keystrokes": "rm -rf *\n", "duration": 0.1}
                    ],
                    "task_complete": False
                },
                "simulated_terminal": None,
                "governance_block": {
                    "command": "rm -rf *",
                    "reason": "'rm' is not in the allowed commands list. Destructive operations are blocked by governance policy."
                }
            },
            {
                "model_response": {
                    "analysis": "The rm command was blocked by the governance allowlist. I cannot execute destructive delete operations. I should inform the user that this action is not permitted under the current security policy.",
                    "plan": "No commands to run. Inform the user about the governance restriction.",
                    "commands": [],
                    "task_complete": True
                },
                "simulated_terminal": None
            }
        ]
    },
}

EXAMPLE_PROMPTS = list(MOCK_SCENARIOS.keys())

ALLOWED_COMMANDS = [
    "cd", "ls", "cat", "find", "grep", "echo", "touch", "mkdir", "pwd",
    "head", "tail", "sort", "du", "cp", "wget", "wc", "date", "whoami",
    "uname", "df", "file", "tree",
]

# ---------------------------------------------------------------------------
# Theme & CSS
# ---------------------------------------------------------------------------

NVIDIA_THEME = gr.themes.Base(
    primary_hue=gr.themes.Color(
        c50="#f0fdf0", c100="#dcfce7", c200="#bbf7d0", c300="#86efac",
        c400="#4ade80", c500="#76b900", c600="#65a300", c700="#4d7a00",
        c800="#365200", c900="#1a2900", c950="#0d1500",
    ),
    secondary_hue=gr.themes.colors.neutral,
    neutral_hue=gr.themes.colors.gray,
    font=gr.themes.GoogleFont("Inter"),
    font_mono=gr.themes.GoogleFont("JetBrains Mono"),
).set(
    body_background_fill="#0d1117",
    body_background_fill_dark="#0d1117",
    body_text_color="#e6edf3",
    body_text_color_dark="#e6edf3",
    block_background_fill="#161b22",
    block_background_fill_dark="#161b22",
    block_border_color="#30363d",
    block_border_color_dark="#30363d",
    block_label_text_color="#8b949e",
    block_label_text_color_dark="#8b949e",
    block_title_text_color="#e6edf3",
    block_title_text_color_dark="#e6edf3",
    input_background_fill="#0d1117",
    input_background_fill_dark="#0d1117",
    input_border_color="#30363d",
    input_border_color_dark="#30363d",
    button_primary_background_fill="#76b900",
    button_primary_background_fill_dark="#76b900",
    button_primary_text_color="#ffffff",
    button_primary_text_color_dark="#ffffff",
    button_primary_background_fill_hover="#65a300",
    button_primary_background_fill_hover_dark="#65a300",
    button_secondary_background_fill="#21262d",
    button_secondary_background_fill_dark="#21262d",
    button_secondary_text_color="#e6edf3",
    button_secondary_text_color_dark="#e6edf3",
    button_secondary_border_color="#30363d",
    button_secondary_border_color_dark="#30363d",
)

CSS = """
.banner-container {
    text-align: center;
    padding: 20px 0 10px 0;
}
.banner-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #76b900;
    margin-bottom: 4px;
}
.banner-subtitle {
    font-size: 0.95rem;
    color: #8b949e;
}
.banner-mock {
    font-size: 0.8rem;
    color: #f0883e;
    margin-top: 4px;
}
.nvidia-badge {
    display: inline-block;
    background: linear-gradient(135deg, #76b900, #4d7a00);
    color: white;
    padding: 2px 10px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 2.55rem;
    margin-right: 8px;
    vertical-align: middle;
}
.allowed-commands-box {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #76b900;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 10px;
    line-height: 1.6;
}
.trace-panel {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.5;
    color: #e6edf3;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 14px;
    max-height: 500px;
    overflow-y: auto;
}
.trace-step {
    margin-bottom: 10px;
    padding: 8px;
    border-left: 3px solid #30363d;
    padding-left: 10px;
}
.trace-step.pass { border-left-color: #76b900; }
.trace-step.fail { border-left-color: #f85149; }
.trace-step.info { border-left-color: #58a6ff; }
.trace-step.model { border-left-color: #f0883e; }
.trace-label {
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.trace-label.pass { color: #76b900; }
.trace-label.fail { color: #f85149; }
.trace-label.info { color: #58a6ff; }
.trace-label.model { color: #f0883e; }
.cmd-block {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    margin: 6px 0;
    overflow: hidden;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
}
.cmd-header {
    background: #161b22;
    padding: 6px 10px;
    color: #76b900;
    font-weight: 600;
    border-bottom: 1px solid #30363d;
}
.cmd-output {
    padding: 8px 10px;
    color: #e6edf3;
    white-space: pre-wrap;
    max-height: 200px;
    overflow-y: auto;
}
.cmd-blocked {
    border-color: #f85149;
}
.cmd-blocked .cmd-header {
    color: #f85149;
}
.json-block {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    margin: 6px 0;
    overflow: hidden;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}
.json-header {
    background: #1c2333;
    padding: 6px 10px;
    color: #f0883e;
    font-weight: 600;
    border-bottom: 1px solid #30363d;
    font-size: 0.75rem;
}
.json-body {
    padding: 8px 10px;
    color: #e6edf3;
    white-space: pre-wrap;
    max-height: 300px;
    overflow-y: auto;
}
.json-body .key { color: #79c0ff; }
.json-body .str { color: #a5d6ff; }
.json-body .bool { color: #ff7b72; }
.json-body .num { color: #76b900; }
.status-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    font-size: 0.85rem;
}
.status-label { color: #8b949e; }
.status-value { color: #e6edf3; font-family: 'JetBrains Mono', monospace; }
footer { display: none !important; }
"""

# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def trace_step(label: str, content: str, level: str = "info") -> str:
    return (
        f'<div class="trace-step {level}">'
        f'<div class="trace-label {level}">{label}</div>'
        f'<div>{content}</div>'
        f'</div>'
    )


def json_syntax_highlight(obj: dict) -> str:
    """Produce coloured HTML from a dict, matching terminal JSON aesthetics."""
    raw = json.dumps(obj, indent=2, ensure_ascii=False)
    # Highlight keys
    raw_esc = esc(raw)
    # keys
    raw_esc = __import__("re").sub(
        r'&quot;(\w+)&quot;(\s*:)',
        r'<span class="key">&quot;\1&quot;</span>\2',
        raw_esc,
    )
    # string values
    raw_esc = __import__("re").sub(
        r':\s*&quot;(.*?)&quot;',
        r': <span class="str">&quot;\1&quot;</span>',
        raw_esc,
    )
    # booleans
    raw_esc = raw_esc.replace("true", '<span class="bool">true</span>')
    raw_esc = raw_esc.replace("false", '<span class="bool">false</span>')
    # numbers after colon
    raw_esc = __import__("re").sub(
        r':\s*(\d+\.?\d*)',
        r': <span class="num">\1</span>',
        raw_esc,
    )
    return raw_esc


def model_response_html(response: dict) -> str:
    """Render the full Nemotron-Terminal JSON response as a styled block."""
    highlighted = json_syntax_highlight(response)
    return (
        f'<div class="json-block">'
        f'<div class="json-header">Nemotron-Terminal-8B Response</div>'
        f'<div class="json-body">{highlighted}</div>'
        f'</div>'
    )


def command_block_html(command: str, output: str, blocked: bool = False, block_reason: str = "") -> str:
    cls = "cmd-block cmd-blocked" if blocked else "cmd-block"
    header_label = "BLOCKED" if blocked else "Terminal Output"
    display_output = block_reason if blocked else (output or "(no output)")
    return (
        f'<div class="{cls}">'
        f'<div class="cmd-header">{header_label} — $ {esc(command)}</div>'
        f'<div class="cmd-output">{esc(display_output)}</div>'
        f'</div>'
    )


def wrap_trace(entries: list[str]) -> str:
    return '<div class="trace-panel">' + "\n".join(entries) + "</div>"


def status_html(turn_count: int, cmd_count: int) -> str:
    return (
        f'<div class="status-row"><span class="status-label">Mode</span>'
        f'<span class="status-value">Mock (simulated)</span></div>'
        f'<div class="status-row"><span class="status-label">Model turns</span>'
        f'<span class="status-value">{turn_count}</span></div>'
        f'<div class="status-row"><span class="status-label">Commands issued</span>'
        f'<span class="status-value">{cmd_count}</span></div>'
    )


# ---------------------------------------------------------------------------
# Mock agent loop
# ---------------------------------------------------------------------------

def run_mock_scenario(user_message: str, history: list, state: dict | None):
    """
    Generator yielding (history, trace_html, status_html, state) for each turn.
    Plays back pre-configured mock responses with simulated delays.
    """
    t0 = time.time()
    trace_entries = []
    state = state or {"turn_count": 0, "cmd_count": 0}

    # Match to a scenario (fuzzy)
    scenario = None
    msg_lower = user_message.lower()
    for key, val in MOCK_SCENARIOS.items():
        # Match on keywords
        key_words = key.lower().split()
        if sum(1 for w in key_words if w in msg_lower) >= 2:
            scenario = val
            break

    if scenario is None:
        # Default to first scenario for unrecognised input
        scenario = list(MOCK_SCENARIOS.values())[0]
        trace_entries.append(trace_step(
            "Input Matching",
            f"No exact scenario match for \"{esc(user_message)}\". "
            "Using default scenario for demonstration.",
            "info"
        ))

    history = history + [{"role": "user", "content": user_message}]
    trace_entries.append(trace_step("Pre-flight", "Input validated. No injection patterns detected.", "pass"))

    # Play each turn
    for i, turn in enumerate(scenario["turns"]):
        model_resp = turn["model_response"]
        terminal_out = turn.get("simulated_terminal")
        gov_block = turn.get("governance_block")

        state["turn_count"] += 1
        delay = random.uniform(0.4, 0.8)
        time.sleep(delay)

        # Trace — model analysis
        trace_entries.append(trace_step(
            f"Turn {i + 1} — Analysis",
            esc(model_resp["analysis"]),
            "model"
        ))

        # Trace — model plan
        trace_entries.append(trace_step(
            f"Turn {i + 1} — Plan",
            esc(model_resp["plan"]),
            "info"
        ))

        # Show the full JSON response in chat
        response_block = model_response_html(model_resp)
        history = history + [{"role": "assistant", "content": response_block}]

        # Process commands
        if model_resp["commands"]:
            for cmd_obj in model_resp["commands"]:
                cmd = cmd_obj["keystrokes"].rstrip("\n")
                state["cmd_count"] += 1

                # Check for governance block
                if gov_block and gov_block["command"] == cmd:
                    trace_entries.append(trace_step(
                        "Allowlist Check",
                        f"BLOCKED: {esc(gov_block['reason'])}",
                        "fail"
                    ))
                    block_html = command_block_html(
                        cmd, "", blocked=True, block_reason=gov_block["reason"]
                    )
                    history = history + [{"role": "assistant", "content": block_html}]
                else:
                    trace_entries.append(trace_step(
                        "Allowlist Check",
                        f"<code>$ {esc(cmd)}</code> — Passed",
                        "pass"
                    ))
                    if terminal_out is not None:
                        cmd_html = command_block_html(cmd, terminal_out)
                        history = history + [{"role": "assistant", "content": cmd_html}]
                        trace_entries.append(trace_step(
                            "Execution",
                            esc(terminal_out[:300]) if terminal_out else "(no output)",
                            "pass"
                        ))

        # Task complete?
        if model_resp["task_complete"]:
            trace_entries.append(trace_step("Task Complete", "Model signalled task_complete = true", "pass"))

        yield (
            history,
            wrap_trace(trace_entries),
            status_html(state["turn_count"], state["cmd_count"]),
            state,
        )

    elapsed = time.time() - t0
    trace_entries.append(trace_step("Timing", f"{elapsed:.2f}s total (simulated)", "info"))
    yield (
        history,
        wrap_trace(trace_entries),
        status_html(state["turn_count"], state["cmd_count"]),
        state,
    )


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

def build_ui():
    with gr.Blocks(title="Nemotron-Terminal Agent") as demo:

        agent_state = gr.State(None)

        # Banner
        gr.HTML(
            '<div class="banner-container">'
            '<div class="banner-title">'
            '<span class="nvidia-badge">NVIDIA</span> Nemotron-Terminal Agent'
            '</div>'
            '<div class="banner-subtitle">AI-powered bash agent with structured command output</div>'
            '</div>'
        )

        with gr.Row():
            # ---- Sidebar ----
            with gr.Column(scale=1, min_width=280):
                gr.Markdown("### Model Info")
                gr.HTML(
                    '<div style="font-size:0.85rem; color:#8b949e; line-height:1.6;">'
                    '<b style="color:#e6edf3;">Model</b> nvidia/Nemotron-Terminal-8B<br>'
                    '<b style="color:#e6edf3;">Base</b> Qwen3-8B (fine-tuned)<br>'
                    '<b style="color:#e6edf3;">Output</b> Structured JSON<br>'
                    '<b style="color:#e6edf3;">Source</b> '
                    '<a href="https://huggingface.co/nvidia/Nemotron-Terminal-8B" '
                    'target="_blank" style="color:#58a6ff;">HuggingFace</a><br>'
                    '<b style="color:#e6edf3;">Hosting</b> Self-hosted (Ollama / vLLM)'
                    '</div>'
                )

                gr.Markdown("### Output Schema")
                gr.HTML(
                    '<div class="allowed-commands-box" style="color:#e6edf3; font-size:0.75rem;">'
                    '{\n'
                    '  <span style="color:#79c0ff;">"analysis"</span>: "...",\n'
                    '  <span style="color:#79c0ff;">"plan"</span>: "...",\n'
                    '  <span style="color:#79c0ff;">"commands"</span>: [\n'
                    '    {\n'
                    '      <span style="color:#79c0ff;">"keystrokes"</span>: "ls -la\\n",\n'
                    '      <span style="color:#79c0ff;">"duration"</span>: <span style="color:#76b900;">0.1</span>\n'
                    '    }\n'
                    '  ],\n'
                    '  <span style="color:#79c0ff;">"task_complete"</span>: <span style="color:#ff7b72;">false</span>\n'
                    '}'
                    '</div>'
                )

                gr.Markdown("### Allowed Commands")
                cmd_list = "  ".join(f"`{c}`" for c in ALLOWED_COMMANDS)
                gr.HTML(f'<div class="allowed-commands-box">{cmd_list}</div>')

                gr.Markdown("### Agent Status")
                status_display = gr.HTML(status_html(0, 0))

                gr.Markdown("### Example Scenarios")
                example_buttons = []
                for prompt_text in EXAMPLE_PROMPTS:
                    btn = gr.Button(prompt_text, variant="secondary", size="sm")
                    example_buttons.append(btn)

            # ---- Main panel ----
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="Nemotron-Terminal Agent",
                    height=500,
                    buttons=["copy"],
                    sanitize_html=False,
                    render_markdown=True,
                )

                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Ask the terminal agent to do something...",
                        scale=4,
                        show_label=False,
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)

                with gr.Accordion("Governance Trace", open=True):
                    trace_display = gr.HTML('<div class="trace-panel">No activity yet. Click an example scenario to begin.</div>')

        # ---- Event wiring ----

        def on_send(message, history, state):
            if not message.strip():
                yield history or [], wrap_trace([]), status_html(0, 0), state
                return
            for h, trace, st, new_state in run_mock_scenario(message, history or [], state):
                yield h, trace, st, new_state

        send_outputs = [chatbot, trace_display, status_display, agent_state]

        send_btn.click(
            on_send,
            inputs=[msg_input, chatbot, agent_state],
            outputs=send_outputs,
        ).then(lambda: "", outputs=[msg_input])

        msg_input.submit(
            on_send,
            inputs=[msg_input, chatbot, agent_state],
            outputs=send_outputs,
        ).then(lambda: "", outputs=[msg_input])

        def make_example_handler(prompt_text):
            def handler(history, state):
                for h, trace, st, new_state in run_mock_scenario(prompt_text, history or [], state):
                    yield h, trace, st, new_state
            return handler

        for btn, prompt_text in zip(example_buttons, EXAMPLE_PROMPTS):
            handler = make_example_handler(prompt_text)
            btn.click(
                handler,
                inputs=[chatbot, agent_state],
                outputs=send_outputs,
            )

    return demo


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_port=PORT, share=False, theme=NVIDIA_THEME, css=CSS)

# Nemotron-Terminal Agent — Gradio Demo

A visual companion to the **"CLI Is The Path To AI Autonomy"** blog post. Demonstrates NVIDIA's [Nemotron-Terminal-8B](https://huggingface.co/nvidia/Nemotron-Terminal-8B) model as a governed bash agent with a polished Gradio UI.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Gradio](https://img.shields.io/badge/Gradio-6.x-orange)
![NVIDIA](https://img.shields.io/badge/NVIDIA-Nemotron--Terminal-76b900)

## What This Does

Nemotron-Terminal is a family of models from NVIDIA, fine-tuned from Qwen3, purpose-built for **autonomous terminal interaction**. Unlike standard chat models that use tool-calling, Nemotron-Terminal outputs structured JSON with explicit reasoning before every command.

This Gradio app visualises the full agent loop in real time.

### The Structured Output Format

Every model turn produces JSON with four fields:

```json
{
  "analysis": "Assessment of current terminal state...",
  "plan": "Step-by-step plan for the next command...",
  "commands": [
    {
      "keystrokes": "ls -la\n",
      "duration": 0.1
    }
  ],
  "task_complete": false
}
```

**analysis** — the model's reading of the current terminal state before acting

**plan** — explicit step-by-step reasoning about what to do next

**commands** — the actual keystrokes to send to the terminal, with expected duration

**task_complete** — boolean flag signalling whether the task is finished

## Governance

The agent enforces an **allowlist** of safe commands:

```
cd  ls  cat  find  grep  echo  touch  mkdir  pwd
head  tail  sort  du  cp  wget  wc  date  whoami
uname  df  file  tree
```

Destructive commands like `rm`, `chmod`, `kill` are blocked at the governance layer. The **Governance Trace** panel shows every validation step in real time.

## Pre-configured Scenarios

The demo ships with five walkthrough scenarios:

| Scenario | Turns | What It Shows |
|----------|-------|---------------|
| List all files and show their sizes | 2 | Single command, analysis → completion |
| Create a project with Python files | 4 | Multi-step chained commands |
| Find .py files and count lines of code | 3 | Piped commands, progressive reasoning |
| Show system information | 3 | Multiple independent commands |
| Attempt a blocked command (rm -rf) | 2 | Governance rejection in action |

## Running Locally

```bash
pip install gradio openai python-dotenv
python app.py
```

Opens on **http://localhost:7863**. No API key or GPU needed — the demo runs in simulation mode.

## Connecting to a Live Model

When Nemotron-Terminal-8B becomes available via Ollama or vLLM, the app can be pointed at a local endpoint. The model requires self-hosting (no NIM API available yet).

**Ollama** — pending GGUF quantisation from community

**vLLM** — `vllm serve nvidia/Nemotron-Terminal-8B`

## Screenshot

The UI features an NVIDIA green terminal theme with a sidebar showing model info, output schema reference, allowed commands, and clickable example scenarios. The main panel displays the chat with syntax-highlighted JSON responses, styled command blocks, and a collapsible governance trace.

## Author

**Cobus Greyling** — Chief Evangelist @ Kore.ai

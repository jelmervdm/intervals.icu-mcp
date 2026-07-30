# Intervals.icu MCP Server

[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue.svg)](https://github.com/jelmervdm/intervals.icu-mcp)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](pyproject.toml)
[![TDQS Score](https://img.shields.io/badge/TDQS-5.00%2F5.00%20(Tier%20A%2B)-success.svg)](https://github.com/glama-ai/tool-definition-quality-score)

Model Context Protocol (MCP) server for [Intervals.icu](https://intervals.icu), providing athletic training analysis, activity management, calendar event planning, wellness tracking, and workout library integration to AI assistants like Claude Desktop, Cursor, and IBM ContextForge.

---

## 🏆 Tool Definition Quality Score (TDQS)

This server is audited against the **[Tool Definition Quality Score (TDQS)](https://github.com/glama-ai/tool-definition-quality-score)** framework to guarantee optimal function calling, type safety, and runtime safety for LLMs:
- **Score:** `5.00 / 5.00` (**Tier A+**)
- **Behavioral Annotations (`ToolAnnotations`):** 100% of tools specify `readOnlyHint`, `destructiveHint`, and `idempotentHint` metadata.
- **Parameter Descriptions:** 100% of tool parameters use explicit Pydantic `Annotated[T, Field(description=...)]` metadata.
- **Operational Guidelines:** Standardized docstrings detailing explicit "Use when..." context across all 17 tools.

```text
---------------- SCORECARD METRICS ----------------
Tools Evaluated              : 17
Behavioral Annotations      : 17 / 17 (100.0%)
100% Parameter Descriptions : 17 / 17 (100.0%)
Usage Guidelines (Docstrings): 17 / 17 (100.0%)
Overall TDQS Score           : 5.00 / 5.00
TDQS Quality Tier            : Tier A+
========================================================
```

---

## Features

- **Athlete Profile**: Fetch FTP, LTHR, max HR, weight, and training zone settings.
- **Activities**: Search, view detailed metrics, update activity names/types, delete activities, and comment on activities.
- **Calendar & Events**: Manage planned workouts, races, and note events on your training calendar.
- **Wellness Tracking**: Log and retrieve daily wellness metrics (HRV, resting HR, weight, sleep, readiness, fatigue, mood).
- **Workout Library**: Browse workout folders and structured training library workouts.
- **Semantic Tool Routing**: Optional embedding-based tool discovery using `fastembed` for minimal context overhead.
- **ContextForge Gateway Support**: Built-in support for IBM ContextForge Gateway SSE transport.

## Installation

### Local Editable Install

Clone the repository and install in editable mode:

```bash
git clone https://github.com/jelmervdm/intervals.icu-mcp.git
cd intervals.icu-mcp
pip install -e ".[dev,router]"
```

### Container Deployment (Podman / Docker)

Pull pre-built image or build locally:

```bash
podman pull ghcr.io/jelmervdm/intervals.icu-mcp:latest
```

---

## Configuration

Set the following environment variables:

| Variable | Description | Default |
|---|---|---|
| `INTERVALS_API_KEY` | Your Intervals.icu API key (Required) | - |
| `INTERVALS_ATHLETE_ID` | Athlete ID | `0` (authenticated user) |
| `INTERVALS_BASE_URL` | Intervals.icu API base URL | `https://intervals.icu/api/v1` |
| `TOOL_ROUTING` | Enable fastembed semantic tool discovery | `false` |
| `ENABLE_CONTEXTFORGE_GATEWAY` | Enable IBM ContextForge SSE gateway on port 8000 | `false` |

### Obtaining your API Key

1. Log into your account at [Intervals.icu](https://intervals.icu).
2. Go to **Settings** -> **API Access**.
3. Copy your API Key.

---

## Usage with VS Code, Antigravity IDE & Claude Desktop

Add to your `.vscode/mcp.json` or MCP configuration file (`"servers"` for VS Code / Antigravity IDE, or `"mcpServers"` for Claude Desktop):

### Option 1: Docker / Podman

Podman is fully supported on Fedora/RHEL as a rootless drop-in replacement for Docker:

```json
{
  "servers": {
    "intervals": {
      "command": "podman",
      "args": [
        "run", "-i", "--rm", "--pull=newer",
        "-e", "INTERVALS_API_KEY",
        "-e", "INTERVALS_ATHLETE_ID",
        "ghcr.io/jelmervdm/intervals.icu-mcp:latest"
      ],
      "env": {
        "INTERVALS_API_KEY": "your_api_key_here",
        "INTERVALS_ATHLETE_ID": "0"
      }
    }
  }
}
```

> **Tip for Docker vs Podman**: Replace `"command": "podman"` with `"command": "docker"` if using standard Docker or `podman-docker`. Always use `-i` (interactive stdin) and **never** `-t` (TTY) to avoid formatting corruption over stdio.

### Option 2: Local Python Execution (without PyPI)

**Via `uv` (local workspace directory):**
```json
{
  "servers": {
    "intervals": {
      "command": "uv",
      "args": ["--directory", "/path/to/intervals.icu-mcp", "run", "intervals-icu-mcp-server"],
      "env": {
        "INTERVALS_API_KEY": "your_api_key_here",
        "INTERVALS_ATHLETE_ID": "0"
      }
    }
  }
}
```

**Via `python` (editable install `pip install -e .`):**
```json
{
  "mcpServers": {
    "intervals": {
      "command": "python",
      "args": ["-m", "intervals_mcp.server"],
      "env": {
        "INTERVALS_API_KEY": "your_api_key_here",
        "INTERVALS_ATHLETE_ID": "0"
      }
    }
  }
}
```

**Via `uvx` directly from GitHub repository:**
```json
{
  "mcpServers": {
    "intervals": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/jelmervdm/intervals.icu-mcp.git", "intervals-icu-mcp-server"],
      "env": {
        "INTERVALS_API_KEY": "your_api_key_here",
        "INTERVALS_ATHLETE_ID": "0"
      }
    }
  }
}
```

## Available Tools

### Athlete Tools
- `get_athlete_profile(athlete_id="0")`: Retrieve athlete profile, FTP, zones, and settings.

### Activity Tools
- `list_activities(oldest, newest, athlete_id="0")`: List activities in a date range (YYYY-MM-DD).
- `get_activity(activity_id)`: Retrieve detailed metrics for a specific activity.
- `update_activity(activity_id, name, description, type, gear)`: Update activity details.
- `delete_activity(activity_id)`: Delete an activity.
- `list_activity_messages(activity_id)`: Retrieve activity comments/messages.
- `add_activity_message(activity_id, text)`: Post a comment/note to an activity.

### Calendar & Event Tools
- `list_events(oldest, newest, athlete_id="0")`: List calendar events and planned workouts.
- `get_event(event_id, athlete_id="0")`: Fetch details of a planned workout or event.
- `create_event(start_date_local, name, description, type, category, athlete_id="0")`: Plan a workout or event.
- `update_event(event_id, start_date_local, name, description, athlete_id="0")`: Update a planned event.
- `delete_event(event_id, athlete_id="0")`: Delete a calendar event.

### Wellness Tools
- `list_wellness(oldest, newest, athlete_id="0")`: List daily wellness entries.
- `get_wellness(date, athlete_id="0")`: Fetch wellness record for a date (YYYY-MM-DD).
- `update_wellness(date, weight, resting_hr, hrv, sleep_secs, readiness, fatigue, mood, comments, athlete_id="0")`: Update wellness metrics.

### Workout Library Tools
- `list_workout_folders(athlete_id="0")`: List folders in the workout library.
- `list_workouts(folder_id, athlete_id="0")`: List structured library workouts.

---

## AI Coaching Skills

For AI agents acting as endurance coaches, this MCP server pairs directly with the [Athletic Performance Coaching Skills](https://github.com/jelmervdm/skills) repository.

While `intervals.icu-mcp` provides data access (activity streams, daily wellness, calendar planning, and workout library management), `jelmervdm/skills` provides physiological rules, workout analysis workflows, and evidence-based training prescription guardrails for AI assistants.

### Available Skills in [jelmervdm/skills](https://github.com/jelmervdm/skills)

- **[Cycling](https://github.com/jelmervdm/skills/tree/main/coach/cycling)**: Coggan power/HR zones, aerobic decoupling ($P\text{:}HR$), interval compliance scoring, periodization, and race pacing.
- **[Running](https://github.com/jelmervdm/skills/tree/main/coach/running)**: Jack Daniels VDOT pacing formulas, cadence dynamics, Grade-Adjusted Pace (GAP), rTSS, and race strategies.
- **[Swimming](https://github.com/jelmervdm/skills/tree/main/coach/swimming)**: Critical Swim Speed (CSS), SWOLF stroke efficiency, send-off clocks, and open-water drafting.
- **[Triathlon](https://github.com/jelmervdm/skills/tree/main/coach/triathlon)**: Multi-sport stress balancing ($\text{TSS} + \text{rTSS} + \text{sTSS}$), brick workout design, and T1/T2 transition execution.
- **[Ironman](https://github.com/jelmervdm/skills/tree/main/coach/ironman)**: Long-course 70.3/140.6 pacing budgets, high-carb gut training ($80\text{--}120\text{g/hr}$), special needs strategy, and 21-day tapers.
- **[Cross-Country Skiing](https://github.com/jelmervdm/skills/tree/main/coach/xc-skiing)**: Skate & Classic subtechnique kinematics (V1/V2, Diagonal, Double Poling), dryland roller skiing, and marathon ski pacing.
- **[Weight Training](https://github.com/jelmervdm/skills/tree/main/coach/weight-training)**: RIR/RPE autoregulation, strength/hypertrophy mesocycles, and concurrent endurance training integration.

---

## Development

```bash
git clone https://github.com/jelmervdm/intervals.icu-mcp.git
cd intervals.icu-mcp
pip install -e ".[dev,router]"
pytest tests/ -v
```

## License

[Apache-2.0 License](LICENSE)

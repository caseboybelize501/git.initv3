# git.initv3

**Autonomous Repo Harvester & Idea Deployment Engine**

A self-aware automation loop that watches your GitHub repositories, detects net-new projects, validates architectures through a multi-model ring, gates every elevation through explicit user approval, and ships ideas to free-tier hosting — with zero redundancy against your existing C:\ and D:\ asset ecosystem.

## The Problem

Most developers accumulate GitHub repositories faster than they can scaffold, deploy, or validate them. The gap between having an idea checked into a repo and having a running, hosted proof-of-concept is filled with repetitive overhead that nobody has automated end-to-end.

## The Solution

A single coherent system that treats your local asset inventory as the canonical starting point for every decision:

- **GitHub Watcher** → polls GitHub REST API for repositories
- **Job Emitter** → detects new projects and emits events
- **Master LLM Planner** → generates architecture plans
- **Validator Ring** → 3 specialist models validate the plan
- **Adjudicator** → final ruling on plan approval
- **Permission Gate** → explicit user approvals required
- **Deployment Agent** → scaffolds and deploys to free-tier hosting

## Architecture


┌─────────────────────────────────────────────────────────────┐
│  PHASE 1 — LOCAL MODEL INVENTORY                           │
│  → Walk C:\ and D:\ recursively                            │
│  → Match: .gguf .ggml .safetensors .bin .onnx .pt .pth (>100MB) │
│  → sha256(first 4KB + file size) → dedup index keyed by hash │
│  → Register: { hash, path, size_gb, format, detected_at }   │
│                                                             │
│  PHASE 2 — INFERENCE SERVER PROBE                          │
│  → HTTP GET: :11434/api/tags (Ollama), :8000/:1234/v1/models │
│  → Parse available model list, measure response_ms         │
│  → Register: { port, provider, models[], response_ms, alive: bool}│
│                                                             │
│  PHASE 3 — TOOL INVENTORY                                  │
│  → which/where: node, python3, git, docker, pnpm, bun, npm │
│  → For each found: version string, full path               │
│  → Register: { tool, version, path, in_path: bool }        │
│                                                             │
│  PHASE 4 — PORT REGISTRY (collision prevention baseline)   │
│  → netstat -an → extract all LISTEN entries                │
│  → Register: { port, pid, process_name }                   │
│  → This registry is checked by every agent before any bind()│
│                                                             │
│  PHASE 5 — KNOWN REPOS REGISTER                            │
│  → Load known_repos.json (create empty on first run)      │
│  → Structure: { repo_name, url, detected_at, job_status,   │
│                 plan_id, deploy_url }                       │
│  → This is the delta-detection baseline for WatcherAgent   │
│                                                             │
│  → Write SystemInventory.json → VALIDATE → unlock agents  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  WATCHER LOOP (continuous, configurable interval)          │
│  → GET /users/caseboybelize501/repos?per_page=100&sort=updated │
│  → Parse: name, url, description, language, topics[], updated_at │
│  → For each repo: check known_repos.json                   │
│    → FOUND   → skip (already processed)                    │
│    → NOT FOUND → emit repo_detected event → queue for Gate A │
│                                                             │
│  GATE A — USER PERMISSION (pre-planning)                   │
│  → Surface to GUI: repo name + description                 │
│  → Show: SystemInventory summary                           │
│  → Show: which local assets will be considered for reuse   │
│  → User action: APPROVE → proceed to PlannerAgent          │
│                 SKIP    → add to known_repos, never re-trigger │
│                                                             │
│  PLANNER (Master LLM — post Gate A)                        │
│  → Read SystemInventory (mandatory, before any decision)   │
│  → Generate plan JSON: stack, modules, deployment_target,  │
│    local_assets_reused, ports_required, integration_points │
│  → Store in plans/{project_id}.json                        │
│  → Emit plan_ready event to Validator Ring                 │
│                                                             │
│  VALIDATOR RING (parallel execution)                       │
│  → ArchitectureValidator  → reviewer_feedback/arch_{id}.json │
│  → DeploymentValidator    → reviewer_feedback/deploy_{id}.json │
│  → SecurityValidator      → reviewer_feedback/security_{id}.json │
│                                                             │
│  ADJUDICATOR (Master LLM — collects all 3 feedbacks)       │
│  → ALL 3 APPROVED       → plan_status: approved → trigger Gate B │
│  → 1-2 REJECTED         → revision cycle (max 3) → re-validate │
│  → ALL 3 REJECTED       → plan_status: failed → notify user │
│  → Any confidence < 0.6 → flag to user even if APPROVED    │
│                                                             │
│  GATE B — USER PERMISSION (pre-deployment)                 │
│  → Surface to GUI: full validated plan document            │
│  → Show: selected free-tier host + justification           │
│  → Show: ports that will be used (confirmed vs active_ports)│
│  → User action: APPROVE → proceed to DeploymentAgent       │
│                 CANCEL  → plan archived, no deployment     │
│                                                             │
│  DEPLOYMENT AGENT (post Gate B)                            │
│  → Generate scaffold from plan (no LLM — template-based)   │
│  → git push to repo                                        │
│  → Configure host platform via CLI/API                     │
│  → Update known_repos.json: { job_status: deployed, deploy_url } │
└─────────────────────────────────────────────────────────────┘

## Features

- ✅ Self-aware system that scans local assets before any action
- ✅ Multi-model validation ring (Architecture, Deployment, Security)
- ✅ Explicit user permission gates for all decisions
- ✅ Free-tier hosting deployment engine
- ✅ Zero redundancy against existing C:\ and D:\ asset ecosystem
- ✅ End-to-end automation from observation to deployment

## Requirements

- Python 3.10+
- Docker (for containerized deployment)

## Installation

bash
# Clone the repository
$ git clone https://github.com/caseboybelize501/git.initv3.git
$ cd git.initv3

# Install dependencies
$ pip install -r requirements.txt

# Run the application
$ python src/main.py


## Usage

The system will automatically:

1. Scan your local C:\ and D:\ drives for models, tools, and running servers
2. Monitor GitHub repositories for new projects
3. Validate each project through a multi-model validation ring
4. Request user approval before proceeding with deployment
5. Deploy to free-tier hosting platforms

## License

MIT
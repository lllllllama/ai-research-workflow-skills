# Routing Policy

This repository uses RigorPilot display modes plus explicit research lanes to keep skill routing predictable and safe.

## Default stance

Route ambiguous requests to the trusted lane by default.

Do not route to exploration unless the user clearly authorizes speculative trial work.

Use `agent-operating-principles.md` as the shared posture: think before acting,
keep the solution small, change only what is necessary, and work toward
verifiable goals. These principles guide lane choice without forcing a fixed
implementation sequence.

## Lifecycle model

Route by the user's current lifecycle need before choosing a concrete skill.
RigorPilot short modes are display names and future aliases; current installs
still use the compatible skill slugs.

| Lifecycle need | RigorPilot display name | Short mode | Compatible skill slug |
|---|---|---|---|
| Understand a repository without heavy execution | Rigor Analyze | `rigor-analyze` | `analyze-project` |
| Reproduce a README-documented repository end to end | Rigor Reproduce | `rigor-reproduce` | `ai-research-reproduction` |
| Prepare environment, assets, checkpoints, or caches | Rigor Setup | `rigor-setup` | `env-and-assets-bootstrap` |
| Run documented inference or evaluation | Rigor Run | `rigor-run` | `minimal-run-and-audit` |
| Start, resume, or verify training | Rigor Train | `rigor-train` | `run-train` |
| Diagnose an active research-code failure | Rigor Debug | `rigor-debug` | `safe-debug` |
| Explore candidates on top of `current_research` | Rigor Explore / Rigor Improve | `rigor-explore`, `rigor-improve` | `ai-research-explore`, `explore-code`, or `explore-run` |
| Report or package evidence | Rigor Audit | `rigor-audit` | the skill that owns the active output directory |

## Trusted lane

Trusted-lane skills are for:

- README-first paper reproduction
- repository analysis and code familiarization
- environment and asset preparation
- conservative run verification
- training execution requested by the researcher
- safe research debugging

Current trusted public skills:

- Rigor Reproduce: `ai-research-reproduction`
- Rigor Setup: `env-and-assets-bootstrap`
- Rigor Run: `minimal-run-and-audit`
- Rigor Analyze / Rigor Audit: `analyze-project`
- Rigor Train: `run-train`
- Rigor Debug / Rigor Audit: `safe-debug`

Traits:

- preserve scientific meaning
- minimize unreviewed code changes
- write durable audit outputs
- surface assumptions, deviations, and blockers

## Explore lane

Explore-lane skills are for:

- end-to-end exploratory work on top of `current_research`
- meaningful and potentially novel candidate hypotheses
- broad-sweep experiments
- low-cost speculative variants
- isolated branch or worktree modifications
- migration-learning style adaptation attempts
- summary-oriented result ranking

Current explore public skills:

- Rigor Explore: `ai-research-explore`
- Rigor Improve: `explore-code`
- Rigor Improve / Rigor Explore: `explore-run`

The explore lane follows a two-loop rhythm:

- outer loop: understand the repository, freeze task/evaluation/budget, map
  sources, gate ideas, and decide whether a candidate is worth trying
- inner loop: make one bounded candidate change or run, smoke-check it, collect
  evidence, rank it, then stop or return to the outer loop

This is not a never-stop autonomous research policy. Stop at blockers, missing
anchors, unclear scientific meaning, exhausted budget, or human checkpoints.
Novelty and significance remain hypotheses until supported by literature
contrast, ablation evidence, and fair comparison.

Explore-lane requests should usually contain signals such as:

- "try a batch"
- "sweep"
- "see what works"
- "idle GPU"
- "broad search"
- "explore"
- "try several variants"
- "current_research"
- "on top of the current research"
- "coordinate code and run exploration"

## Helper lane

Helper skills are narrow and should not dominate routing when a public trusted-lane skill is a better fit.

Helpers should mostly be:

- orchestrator-invoked
- explicitly named by the user
- used only when the request is clearly narrower than a public skill

Current helper skills:

- Rigor Intake: `repo-intake-and-plan`
- Rigor Paper Context: `paper-context-resolver`

## Safety rules

- Trusted skills must not auto-route into exploration.
- Exploration must not silently claim trusted reproduction success.
- Peer leaf skills should not call each other directly.
- End-to-end orchestration should happen through the public orchestrator skill for the relevant task family.


#!/usr/bin/env python3
"""Regression checks for neutral, Codex, and Claude Code installer target resolution."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from install_skills import default_target, install_skills


SHARED_REFERENCE_REFS = [
    "../../references/agent-operating-principles.md",
    "../../references/research-rigor-principles.md",
    "../../references/deep-learning-experiment-principles.md",
]


def assert_shared_references_resolve(installed: list[Path]) -> None:
    checked: dict[str, int] = {ref: 0 for ref in SHARED_REFERENCE_REFS}
    for skill_path in installed:
        skill_text = (skill_path / "SKILL.md").read_text(encoding="utf-8")
        for ref in SHARED_REFERENCE_REFS:
            if ref not in skill_text:
                continue
            checked[ref] += 1
            reference_path = (skill_path / ref).resolve()
            if not reference_path.exists():
                raise AssertionError(f"shared reference {ref} does not resolve for {skill_path.name}")
    if checked["../../references/agent-operating-principles.md"] == 0:
        raise AssertionError("installer test did not find any skill using the shared operating principles reference")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    temp_root = Path(tempfile.mkdtemp(prefix="codex-install-targets-", dir=repo_root))
    try:
        codex_home = temp_root / "codex-home"
        claude_home = temp_root / "claude-home"
        agents_home = temp_root / "agents-home"
        fake_home = temp_root / "fake-home"

        agents_target = default_target("agents", env={"AGENTS_HOME": str(agents_home)}, home=fake_home)
        codex_target = default_target("codex", env={"CODEX_HOME": str(codex_home)}, home=fake_home)
        claude_target = default_target("claude", env={"CLAUDE_HOME": str(claude_home)}, home=fake_home)
        fallback_agents_target = default_target("agents", env={}, home=fake_home)
        fallback_claude_target = default_target("claude", env={}, home=fake_home)

        if agents_target != (agents_home / "skills").resolve():
            raise AssertionError("agents target resolution ignored AGENTS_HOME")
        if codex_target != (codex_home / "skills").resolve():
            raise AssertionError("codex target resolution ignored CODEX_HOME")
        if claude_target != (claude_home / "skills").resolve():
            raise AssertionError("claude target resolution ignored CLAUDE_HOME")
        if fallback_agents_target != (fake_home / ".agents" / "skills").resolve():
            raise AssertionError("agents fallback target did not resolve to ~/.agents/skills")
        if fallback_claude_target != (fake_home / ".claude" / "skills").resolve():
            raise AssertionError("claude fallback target did not resolve to ~/.claude/skills")

        installed = install_skills(repo_root, temp_root / "installed-skills", mode="copy", force=False)
        if len(installed) != len(list((repo_root / "skills").glob("*/SKILL.md"))):
            raise AssertionError("installer did not copy the full skill set")
        if not all((path / "SKILL.md").exists() for path in installed):
            raise AssertionError("installer lost SKILL.md during copy")
        for filename in [
            "agent-operating-principles.md",
            "research-rigor-principles.md",
            "deep-learning-experiment-principles.md",
        ]:
            shared_reference = temp_root / "references" / filename
            if not shared_reference.exists():
                raise AssertionError(f"installer did not copy the shared reference {filename}")
        assert_shared_references_resolve(installed)

        print("ok: True")
        print("checks: 9")
        print("failures: 0")
        return 0
    finally:
        if temp_root.exists():
            shutil.rmtree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Builds avengers-assemble.zip for the Claude app: the skill folder at the root of the zip, with the
four hero files in heroes/ so the skill can play each hero there (the Claude app doesn't run agents)."""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "skills" / "avengers-assemble"
AGENTS = ROOT / "agents"
OUT = ROOT / "avengers-assemble.zip"
FIXED_TIME = (2026, 10, 9, 0, 0, 0)  # same bytes every build


def _add(z: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    z.writestr(info, data)


def build(out: Path = OUT) -> Path:
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file() and path.name != ".DS_Store":
                _add(z, f"avengers-assemble/{path.relative_to(SKILL).as_posix()}", path.read_bytes())
        for path in sorted(AGENTS.glob("*.md")):
            _add(z, f"avengers-assemble/heroes/{path.name}", path.read_bytes())
    return out


if __name__ == "__main__":
    print(build())

import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
SKILL = ROOT / "skills" / "avengers-assemble" / "SKILL.md"
HEROES = {"spidey-researcher", "iron-builder", "hulk-tester", "thor-reviewer"}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "Bash", "PowerShell"}


def front(path: Path) -> dict:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path.name} has no frontmatter"
    out = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


def tools(path: Path) -> set:
    return {t.strip() for t in front(path).get("tools", "").split(",") if t.strip()}


class TheTeam(unittest.TestCase):
    def test_five_heroes_four_agents(self):
        names = {p.stem for p in AGENTS.glob("*.md")}
        self.assertEqual(names, HEROES)
        for p in AGENTS.glob("*.md"):
            self.assertEqual(front(p)["name"], p.stem)

    def test_every_hero_has_an_explicit_tool_list(self):
        # An agent with no tools line inherits every tool, Agent included.
        for p in AGENTS.glob("*.md"):
            self.assertTrue(tools(p), f"{p.name} must list its tools")

    def test_thor_has_no_edit_tools(self):
        t = tools(AGENTS / "thor-reviewer.md")
        self.assertFalse(t & EDIT_TOOLS, f"Thor can edit with {t & EDIT_TOOLS}")
        self.assertEqual(t, {"Read", "Grep", "Glob"})

    def test_spidey_is_read_only(self):
        self.assertFalse(tools(AGENTS / "spidey-researcher.md") & EDIT_TOOLS)

    def test_only_iron_man_can_write(self):
        for p in AGENTS.glob("*.md"):
            can_write = bool(tools(p) & {"Edit", "Write"})
            self.assertEqual(can_write, p.stem == "iron-builder", p.name)

    def test_no_hero_can_call_another(self):
        for p in AGENTS.glob("*.md"):
            self.assertFalse(tools(p) & {"Agent", "Task"}, p.name)

    def test_skill_names_every_hero(self):
        text = SKILL.read_text()
        for name in HEROES:
            self.assertIn(f"`{name}`", text)

    def test_skill_rules(self):
        text = SKILL.read_text()
        self.assertIn("Small job, so no team needed", text)
        self.assertIn("uses more of your Claude plan", text)
        self.assertIn("Never send Thor the plan", text)
        self.assertIn("Three Thor rounds at most", text)
        self.assertIn("before the first hero call, every time", text)

    def test_descriptions_fit_the_claude_app(self):
        d = front(SKILL)["description"]
        self.assertLessEqual(len(d), 200, len(d))
        self.assertEqual(front(SKILL)["name"], "avengers-assemble")


class ThePackage(unittest.TestCase):
    def test_manifests(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.assertEqual(plugin["name"], "avengers-assemble")
        self.assertEqual(market["plugins"][0]["name"], "avengers-assemble")
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_zip_is_current(self):
        sys.path.insert(0, str(ROOT))
        from make_zip import build
        with tempfile.TemporaryDirectory() as tmp:
            fresh = build(Path(tmp) / "fresh.zip").read_bytes()
        self.assertEqual(fresh, (ROOT / "avengers-assemble.zip").read_bytes(),
                         "avengers-assemble.zip is stale: run python3 make_zip.py")

    def test_zip_layout(self):
        with zipfile.ZipFile(ROOT / "avengers-assemble.zip") as z:
            names = set(z.namelist())
        self.assertIn("avengers-assemble/SKILL.md", names)
        for hero in HEROES:
            self.assertIn(f"avengers-assemble/heroes/{hero}.md", names)

    def test_claude_plugin_validate(self):
        try:
            r = subprocess.run(["claude", "plugin", "validate", str(ROOT)], capture_output=True, text=True, timeout=60)
        except FileNotFoundError:
            self.skipTest("claude CLI not installed")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()

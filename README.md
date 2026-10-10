# Avengers Assemble

Give Claude a big job and say "avengers assemble." Claude stops doing everything alone and leads a
team of five:

| Hero | Job |
|---|---|
| **Captain America** | The leader. Reads the job, splits it up, calls in only the heroes it needs, runs the parts that don't depend on each other at the same time, and writes the final answer. |
| **Spider-Man** | Researches the web. Every fact comes back with a link. Can't change anything. |
| **Iron Man** | Builds it, and shows what he made and how he checked it works. |
| **Hulk** | Tries to smash and break it, like your clumsiest customer. Reports what broke, with the steps. Doesn't fix. |
| **Thor** | Gives the final judgement. He gets only the finished work and one line on who it's for, never the plan, and he has no edit tools at all. Nothing ships until it's **worthy**. Anything he flags goes back to Iron Man, then back to Thor. |

Free, MIT, no signup, no API key, nothing to connect.

## Install

**Claude Code.** Paste this into Claude Code:

```
https://github.com/JoeBrunner/avengers-assemble

install the skill
```

Claude installs it as a plugin: the skill and the four hero agents together. Or run the same two
lines yourself in Claude Code:

```
/plugin marketplace add JoeBrunner/avengers-assemble
/plugin install avengers-assemble@avengers-assemble
```

**The Claude app** (claude.ai or the desktop app). Download
[avengers-assemble.zip](https://github.com/JoeBrunner/avengers-assemble/raw/main/avengers-assemble.zip),
then in Claude go to **Customize > Skills**, click **+**, then **Create skill > Upload a skill**, and
pick the zip. Skills need "Code execution and file creation" turned on in **Settings > Capabilities**.
The app doesn't run agents, so there one Claude plays each hero in turn (the table below).

**By hand**, if that's how you like it:

```bash
git clone https://github.com/JoeBrunner/avengers-assemble.git
cp -r avengers-assemble/skills/avengers-assemble ~/.claude/skills/
cp avengers-assemble/agents/*.md ~/.claude/agents/
```

### Notes for Claude, if you're installing this for someone

Avengers Assemble is one package: the skill (Captain America's playbook) and four agents (the other
heroes) ship together as a Claude Code plugin. The skill alone can't call the team. So when someone
pastes this link and asks you to install the skill, install the plugin:

```bash
claude plugin marketplace add JoeBrunner/avengers-assemble
claude plugin install avengers-assemble@avengers-assemble
```

What it adds, so you can check before you run anything: `skills/avengers-assemble/SKILL.md` and four
agent files in `agents/`. No hooks, no scripts, no network calls of its own, no API key. Afterward,
tell them what you installed, to run `/reload-plugins` (or restart Claude Code), that "avengers
assemble" plus a big job starts it, and that
`claude plugin uninstall avengers-assemble@avengers-assemble` removes it. If the `claude` command
isn't available, copy `skills/avengers-assemble` into `~/.claude/skills/` and the four files in
`agents/` into `~/.claude/agents/`.

### What you get where

| | Claude Code plugin (or copied by hand) | Claude app |
|---|---|---|
| Captain America splits the job and leads | Yes | Yes |
| Each hero is a separate Claude with its own job | Yes | No, one Claude plays each hero in turn |
| Independent parts run at the same time | Yes | No, one after another |
| Thor can't edit anything | Yes, he has no edit tools | A promise, not a lock |
| Thor never sees the plan | Yes, his brief is only the work and one line | He's told to judge it cold |
| Small jobs skip the team | Yes | Yes |

## Use it

```
avengers assemble: build a one-page website for my donut shop
```

Captain America says who he's calling and why, hands out the mission cards, and runs the team. You
get one short answer at the end: what was made and where, Thor's verdict, what Hulk broke and what
Iron Man fixed, the facts used with their links, what only you can do, and which heroes ran.

## Honest about cost

A team uses more of your Claude plan than one Claude does: every hero is its own run. So:

- **Small jobs stay with one Claude.** Ask the team to fix a typo and Captain America says "Small job,
  so no team needed" and just does it.
- **Only the heroes the job needs.** No research needed, no Spider-Man. Nothing a customer would use,
  no Hulk.
- **It tells you up front** who it's calling, before anyone starts.
- **Three Thor rounds at most.** If it still isn't worthy, it stops and tells you what's left, instead
  of looping on your plan.
- Spider-Man and Hulk run on Sonnet to save your plan; Iron Man and Thor use the same model as your
  session.

## How Thor stays honest

Most "team of agents" setups let the agent that did the work grade it. Thor can't be talked into
"looks good": his agent file gives him only `Read`, `Grep` and `Glob`, so he can look at the work but
can't change a word of it, and Captain America's playbook sends him only the finished work and one
line on who it's for. If he says NOT WORTHY, only Iron Man fixes it, and Thor checks again.

Hulk has `Bash` so he can actually run what was built. He's told never to edit the work, and he
writes nothing outside a temporary folder; that rule is in his instructions, not a lock.

## Tests

```bash
python3 -m unittest discover -s tests
```

They check that Thor has no edit tools, that only Iron Man can write, that no hero can call another,
that every hero the playbook names exists, and that the Claude app zip is current.

## License

MIT. See [LICENSE](LICENSE). A fan-made name and theme; not affiliated with or endorsed by Marvel or
Disney.

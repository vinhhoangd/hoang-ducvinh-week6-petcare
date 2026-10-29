"""Week 6 team sync: shared checklist page <-> project folder <-> GitHub.

Used by the hourly "Week 6 team sync" scheduled task. Only the exact,
repeatable steps live here; the task itself reads and writes the page's
database with the ArtifactData tool.

    python3 tools/team_sync.py pull
    python3 tools/team_sync.py sync --run RUN_DIR

RUN_DIR must contain:
    page/files/*.json   the page's "files" collection (ArtifactData list, out_dir)
    ticks/ticks/*.json  the page's "ticks" collection (ArtifactData list, out_dir)
    versions.json       {"files/<doc_id>": <version>, "ticks/<doc_id>": <version>} from the list outputs

`sync` then:
 1. copies page edits (changed=true) into project-workspace/, unless the
    same file also changed on GitHub since the page copy was made (conflict);
 2. merges ticks both ways: page ticks <-> the [x] boxes in WEEK6-CHECKLIST.md
    (only the boxes are flipped; people's notes in that file are kept), using
    tools/sync_state.json to tell a new tick from an untick;
 3. lists blanks still left in the required files;
 4. refuses to commit if the Census key appears in any staged file;
 5. commits and pushes (fast-forward only, never force);
 6. writes RUN_DIR/page_batch.json: page writes for ArtifactData batch.
It never writes predictions, results, or anyone's own-words answers, never
touches .env, and never deletes a file.
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WS = REPO / "project-workspace"
ENV = WS / ".env"
CHECKLIST_MD = REPO / "WEEK6-CHECKLIST.md"
STATE = REPO / "tools" / "sync_state.json"
BOX = re.compile(r"^(- \[)( |x|X)(\] )(\*\*\[([VYST])\]\*\* )?(.*)$")
SECTION_OWNER = {"## Vinh's list": "V", "## Yuhe's list": "Y", "## Shiming's list": "S"}
DATA = json.loads((REPO / "tools" / "checklist.json").read_text())

# Files the page may add when they appear on GitHub (text only; never code, data, or keys).
ADI501 = {"evidence/source-quality-adoption.md", "evidence/governance-controls.md",
          "evidence/model-risk-note.md", "evidence/pilot-recommendation.md"}
REQUIRED = ["evidence/decision-frame.md", "evidence/tool-check.md", "ai-use-log.md", "completed-workbook.md",
            "evidence/claim-ledger.csv", "evidence/notebooklm-transcript.md", "evidence/model-card.md",
            "evidence/failure-recovery-log.md", "evidence/transfer-trial.md", "decision-brief.md", "README.md",
            "team-agreement.md", "team-contributions.md", "evidence/demo-checklist.md"]
BLANK_PATTERNS = [(r"_{4,}", "blank ____"), (r"^\|(\s*\|)+\s*$", "empty table row"), (r"Example only", "example row"),
                  (r"\(your answer here\)", "(your answer here)"), (r"^>\s*$", "empty > line"),
                  (r"^\*\([^)]*\)\*$|\*\(Filled in after", "placeholder note"), (r"^EX[12],", "example ledger row")]


def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def key_value():
    if not ENV.exists():
        return None
    for line in ENV.read_text().splitlines():
        if line.startswith("CENSUS_API="):
            return line.split("=", 1)[1].strip() or None
    return None


def doc_id(path):
    return path.replace("/", "~")


def group_for(path):
    if path.startswith(("sample-data/", "seeded-ai-briefs/", "data/raw/")) or path in ("api-manifest.md", "requirements.txt"):
        return "Reference (read-only)", False
    if path.endswith("/README.md") and path.count("/") >= 1 and not path.startswith("evidence/"):
        return "Reference (read-only)", False
    return ("Evidence" if path.startswith("evidence/") else "Deliverables"), True


def addable(path):
    """Text files the page may show. Never code, .env, the venv, or ADI501-only templates."""
    if path in ADI501 or ".venv/" in path or path.startswith(".") or "/." in path:
        return False
    if path.startswith("data/raw/") or path.startswith("data/clean/"):
        return False
    return path.endswith(".md") or (path.endswith(".csv") and path.startswith("evidence/"))


def cmd_pull(_):
    if git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("STOP: the project folder has uncommitted changes. Commit or ask Vinh before syncing.")
    out = git("pull", "--ff-only", check=False)
    print(out or "pulled")
    print("HEAD", git("rev-parse", "--short", "HEAD"))


def match_md_lines(lines):
    """Map each checkbox line in WEEK6-CHECKLIST.md to a checklist item id (fuzzy on the
    text before ' — ', within the owner's items). Unmatched lines are left alone."""
    owner, out = None, {}
    for n, line in enumerate(lines):
        if line.startswith("## "):
            owner = next((o for h, o in SECTION_OWNER.items() if line.startswith(h)), None)
        m = BOX.match(line)
        if not m:
            continue
        who = m.group(5) or owner
        text = m.group(6).split(" — ")[0].strip().lower()
        cands = [i for i in DATA["items"] if who is None or i["owners"] == who]
        best = max(cands, key=lambda i: difflib.SequenceMatcher(None, text, i["text"].lower()).ratio(), default=None)
        if best and difflib.SequenceMatcher(None, text, best["text"].lower()).ratio() >= 0.55:
            out[n] = best["id"]
    return out


def md_done(lines, mapping):
    by_id = {}
    for n, iid in mapping.items():
        by_id.setdefault(iid, []).append(BOX.match(lines[n]).group(2).lower() == "x")
    return {iid for iid, boxes in by_id.items() if all(boxes)}


def write_md_boxes(lines, mapping, done):
    changed = False
    for n, iid in mapping.items():
        m = BOX.match(lines[n])
        want = "x" if iid in done else " "
        if m.group(2).lower() != want:
            lines[n] = m.group(1) + want + lines[n][len(m.group(1)) + 1:]
            changed = True
    total = len(DATA["items"])
    for n, line in enumerate(lines):
        if line.startswith("**Progress:"):
            new = f"**Progress: {len(done)} of {total} done.**"
            if line != new:
                lines[n], changed = new, True
    return changed


def blanks_report():
    out = {}
    for rel in REQUIRED:
        p = WS / rel
        if not p.exists():
            out[rel] = ["file not created yet"]
            continue
        hits = []
        for n, line in enumerate(p.read_text().splitlines(), 1):
            for pat, label in BLANK_PATTERNS:
                if label and re.search(pat, line, re.M):
                    hits.append(f"line {n}: {label}")
                    break
        if hits:
            out[rel] = hits
    return out


def cmd_sync(a):
    run = Path(a.run)
    versions = json.loads((run / "versions.json").read_text())
    page = {}
    for f in (run / "page" / "files").glob("*.json"):
        d = json.loads(f.read_text())
        page[d["path"]] = d
    page_ticks = {}
    tdir = run / "ticks" / "ticks"
    if tdir.exists():
        for f in tdir.glob("*.json"):
            d = json.loads(f.read_text())
            if d.get("done"):
                page_ticks[f.stem] = d
    lines = CHECKLIST_MD.read_text().splitlines() if CHECKLIST_MD.exists() else []
    mapping = match_md_lines(lines)
    in_md = md_done(lines, mapping)
    in_page = set(page_ticks)
    # First run (no state yet): nothing counts as an untick, so ticks from both sides are combined.
    last = set(json.loads(STATE.read_text())["done"]) if STATE.exists() else in_page & in_md
    # Only items that have a matching line in the file can be unticked from the file side;
    # an item whose line a person reworded or split must not count as unticked.
    md_ids = set(mapping.values())
    unticked = (last - in_page) | ((last & md_ids) - in_md)
    unticked -= (in_page - last) | (in_md - last)          # a fresh tick on one side wins over a stale untick
    done = ((in_page | in_md) - unticked) & {i["id"] for i in DATA["items"]}

    head = git("rev-parse", "--short", "HEAD")
    applied, conflicts, page_updates, added = [], [], [], []

    # 1. page edits -> project folder
    for path, d in sorted(page.items()):
        if not d.get("changed") or not d.get("editable"):
            continue
        target = WS / path
        repo_now = target.read_text() if target.exists() else None
        if repo_now == d["content"]:
            applied.append(path)            # already identical: just clear the page's dot
            continue
        m = re.match(r"repo ([0-9a-f]{7,40})", d.get("source", ""))
        base = git("show", f"{m.group(1)}:project-workspace/{path}", check=False) if m else None
        if repo_now is not None and (base is None or base.rstrip("\n") != repo_now.rstrip("\n")):
            conflicts.append(path)          # changed on both sides: leave both untouched
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(d["content"])
        applied.append(path)

    # 2. ticks both ways: flip boxes in WEEK6-CHECKLIST.md (notes kept), remember the merged set
    md_changed = write_md_boxes(lines, mapping, done)
    if md_changed:
        CHECKLIST_MD.write_text("\n".join(lines) + "\n")
    STATE.write_text(json.dumps({"done": sorted(done)}, indent=0))

    # 3/4/5. key scan, commit, push
    git("add", "-A")
    staged = git("diff", "--cached", "--name-only").splitlines()
    pushed = None
    if staged:
        key = key_value()
        leaked = [s for s in staged if s.endswith(".env") or (key and key in (REPO / s).read_text(errors="ignore"))]
        if leaked:
            git("reset", "-q")
            sys.exit(f"STOP: refusing to commit; the key or .env is in {len(leaked)} staged file(s). Nothing was committed.")
        who = ", ".join(sorted({p.split('/')[-1] for p in applied})) or "checklist"
        git("commit", "-q", "-m", f"Team sync: {who}\n\nCopied saved edits from the shared page and updated WEEK6-CHECKLIST.md "
            f"from the ticks ({len(done)}/{len(DATA['items'])} done).\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
        out = subprocess.run(["git", "-C", str(REPO), "push", "-q"], capture_output=True, text=True)
        if out.returncode != 0:
            # Someone pushed meanwhile: merge their commits once (never rebase or force), then retry.
            m = subprocess.run(["git", "-C", str(REPO), "pull", "--no-rebase", "--no-edit", "-q"], capture_output=True, text=True)
            if m.returncode != 0:
                subprocess.run(["git", "-C", str(REPO), "merge", "--abort"], capture_output=True)
                sys.exit("STOP: a teammate pushed changes that conflict with this sync. Merge aborted; nothing was pushed. "
                         "Vinh must resolve it by hand.")
            out = subprocess.run(["git", "-C", str(REPO), "push", "-q"], capture_output=True, text=True)
            if out.returncode != 0:
                sys.exit(f"STOP: push failed again (nothing forced): {out.stderr.strip()}")
        pushed = git("rev-parse", "--short", "HEAD")
        head = pushed

    # 6. page writes: clear dots on applied docs, refresh docs that changed on GitHub, add new text files
    batch, staging = [], run / "page_docs"
    staging.mkdir(exist_ok=True)

    def stage(path, content, rev):
        g, e = group_for(path)
        body = {"path": path, "group": g, "editable": e, "content": content, "rev": rev,
                "changed": False, "source": f"repo {head}"}
        fp = staging / f"{doc_id(path)}.json"
        fp.write_text(json.dumps(body))
        entry = {"op": "set", "collection": "files", "doc_id": doc_id(path), "file_path": str(fp)}
        if f"files/{doc_id(path)}" in versions:
            entry["if_version"] = versions[f"files/{doc_id(path)}"]
        batch.append(entry)

    for path in applied:
        stage(path, (WS / path).read_text(), page[path].get("rev", 0))
    for path, d in sorted(page.items()):
        if path in applied or path in conflicts or d.get("changed"):
            continue
        target = WS / path
        if target.exists() and target.read_text() != d["content"]:
            stage(path, target.read_text(), d.get("rev", 0) + 1)
            page_updates.append(path)
    tracked = [p[len("project-workspace/"):] for p in git("ls-files", "project-workspace").splitlines()]
    for path in tracked:
        if path not in page and addable(path):
            stage(path, (WS / path).read_text(), 0)
            added.append(path)
    ticks_added, ticks_removed = sorted(done - in_page), sorted(in_page - done)
    for iid in ticks_added:
        batch.append({"op": "set", "collection": "ticks", "doc_id": iid,
                      "data": {"done": True, "note": "Ticked in WEEK6-CHECKLIST.md on GitHub (team sync)"}})
    for iid in ticks_removed:
        batch.append({"op": "delete", "collection": "ticks", "doc_id": iid,
                      "if_version": versions.get(f"ticks/{iid}", 1)})
    (run / "page_batch.json").write_text(json.dumps(batch, indent=1))

    report = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "head": head, "pushed": pushed,
              "ticked": f"{len(done)}/{len(DATA['items'])}", "checklist_md_updated": md_changed,
              "ticks_added_to_page_from_github": ticks_added, "ticks_removed_from_page": ticks_removed,
              "md_lines_matched": len(mapping),
              "page_edits_copied_to_github": applied, "conflicts_left_untouched": conflicts,
              "page_files_refreshed_from_github": page_updates, "files_added_to_page": added,
              "page_batch_entries": len(batch), "blanks_left_in_required_files": blanks_report()}
    (run / "report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pull")
    s = sub.add_parser("sync")
    s.add_argument("--run", required=True)
    a = ap.parse_args()
    {"pull": cmd_pull, "sync": cmd_sync}[a.cmd](a)


if __name__ == "__main__":
    main()

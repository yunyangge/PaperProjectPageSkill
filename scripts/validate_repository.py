"""Check package metadata, local documentation links, and SVG well-formedness."""
from pathlib import Path
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "paper-project-page"
errors = []
text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
if not re.search(r"\A---\s*\nname: paper-project-page\s*\ndescription: .+?\n---", text, re.S):
    errors.append("Invalid skill frontmatter")
if "[TODO" in text or "[TBD" in text:
    errors.append("Unfinished skill scaffold")

required = ["README.md", "README.en.md", "LICENSE", "install_skill.py",
            "skills/paper-project-page/agents/openai.yaml"]
for filename in required:
    if not (ROOT / filename).is_file():
        errors.append("Missing required file: " + filename)

for doc in [ROOT / "README.md", ROOT / "README.en.md", *SKILL.rglob("*.md")]:
    body = doc.read_text(encoding="utf-8")
    targets = re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", body)
    targets += re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', body)
    for raw in targets:
        parsed = urllib.parse.urlsplit(raw)
        if parsed.scheme or raw.startswith("#"):
            continue
        target = (doc.parent / urllib.parse.unquote(parsed.path)).resolve()
        if not target.is_relative_to(ROOT):
            errors.append(f"Link leaves repository: {doc.relative_to(ROOT)} -> {raw}")
        elif not target.exists():
            errors.append(f"Broken local link: {doc.relative_to(ROOT)} -> {raw}")

for path in (ROOT / "assets").glob("*.svg"):
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        errors.append(f"Invalid SVG {path.name}: {exc}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("Package metadata, local file links, and SVG XML are valid.")
print("External links, anchor rendering, and generated websites require separate checks.")

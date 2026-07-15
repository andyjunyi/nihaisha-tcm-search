#!/usr/bin/env python3
"""Merge and deduplicate the search index, keeping formula composition entries."""
import json
from pathlib import Path

OUT_DIR = Path("/srv/projects/05 倪海廈中醫查詢")

# Load both
search = json.loads((OUT_DIR / "search_index.json").read_text())

# Deduplicate: keep entries with composition (longer content) for same formula name
seen = {}
deduped = []
removed = 0

for entry in search:
    title = entry.get("title", "").strip().strip("*")  # Remove markdown bold
    # Normalize traditional/simplified for matching
    title_simp = title
    
    if title_simp in seen:
        existing = seen[title_simp]
        # Keep the one with longer content (composition entries are longer)
        if len(entry.get("content", "")) > len(existing.get("content", "")):
            deduped.remove(existing)
            deduped.append(entry)
            seen[title_simp] = entry
            removed += 1
        else:
            removed += 1
    else:
        seen[title_simp] = entry
        deduped.append(entry)

# Also boost formula composition entries: add extra weight field
for entry in deduped:
    content = entry.get("content", "")
    if "**組成**" in content:
        entry["boost"] = 5  # Higher search ranking

# Write
out_path = OUT_DIR / "search_index.json"
out_path.write_text(json.dumps(deduped, ensure_ascii=False, indent=2))

print(f"Deduped: {len(search)} -> {len(deduped)} (removed {removed} duplicates)")

# Show formulas with composition
formulas = [s for s in deduped if "**組成**" in s.get("content", "")]
print(f"\nFormulas with composition: {len(formulas)}")
for f in formulas[:5]:
    print(f"  {f['title']}: {f['content'][:80]}...")

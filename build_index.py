#!/usr/bin/env python3
"""
Convert Ni Haixia reference markdown files into a searchable JSON index.
Improvements:
- Parse markdown tables into individual entries (one per formula/herb/etc.)
- Split clinical cases by lesson
- Better content formatting for display
"""
import json, re, os
from pathlib import Path

REF_DIR = Path("/home/andy/.hermes/skills/nihaisha/references")
OUT_DIR = Path("/srv/projects/05 倪海廈中醫查詢")

def fmt_name(filename: str) -> str:
    """Convert filename to a Chinese-friendly display name."""
    mapping = {
        'formula-patterns.md': '方劑方證總表',
        'symptom-index.md': '症狀索引',
        'six-channel.md': '六經辨證',
        'shanghanlun.md': '傷寒論',
        'clinical-cases.md': '臨床醫案',
        'bencao.md': '神農本草',
        'acupuncture.md': '針灸',
        'jingui.md': '金匱要略',
        'bagang.md': '八綱辨證',
        'fuyang.md': '扶陽論壇',
        'tianji.md': '天紀',
        'huangdi.md': '黃帝內經',
        'yijinjing.md': '易筋經',
        'liangdong.md': '梁冬對話',
        'stanford.md': '斯坦福演講',
        'zhongjing-xinfa.md': '仲景心法',
        'learning-entry.md': '學習入口',
        'beginner-questions.md': '初學者問答',
        'ebooks.md': '古籍溯源',
        'audio-collection.md': '音檔合集',
    }
    return mapping.get(filename, filename.replace('.md', ''))

def parse_table_rows(text: str, heading: str, filename: str) -> list[dict]:
    """Parse a markdown table into individual entries, one per row."""
    entries = []
    lines = text.split('\n')
    
    # Find table: lines starting with |
    table_lines = []
    in_table = False
    header = None
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and not stripped.startswith('|---'):
            if not in_table:
                in_table = True
                header = [c.strip() for c in stripped.split('|')[1:-1]]
                continue
            table_lines.append(stripped)
        else:
            if in_table and table_lines:
                # Process collected table
                entries.extend(_rows_to_entries(table_lines, header, heading, filename))
                table_lines = []
                header = None
                in_table = False
    
    # Don't forget last table
    if in_table and table_lines:
        entries.extend(_rows_to_entries(table_lines, header, heading, filename))
    
    return entries

def _rows_to_entries(rows: list[str], header: list[str] | None, heading: str, filename: str) -> list[dict]:
    """Convert table rows to search entries."""
    entries = []
    for row in rows:
        cols = [c.strip() for c in row.split('|')[1:-1]]
        if not cols or not cols[0]:
            continue
        
        # First column is the primary name (formula name, herb name, etc.)
        primary = cols[0]
        
        # Build content from remaining columns
        if header and len(header) > 1 and len(cols) > 1:
            parts = []
            for i in range(1, min(len(cols), len(header))):
                if cols[i]:
                    parts.append(f"**{header[i]}**：{cols[i]}")
            content = '\n\n'.join(parts)
        else:
            content = ' | '.join(cols[1:]) if len(cols) > 1 else ''
        
        entries.append({
            "title": primary,
            "content": content,
            "file": filename,
            "category": heading
        })
    
    return entries

def parse_markdown_sections(filepath: Path) -> list[dict]:
    """Parse a markdown file into searchable sections."""
    text = filepath.read_text(encoding="utf-8")
    filename = filepath.name
    sections = []
    
    # Special handling for formula-patterns: parse tables row-by-row
    if filename == 'formula-patterns.md':
        return parse_formula_file(text, filename)
    
    # Special handling for clinical cases: split by lesson
    if filename == 'clinical-cases.md':
        return parse_clinical_cases(text, filename)
    
    if filename == 'bencao.md':
        return parse_bencao_file(text, filename)
    
    # Generic: split by ## headings
    chunks = re.split(r'\n(?=## )', text)
    
    for chunk in chunks:
        heading_match = re.match(r'^## (.+)', chunk)
        heading = heading_match.group(1).strip() if heading_match else fmt_name(filename)
        content = chunk[heading_match.end():].strip() if heading_match else chunk.strip()
        
        if not content or len(content) < 20:
            continue
        
        # Check if this section contains a table
        table_entries = parse_table_rows(content, heading, filename)
        if table_entries:
            sections.extend(table_entries)
        else:
            # Clean up markdown for display
            clean = clean_content(content)
            sections.append({
                "title": heading,
                "content": clean[:2500],
                "file": filename,
                "category": fmt_name(filename)
            })
    
    return sections

def parse_formula_file(text: str, filename: str) -> list[dict]:
    """Parse formula-patterns.md: extract all table rows."""
    entries = []
    current_heading = '方劑方證'
    
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            current_heading = line[3:].strip()
    
    # Parse all tables in the file
    return parse_table_rows(text, current_heading, filename)

def parse_clinical_cases(text: str, filename: str) -> list[dict]:
    """Parse clinical-cases.md: split by lesson entries."""
    entries = []
    
    # Split by ### headings (individual lessons)
    chunks = re.split(r'\n(?=### )', text)
    
    for chunk in chunks:
        heading_match = re.match(r'^### (.+)', chunk)
        if not heading_match:
            continue
        
        title = heading_match.group(1).strip()
        content = chunk[heading_match.end():].strip()
        
        if len(content) > 30:
            clean = clean_content(content)
            entries.append({
                "title": title,
                "content": clean[:2500],
                "file": filename,
                "category": '臨床醫案'
            })
    
    return entries

def parse_bencao_file(text: str, filename: str) -> list[dict]:
    """Parse bencao.md: extract herb entries."""
    entries = []
    current_heading = '神農本草'
    
    # First try to parse tables
    table_entries = parse_table_rows(text, current_heading, filename)
    if table_entries:
        return table_entries
    
    # Fallback: split by headings
    chunks = re.split(r'\n(?=## )', text)
    for chunk in chunks:
        heading_match = re.match(r'^## (.+)', chunk)
        heading = heading_match.group(1).strip() if heading_match else fmt_name(filename)
        content = chunk[heading_match.end():].strip() if heading_match else chunk.strip()
        
        if content and len(content) > 20:
            clean = clean_content(content)
            entries.append({
                "title": heading,
                "content": clean[:2500],
                "file": filename,
                "category": '神農本草'
            })
    
    return entries

def clean_content(text: str) -> str:
    """Clean markdown for display."""
    # Remove markdown links: [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove image syntax
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove horizontal rules
    text = re.sub(r'\n---+\n', '\n', text)
    # Remove excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Remove code fences but keep content
    text = re.sub(r'```\w*\n?', '', text)
    return text.strip()

def main():
    all_sections = []
    
    for md_file in sorted(REF_DIR.glob("*.md")):
        # Skip screenshot evidence files (too granular, binary references)
        if 'screenshot' in md_file.name or 'pdf-evidence' in md_file.name:
            continue
        
        try:
            sections = parse_markdown_sections(md_file)
            all_sections.extend(sections)
        except Exception as e:
            print(f"Error parsing {md_file.name}: {e}")
    
    # Write index
    out_path = OUT_DIR / "search_index.json"
    out_path.write_text(json.dumps(all_sections, ensure_ascii=False, indent=2))
    
    # Stats
    by_file = {}
    for s in all_sections:
        cat = s.get('category', s['file'])
        by_file[cat] = by_file.get(cat, 0) + 1
    
    print(f"Generated {len(all_sections)} searchable entries:")
    for cat, count in sorted(by_file.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print(f"Output: {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")

if __name__ == "__main__":
    main()

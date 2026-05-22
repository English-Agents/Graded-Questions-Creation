"""
Imports reading material from the 4 course CSV files.

Usage:
  # Place CSVs in data/ directory, then run:
  python -m backend.scripts.import_csv_material

Expected file names in data/:
  foundation.csv         (Foundation course — columns: Modules, Session Type, Topic, Fortnight, Reading Material)
  advanced.csv           (Advanced course)
  applied.csv            (Applied course)
  language_analytics.csv (Language Analytics course)

For Foundation, the Reading Material column contains the actual material text.
For others, material is uploaded separately via POST /api/content/material.

Output:
  courses/{course}/{module}/{topic}/material/{topic_slug}.md
"""
import csv
import re
from pathlib import Path

from backend.config import settings
from backend.scripts.setup_courses import COURSES


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


def _find_topic_dir(courses_root: Path, course_slug: str, topic_name: str) -> Path | None:
    """Find the topic folder by matching topic name in metadata.json."""
    course_data = COURSES.get(course_slug, {})
    for module_slug, module_data in course_data.get("modules", {}).items():
        for topic_slug, topic_data in module_data.get("topics", {}).items():
            if topic_data["name"].lower().strip() == topic_name.lower().strip():
                return courses_root / course_slug / module_slug / topic_slug
    return None


def import_foundation_csv(csv_path: Path, courses_root: Path) -> int:
    """
    Parse Foundation CSV and save reading material per topic.
    Expected columns: Modules, Session Type, Topic, Fortnight, Reading Material
    Returns number of material files written.
    """
    written = 0
    with csv_path.open(encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header

        for row in reader:
            if len(row) < 5:
                continue
            # Columns: [Modules, Session Type/Topic ID, Topic Name, Fortnight, Reading Material]
            _, topic_id, topic_name, _, material = (row + [""] * 5)[:5]
            topic_name = topic_name.strip()
            material = material.strip()

            if not topic_name or not material:
                continue

            topic_dir = _find_topic_dir(courses_root, "foundation", topic_name)
            if not topic_dir:
                print(f"  [WARN] Topic not found in course definition: '{topic_name}'")
                continue

            material_dir = topic_dir / "material"
            material_dir.mkdir(exist_ok=True)
            out_file = material_dir / f"{_slug(topic_name)}.md"
            out_file.write_text(material, encoding="utf-8")
            print(f"  [foundation] Saved material for: {topic_name} ({len(material)} chars)")
            written += 1

    return written


def import_generic_csv(csv_path: Path, courses_root: Path, course_slug: str) -> int:
    """
    Parse a generic course CSV (no embedded material).
    Just validates that topics in the CSV match the course definition.
    Advanced/Applied/Language Analytics CSVs have no material column —
    material should be uploaded via POST /api/content/material.
    """
    found = 0
    with csv_path.open(encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            row = (row + [""] * 4)[:4]
            _, _, topic_name = row[0].strip(), row[1].strip(), row[2].strip()
            if not topic_name:
                continue
            topic_dir = _find_topic_dir(courses_root, course_slug, topic_name)
            status = "✓" if topic_dir else "✗ not found"
            print(f"  [{course_slug}] {topic_name}: {status}")
            if topic_dir:
                found += 1
    return found


CSV_MAP = {
    "foundation.csv": ("foundation", import_foundation_csv),
    "advanced.csv": ("advanced", None),
    "applied.csv": ("applied", None),
    "language_analytics.csv": ("language_analytics", None),
}


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent.parent / "data"
    courses_root = Path(settings.courses_dir)

    if not data_dir.exists():
        print(f"data/ directory not found at {data_dir}. Create it and place CSV files there.")
        raise SystemExit(1)

    for filename, (course_slug, handler) in CSV_MAP.items():
        csv_path = data_dir / filename
        if not csv_path.exists():
            print(f"[SKIP] {filename} not found in data/")
            continue

        print(f"\nProcessing {filename} → course: {course_slug}")
        if handler:
            count = handler(csv_path, courses_root)
            print(f"  → {count} material files written")
        else:
            count = import_generic_csv(csv_path, courses_root, course_slug)
            print(f"  → {count} topics matched")

    print("\nDone. Upload material via POST /api/content/material for courses without embedded material.")

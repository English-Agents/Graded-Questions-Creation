"""
Bulk ingest script: ingests reading material and sample question CSVs for all topics
that already have files in their material/ and reference_questions/ directories.

Run after seeding: python -m backend.ingest_sample

This is a helper for local development. In production, use:
  POST /api/content/material   for reading material
  POST /api/content/samples    for sample question CSVs
"""
import asyncio
import csv
import io
from pathlib import Path

from sqlalchemy import select

from backend.config import settings
from backend.db.connection import AsyncSessionLocal
from backend.db.models import Course, Module, SampleQuestion, Topic
from backend.rag.ingestor import ingest_file
from backend.scripts.setup_courses import COURSES


async def ingest_all():
    courses_root = Path(settings.courses_dir)

    async with AsyncSessionLocal() as db:
        # Load all topics from DB
        result = await db.execute(
            select(Topic, Module, Course)
            .join(Module, Module.id == Topic.module_id)
            .join(Course, Course.id == Module.course_id)
            .order_by(Course.name, Module.order_index, Topic.id)
        )
        rows = result.all()

        if not rows:
            print("No topics in DB. Run `python -m backend.seed` first.")
            return

        print(f"Found {len(rows)} topics in DB.\n")

        total_chunks = 0
        total_samples = 0

        for topic, module, course in rows:
            # Find the folder on disk for this topic
            topic_dir = _find_topic_dir(courses_root, course.name, module.name, topic.name)
            if not topic_dir:
                continue

            # Ingest material files
            material_dir = topic_dir / "material"
            if material_dir.exists():
                for f in material_dir.iterdir():
                    if f.suffix.lower() in {".md", ".txt", ".pdf", ".docx"}:
                        count = await ingest_file(topic.id, f)
                        if count:
                            print(f"  [{course.name}] {topic.name}: ingested {f.name} → {count} chunks")
                            total_chunks += count

            # Ingest reference question CSVs
            ref_dir = topic_dir / "reference_questions"
            if ref_dir.exists():
                for csv_path in ref_dir.glob("*.csv"):
                    inserted = await _import_samples(db, topic.id, csv_path)
                    if inserted:
                        print(f"  [{course.name}] {topic.name}: inserted {inserted} sample questions from {csv_path.name}")
                        total_samples += inserted

        await db.commit()
        print(f"\nDone. {total_chunks} chunks ingested, {total_samples} sample questions inserted.")


def _find_topic_dir(courses_root: Path, course_name: str, module_name: str, topic_name: str) -> Path | None:
    """Locate topic directory by matching names against COURSES definition."""
    for course_slug, course_data in COURSES.items():
        if course_data["name"].lower() != course_name.lower():
            continue
        for module_slug, module_data in course_data["modules"].items():
            if module_data["name"].lower() != module_name.lower():
                continue
            for topic_slug, topic_data in module_data["topics"].items():
                if topic_data["name"].lower().strip() == topic_name.lower().strip():
                    return courses_root / course_slug / module_slug / topic_slug
    return None


async def _import_samples(db, topic_id: int, csv_path: Path) -> int:
    text = csv_path.read_text(encoding="utf-8", errors="replace")
    reader = csv.reader(
        line for line in io.StringIO(text)
        if not line.strip().startswith("#") and line.strip()
    )
    inserted = 0
    for row in reader:
        if len(row) < 5:
            continue
        row = (row + [""] * 11)[:11]
        skill, marks_str, question_type, difficulty, text_val = row[:5]
        answer_key, opt_a, opt_b, opt_c, opt_d, bloom_str = row[5:]

        skill = skill.strip()
        text_val = text_val.strip()
        difficulty = difficulty.strip().lower()

        if not skill or not text_val or difficulty not in ("easy", "medium", "hard"):
            continue
        try:
            marks = int(marks_str.strip())
        except ValueError:
            continue

        bloom_level = None
        try:
            bloom_level = int(bloom_str.strip())
        except (ValueError, AttributeError):
            pass

        options = None
        if opt_a.strip():
            options = {"a": opt_a.strip(), "b": opt_b.strip(), "c": opt_c.strip(), "d": opt_d.strip()}

        db.add(SampleQuestion(
            topic_id=topic_id,
            skill=skill,
            marks=marks,
            question_type=question_type.strip(),
            difficulty=difficulty,
            text=text_val,
            answer_key=answer_key.strip() or None,
            options=options,
            bloom_level=bloom_level,
        ))
        inserted += 1
    return inserted


if __name__ == "__main__":
    asyncio.run(ingest_all())

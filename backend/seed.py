"""
Seed script: creates all 4 courses in the database and sets up course folders.

Run:  python -m backend.seed
"""
import asyncio
import json
from pathlib import Path

from sqlalchemy import select, text

from backend.config import settings
from backend.db.connection import AsyncSessionLocal, engine
from backend.db.models import Course, Module, Skill, Topic
from backend.scripts.setup_courses import COURSES, setup_all_courses


async def seed():
    # 1. Ensure schema exists
    schema_path = Path(__file__).parent / "db" / "schema.sql"
    async with engine.begin() as conn:
        await conn.execute(text(schema_path.read_text()))

    # 2. Create folder structure for all courses
    courses_root = Path(settings.courses_dir)
    stats = setup_all_courses(courses_root)
    print(f"Folders: {stats['courses']} courses, {stats['modules']} modules, {stats['topics']} topics")

    async with AsyncSessionLocal() as db:
        # Check if already seeded
        existing = await db.execute(select(Course).limit(1))
        if existing.scalars().first():
            print("Database already seeded. Skipping.")
            return

        # 3. Seed all 4 courses
        for course_slug, course_data in COURSES.items():
            course = Course(name=course_data["name"], subject="English")
            db.add(course)
            await db.flush()
            print(f"\nCourse: {course.name} (id={course.id})")

            for order_idx, (module_slug, module_data) in enumerate(course_data["modules"].items(), 1):
                module = Module(
                    course_id=course.id,
                    name=module_data["name"],
                    order_index=order_idx,
                )
                db.add(module)
                await db.flush()

                for topic_slug, topic_data in module_data["topics"].items():
                    # Load metadata.json from disk (may have been written by setup_all_courses)
                    meta_path = courses_root / course_slug / module_slug / topic_slug / "metadata.json"
                    metadata = {}
                    if meta_path.exists():
                        metadata = json.loads(meta_path.read_text())

                    topic = Topic(
                        module_id=module.id,
                        name=topic_data["name"],
                        metadata_=metadata,
                    )
                    db.add(topic)

                print(f"  Module: {module_data['name']} → {len(module_data['topics'])} topics")

        await db.commit()
        print("\nDatabase seeded successfully.")
        print("\nTopic IDs for API calls:")

        # Print topic summary
        result = await db.execute(
            select(Topic, Module, Course)
            .join(Module, Module.id == Topic.module_id)
            .join(Course, Course.id == Module.course_id)
            .order_by(Course.name, Module.order_index, Topic.id)
        )
        for topic, mod, course in result.all():
            print(f"  [{course.name}] {mod.name} / {topic.name}  →  topic_id={topic.id}")


if __name__ == "__main__":
    asyncio.run(seed())

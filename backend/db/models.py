import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.connection import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    pool_configs: Mapped[list["PoolConfig"]] = relationship(back_populates="skill")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False, default="English")

    modules: Mapped[list["Module"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    course: Mapped["Course"] = relationship(back_populates="modules")
    topics: Mapped[list["Topic"]] = relationship(back_populates="module", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)

    module: Mapped["Module"] = relationship(back_populates="topics")
    pool_configs: Mapped[list["PoolConfig"]] = relationship(back_populates="topic", cascade="all, delete-orphan")
    sample_questions: Mapped[list["SampleQuestion"]] = relationship(back_populates="topic", cascade="all, delete-orphan")


class PoolConfig(Base):
    __tablename__ = "pool_configs"
    __table_args__ = (
        UniqueConstraint("topic_id", "skill_id", "marks", "question_type", "difficulty"),
        CheckConstraint("difficulty IN ('easy','medium','hard')", name="ck_pool_difficulty"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    marks: Mapped[int] = mapped_column(Integer, nullable=False)
    question_type: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    target_count: Mapped[int] = mapped_column(Integer, default=0)
    current_count: Mapped[int] = mapped_column(Integer, default=0)

    topic: Mapped["Topic"] = relationship(back_populates="pool_configs")
    skill: Mapped["Skill"] = relationship(back_populates="pool_configs")
    questions: Mapped[list["Question"]] = relationship(back_populates="pool_config", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint("difficulty IN ('easy','medium','hard')", name="ck_q_difficulty"),
        CheckConstraint("validation_status IN ('pending','approved','rejected')", name="ck_q_status"),
        CheckConstraint("bloom_level BETWEEN 1 AND 6", name="ck_q_bloom"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pool_config_id: Mapped[int] = mapped_column(ForeignKey("pool_configs.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String, nullable=False)
    marks: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    bloom_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    answer_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    validation_status: Mapped[str] = mapped_column(String, default="pending")
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    chroma_id: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    pool_config: Mapped["PoolConfig"] = relationship(back_populates="questions")


class SampleQuestion(Base):
    __tablename__ = "sample_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    skill: Mapped[str] = mapped_column(String, nullable=False)
    marks: Mapped[int] = mapped_column(Integer, nullable=False)
    question_type: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    answer_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    bloom_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    topic: Mapped["Topic"] = relationship(back_populates="sample_questions")

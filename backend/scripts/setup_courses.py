"""
Setup script: creates the complete course folder structure and metadata.json
for all 4 English courses.

Run once:  python -m backend.scripts.setup_courses

Creates:
  courses/{course}/{module}/{topic}/material/
  courses/{course}/{module}/{topic}/reference_questions/
  courses/{course}/{module}/{topic}/metadata.json
"""
import json
import re
from pathlib import Path

from backend.config import settings

# ─────────────────────────────────────────────────────────────────────────────
# Course / Module / Topic definitions
# skill      : Grammar & Vocabulary | Reading | Writing
# marks      : primary marks value for questions in this topic
# types      : allowed question types
# difficulty : default difficulty distribution
# ─────────────────────────────────────────────────────────────────────────────

COURSES = {
    "foundation": {
        "name": "English Foundation",
        "modules": {
            "module_1": {
                "name": "Module 1 - Parts of Speech",
                "topics": {
                    "topic_1": {
                        "name": "Noun Vs Main Verb",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_2": {
                        "name": "Noun: Number and Collection",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Sentence Conversion"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_3": {
                        "name": "Countable and Uncountable Nouns",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                },
            },
            "module_2": {
                "name": "Module 2 - Verbs and Pronouns",
                "topics": {
                    "topic_4": {
                        "name": "Verb Forms and Noun + Helping Verb Agreement",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Cloze"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_5": {
                        "name": "Possessive Noun: Apostrophe and Of Form",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_6": {
                        "name": "Pronouns: People and Things",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_7": {
                        "name": "Possessive Pronouns",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                },
            },
            "module_3": {
                "name": "Module 3 - Adjectives and Articles",
                "topics": {
                    "topic_8": {
                        "name": "Real Time Session 1",
                        "skill": "Writing", "marks": 3,
                        "types": ["Short functional writing"],
                        "difficulty": {"easy": 5, "medium": 10, "hard": 5},
                    },
                    "topic_9": {
                        "name": "Adjectives: Identification, Application and Degree",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_10": {
                        "name": "Articles: A / An and The",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Cloze"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                },
            },
            "module_4": {
                "name": "Module 4 - Prepositions and Question Words",
                "topics": {
                    "topic_11": {
                        "name": "Prepositions",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Cloze"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_12": {
                        "name": "Question Words",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_13": {
                        "name": "Adverbs",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                },
            },
            "module_5": {
                "name": "Module 5 - Conjunctions and Tenses",
                "topics": {
                    "topic_14": {
                        "name": "Real Time Session 2",
                        "skill": "Writing", "marks": 3,
                        "types": ["Short functional writing"],
                        "difficulty": {"easy": 5, "medium": 10, "hard": 5},
                    },
                    "topic_15": {
                        "name": "Contractions and Interjections",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_16": {
                        "name": "Conjunctions",
                        "skill": "Grammar & Vocabulary", "marks": 3,
                        "types": ["Fill in the blanks", "Sentence arrangement", "Sentence Conversion"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_17": {
                        "name": "Tenses Possession",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Cloze"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                },
            },
            "module_6": {
                "name": "Module 6 - Present Simple",
                "topics": {
                    "topic_18": {
                        "name": "Present Simple 1",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Cloze"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_19": {
                        "name": "Present Simple 2",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_20": {
                        "name": "Present Simple 3",
                        "skill": "Grammar & Vocabulary", "marks": 3,
                        "types": ["Sentence arrangement", "Jumbled Sentences"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_21": {
                        "name": "Present Simple 4",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_22": {
                        "name": "Present Simple: Scenario Application",
                        "skill": "Grammar & Vocabulary", "marks": 3,
                        "types": ["Sentence arrangement", "Sentence Conversion"],
                        "difficulty": {"easy": 5, "medium": 10, "hard": 5},
                    },
                },
            },
            "module_7": {
                "name": "Module 7 - Past Simple",
                "topics": {
                    "topic_23": {
                        "name": "Past Simple 1",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Cloze"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_24": {
                        "name": "Past Simple 2",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_25": {
                        "name": "Past Simple 3",
                        "skill": "Grammar & Vocabulary", "marks": 3,
                        "types": ["Sentence arrangement", "Jumbled Sentences"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_26": {
                        "name": "Past Simple 4",
                        "skill": "Grammar & Vocabulary", "marks": 2,
                        "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"],
                        "difficulty": {"easy": 10, "medium": 15, "hard": 5},
                    },
                    "topic_27": {
                        "name": "Past Simple: Scenario Application",
                        "skill": "Grammar & Vocabulary", "marks": 3,
                        "types": ["Sentence arrangement", "Sentence Conversion"],
                        "difficulty": {"easy": 5, "medium": 10, "hard": 5},
                    },
                },
            },
        },
    },

    "advanced": {
        "name": "English Advanced",
        "modules": {
            "module_1": {
                "name": "Module 1 - Future Simple",
                "topics": {
                    "topic_1": {"name": "Future Simple 1", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_2": {"name": "Future Simple 2", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_3": {"name": "Future Simple: Scenario Application", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence Conversion", "Sentence arrangement"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_4": {"name": "Tenses Ability", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence Conversion", "Error correction"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                },
            },
            "module_2": {
                "name": "Module 2 - Continuous Tenses and Modals",
                "topics": {
                    "topic_5": {"name": "Real Time Session 3", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_6": {"name": "Tenses Continuous", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Cloze"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_7": {"name": "Scenario Application: Simple and Continuous Tenses", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence Conversion", "Sentence arrangement"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_8": {"name": "Modal Verbs", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                },
            },
            "module_3": {
                "name": "Module 3 - Perfect Tenses",
                "topics": {
                    "topic_9":  {"name": "Present Perfect Tense", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Cloze"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_10": {"name": "Present Perfect Continuous Tense", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_11": {"name": "Present Perfect and Perfect Continuous Application", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence Conversion", "Sentence arrangement"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_12": {"name": "Past Perfect", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Cloze"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_13": {"name": "Past Perfect Continuous", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_14": {"name": "Past Perfect and Past Perfect Continuous Application", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence Conversion", "Sentence arrangement"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                },
            },
            "module_4": {
                "name": "Module 4 - Future Perfect and Writing",
                "topics": {
                    "topic_15": {"name": "Future Perfect", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Cloze"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_16": {"name": "Future Perfect Continuous", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_17": {"name": "Question Making with Question Words", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Sentence Conversion", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_18": {"name": "Question Making with Question Verbs", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Sentence Conversion"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_19": {"name": "Real Time Session 4", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_20": {"name": "Punctuation", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Error correction", "Fill in the blanks"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_21": {"name": "Articulation", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_22": {"name": "Written Practice", "skill": "Writing", "marks": 5, "types": ["Essay writing", "Story writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                },
            },
        },
    },

    "applied": {
        "name": "English Applied",
        "modules": {
            "module_1": {
                "name": "Module 1 - Structure and Discussion",
                "topics": {
                    "topic_1": {"name": "Accuracy in Sentence Structure", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Error correction", "Sentence arrangement"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_2": {"name": "The Language of Connection", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence arrangement", "Sentence Conversion"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_4": {"name": "Mastering the Art of Discussion", "skill": "Writing", "marks": 5, "types": ["Essay writing", "Story writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_5": {"name": "Designing Clear Prompts", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                },
            },
            "module_2": {
                "name": "Module 2 - Expression and Obligation",
                "topics": {
                    "topic_7":  {"name": "Framing Effective Questions", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Sentence Conversion", "Fill in the blanks"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_8":  {"name": "Emphasizing Self-Expression", "skill": "Writing", "marks": 5, "types": ["Essay writing", "Story writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_10": {"name": "Expressing Possibility and Obligation", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_11": {"name": "Rephrasing Speech Accurately", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence Conversion", "Sentence arrangement"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                },
            },
            "module_3": {
                "name": "Module 3 - Communication and Fluency",
                "topics": {
                    "topic_13": {"name": "Shifting Focus in Communication", "skill": "Writing", "marks": 5, "types": ["Essay writing", "Story writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_14": {"name": "Improving Natural Fluency", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Error correction", "Sentence arrangement"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                },
            },
            "module_4": {
                "name": "Module 4 - Advanced Writing",
                "topics": {
                    "topic_16": {"name": "Balancing Ideas Clearly", "skill": "Writing", "marks": 7, "types": ["Process writing / sequencing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_17": {"name": "Managing Hesitation and Highlighting Key Points", "skill": "Writing", "marks": 5, "types": ["Essay writing", "Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                },
            },
        },
    },

    "language_analytics": {
        "name": "English Language Analytics",
        "modules": {
            "module_1": {
                "name": "Module 1 - Verbal Ability and Vocabulary",
                "topics": {
                    "topic_1": {"name": "Verbal Ability: Question Solving Strategies Part 1", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Cloze"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_2": {"name": "Real Time Session 1: Highlighting Key Points", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_3": {"name": "Vocabulary: Synonyms, Antonyms and Root Words", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_4": {"name": "Idioms, Phrases and One Word Substitutions", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_5": {"name": "Fill in the Blanks (Single and Double) and Cloze Test", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Cloze"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_6": {"name": "Analogy, Contextual Words and Miscellaneous Vocabulary", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                },
            },
            "module_2": {
                "name": "Module 2 - Reading Comprehension",
                "topics": {
                    "topic_7":  {"name": "Verbal Ability: Question Solving Strategies Part 2", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Cloze"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_8":  {"name": "Real Time Session 2: Significance of Choosing Correct Words", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_9":  {"name": "Reading Comprehension", "skill": "Reading", "marks": 5, "types": ["Literal & inferential comprehension"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_10": {"name": "Sentence (Continue the Context) and Paragraph Completion", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Fill in the blanks", "Sentence arrangement"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_12": {"name": "Spot the Error and Sentence Correction", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_13": {"name": "Jumbled Words", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Jumbled Sentences"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                },
            },
            "module_3": {
                "name": "Module 3 - Sentence Structure",
                "topics": {
                    "topic_11": {"name": "Verbal Ability: Question Solving Strategies Part 3", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_14": {"name": "Sentence Construction", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence arrangement", "Sentence Conversion"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_15": {"name": "Jumbled Sentences and Paragraphs", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Jumbled Sentences", "Sentence arrangement"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_16": {"name": "Clauses", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Fill in the blanks", "Error correction", "Sentence Conversion"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                    "topic_17": {"name": "Voice and Speech", "skill": "Grammar & Vocabulary", "marks": 3, "types": ["Sentence Conversion", "Error correction"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_18": {"name": "Spell Check", "skill": "Grammar & Vocabulary", "marks": 2, "types": ["Error correction"], "difficulty": {"easy": 10, "medium": 15, "hard": 5}},
                },
            },
            "module_4": {
                "name": "Module 4 - Academic and Professional Writing",
                "topics": {
                    "topic_19": {"name": "Real Time Session 3: Maintaining Clarity in Delivery", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_20": {"name": "Paragraph and Essay Writing", "skill": "Writing", "marks": 5, "types": ["Essay writing", "Sequencing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_21": {"name": "Report and Summary Writing", "skill": "Writing", "marks": 8, "types": ["Report / Work report"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_22": {"name": "Academic Writing Essentials", "skill": "Writing", "marks": 7, "types": ["Process writing / sequencing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_23": {"name": "Email and Letter Writing", "skill": "Writing", "marks": 8, "types": ["Email writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                },
            },
            "module_5": {
                "name": "Module 5 - Professional Communication",
                "topics": {
                    "topic_24": {"name": "Mock Interviews and Group Discussions", "skill": "Writing", "marks": 5, "types": ["Essay writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_25": {"name": "Oral Presentations and Elevator Pitches", "skill": "Writing", "marks": 5, "types": ["Essay writing", "Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_26": {"name": "Role-Plays for Professional Communication", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_27": {"name": "Non-Verbal Cues and Body-Language Practice", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_28": {"name": "Workplace Conversation Drills", "skill": "Writing", "marks": 3, "types": ["Short functional writing"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                    "topic_29": {"name": "Resume and Cover-Letter Writing Practice", "skill": "Writing", "marks": 8, "types": ["Report / Work report"], "difficulty": {"easy": 5, "medium": 10, "hard": 5}},
                },
            },
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


def _topic_metadata(course_slug: str, course_name: str, module_name: str, topic: dict) -> dict:
    return {
        "topic_name": topic["name"],
        "module": module_name,
        "course": course_name,
        "skills": [
            {
                "skill": topic["skill"],
                "marks": topic["marks"],
                "question_types": topic["types"],
                "difficulty_distribution": topic["difficulty"],
            }
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def setup_all_courses(courses_root: Path) -> dict[str, int]:
    """Create folder structure + metadata.json for all courses."""
    stats: dict[str, int] = {"courses": 0, "modules": 0, "topics": 0}

    for course_slug, course_data in COURSES.items():
        course_dir = courses_root / course_slug
        course_dir.mkdir(parents=True, exist_ok=True)
        stats["courses"] += 1

        for module_slug, module_data in course_data["modules"].items():
            module_dir = course_dir / module_slug
            module_dir.mkdir(exist_ok=True)
            stats["modules"] += 1

            for topic_slug, topic_data in module_data["topics"].items():
                topic_dir = module_dir / topic_slug
                (topic_dir / "material").mkdir(parents=True, exist_ok=True)
                (topic_dir / "reference_questions").mkdir(parents=True, exist_ok=True)
                stats["topics"] += 1

                meta_path = topic_dir / "metadata.json"
                if not meta_path.exists():
                    meta = _topic_metadata(
                        course_slug,
                        course_data["name"],
                        module_data["name"],
                        topic_data,
                    )
                    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
                    print(f"  Created: {course_slug}/{module_slug}/{topic_slug}")

    return stats


if __name__ == "__main__":
    courses_root = Path(settings.courses_dir)
    print(f"Setting up courses in: {courses_root.resolve()}")
    stats = setup_all_courses(courses_root)
    print(f"\nDone: {stats['courses']} courses, {stats['modules']} modules, {stats['topics']} topics created.")

"""
Bulk generate questions for ALL subtopics (10 questions per subtopic)
"""

import sys
sys.path.insert(0, 'd:\\COMPETITIVE_EXAM\\backend')

import random
from app.database import SessionLocal
from app import models


def extract_definition(description):
    """Extract definition from description"""
    if not description:
        return "A key concept in this area"
    
    # Try to extract the first sentence/clause
    parts = description.split('.')
    return parts[0] if parts else "A fundamental principle"


def extract_concepts(description):
    """Extract concepts from description"""
    if not description:
        return []
    
    keywords = [
        "systematic", "structured", "organized", "analytical", 
        "comprehensive", "logical", "methodical", "strategic"
    ]
    return keywords


TEMPLATES = {
    "definition": {
        "questions": [
            "What is the definition of {topic}?",
            "{topic} can be defined as:",
            "Which of the following best defines {topic}?",
            "According to standard definition, {topic} is:",
        ],
    },
    "concept": {
        "questions": [
            "Which of the following is a key concept in {topic}?",
            "The main principle of {topic} involves:",
            "What is the fundamental concept behind {topic}?",
        ],
    },
    "application": {
        "questions": [
            "Which of the following is an example of {topic}?",
            "{topic} is commonly used in:",
            "In practical application, {topic} is used for:",
        ],
    },
    "statement": {
        "questions": [
            "Which statement about {topic} is correct?",
            "Which of the following statements regarding {topic} is true?",
            "Select the correct statement about {topic}:",
        ],
    }
}

DISTRACTORS = [
    "It is a theoretical concept with no practical application",
    "It was invented in the 19th century",
    "It is primarily used in warfare",
    "It is only relevant to modern technology",
    "It is a term used exclusively in mathematics",
    "It is a historical figure, not a concept",
    "It is not mentioned in any official curriculum",
    "It is applicable only in specific regions",
    "It is a recent discovery from the 21st century",
    "It has no relevance to competitive exams",
    "It was developed solely for academic purposes",
    "It is an abstract concept without real-world applications",
]


def generate_question(topic, description, topic_id, subtopic_id, question_type="definition"):
    """Generate a single question"""
    
    if question_type == "definition":
        questions = TEMPLATES["definition"]["questions"]
        correct_option = extract_definition(description)
        difficulty = "easy"
    elif question_type == "concept":
        questions = TEMPLATES["concept"]["questions"]
        correct_option = random.choice([
            f"Understanding the fundamentals of {topic}",
            f"Grasping the core principles of {topic}",
            f"Analyzing the structure of {topic}",
        ])
        difficulty = "medium"
    elif question_type == "application":
        questions = TEMPLATES["application"]["questions"]
        correct_option = f"Solving problems related to {topic}"
        difficulty = "medium"
    else:  # statement
        questions = TEMPLATES["statement"]["questions"]
        correct_option = f"{topic} is an important concept in this subject"
        difficulty = "hard"
    
    question_text = random.choice(questions).format(topic=topic)
    
    # Generate wrong options
    wrong_options = random.sample(DISTRACTORS, 3)
    
    # Create options list
    options = [correct_option] + wrong_options
    random.shuffle(options)
    
    # Find correct answer letter
    correct_answer = chr(65 + options.index(correct_option))  # A, B, C, D
    
    return {
        "topic_id": topic_id,
        "subtopic_id": subtopic_id,
        "question": question_text,
        "options": {
            "a": options[0],
            "b": options[1],
            "c": options[2],
            "d": options[3],
        },
        "correct_answer": correct_answer,
        "difficulty": difficulty
    }


def generate_questions_for_all_subtopics():
    """Generate questions for all subtopics"""
    db = SessionLocal()
    
    try:
        # Get all subtopics
        subtopics = db.query(models.Subtopic).all()
        print(f"\n📚 Found {len(subtopics)} subtopics")
        print("=" * 60)
        
        total_questions_created = 0
        
        for idx, subtopic in enumerate(subtopics, 1):
            # Get topic for context
            topic = db.query(models.Topic).filter(models.Topic.id == subtopic.topic_id).first()
            topic_name = topic.title if topic else "Unknown"
            
            # Generate 10 questions per subtopic with different types
            question_types = ["definition", "concept", "application", "statement"]
            
            for q_num in range(10):
                q_type = question_types[q_num % len(question_types)]
                q_data = generate_question(
                    subtopic.title,
                    subtopic.description or "",
                    subtopic.topic_id,
                    subtopic.id,
                    q_type
                )
                
                # Create question object
                question = models.Question(
                    topic_id=q_data["topic_id"],
                    subtopic_id=q_data["subtopic_id"],
                    question=q_data["question"],
                    option_a=q_data["options"]["a"],
                    option_b=q_data["options"]["b"],
                    option_c=q_data["options"]["c"],
                    option_d=q_data["options"]["d"],
                    correct_answer=q_data["correct_answer"],
                    difficulty=q_data["difficulty"]
                )
                
                db.add(question)
                total_questions_created += 1
            
            # Commit every 10 subtopics to avoid memory issues
            if idx % 10 == 0:
                db.commit()
                print(f"✅ Generated questions for {idx}/{len(subtopics)} subtopics ({total_questions_created} questions)")
        
        # Final commit
        db.commit()
        
        print("=" * 60)
        print(f"✅ SUCCESS! Generated {total_questions_created} questions for {len(subtopics)} subtopics")
        print(f"   Average: 10 questions per subtopic")
        print("=" * 60)
        
        # Verify
        final_count = db.query(models.Question).count()
        print(f"\n📊 Database verification: {final_count} total questions now in database")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    generate_questions_for_all_subtopics()

"""
Generate realistic MCQ questions using intelligent templates
Creates 10 questions per subtopic for the 145 subtopics with descriptions
Ultra fast - no AI/Ollama dependency
"""

import random
from app.database import SessionLocal
from app import models

# Question templates - realistic for NDA exam
TEMPLATES = {
    "definition": {
        "questions": [
            "What is the definition of {topic}?",
            "{topic} can be defined as:",
            "Which of the following best defines {topic}?",
            "According to standard definition, {topic} is:",
        ],
        "generator": lambda topic, desc: generate_definition_question(topic, desc)
    },
    "concept": {
        "questions": [
            "Which of the following is a key concept in {topic}?",
            "The main principle of {topic} involves:",
            "What is the fundamental concept behind {topic}?",
        ],
        "generator": lambda topic, desc: generate_concept_question(topic, desc)
    },
    "application": {
        "questions": [
            "Which of the following is an example of {topic}?",
            "{topic} is commonly used in:",
            "In practical application, {topic} is used for:",
        ],
        "generator": lambda topic, desc: generate_application_question(topic, desc)
    },
    "statement": {
        "questions": [
            "Which statement about {topic} is correct?",
            "Which of the following statements regarding {topic} is true?",
            "Select the correct statement about {topic}:",
        ],
        "generator": lambda topic, desc: generate_statement_question(topic, desc)
    }
}

# Common NDA-style options
DISTRACTORS = [
    "It is a theoretical concept with no practical application",
    "It was invented in the 19th century",
    "It is primarily used in warfare",
    "It is only relevant to modern technology",
    "It is a term used exclusively in mathematics",
    "It is a historical figure, not a concept",
    "It is not mentioned in any official curriculum",
    "It is applicable only in specific regions",
]


def generate_definition_question(topic, description):
    """Generate a definition-based question"""
    correct_option = extract_definition(description)
    
    wrong_options = random.sample(DISTRACTORS, 3)
    
    options = [correct_option] + wrong_options
    random.shuffle(options)
    correct = chr(65 + options.index(correct_option))  # A, B, C, D
    
    return {
        "question": random.choice(TEMPLATES["definition"]["questions"]).format(topic=topic),
        "options": options,
        "correct": correct,
        "difficulty": "easy"
    }


def generate_concept_question(topic, description):
    """Generate a concept-based question"""
    concepts = extract_concepts(description)
    if not concepts:
        concepts = ["Understanding the fundamental structure", "Analyzing key relationships", "Identifying core principles"]
    
    correct_option = random.choice(concepts)
    wrong_options = random.sample(DISTRACTORS, 3)
    
    options = [correct_option] + wrong_options
    random.shuffle(options)
    correct = chr(65 + options.index(correct_option))
    
    return {
        "question": random.choice(TEMPLATES["concept"]["questions"]).format(topic=topic),
        "options": options,
        "correct": correct,
        "difficulty": "medium"
    }


def generate_application_question(topic, description):
    """Generate an application-based question"""
    applications = [
        f"Solving problems related to {topic}",
        f"Understanding {topic} in practical contexts",
        f"Applying principles of {topic} to real scenarios",
        f"Analyzing systems based on {topic}",
    ]
    
    correct_option = random.choice(applications)
    wrong_options = random.sample(DISTRACTORS, 3)
    
    options = [correct_option] + wrong_options
    random.shuffle(options)
    correct = chr(65 + options.index(correct_option))
    
    return {
        "question": random.choice(TEMPLATES["application"]["questions"]).format(topic=topic),
        "options": options,
        "correct": correct,
        "difficulty": "medium"
    }


def generate_statement_question(topic, description):
    """Generate a true/false statement question"""
    true_statement = f"{topic} is an important concept covered in competitive exams"
    
    false_statements = [
        f"{topic} is a fictional concept with no real application",
        f"{topic} was completely obsolete by the year 2000",
        f"{topic} is only taught at advanced PhD levels",
        f"{topic} is not relevant to any standardized examination",
    ]
    
    correct_is_true = random.choice([True, False])
    
    if correct_is_true:
        correct_option = true_statement
        wrong_options = random.sample(false_statements, 3)
    else:
        correct_option = random.choice(false_statements)
        wrong_options = [true_statement] + random.sample(
            [s for s in false_statements if s != correct_option], 2
        )
    
    options = [correct_option] + wrong_options
    random.shuffle(options)
    correct = chr(65 + options.index(correct_option))
    
    return {
        "question": random.choice(TEMPLATES["statement"]["questions"]).format(topic=topic),
        "options": options,
        "correct": correct,
        "difficulty": "hard"
    }


def extract_definition(description):
    """Extract a definition-like statement from description"""
    if not description:
        return "A fundamental concept in competitive examinations"
    
    # Get first sentence or first 30 words
    sentences = description.split('.')
    if sentences:
        first_sent = sentences[0].strip()
        if len(first_sent) > 20:
            return first_sent
    
    return description[:100] + "..." if len(description) > 100 else description


def extract_concepts(description):
    """Extract concepts from description"""
    if not description:
        return []
    
    # Extract numbered points or key terms
    lines = description.split('\n')
    concepts = []
    for line in lines:
        if any(line.startswith(f"{i}.") for i in range(1, 10)):
            concept = line.split('.', 1)[1].strip()
            if concept and len(concept) > 5:
                concepts.append(concept[:80])
    
    return concepts[:3] if concepts else []


def generate_questions_for_subtopic(subtopic_id, topic_title, description):
    """Generate 10 diverse questions for a subtopic"""
    questions = []
    
    # Distribution: 3 easy, 4 medium, 3 hard
    try:
        # Easy questions (definition/concept)
        questions.append(generate_definition_question(topic_title, description))
        questions.append(generate_concept_question(topic_title, description))
        questions.append(generate_statement_question(topic_title, description))
        
        # Medium questions (application)
        for _ in range(4):
            q = random.choice([
                generate_application_question(topic_title, description),
                generate_concept_question(topic_title, description),
            ])
            questions.append(q)
        
        # Hard questions
        for _ in range(3):
            questions.append(generate_statement_question(topic_title, description))
        
        # Set difficulty levels
        for i, q in enumerate(questions):
            if i < 3:
                q["difficulty"] = "easy"
            elif i < 7:
                q["difficulty"] = "medium"
            else:
                q["difficulty"] = "hard"
        
        return questions[:10]  # Return exactly 10
    
    except Exception as e:
        print(f"  Error generating: {str(e)[:50]}")
        return []


def save_questions(db, subtopic_id, topic_id, questions):
    """Save questions to database"""
    if not questions:
        return 0
    
    saved = 0
    for q in questions:
        try:
            question = models.Question(
                topic_id=topic_id,
                subtopic_id=subtopic_id,
                question=q.get("question", ""),
                option_a=q.get("options", ["", "", "", ""])[0],
                option_b=q.get("options", ["", "", "", ""])[1],
                option_c=q.get("options", ["", "", "", ""])[2],
                option_d=q.get("options", ["", "", "", ""])[3],
                correct_answer=q.get("correct", "A"),
                difficulty=q.get("difficulty", "medium")
            )
            db.add(question)
            saved += 1
        except Exception as e:
            print(f"    Save error: {str(e)[:30]}")
            continue
    
    try:
        db.commit()
    except Exception as e:
        print(f"    Commit error: {str(e)[:30]}")
        db.rollback()
    
    return saved


def main():
    print("=" * 70)
    print("📝 TEMPLATE-BASED QUESTION GENERATOR FOR 145 SUBTOPICS")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # Get subtopics with descriptions
        subtopics = db.query(models.Subtopic).filter(
            models.Subtopic.description.isnot(None)
        ).all()
        
        print(f"\n📚 Found {len(subtopics)} subtopics with descriptions\n")
        
        total_subtopics = len(subtopics)
        total_questions = 0
        successful = 0
        
        for i, subtopic in enumerate(subtopics, 1):
            # Check if already has questions
            existing = db.query(models.Question).filter(
                models.Question.subtopic_id == subtopic.id
            ).count()
            
            if existing > 0:
                print(f"[{i:3d}/{total_subtopics}] ⏭️  {subtopic.title:50s} ({existing} questions exist)")
                continue
            
            # Generate questions
            questions = generate_questions_for_subtopic(
                subtopic.id,
                subtopic.title,
                subtopic.description
            )
            
            if questions:
                saved = save_questions(db, subtopic.id, subtopic.topic_id, questions)
                print(f"[{i:3d}/{total_subtopics}] ✅ {subtopic.title:50s} ({saved} questions)")
                total_questions += saved
                successful += 1
            else:
                print(f"[{i:3d}/{total_subtopics}] ⚠️  {subtopic.title:50s} (failed)")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 GENERATION COMPLETE")
        print("=" * 70)
        print(f"✅ Successful: {successful}/{total_subtopics} subtopics")
        print(f"📝 Total questions generated: {total_questions}")
        print(f"📈 Questions per subtopic: {total_questions // successful if successful > 0 else 0}")
        print("=" * 70)
        print("\n🎉 You can now TEST the entire platform!")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:8000")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

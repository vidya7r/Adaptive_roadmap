import sys
sys.path.insert(0, 'd:\\COMPETITIVE_EXAM\\backend')

from app.database import SessionLocal
from app import models

db = SessionLocal()

total_questions = db.query(models.Question).count()
total_subtopics = db.query(models.Subtopic).count()

print(f'Total Questions: {total_questions}')
print(f'Total Subtopics: {total_subtopics}')

subtopics = db.query(models.Subtopic).limit(3).all()
for sub in subtopics:
    q_count = db.query(models.Question).filter(models.Question.subtopic_id == sub.id).count()
    print(f'  Subtopic {sub.id} ({sub.title}): {q_count} questions')

db.close()

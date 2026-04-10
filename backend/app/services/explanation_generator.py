from sqlalchemy.orm import Session
from .. import models
from .ai_services import generate_explanation


def generate_and_store_explanations(db: Session):

    subtopics = db.query(models.Subtopic).all()

    for subtopic in subtopics:

        if not subtopic.description:

            print(f"Generating: {subtopic.title}")

            explanation = generate_explanation(
                subtopic.title
            )

            subtopic.description = explanation

            db.commit()

    return {"message": "All explanations generated"}
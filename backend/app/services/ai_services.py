import requests
import json
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi"  # Switched from mistral to phi (3-5x faster)

def generate_explanation(subtopic_title):

    prompt = f"""
    Explain the topic "{subtopic_title}" for NDA exam preparation.

    Include:
    1. Definition
    2. Key Concepts
    3. Example
    4. Important Points

    Keep explanation simple and student-friendly.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7
        },
        timeout=300  # 5 minute timeout
    )

    data = response.json()

    return data["response"]


def generate_mcq_questions(
    subtopic_title: str,
    num_questions: int = 5,  # Reduced from 10 to 5 for faster generation
    difficulty: str = "medium"
) -> Dict:
    """
    Generate MCQ questions for a subtopic using Ollama.
    
    Args:
        subtopic_title (str): Title of the subtopic
        num_questions (int): Number of questions to generate (5, 10, or 20)
        difficulty (str): Difficulty level (easy, medium, hard)
    
    Returns:
        Dict: Contains 'questions' list with MCQ objects
    """
    
    difficulty_desc = {
        "easy": "basic and foundational",
        "medium": "moderate and application-based",
        "hard": "advanced and analytical"
    }.get(difficulty, "moderate and application-based")
    
    prompt = f"""
    Generate exactly {num_questions} multiple choice questions for NDA exam preparation.
    
    Topic: {subtopic_title}
    Difficulty: {difficulty_desc}
    
    Format your response as a JSON array with this exact structure:
    [
        {{
            "question": "Question text here?",
            "option_a": "First option",
            "option_b": "Second option",
            "option_c": "Third option",
            "option_d": "Fourth option",
            "correct_answer": "A"
        }},
        ...
    ]
    
    Requirements:
    - Each question must be a proper MCQ for NDA exam
    - Options should be realistic and distinct
    - Correct answer must be one of: A, B, C, D
    - Questions should test understanding, not just memorization
    - Return ONLY the JSON array, no extra text
    """
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,  # Using phi model
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=300  # 5 minutes for Ollama inference
        )
        
        data = response.json()
        response_text = data.get("response", "")
        
        # Clean up response - remove markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        response_text = response_text.strip()
        
        # Parse JSON response
        questions = json.loads(response_text)
        
        # Validate questions
        validated_questions = []
        for q in questions:
            if all(key in q for key in ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer"]):
                q["difficulty"] = difficulty
                validated_questions.append(q)
        
        return {
            "success": True,
            "questions": validated_questions,
            "count": len(validated_questions),
            "requested": num_questions
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Failed to parse JSON response: {str(e)}",
            "questions": []
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout - Ollama took too long to respond",
            "questions": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error generating questions: {str(e)}",
            "questions": []
        }


# --------------------------------------------------
# 📚 ADAPTIVE EXPLANATION GENERATOR
# --------------------------------------------------

def simplify_explanation(explanation: str) -> str:
    """
    Simplify an explanation for beginners (2-3 sentences max).
    
    Args:
        explanation (str): Original explanation
    
    Returns:
        str: Simplified version
    """
    
    prompt = f"""
    Simplify this explanation into 2-3 sentences for a beginner student.
    Make it easy to understand with simple words.
    Remove technical jargon and examples.
    
    Original explanation:
    {explanation}
    
    Simplified version (2-3 sentences only):
    """
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.5
            },
            timeout=60
        )
        
        data = response.json()
        return data["response"].strip()
        
    except Exception as e:
        print(f"Error simplifying explanation: {str(e)}")
        return explanation  # Return original if error


def expand_explanation(explanation: str) -> str:
    """
    Expand an explanation with more details for advanced learners.
    
    Args:
        explanation (str): Original explanation
    
    Returns:
        str: Expanded version with more details
    """
    
    prompt = f"""
    Expand this explanation with more advanced details and real-world applications.
    Add examples, edge cases, and advanced concepts.
    Keep it well-structured with multiple paragraphs.
    
    Original explanation:
    {explanation}
    
    Expanded version (for advanced learners):
    """
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=60
        )
        
        data = response.json()
        return data["response"].strip()
        
    except Exception as e:
        print(f"Error expanding explanation: {str(e)}")
        return explanation  # Return original if error


# --------------------------------------------------
# 💬 AI TUTORING SYSTEM (TASK 3)
# --------------------------------------------------

def tutor_answer_question(subtopic_title: str, user_question: str) -> str:
    """
    Answer a student's question about a topic using AI tutoring.
    
    Args:
        subtopic_title (str): Topic the question is about
        user_question (str): Student's question
    
    Returns:
        str: Personalized tutoring answer
    """
    
    prompt = f"""
    You are an expert NDA exam tutor. A student has asked a question about: {subtopic_title}
    
    Student's question: {user_question}
    
    Provide a clear, educational answer that:
    1. Directly answers their question
    2. Explains the concept simply
    3. Includes a relevant example if possible
    4. Mentions key points to remember
    
    Keep the answer concise but complete (3-5 sentences).
    """
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=60
        )
        
        data = response.json()
        return data["response"].strip()
        
    except Exception as e:
        print(f"Error generating tutoring answer: {str(e)}")
        return f"I couldn't generate an answer. Please try again."


def generate_question_hint(question: str, option_a: str, option_b: str, 
                          option_c: str, option_d: str, hint_level: int = 1) -> str:
    """
    Generate progressive hints for a multiple choice question.
    
    Args:
        question (str): The MCQ question
        option_a, b, c, d (str): The four options
        hint_level (int): Level of hint (1=easy, 2=medium, 3=answer)
    
    Returns:
        str: Progressive hint
    """
    
    options_text = f"""
    A) {option_a}
    B) {option_b}
    C) {option_c}
    D) {option_d}
    """
    
    if hint_level == 1:
        # General guidance
        prompt = f"""
        Give a GENERAL HINT for this NDA exam question (1-2 sentences).
        Don't reveal the answer. Just guide the student on what to think about.
        
        Question: {question}
        
        Options:
        {options_text}
        
        HINT (general guidance only):
        """
    
    elif hint_level == 2:
        # Step-by-step approach
        prompt = f"""
        Give a STEP-BY-STEP HINT for this question (2-3 sentences).
        Help the student eliminate wrong options or think through the logic.
        Still don't give the direct answer.
        
        Question: {question}
        
        Options:
        {options_text}
        
        STEP-BY-STEP HINT (approach to solve):
        """
    
    else:  # hint_level == 3
        # Direct answer with explanation
        prompt = f"""
        This student needs the answer. Provide the CORRECT ANSWER and explain WHY it's correct.
        
        Question: {question}
        
        Options:
        {options_text}
        
        ANSWER with explanation:
        """
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.5
            },
            timeout=60
        )
        
        data = response.json()
        return data["response"].strip()
        
    except Exception as e:
        print(f"Error generating hint: {str(e)}")
        if hint_level == 1:
            return "Try to recall what you learned about this topic."
        elif hint_level == 2:
            return "Think about which options are clearly wrong and eliminate them."
        else:
            return "The answer is available in your study material or explanation."


# --------------------------------------------------
# 💬 CONVERSATIONAL CHATBOT (Like ChatGPT/Gemini)
# --------------------------------------------------

def generate_chat_response(
    user_message: str,
    conversation_history: list,
    topic_context: str = None,
    subtopic_context: str = None
) -> str:
    """
    Generate a conversational response maintaining chat history.
    
    Args:
        user_message (str): Current user message
        conversation_history (list): List of previous messages [{"role": "user"/"assistant", "content": "..."}]
        topic_context (str): Current topic (e.g., "Mathematics")
        subtopic_context (str): Current subtopic (e.g., "Mean, Median, Mode")
    
    Returns:
        str: AI tutor response
    """
    
    # Build conversation context
    history_text = ""
    for msg in conversation_history[-6:]:  # Keep last 6 messages for context (3 turns)
        role = "Student" if msg["role"] == "user" else "Tutor"
        history_text += f"{role}: {msg['content']}\n"
    
    # Build context information
    context_info = "NDA Exam Tutoring Session"
    if subtopic_context:
        context_info += f"\nCurrent Topic: {subtopic_context}"
    elif topic_context:
        context_info += f"\nCurrent Subject: {topic_context}"
    
    prompt = f"""
You are an expert NDA exam tutor having a conversation with a student.
{context_info}

Previous conversation:
{history_text}

Student: {user_message}

Provide a helpful, educational response that:
1. Answers their question directly and clearly
2. Builds on previous messages if relevant
3. Explains concepts in simple terms
4. Includes examples when helpful
5. Offers to clarify or help with related topics

Keep response concise but complete (2-4 sentences typically).

Tutor:
"""
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=90
        )
        
        data = response.json()
        return data["response"].strip()
        
    except Exception as e:
        print(f"Error generating chat response: {str(e)}")
        return "I'm having trouble responding right now. Please try again."
import React, { useState, useEffect } from 'react';
import { ArrowLeft, Loader, CheckCircle, XCircle } from 'lucide-react';
import { ResultsPage } from './ResultsPage';
import '../styles/adaptive-test.css';

export const AdaptiveTestMode = ({ moduleId, onBack }) => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [difficulty, setDifficulty] = useState('easy'); // easy, medium, hard
  const [answeredQuestions, setAnsweredQuestions] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    fetchQuestions();
  }, [moduleId]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      // Mock data - 10 adaptive test questions
      // In real implementation, fetch from /api/questions/{moduleId} with difficulty filtering
      const mockQuestions = [
        {
          id: 1,
          text: 'What is 2 + 2?',
          options: ['3', '4', '5', '6'],
          correct: 1,
          difficulty: 'easy',
          subtopicName: 'Basic Arithmetic',
        },
        {
          id: 2,
          text: 'What is the square of 3?',
          options: ['6', '8', '9', '12'],
          correct: 2,
          difficulty: 'easy',
          subtopicName: 'Basic Arithmetic',
        },
        {
          id: 3,
          text: 'Solve: x + 5 = 12',
          options: ['x = 5', 'x = 7', 'x = 8', 'x = 9'],
          correct: 1,
          difficulty: 'easy',
          subtopicName: 'Linear Equations',
        },
        {
          id: 4,
          text: 'What is 15% of 200?',
          options: ['20', '25', '30', '35'],
          correct: 2,
          difficulty: 'medium',
          subtopicName: 'Percentages',
        },
        {
          id: 5,
          text: 'Solve: 2x² + 5x - 3 = 0',
          options: ['x = 1/2 or x = -3', 'x = 1 or x = -2', 'x = 2 or x = -1/2', 'x = 3 or x = -1'],
          correct: 0,
          difficulty: 'medium',
          subtopicName: 'Quadratic Equations',
        },
        {
          id: 6,
          text: 'What is the derivative of x³?',
          options: ['x²', '3x', '3x²', 'x³/3'],
          correct: 2,
          difficulty: 'hard',
          subtopicName: 'Calculus - Derivatives',
        },
        {
          id: 7,
          text: 'Evaluate: ∫(2x + 3)dx',
          options: ['x² + 3x + C', '2x² + 3x + C', 'x² + 3 + C', '2x + 3 + C'],
          correct: 0,
          difficulty: 'hard',
          subtopicName: 'Calculus - Integration',
        },
        {
          id: 8,
          text: 'What is the common ratio of 2, 6, 18, 54?',
          options: ['2', '3', '4', '5'],
          correct: 1,
          difficulty: 'medium',
          subtopicName: 'Geometric Sequences',
        },
        {
          id: 9,
          text: 'If sin(θ) = 3/5, find cos(θ)?',
          options: ['4/5', '3/4', '2/3', '1/2'],
          correct: 0,
          difficulty: 'hard',
          subtopicName: 'Trigonometry',
        },
        {
          id: 10,
          text: 'What is log₁₀(1000)?',
          options: ['1', '2', '3', '4'],
          correct: 2,
          difficulty: 'medium',
          subtopicName: 'Logarithms',
        },
      ];
      setQuestions(mockQuestions);
    } catch (err) {
      console.error('Error fetching questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const getNextDifficulty = (isCorrect, currentDiff) => {
    if (isCorrect) {
      // If correct, increase difficulty
      if (currentDiff === 'easy') return 'medium';
      if (currentDiff === 'medium') return 'hard';
      return 'hard'; // Stay at hard
    } else {
      // If incorrect, decrease difficulty
      if (currentDiff === 'hard') return 'medium';
      if (currentDiff === 'medium') return 'easy';
      return 'easy'; // Stay at easy
    }
  };

  const handleSelectAnswer = (index) => {
    if (answered) return;
    setSelectedAnswer(index);
    setAnswered(true);

    const isCorrect = index === questions[currentIndex].correct;
    if (isCorrect) {
      setScore(score + 1);
    }

    // Record the answer
    setAnsweredQuestions([
      ...answeredQuestions,
      {
        question: questions[currentIndex],
        selected: index,
        isCorrect,
        difficulty,
      },
    ]);

    // Calculate next difficulty
    if (currentIndex < 9) {
      const nextDiff = getNextDifficulty(isCorrect, difficulty);
      setDifficulty(nextDiff);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelectedAnswer(null);
      setAnswered(false);
    } else {
      // Test completed, show results
      setShowResults(true);
    }
  };

  if (loading) {
    return (
      <div className="adaptive-container loading">
        <Loader size={48} className="spinner" />
        <p>Loading adaptive test...</p>
      </div>
    );
  }

  if (showResults) {
    const timeTaken = Math.round((Date.now() - startTime) / 1000);
    
    // Format answered questions for ResultsPage
    const formattedQuestions = answeredQuestions.map((aq) => ({
      questionId: aq.question.id,
      text: aq.question.text,
      options: aq.question.options,
      userAnswer: aq.selected,
      correctAnswer: aq.question.correct,
      isCorrect: aq.isCorrect,
      difficulty: aq.difficulty,
      subtopicName: aq.question.subtopicName || 'Unknown Topic',
    }));

    const testData = {
      questions: formattedQuestions,
      answeredQuestions: formattedQuestions,
      score: score,
      totalQuestions: questions.length,
      timeTaken: timeTaken,
      accuracy: Math.round((score / questions.length) * 100),
    };

    return (
      <ResultsPage 
        testData={testData}
        testType="adaptive"
        onRetry={() => {
          // Reset to initial state
          setCurrentIndex(0);
          setSelectedAnswer(null);
          setAnswered(false);
          setScore(0);
          setDifficulty('easy');
          setAnsweredQuestions([]);
          setShowResults(false);
        }}
        onBack={onBack}
      />
    );
  }

  const currentQuestion = questions[currentIndex];
  const isCorrect = selectedAnswer === currentQuestion.correct;

  return (
    <div className="adaptive-container">
      <div className="adaptive-header">
        <button className="back-btn" onClick={onBack}>
          <ArrowLeft size={20} />
        </button>

        <div className="header-info">
          <div className="progress-section">
            <span className="progress-text">Question {currentIndex + 1}/10</span>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${((currentIndex + 1) / 10) * 100}%` }}
              />
            </div>
          </div>

          <div className="header-stats">
            <div className="stat">
              <span className="stat-label">Score</span>
              <span className="stat-value">{score}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Difficulty</span>
              <span className={`stat-value diff-${difficulty}`}>{difficulty.toUpperCase()}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="adaptive-content">
        <div className="difficulty-indicator">
          <div className={`difficulty-dot diff-${difficulty}`} />
          <span>
            {difficulty === 'easy' && '⭐ Easy - Building Foundation'}
            {difficulty === 'medium' && '⭐⭐ Medium - Testing Knowledge'}
            {difficulty === 'hard' && '⭐⭐⭐ Hard - Advanced Challenge'}
          </span>
        </div>

        <div className="question-box">
          <h3>Question {currentIndex + 1}</h3>
          <p className="question-text">{currentQuestion.text}</p>
        </div>

        <div className="options-list">
          {currentQuestion.options.map((option, index) => {
            let className = 'option-btn';
            if (answered) {
              if (index === currentQuestion.correct) {
                className += ' correct';
              } else if (index === selectedAnswer && index !== currentQuestion.correct) {
                className += ' incorrect';
              }
            }

            return (
              <button
                key={index}
                className={className}
                onClick={() => handleSelectAnswer(index)}
                disabled={answered}
              >
                <span className="option-letter">
                  {String.fromCharCode(65 + index)}
                </span>
                <span className="option-text">{option}</span>
                {answered && index === currentQuestion.correct && (
                  <CheckCircle size={20} className="icon" />
                )}
                {answered && index === selectedAnswer && index !== currentQuestion.correct && (
                  <XCircle size={20} className="icon" />
                )}
              </button>
            );
          })}
        </div>

        {answered && (
          <div className={`feedback ${isCorrect ? 'correct' : 'incorrect'}`}>
            <p>
              {isCorrect
                ? '✓ Correct! Great job!'
                : `✗ Incorrect - Difficulty adjusting for you`}
            </p>
            {!isCorrect && (
              <p className="correct-answer">
                Correct answer: {currentQuestion.options[currentQuestion.correct]}
              </p>
            )}
          </div>
        )}
      </div>

      {answered && (
        <div className="adaptive-footer">
          {currentIndex < 9 ? (
            <button className="btn btn-next" onClick={handleNext}>
              Next Question →
            </button>
          ) : (
            <button className="btn btn-finish" onClick={handleNext}>
              View Results
            </button>
          )}
        </div>
      )}
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { ArrowLeft, Loader, CheckCircle, XCircle } from 'lucide-react';
import { ResultsPage } from './ResultsPage';
import '../styles/practice-mode.css';

export const PracticeMode = ({ subtopicId, onBack }) => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [answeredQuestions, setAnsweredQuestions] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    fetchQuestions();
  }, [subtopicId]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      // Mock data - 5 practice questions
      // In real implementation, fetch from /api/questions/{subtopicId}
      const mockQuestions = [
        {
          id: 1,
          text: 'What is the solution to 2x + 5 = 13?',
          options: ['x = 4', 'x = 5', 'x = 6', 'x = 8'],
          correct: 0,
          subtopicName: 'Linear Equations',
        },
        {
          id: 2,
          text: 'Solve: 3x - 7 = 11',
          options: ['x = 4', 'x = 6', 'x = 8', 'x = 10'],
          correct: 1,
          subtopicName: 'Linear Equations',
        },
        {
          id: 3,
          text: 'What is x if 4x = 20?',
          options: ['x = 4', 'x = 5', 'x = 6', 'x = 7'],
          correct: 1,
          subtopicName: 'Linear Equations',
        },
        {
          id: 4,
          text: 'Solve: x/2 + 3 = 8',
          options: ['x = 8', 'x = 10', 'x = 12', 'x = 14'],
          correct: 1,
          subtopicName: 'Linear Equations',
        },
        {
          id: 5,
          text: 'Find x: 5x - 2 = 3x + 6',
          options: ['x = 2', 'x = 4', 'x = 6', 'x = 8'],
          correct: 2,
          subtopicName: 'Linear Equations',
        },
      ];
      setQuestions(mockQuestions);
    } catch (err) {
      console.error('Error fetching questions:', err);
    } finally {
      setLoading(false);
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

    // Track answered question
    setAnsweredQuestions([
      ...answeredQuestions,
      {
        questionId: questions[currentIndex].id,
        text: questions[currentIndex].text,
        options: questions[currentIndex].options,
        userAnswer: index,
        correctAnswer: questions[currentIndex].correct,
        isCorrect: isCorrect,
        difficulty: 'normal',
        subtopicName: questions[currentIndex].subtopicName || 'Practice Topic',
      },
    ]);
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
      <div className="practice-container loading">
        <Loader size={48} className="spinner" />
        <p>Loading practice questions...</p>
      </div>
    );
  }

  if (showResults) {
    const timeTaken = Math.round((Date.now() - startTime) / 1000);
    const testData = {
      questions: questions,
      answeredQuestions: answeredQuestions,
      score: score,
      totalQuestions: questions.length,
      timeTaken: timeTaken,
      accuracy: Math.round((score / questions.length) * 100),
    };

    return (
      <ResultsPage 
        testData={testData}
        testType="practice"
        onRetry={() => {
          setCurrentIndex(0);
          setSelectedAnswer(null);
          setAnswered(false);
          setScore(0);
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
    <div className="practice-container">
      <div className="practice-header">
        <button className="back-btn" onClick={onBack}>
          <ArrowLeft size={20} />
        </button>
        <div className="progress">
          <span className="progress-text">Question {currentIndex + 1}/{questions.length}</span>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>
        <div className="score-badge">Score: {score}</div>
      </div>

      <div className="practice-content">
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
            <p>{isCorrect ? '✓ Correct!' : '✗ Incorrect'}</p>
            {!isCorrect && (
              <p className="correct-answer">
                Correct answer: {currentQuestion.options[currentQuestion.correct]}
              </p>
            )}
          </div>
        )}
      </div>

      {answered && (
        <div className="practice-footer">
          {currentIndex < questions.length - 1 ? (
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

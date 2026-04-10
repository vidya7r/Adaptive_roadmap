import React, { useState } from 'react';
import { ArrowLeft, RotateCcw, Share2, CheckCircle, XCircle, Clock, TrendingUp, ChevronRight } from 'lucide-react';
import '../styles/results-page.css';

export const ResultsPage = ({ 
  testData, 
  testType = 'practice', // 'practice' or 'adaptive'
  onRetry, 
  onBack 
}) => {
  const [expandedQuestion, setExpandedQuestion] = useState(null);

  if (!testData) {
    return (
      <div className="results-container error">
        <p>No test data available</p>
      </div>
    );
  }

  const {
    questions = [],
    answeredQuestions = [],
    score = 0,
    totalQuestions = 0,
    timeTaken = 0,
  } = testData;

  const accuracy = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;
  
  // Categorize questions by result
  const correctAnswers = answeredQuestions.filter(q => q.isCorrect).length;
  const incorrectAnswers = totalQuestions - correctAnswers;
  
  // Get performance rating
  const getPerformanceRating = (acc) => {
    if (acc >= 90) return { rating: 'Outstanding!', color: '#4CAF50', emoji: '🌟' };
    if (acc >= 80) return { rating: 'Excellent!', color: '#66BB6A', emoji: '⭐' };
    if (acc >= 70) return { rating: 'Good', color: '#FFA726', emoji: '👍' };
    if (acc >= 60) return { rating: 'Fair', color: '#FFC107', emoji: '📈' };
    return { rating: 'Needs Improvement', color: '#EF5350', emoji: '💪' };
  };

  const performance = getPerformanceRating(accuracy);

  // Format time
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  // Difficulty breakdown
  const difficultyStats = {
    easy: answeredQuestions.filter(q => q.difficulty === 'easy').length,
    medium: answeredQuestions.filter(q => q.difficulty === 'medium').length,
    hard: answeredQuestions.filter(q => q.difficulty === 'hard').length,
  };

  // Topics performance analysis
  const getTopicsPerformance = () => {
    const topicsPerformance = [];
    
    if (testType === 'adaptive') {
      // For adaptive tests, analyze ALL subtopics
      const incorrectBySubtopic = {};
      const totalBySubtopic = {};
      const correctBySubtopic = {};

      answeredQuestions.forEach((question) => {
        // Get subtopic name from question data
        const subtopicName = question.subtopicName || question.topicName || `Topic ${question.id}`;
        
        if (!totalBySubtopic[subtopicName]) {
          totalBySubtopic[subtopicName] = 0;
          correctBySubtopic[subtopicName] = 0;
          incorrectBySubtopic[subtopicName] = [];
        }

        totalBySubtopic[subtopicName]++;
        if (question.isCorrect) {
          correctBySubtopic[subtopicName]++;
        } else {
          incorrectBySubtopic[subtopicName].push(question);
        }
      });

      // Show ONLY weak subtopics (accuracy < 70%)
      Object.keys(totalBySubtopic).forEach((subtopic) => {
        const totalQuestions = totalBySubtopic[subtopic];
        const correctAnswers = correctBySubtopic[subtopic];
        const accuracy = Math.round((correctAnswers / totalQuestions) * 100);
        const isWeak = accuracy < 70; // ONLY show if accuracy < 70%

        // Only add to topicsPerformance if it's weak
        if (isWeak) {
          topicsPerformance.push({
            area: `📚 ${subtopic}`,
            accuracy: accuracy,
            correctCount: correctAnswers,
            totalCount: totalQuestions,
            incorrectCount: incorrectBySubtopic[subtopic].length,
            isWeak: isWeak,
            status: 'Needs Review',
            recommendation: `Study "${subtopic}" again • ${incorrectBySubtopic[subtopic].length} question${incorrectBySubtopic[subtopic].length > 1 ? 's' : ''} missed`
          });
        }
      });

      // Sort: weak first, then strong
      topicsPerformance.sort((a, b) => {
        if (a.isWeak !== b.isWeak) {
          return a.isWeak ? -1 : 1; // Weak topics first
        }
        return a.accuracy - b.accuracy; // Within same category, sort by accuracy
      });
    } else {
      // For practice tests, show only if there are mistakes (accuracy < 100%)
      const incorrectQuestions = answeredQuestions.filter(q => !q.isCorrect);
      const accuracy = Math.round(((answeredQuestions.length - incorrectQuestions.length) / answeredQuestions.length) * 100);
      const isWeak = accuracy < 100; // Show only if not perfect
      
      if (isWeak) {
        topicsPerformance.push({
          area: answeredQuestions[0]?.subtopicName || 'Practice Topic',
          accuracy: accuracy,
          correctCount: answeredQuestions.length - incorrectQuestions.length,
          totalCount: answeredQuestions.length,
          incorrectCount: incorrectQuestions.length,
          isWeak: isWeak,
          status: 'Needs Review',
          recommendation: `Review the ${incorrectQuestions.length} question${incorrectQuestions.length > 1 ? 's' : ''} you missed`
        });
      }
    }
    
    return topicsPerformance;
  };

  const topicsPerformance = getTopicsPerformance();
  // topicsPerformance now contains ONLY weak topics (accuracy < 70%)

  const handleShare = () => {
    const message = `I scored ${score}/${totalQuestions} (${accuracy}%) on the ${testType} test! 🎯`;
    if (navigator.share) {
      navigator.share({
        title: 'NDA Exam Score',
        text: message,
      });
    } else {
      navigator.clipboard.writeText(message);
      alert('Score copied to clipboard!');
    }
  };

  return (
    <div className="results-container">
      {/* Header */}
      <div className="results-header">
        <button className="back-btn" onClick={onBack}>
          <ArrowLeft size={20} />
        </button>
        <h1>Test Complete!</h1>
        <div className="header-spacer" />
      </div>

      {/* Main Score Card */}
      <div className="score-card">
        <div className="score-circle">
          <div className="score-value">{accuracy}%</div>
          <div className="score-label">Accuracy</div>
        </div>

        <div className="score-details">
          <div className="detail-item">
            <div className="detail-number">{score}/{totalQuestions}</div>
            <div className="detail-label">Correct Answers</div>
          </div>

          <div className="detail-item">
            <div className="detail-number">{formatTime(timeTaken)}</div>
            <div className="detail-label">Time Spent</div>
          </div>

          <div className="detail-item">
            <div className="detail-number">{testType === 'practice' ? 'Normal' : 'Adaptive'}</div>
            <div className="detail-label">Test Type</div>
          </div>
        </div>
      </div>

      {/* Performance Badge */}
      <div className="performance-badge" style={{ borderColor: performance.color }}>
        <span className="performance-emoji">{performance.emoji}</span>
        <span className="performance-text">{performance.rating}</span>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-box correct">
          <CheckCircle size={24} />
          <div className="stat-number">{correctAnswers}</div>
          <div className="stat-label">Correct</div>
        </div>

        <div className="stat-box incorrect">
          <XCircle size={24} />
          <div className="stat-number">{incorrectAnswers}</div>
          <div className="stat-label">Incorrect</div>
        </div>

        {testType === 'adaptive' && (
          <>
            <div className="stat-box easy">
              <TrendingUp size={24} />
              <div className="stat-number">{difficultyStats.easy}</div>
              <div className="stat-label">Easy</div>
            </div>

            <div className="stat-box medium">
              <TrendingUp size={24} />
              <div className="stat-number">{difficultyStats.medium}</div>
              <div className="stat-label">Medium</div>
            </div>

            <div className="stat-box hard">
              <TrendingUp size={24} />
              <div className="stat-number">{difficultyStats.hard}</div>
              <div className="stat-label">Hard</div>
            </div>
          </>
        )}
      </div>

      {/* Topics Performance Analysis */}
      {topicsPerformance.length > 0 && (
        <div className="topics-performance-section">
          <h2>📊 Weak Topics Identified</h2>
          <div className="topics-performance-list">
            {topicsPerformance.map((topic, index) => (
              <div 
                key={index} 
                className="topic-performance-card weak"
              >
                <div className="topic-header">
                  <div className="topic-name">{topic.area}</div>
                  <div className="topic-accuracy weak-acc">
                    <span>{topic.accuracy}%</span>
                    <span className="status-badge">Needs Review</span>
                  </div>
                </div>
                <div className="topic-stats">
                  <span className="stat">{topic.correctCount}/{topic.totalCount} correct</span>
                </div>
                <p className="topic-recommendation">
                  ⚠️ {topic.recommendation}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Question Review */}
      <div className="review-section">
        <h2>Question Review</h2>
        <div className="questions-list">
          {answeredQuestions.map((question, index) => (
            <div 
              key={index}
              className={`question-item ${question.isCorrect ? 'correct' : 'incorrect'}`}
              onClick={() => setExpandedQuestion(expandedQuestion === index ? null : index)}
            >
              <div className="question-header">
                <div className="question-number">Q{index + 1}</div>
                <div className="question-status">
                  {question.isCorrect ? (
                    <>
                      <CheckCircle size={20} className="icon-correct" />
                      <span className="status-text">Correct</span>
                    </>
                  ) : (
                    <>
                      <XCircle size={20} className="icon-incorrect" />
                      <span className="status-text">Incorrect</span>
                    </>
                  )}
                </div>
              </div>

              {expandedQuestion === index && (
                <div className="question-details">
                  <p className="question-text">
                    <strong>Question:</strong> {question.question?.text || 'Question text not available'}
                  </p>

                  <div className="options-review">
                    <p className="section-label">Your Answer:</p>
                    <div className={`option-box ${question.isCorrect ? 'user-correct' : 'user-wrong'}`}>
                      {question.question?.options?.[question.selected] || 'N/A'}
                    </div>

                    {!question.isCorrect && (
                      <>
                        <p className="section-label">Correct Answer:</p>
                        <div className="option-box correct-answer">
                          {question.question?.options?.[question.question?.correct] || 'N/A'}
                        </div>
                      </>
                    )}
                  </div>

                  {testType === 'adaptive' && (
                    <div className="difficulty-badge">
                      Difficulty: <span className={`diff-${question.difficulty}`}>{question.difficulty.toUpperCase()}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button className="btn btn-retry" onClick={onRetry}>
          <RotateCcw size={18} />
          Retry Test
        </button>

        <button className="btn btn-share" onClick={handleShare}>
          <Share2 size={18} />
          Share Score
        </button>

        <button className="btn btn-ok" onClick={onBack}>
          <ChevronRight size={18} />
          OK
        </button>
      </div>

      {/* Learning Tips */}
      <div className="tips-section">
        <h3>💡 Learning Tips</h3>
        {accuracy >= 80 ? (
          <p>Great work! Keep practicing to maintain your performance. Try the harder questions next.</p>
        ) : accuracy >= 60 ? (
          <p>Good effort! Review the topics where you struggled and practice more questions.</p>
        ) : (
          <p>Don't worry! Go back and review the learning materials for this topic, then try again.</p>
        )}
      </div>
    </div>
  );
};

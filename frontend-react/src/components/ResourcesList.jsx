import React, { useState, useEffect } from 'react';
import resourceService from '../services/resourceService';
import '../styles/resources-list.css';

/**
 * ResourcesList Component
 * Displays dynamic study materials for a subtopic
 * Supports: YouTube videos, PDFs (from arXiv), Articles (from multiple sources)
 */
export const ResourcesList = ({ subtopicId, subtopicTitle }) => {
  const [resources, setResources] = useState({
    videos: [],
    pdfs: [],
    articles: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('videos');

  // Load all resources when subtopic changes
  useEffect(() => {
    if (subtopicId) {
      loadResources();
    }
  }, [subtopicId]);

  const loadResources = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch all dynamic resources
      const data = await resourceService.getAllResources(subtopicId);
      
      setResources({
        videos: data.videos || [],
        pdfs: data.pdfs || [],
        articles: data.articles || []
      });
    } catch (err) {
      console.error('Error loading resources:', err);
      setError('Failed to load study materials');
    } finally {
      setLoading(false);
    }
  };

  const handleVideoClick = (videoId) => {
    const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
    window.open(videoUrl, '_blank');
  };

  const handlePdfClick = (pdfUrl) => {
    window.open(pdfUrl, '_blank');
  };

  const handleArticleClick = (articleUrl) => {
    window.open(articleUrl, '_blank');
  };

  if (loading) {
    return (
      <div className="resources-wrapper">
        <div className="resources-loading">⏳ Loading study materials...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="resources-wrapper">
        <div className="resources-error">⚠️ {error}</div>
      </div>
    );
  }

  return (
    <div className="resources-wrapper">
      {/* Resource Tabs */}
      <div className="resources-tabs">
        <button 
          className={`resource-tab ${activeTab === 'videos' ? 'active' : ''}`}
          onClick={() => setActiveTab('videos')}
        >
          🎥 Videos {resources.videos.length > 0 && `(${resources.videos.length})`}
        </button>
        <button 
          className={`resource-tab ${activeTab === 'pdfs' ? 'active' : ''}`}
          onClick={() => setActiveTab('pdfs')}
        >
          📄 PDFs {resources.pdfs.length > 0 && `(${resources.pdfs.length})`}
        </button>
        <button 
          className={`resource-tab ${activeTab === 'articles' ? 'active' : ''}`}
          onClick={() => setActiveTab('articles')}
        >
          📖 Articles {resources.articles.length > 0 && `(${resources.articles.length})`}
        </button>
      </div>

      {/* Videos Tab */}
      {activeTab === 'videos' && (
        <div className="resources-content">
          {resources.videos.length > 0 ? (
            <div className="video-list">
              {resources.videos.map((video, index) => (
                <div key={index} className="video-card">
                  <div className="video-header">
                    <img 
                      src={video.thumbnail} 
                      alt={video.title}
                      className="video-thumbnail"
                    />
                    <div className="video-info">
                      <h4 className="video-title">{video.title}</h4>
                      <p className="video-channel">By {video.channelTitle}</p>
                    </div>
                  </div>
                  <p className="video-description">{video.description}</p>
                  <button 
                    className="video-button"
                    onClick={() => handleVideoClick(video.videoId)}
                  >
                    ▶️ Watch on YouTube
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-resource">
              <p>No videos found for {subtopicTitle}</p>
            </div>
          )}
        </div>
      )}

      {/* PDFs Tab */}
      {activeTab === 'pdfs' && (
        <div className="resources-content">
          {resources.pdfs.length > 0 ? (
            <div className="pdf-list">
              {resources.pdfs.map((pdf, index) => (
                <div key={index} className="pdf-card">
                  <div className="pdf-header">
                    <div className="pdf-icon">📄</div>
                    <div className="pdf-info">
                      <h4 className="pdf-title">{pdf.title}</h4>
                      <p className="pdf-source">From: {pdf.source}</p>
                      <p className="pdf-author">By: {pdf.author_display}</p>
                    </div>
                  </div>
                  <div className="pdf-meta">
                    <span className="pdf-date">📅 {pdf.published_date}</span>
                    {pdf.pages && <span className="pdf-pages">📖 {pdf.pages} pages</span>}
                    {pdf.file_size && <span className="pdf-size">💾 {pdf.file_size}</span>}
                    {pdf.rating && <span className="pdf-rating">⭐ {pdf.rating}/5</span>}
                  </div>
                  <p className="pdf-description">{pdf.description}</p>
                  <div className="pdf-actions">
                    <button 
                      className="pdf-button pdf-download"
                      onClick={() => handlePdfClick(pdf.url)}
                    >
                      📥 Download / View
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-resource">
              <p>No PDFs found for {subtopicTitle}</p>
            </div>
          )}
        </div>
      )}

      {/* Articles Tab */}
      {activeTab === 'articles' && (
        <div className="resources-content">
          {resources.articles.length > 0 ? (
            <div className="article-list">
              {resources.articles.map((article, index) => (
                <div key={index} className="article-card">
                  <div className="article-header">
                    <div className="article-icon">📖</div>
                    <div className="article-info">
                      <h4 className="article-title">{article.title}</h4>
                      <p className="article-source">From: {article.source}</p>
                      <p className="article-author">By: {article.author_display}</p>
                    </div>
                  </div>
                  <div className="article-meta">
                    <span className="article-date">📅 {article.published_date}</span>
                    {article.reading_time && <span className="article-time">⏱️ {article.reading_time}</span>}
                    {article.category && <span className="article-category">🏷️ {article.category}</span>}
                    {article.views && <span className="article-views">👁️ {article.views.toLocaleString()} views</span>}
                  </div>
                  <p className="article-description">{article.description}</p>
                  <div className="article-actions">
                    <button 
                      className="article-button article-read"
                      onClick={() => handleArticleClick(article.url)}
                    >
                      🔗 Read Article
                    </button>
                    <button 
                      className="article-button article-save"
                      onClick={() => {
                        // TODO: Implement save/bookmark functionality
                        alert('Feature coming soon!');
                      }}
                    >
                      📌 Save
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-resource">
              <p>No articles found for {subtopicTitle}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResourcesList;

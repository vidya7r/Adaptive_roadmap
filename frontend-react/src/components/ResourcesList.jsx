import React, { useState, useEffect } from 'react';
import resourceService from '../services/resourceService';
import '../styles/resources-list.css';

/**
 * ResourcesList Component
 * Displays dynamic study materials for a subtopic
 * Supports: YouTube videos, PDFs, Articles
 */
export const ResourcesList = ({ subtopicId, subtopicTitle }) => {
  const [resources, setResources] = useState({
    videos: [],
    pdf: null,
    article: null
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
        pdf: data.pdf || null,
        article: data.article || null
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
          className={`resource-tab ${activeTab === 'pdf' ? 'active' : ''}`}
          onClick={() => setActiveTab('pdf')}
        >
          📄 PDF Notes
        </button>
        <button 
          className={`resource-tab ${activeTab === 'article' ? 'active' : ''}`}
          onClick={() => setActiveTab('article')}
        >
          📖 Study Material
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

      {/* PDF Tab */}
      {activeTab === 'pdf' && (
        <div className="resources-content">
          {resources.pdf ? (
            <div className="resource-item">
              <div className="resource-icon">📄</div>
              <div className="resource-details">
                <h4>PDF Study Notes</h4>
                <p className="resource-search">Search: {resources.pdf.search_query}</p>
                <p className="resource-description">Find comprehensive PDF notes and study materials</p>
                <a 
                  href={resources.pdf.pdf_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="resource-button"
                >
                  🔍 Search PDFs
                </a>
              </div>
            </div>
          ) : (
            <div className="empty-resource">
              <p>No PDF resources available</p>
            </div>
          )}
        </div>
      )}

      {/* Article Tab */}
      {activeTab === 'article' && (
        <div className="resources-content">
          {resources.article ? (
            <div className="resource-item">
              <div className="resource-icon">📖</div>
              <div className="resource-details">
                <h4>Study Materials & Articles</h4>
                <p className="resource-search">Search: {resources.article.search_query}</p>
                <p className="resource-description">Access articles, guides, and study materials</p>
                <a 
                  href={resources.article.article_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="resource-button"
                >
                  🔍 Search Materials
                </a>
              </div>
            </div>
          ) : (
            <div className="empty-resource">
              <p>No article resources available</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResourcesList;

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from ..database import get_db
from ..dependencies import get_current_user
from .. import crud, models
from ..services.resource_service import resource_service

router = APIRouter(prefix="/api/resources", tags=["Resources"])


# --------------------------------------------------
# REQUEST/RESPONSE SCHEMAS
# --------------------------------------------------

class ResourceCreate(BaseModel):
    """Request to create a resource"""
    subtopic_id: int
    title: str
    resource_type: str  # pdf, video, link, document
    url: Optional[str] = None
    file_path: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None  # Recommended, Optional, Practice
    order: Optional[int] = 0


class ResourceUpdate(BaseModel):
    """Request to update a resource"""
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class ResourceResponse(BaseModel):
    """Resource response model"""
    id: int
    subtopic_id: int
    title: str
    resource_type: str
    url: Optional[str] = None
    file_path: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    order: int
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


# --------------------------------------------------
# DYNAMIC RESOURCE ENDPOINTS (YouTube, PDF, Articles)
# --------------------------------------------------

@router.get("/youtube/{subtopic_id}")
def get_youtube_videos(
    subtopic_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch YouTube videos dynamically for a subtopic
    
    Returns top 3 YouTube videos related to the subtopic:
    {
        "subtopic_id": 1,
        "subtopic_title": "Kinematics",
        "videos": [
            {
                "title": "...",
                "videoId": "...",
                "description": "...",
                "thumbnail": "...",
                "channelTitle": "..."
            }
        ]
    }
    """
    try:
        # Fetch subtopic from database
        subtopic = db.query(models.Subtopic).filter(
            models.Subtopic.id == subtopic_id
        ).first()
        
        if not subtopic:
            raise HTTPException(
                status_code=404,
                detail=f"Subtopic {subtopic_id} not found"
            )
        
        # Fetch YouTube videos using service
        videos = resource_service.fetch_youtube_videos(subtopic.title, max_results=3)
        
        return {
            "subtopic_id": subtopic_id,
            "subtopic_title": subtopic.title,
            "videos": videos,
            "total": len(videos)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching YouTube videos: {str(e)}"
        )


@router.get("/pdf/{subtopic_id}")
def get_pdf_resources(
    subtopic_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch actual PDF resources from arXiv for a subtopic
    
    Returns:
    {
        "subtopic_id": 1,
        "subtopic_title": "Kinematics",
        "pdfs": [
            {
                "title": "...",
                "url": "...",
                "source": "arXiv",
                "author_display": "...",
                "published_date": "...",
                "description": "...",
                "type": "pdf",
                "pages": "50+",
                "file_size": "2.5 MB",
                "rating": 4.5
            }
        ],
        "total": 5
    }
    """
    try:
        # Fetch subtopic from database
        subtopic = db.query(models.Subtopic).filter(
            models.Subtopic.id == subtopic_id
        ).first()
        
        if not subtopic:
            raise HTTPException(
                status_code=404,
                detail=f"Subtopic {subtopic_id} not found"
            )
        
        # Fetch actual PDFs using MCP resource fetcher
        pdfs = resource_service.fetch_pdfs(subtopic.title, max_results=5)
        
        return {
            "subtopic_id": subtopic_id,
            "subtopic_title": subtopic.title,
            "pdfs": pdfs,
            "total": len(pdfs)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching PDFs: {str(e)}"
        )


@router.get("/article/{subtopic_id}")
def get_article_resources(
    subtopic_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch educational articles from multiple sources for a subtopic
    
    Returns:
    {
        "subtopic_id": 1,
        "subtopic_title": "Kinematics",
        "articles": [
            {
                "title": "...",
                "url": "...",
                "source": "Dev.to",
                "author_display": "...",
                "published_date": "...",
                "description": "...",
                "type": "article",
                "reading_time": "10 min read",
                "category": "Tutorial",
                "views": 1000
            }
        ],
        "total": 5
    }
    """
    try:
        # Fetch subtopic from database
        subtopic = db.query(models.Subtopic).filter(
            models.Subtopic.id == subtopic_id
        ).first()
        
        if not subtopic:
            raise HTTPException(
                status_code=404,
                detail=f"Subtopic {subtopic_id} not found"
            )
        
        # Fetch actual articles using MCP resource fetcher
        articles = resource_service.fetch_articles(subtopic.title, max_results=5)
        
        return {
            "subtopic_id": subtopic_id,
            "subtopic_title": subtopic.title,
            "articles": articles,
            "total": len(articles)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching articles: {str(e)}"
        )


@router.get("/all/{subtopic_id}")
def get_all_resources_for_subtopic(
    subtopic_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all dynamic resources for a subtopic (videos, PDFs, articles)
    
    Returns:
    {
        "subtopic_id": 1,
        "subtopic_title": "Kinematics",
        "videos": [...],
        "pdfs": [...],
        "articles": [...]
    }
    """
    try:
        # Fetch subtopic from database
        subtopic = db.query(models.Subtopic).filter(
            models.Subtopic.id == subtopic_id
        ).first()
        
        if not subtopic:
            raise HTTPException(
                status_code=404,
                detail=f"Subtopic {subtopic_id} not found"
            )
        
        # Get all resources
        all_resources = resource_service.get_all_resources(subtopic.title)
        
        return {
            "subtopic_id": subtopic_id,
            "subtopic_title": subtopic.title,
            **all_resources
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching resources: {str(e)}"
        )


# --------------------------------------------------
# RESOURCE ENDPOINTS
# --------------------------------------------------

@router.post("/create")
def create_resource(
    request: ResourceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new study resource for a subtopic.
    
    Request:
    {
        "subtopic_id": 5,
        "title": "Kinematics Tutorial Video",
        "resource_type": "video",
        "url": "https://youtube.com/...",
        "description": "Comprehensive kinematics tutorial",
        "category": "Recommended",
        "order": 1
    }
    """
    
    # Verify subtopic exists
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == request.subtopic_id
    ).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=404,
            detail=f"Subtopic {request.subtopic_id} not found"
        )
    
    try:
        resource = crud.create_resource(
            db=db,
            subtopic_id=request.subtopic_id,
            title=request.title,
            resource_type=request.resource_type,
            url=request.url,
            file_path=request.file_path,
            description=request.description,
            category=request.category,
            order=request.order
        )
        
        return {
            "id": resource.id,
            "subtopic_id": resource.subtopic_id,
            "title": resource.title,
            "resource_type": resource.resource_type,
            "url": resource.url,
            "file_path": resource.file_path,
            "description": resource.description,
            "category": resource.category,
            "order": resource.order,
            "is_active": resource.is_active,
            "created_at": resource.created_at.isoformat(),
            "message": "Resource created successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating resource: {str(e)}"
        )


@router.get("/subtopic/{subtopic_id}")
def get_subtopic_resources(
    subtopic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all study resources for a specific subtopic.
    
    Returns:
    {
        "subtopic_id": 5,
        "total_resources": 3,
        "resources": [
            {
                "id": 1,
                "title": "Video Tutorial",
                "resource_type": "video",
                "category": "Recommended",
                ...
            },
            ...
        ]
    }
    """
    
    # Verify subtopic exists
    subtopic = db.query(models.Subtopic).filter(
        models.Subtopic.id == subtopic_id
    ).first()
    
    if not subtopic:
        raise HTTPException(
            status_code=404,
            detail=f"Subtopic {subtopic_id} not found"
        )
    
    try:
        resources = crud.get_resources_by_subtopic(db=db, subtopic_id=subtopic_id)
        
        return {
            "subtopic_id": subtopic_id,
            "total_resources": len(resources),
            "resources": [
                {
                    "id": r.id,
                    "title": r.title,
                    "resource_type": r.resource_type,
                    "url": r.url,
                    "file_path": r.file_path,
                    "description": r.description,
                    "category": r.category,
                    "order": r.order,
                    "is_active": r.is_active,
                    "created_at": r.created_at.isoformat()
                }
                for r in resources
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving resources: {str(e)}"
        )


@router.get("/topic/{topic_id}")
def get_topic_resources(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all resources for a topic (across all subtopics).
    """
    
    # Verify topic exists
    topic = db.query(models.Topic).filter(
        models.Topic.id == topic_id
    ).first()
    
    if not topic:
        raise HTTPException(
            status_code=404,
            detail=f"Topic {topic_id} not found"
        )
    
    try:
        resources = crud.get_resources_by_topic(db=db, topic_id=topic_id)
        
        return {
            "topic_id": topic_id,
            "total_resources": len(resources),
            "resources": [
                {
                    "id": r.id,
                    "subtopic_id": r.subtopic_id,
                    "title": r.title,
                    "resource_type": r.resource_type,
                    "url": r.url,
                    "category": r.category,
                    "description": r.description,
                    "created_at": r.created_at.isoformat()
                }
                for r in resources
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving resources: {str(e)}"
        )


@router.get("/{resource_id}")
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get details of a specific resource"""
    
    resource = crud.get_resource(db=db, resource_id=resource_id)
    
    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource {resource_id} not found"
        )
    
    return {
        "id": resource.id,
        "subtopic_id": resource.subtopic_id,
        "title": resource.title,
        "resource_type": resource.resource_type,
        "url": resource.url,
        "file_path": resource.file_path,
        "description": resource.description,
        "category": resource.category,
        "order": resource.order,
        "is_active": resource.is_active,
        "created_at": resource.created_at.isoformat(),
        "updated_at": resource.updated_at.isoformat()
    }


@router.put("/{resource_id}")
def update_resource(
    resource_id: int,
    request: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a resource"""
    
    resource = crud.get_resource(db=db, resource_id=resource_id)
    
    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource {resource_id} not found"
        )
    
    try:
        update_data = request.dict(exclude_unset=True)
        updated_resource = crud.update_resource(db=db, resource_id=resource_id, **update_data)
        
        return {
            "id": updated_resource.id,
            "title": updated_resource.title,
            "resource_type": updated_resource.resource_type,
            "description": updated_resource.description,
            "category": updated_resource.category,
            "is_active": updated_resource.is_active,
            "message": "Resource updated successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating resource: {str(e)}"
        )


@router.delete("/{resource_id}")
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a resource"""
    
    if not crud.get_resource(db=db, resource_id=resource_id):
        raise HTTPException(
            status_code=404,
            detail=f"Resource {resource_id} not found"
        )
    
    try:
        crud.delete_resource(db=db, resource_id=resource_id)
        
        return {
            "id": resource_id,
            "status": "deleted",
            "message": "Resource deleted successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting resource: {str(e)}"
        )

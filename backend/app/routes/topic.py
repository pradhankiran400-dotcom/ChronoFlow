from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.topic import Topic
from app.schemas.topic import TopicCreate,TopicResponse,TopicUpdate

router = APIRouter(
    prefix = "/topics",
    tags = ["Topics"]
)

@router.post("", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(topic:TopicCreate,db:Session = Depends(get_db)):
    existing_topic = (db.query(Topic).filter(Topic.name == topic.name).first())
    if existing_topic:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic already exists")
    new_topic = Topic(
        name=topic.name,
        description=topic.description
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

@router.get("", response_model=list[TopicResponse])
@router.get("/", response_model=list[TopicResponse])
def get_topics(db:Session = Depends(get_db)):
    topics = db.query(Topic).all()
    return topics


@router.get("/{topic_id}",response_model=TopicResponse)
def get_topic(topic_id:int,db:Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic

@router.put("/{topic_id}",response_model=TopicResponse)
def update_topic(topic_id:int,topic_update:TopicUpdate,db:Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    if topic_update.name is not None:
        topic.name = topic_update.name

    if topic_update.description is not None:
        topic.description = topic_update.description

    db.commit()
    db.refresh(topic)
    return topic

@router.delete("/{topic_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(topic_id:int,db:Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    db.delete(topic)
    db.commit()
    return {
        "message": "Topic deleted successfully"
    }
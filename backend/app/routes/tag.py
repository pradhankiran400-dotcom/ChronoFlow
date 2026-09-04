from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate, TagResponse


router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED
)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    existing_tag = (
        db.query(Tag)
        .filter(Tag.name == tag.name)
        .first()
    )

    if existing_tag:
        raise HTTPException(
            status_code=400,
            detail="Tag already exists"
        )

    new_tag = Tag(name=tag.name)

    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag


@router.get(
    "",
    response_model=list[TagResponse]
)
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()


@router.get(
    "/{tag_id}",
    response_model=TagResponse
)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    return tag


@router.put(
    "/{tag_id}",
    response_model=TagResponse
)
def update_tag(
    tag_id: int,
    updated_tag: TagUpdate,
    db: Session = Depends(get_db)
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    tag.name = updated_tag.name

    db.commit()
    db.refresh(tag)

    return tag


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    db.delete(tag)
    db.commit()

    return {
        "message": "Tag deleted successfully"
    }
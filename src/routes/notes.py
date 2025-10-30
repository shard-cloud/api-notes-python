"""
Notes routes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from ..database import get_db, Note, User
from ..auth import get_current_active_user
from ..schemas import (
    NoteCreate, NoteUpdate, NoteResponse, 
    PaginationParams, PaginatedResponse
)

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_notes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's notes with pagination and search"""
    offset = (page - 1) * limit
    
    # Build query
    query = select(Note).where(Note.user_id == current_user.id)
    
    # Add search filter
    if search:
        search_filter = or_(
            Note.title.ilike(f"%{search}%"),
            Note.content.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.order_by(Note.updated_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    notes = result.scalars().all()
    
    # Calculate pages
    pages = (total + limit - 1) // limit
    
    return PaginatedResponse(
        items=notes,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific note by ID"""
    result = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new note"""
    db_note = Note(
        title=note_data.title,
        content=note_data.content,
        user_id=current_user.id
    )
    
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    
    return db_note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a note"""
    result = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Update fields
    update_data = note_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
    
    await db.commit()
    await db.refresh(note)
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a note"""
    result = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    await db.delete(note)
    await db.commit()

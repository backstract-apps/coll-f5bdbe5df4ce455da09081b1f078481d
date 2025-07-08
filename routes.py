from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile,Query, Form
from sqlalchemy.orm import Session
from typing import List,Annotated
import service, models, schemas
from fastapi import Query
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/document')
async def post_document(document_file: UploadFile, db: Session = Depends(get_db)):
    try:
        return await service.post_document(db, document_file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/user_id')
async def get_users_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_users_user_id(db, user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/login')
async def post_login(raw_data: schemas.PostLogin, db: Session = Depends(get_db)):
    try:
        return await service.post_login(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/user')
async def post_user(db: Session = Depends(get_db)):
    try:
        return await service.post_user(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/')
async def get_users(db: Session = Depends(get_db)):
    try:
        return await service.get_users(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/course')
async def post_course(id: int, subject: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.post_course(db, id, subject)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/users/user_id/')
async def put_users_user_id(user_id: int, name: Annotated[str, Query(max_length=100)], username: Annotated[str, Query(max_length=100)], password_hash: Annotated[str, Query(max_length=100)], email: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.put_users_user_id(db, user_id, name, username, password_hash, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/users/user_id')
async def delete_users_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_users_user_id(db, user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/users/')
async def post_users(user_id: int, name: Annotated[str, Query(max_length=100)], username: Annotated[str, Query(max_length=100)], password_hash: Annotated[str, Query(max_length=100, pattern='^[a-zA-Z0-9!@#$%^&*()_+\\-=\\[\\]{}|;:\'",.<>/?]{8,64}$')], email: Annotated[str, Query(max_length=100, pattern='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')], db: Session = Depends(get_db)):
    try:
        return await service.post_users(db, user_id, name, username, password_hash, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/course/id')
async def get_course_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_course_id(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/student/records')
async def post_student_records(student_name: Annotated[str, Query(max_length=100)], email: Annotated[str, Query(max_length=100, pattern='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')], db: Session = Depends(get_db)):
    try:
        return await service.post_student_records(db, student_name, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/student')
async def post_student(db: Session = Depends(get_db)):
    try:
        return await service.post_student(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


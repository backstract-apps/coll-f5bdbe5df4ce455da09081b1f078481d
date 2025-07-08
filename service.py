from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def post_document(db: Session, document_file: UploadFile):

    bucket_name = "backstract-testing"
    region_name = "ap-south-1"
    file_path = "resources"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id="AKIATET5D5CPSTHVVX25",
        aws_secret_access_key="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",
        aws_session_token=None,  # Optional, can be removed if not used
        region_name="ap-south-1",
    )

    # Read file content
    file_content = await document_file.read()

    name = document_file.filename
    file_path = file_path + "/" + name

    import mimetypes

    document_file.file.seek(0)

    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    s3_client.upload_fileobj(
        document_file.file, bucket_name, name, ExtraArgs={"ContentType": content_type}
    )

    file_type = Path(document_file.filename).suffix
    file_size = 200

    file_url = f"https://{bucket_name}.s3.amazonaws.com/{name}"

    file_upload_url = file_url
    res = {
        "document_file": file_upload_url,
    }
    return res


async def get_users_user_id(db: Session, user_id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    user_subject_list = aliased(models.Course)
    query = db.query(models.Users, user_subject_list)

    query = query.join(
        user_subject_list, and_(models.Users.user_id == user_subject_list.id)
    )

    user_list = query.all()
    user_list = (
        [
            {
                "user_list_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "user_list_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in user_list
        ]
        if user_list
        else user_list
    )
    res = {
        "users_one": users_one,
        "user_list": user_list,
    }
    return res


async def post_login(db: Session, raw_data: schemas.PostLogin):
    username: str = raw_data.username
    password_hash: str = raw_data.password_hash

    query = db.query(models.Users)
    query = query.filter(
        and_(
            models.Users.username == username,
            models.Users.password_hash == password_hash,
        )
    )

    login = query.first()

    login = (
        (login.to_dict() if hasattr(login, "to_dict") else vars(login))
        if login
        else login
    )

    if username != password_hash:
        pass

    res = {
        "login": login,
    }
    return res


async def post_user(db: Session):
    res = {}
    return res


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )
    res = {
        "users_all": users_all,
    }
    return res


async def post_course(db: Session, id: int, subject: str):

    record_to_be_added = {"id": id, "subject": subject}
    new_course = models.Course(**record_to_be_added)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    add_a_record = new_course.to_dict()

    try:
        print("Hello")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    res = {
        "add_a_records": add_a_record,
    }
    return res


async def put_users_user_id(
    db: Session, user_id: int, name: str, username: str, password_hash: str, email: str
):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "name": name,
            "email": email,
            "user_id": user_id,
            "username": username,
            "password_hash": password_hash,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )
    res = {
        "users_edited_record": users_edited_record,
    }
    return res


async def delete_users_user_id(db: Session, user_id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete
    res = {
        "users_deleted": users_deleted,
    }
    return res


async def post_users(
    db: Session, user_id: int, name: str, username: str, password_hash: str, email: str
):

    record_to_be_added = {
        "name": name,
        "email": email,
        "user_id": user_id,
        "username": username,
        "password_hash": password_hash,
    }
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    headers = {}
    headers["Authorization"] = (
        "Bearer v4.public.eyJlbWFpbF9pZCI6ICJzaGl2YW0xQHlvcG1haWwuY29tIiwgInVzZXJfaWQiOiAiMzMwZjRhMGIxOTg1NDJlYmIyZGU0NmQyYjFlMjEwYzIiLCAib3JnX2lkIjogIk5BIiwgInN0YXRlIjogInNpZ251cCIsICJyb2xlX25hbWUiOiAiTkEiLCAicm9sZV9pZCI6ICJOQSIsICJwbGFuX2lkIjogIjExMCIsICJhY2NvdW50X3ZlcmlmaWVkIjogIjEiLCAiYWNjb3VudF9zdGF0dXMiOiAiMCIsICJ1c2VyX25hbWUiOiAiMzMwZjRhMGIxOTg1NDJlYmIyZGU0NmQyYjFlMjEwYzIiLCAic2lnbnVwX3F1ZXN0aW9uIjogMywgImV4cCI6IDM1MDQ2MTI3NzAuMjYzNjkzLCAiZXhwaXJ5X3RpbWUiOiAzNTA0NjEyNzcwfY0FSEqkjrIg2_LvyaUP7hd7myEvFeS_A8cEzaBEnio9Qtm_VHhj-1RcurwHMgoMQ4DNudixZVyV7p3Fza_XLgA"
    )
    payload = {"workspace_name": name, "workspace_description": username}
    apiResponse = requests.post(
        "https://cc1fbde45ead-in-south-01.backstract.io/sigma/api/v1/workspace/create",
        headers=headers,
        json=payload if "raw" == "raw" else None,
    )
    external_apis = (
        apiResponse.json() if "dict" in ["dict", "list"] else apiResponse.text
    )
    res = {
        "users_inserted_record": users_inserted_record,
        "mghjgk": external_apis,
    }
    return res


async def get_course_id(db: Session, id: int):

    test = aliased(models.Course)
    query = db.query(models.Course, test)

    query = query.join(test, and_(models.Course.id == test.id))

    test = query.all()
    test = (
        [
            {
                "test_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "test_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in test
        ]
        if test
        else test
    )
    res = {
        "test": test,
    }
    return res


async def post_student_records(db: Session, student_name: str, email: str):

    import uuid

    try:
        id: str = str(uuid.uuid4())
        print(f"id: {id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    record_to_be_added = {"email": email, "student_name": student_name}
    new_records = models.Records(**record_to_be_added)
    db.add(new_records)
    db.commit()
    db.refresh(new_records)
    add_records = new_records.to_dict()

    res = {
        "add_a_records": add_records,
    }
    return res


async def post_student(db: Session):
    res = {}
    return res

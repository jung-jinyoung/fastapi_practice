from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from starlette import status

from database.db_connection import SessionFactory
from models import Todo
from schema.request import TodoCreateRequest, TodoUpdateRequest
from schema.response import TodoResponse

router = APIRouter()

@router.get(
    "/todos",
    response_model=list[TodoResponse],
    status_code=status.HTTP_201_CREATED,
)
def get_todos_handler():
    session = SessionFactory()
    try:
        stmt = select(Todo)
        todos = session.execute(stmt).scalars().all()
        return todos
    finally:
        session.close()


@router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
def get_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)  # 단일 조회 쿼리 객체 생성 (where)
        todo = session.execute(stmt).scalars().first()  # 쿼리 실행 및 단일 결과 선택
        if todo:
            return todo
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo no found")
    finally:
        session.close()


@router.post(
    "/todos",
    response_model=TodoCreateRequest,
    status_code=status.HTTP_201_CREATED,
)
def create_todo_handler(body: TodoCreateRequest):
    session = SessionFactory()
    try:
        todo = Todo(
            title=body.title,
            is_done=body.is_done,
        )  # ORM 모델 객체 생성
        session.add(todo)  # 세션 등록
        session.commit()  # 데이터베이스에 저장
        return todo
    finally:
        session.close()


@router.patch(
    "/todos/{todo_id}",
    response_model=TodoUpdateRequest,
    status_code=status.HTTP_200_OK,
)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)  # 수정 대상 조회 쿼리 객체 생성
        todo = session.execute(stmt).scalars().first()  # 쿼리 실행 및 단일 결과 선택
        if todo:
            if body.title is not None:
                # 제목 수정
                todo.title = body.title
            if body.is_done is not None:
                # 완료 여부 수정
                todo.is_done = body.is_done

            session.commit()  # 변경 사항 저장
            return todo
        # 예외처리
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    finally:
        session.close()


@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)  # 삭제 대상 조회 쿼리 객체 생성
        todo = session.execute(stmt).scalars().first()  # 쿼리 실행 및 단일 결과 선택
        if todo:
            session.delete(todo)  # 삭제 대상 지정
            session.commit()  # 변경 사항 저장
            return
        # 조회 실패
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    finally:
        session.close()

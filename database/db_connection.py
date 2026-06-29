from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. 데이터베이스 연결 정보 설정
DATABASE_URL = "mysql+pymysql://root:luvdh12@localhost:3306/fastapi_db"

# 2. 엔진 설정
engine = create_engine(DATABASE_URL, echo=True)

# 3. 세션 팩토리 생성
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

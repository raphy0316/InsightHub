from .session import engine
from ..models.base import Base
from ..models import user  # 다른 모델 생기면 여기에서 import

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init_db()

from app.core.database import Base, engine

# Import all models so SQLAlchemy registers all tables.
from app import models  # noqa: F401


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("All tables created successfully.")

import sys
import os
import uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.db.models.category import Category
from app.db.models.comment import Comment
from app.db.models.post import Post
from app.db.models.tag import Tag
from app.db.models.user import User

DEFAULT_CATEGORIES = [
    "TECH",
    "BUSINESS",
    "LIFESTYLE",
    "EDUCATION",
    "NEWS"
]

def seed_categories(db: Session):
    existing_categories = db.query(Category).all()
    if existing_categories:
        print(f"Categories already exist: {[c.name for c in existing_categories]}")
        return
    
    new_categories = []
    for name in DEFAULT_CATEGORIES:
        category = Category(
            category_id=uuid.uuid4(),
            name=name
        )
        new_categories.append(category)

    db.add_all(new_categories)
    db.commit()
    print(f"Successfully added categories: {DEFAULT_CATEGORIES}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_categories(db)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
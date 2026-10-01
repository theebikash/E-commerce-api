from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import require_admin
from app. models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).all()



# Only an ADMIN can create a category.
@router.post(
    "/", response_model=CategoryResponse
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin)

):

    existing_category = db.query(Category). filter(
        Category.name == category_data.name). first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"

        )

    new_category = Category(
        name=category_data.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category




# Now an ADMIN should be able to rename a category. (update - put)

@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category



#Now we'll allow an ADMIN to delete a category. (Delete category)

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully"
    }
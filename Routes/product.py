from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Models.product import Product
from Models.user import User
from Schemas.product import ProductCreate, ProductOut
from typing import List
from Auth.dependencies import get_current_user, admin_only
from Database.database import get_db
from typing import Optional

router = APIRouter()

@router.get("/getProducts", response_model=List[ProductOut])
def get_all_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.is_premium or current_user.is_admin:
        products = db.query(Product).filter(Product.is_active == True).all()
    else:
        products = db.query(Product).filter(Product.is_active == True, Product.is_premium == False).all()

    return products

@router.get("/search", response_model=List[ProductOut])
def search_products(
    name: Optional[str] = Query(None, description="Search by product name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product).filter(Product.is_active == True)

    if not (current_user.is_premium or current_user.is_admin):
        query = query.filter(Product.is_premium == False)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    products = query.all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found matching criteria")

    return products

@router.get("/{product_id}", response_model=ProductOut)
def get_product_by_id_for_user(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.is_premium and not (current_user.is_premium or current_user.is_admin):
        raise HTTPException(status_code=403, detail="This product is available to premium users only")

    return product



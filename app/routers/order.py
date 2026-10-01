from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import(
    get_current_user,
    require_admin
)
from app.models.cart import Cart
from app.models.order import Order, OrderItem

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# create-order endpoint

@router.post("/")
def create_order(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart or not cart.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total = 0

    new_order = Order(
        user_id=current_user.id,
        total_amount=0,
        status="PENDING"
    )

    db.add(new_order)
    db.flush()

    for cart_item in cart.items:

        if cart_item.quantity > cart_item.product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {cart_item.product.name}"
            )

        item_price = cart_item.product.price

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=item_price
        )

        total += item_price * cart_item.quantity

        cart_item.product.stock -= cart_item.quantity

        db.add(order_item)

    new_order.total_amount = total

    for cart_item in list(cart.items):
        db.delete(cart_item)

    db.commit()
    db.refresh(new_order)

    return new_order



# A customer should be able to see their own orders.

@router.get("/")
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()

    return orders


# Now we'll allow an ADMIN to see all customer orders.

@router.get("/admin")
def get_all_orders(
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin)
):
    return db.query(Order).all()



# Now an admin should be able to change an order's status.

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    allowed_statuses = {
        "PENDING",
        "PROCESSING",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED"
    }

    status = status.upper()

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    order.status = status

    db.commit()
    db.refresh(order)

    return order
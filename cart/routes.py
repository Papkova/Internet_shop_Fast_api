from fastapi import APIRouter, Depends, status
from accounts import User
import schema
from products.cruds import get_product
from database import get_db
from .cart import Cart
from accounts.authentication import get_current_user
from decimal import Decimal
from starlette.responses import JSONResponse

router = APIRouter(
    tags=['carts'],
    prefix='/carts'
)


@router.get('/list', response_model=schema.Carts)
async def carts(user: User = Depends(get_current_user())):
    total_price = 0
    items = Cart.carts(user.id)
    for item in items:
        total_price = total_price + float(item["product_price"])

    return {"total_price": total_price, "items": items}


@router.post("/add", dependencies=[Depends(get_db)])
async def add_to_cart(add_to_cart: schema.AddtoCart, user: User = Depends(get_current_user())):
    product = get_product(add_to_cart.product_id)
    Cart.add_to_cart(
        user_id=user.id,
        product_id=product.id,
        product_image=str(product.image),
        product_price=str(Decimal(product.price) * add_to_cart.quantity),
        product_quantity=add_to_cart.quantity,
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "OK"})


@router.delete("/delete-item-cart/{row_id}")
async def delete_item_cart(row_id: str, user: User = Depends(get_current_user())):
    Cart.delete_carts(user.id, row_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"massage": "Delete item cart"})


@router.delete("/clear")
async def clear_cart(user: User = Depends(get_current_user())):
    Cart.delete_all_carts(user.id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Delete all items from cart"})

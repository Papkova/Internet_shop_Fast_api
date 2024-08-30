import uuid
from . import models
import shutil
from fastapi import HTTPException, status


def get_products(skip: int = 0, limit: int = 0):
    return list(models.Product.select().offset(skip).limit(limit))


def get_product(product_id: int):
    product = models.Product.filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product is not found")
    return product


def create_product(title, body, image, price, galleries):
    db_product = models.Product(
        title=title,
        body=body,
        image=image,
        price=price
    )
    db_product.save()
    for image in galleries:
        upload_image_product(image, db_product.id)
    return db_product


def upload_image_product(image, product_id):
    filename = f"media/product_galleries/{uuid.uuid1()}_{image.filename}"
    with open(f"{filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    models.Gallery(product=product_id, image=image).save()
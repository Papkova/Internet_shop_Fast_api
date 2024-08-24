import database
from database import db_state_default
from fastapi import FastAPI
from products import Product, Gallery
from order import Order, OrderItem
from accounts import User

database.db.connect()
database.db.create_tables([Product, Gallery, Order, OrderItem, User])
database.db.close()

app = FastAPI()


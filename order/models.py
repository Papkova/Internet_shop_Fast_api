import datetime
from database import db
import peewee
from products import Product
from accounts import User

class Order(peewee.Model):
    user = peewee.ForeignKeyField(User, on_delete='CASCADE')
    price = peewee.DecimalField(max_digits=10, decimal_places=2)
    paid = peewee.BooleanField(default=False)
    create = peewee.DateTimeField(default=datetime.datetime.now())
    address = peewee.TextField()
    authority = peewee.CharField(null=True, max_length=100)

    class Meta:
        database = db


class OrderItem(peewee.Model):
    order = peewee.ForeignKeyField(Order, on_delete='CASCADE')
    product = peewee.ForeignKeyField(Product, on_delete='CASCADE')

    class Meta:
        database = db
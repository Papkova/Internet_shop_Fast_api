import redis
import settings
import uuid
from products import Product


redis = redis.Redis(host='localhost', port=6379, db=1)


class Cart:
    _Expired_TIME = settings.EXPIRED_TIME

    @classmethod
    def add_to_cart(cls, **kwargs):
        user_id = kwargs['user_id']
        for user_carts in redis.scan_iter(f'carts:{user_id}:*'):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in redis.hgetall(user_carts).items()}
            if int(data['user_id']) == user_id and int(data['product_id']) == kwargs['products_id']:
                return 'Item is already in cart'

            print(data)
        kwargs['row_id'] = uuid.uuid4().hex
        key = f"carts:{user_id}:{kwargs['row_id']}"
        [redis.hset(key, index, value) for index, value in kwargs.items()]
        redis.expire(key, cls._Expired_TIME)
        result = {key.decode('utf-8'): value.decode('utf-8') for key, value in redis.hgetall(key).items()}
        return result


    @classmethod
    def carts(cls, user_id):
        results = []
        for user_carts in redis.scan_iter(f'carts:{user_id}:*'):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in redis.hgetall(user_carts).items()}
            results.append(data)
        return results


    @classmethod
    def delete_carts(cls, user_id, rowId):
        return redis.delete(f'carts:{user_id}:{rowId}')

    @classmethod
    def delete_all_carts(cls, user_id):
        [redis.delete(x) for x in redis.scan_iter(f'carts:{user_id}^*')]
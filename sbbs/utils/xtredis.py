# coding:utf8
from redis import StrictRedis

redis = StrictRedis(host='192.168.201.130', port=6379)


def add_post(post_model):
    # redis.set
    # string/list/set/sorted set/hash
    # lpush/rpush lpop/rpop
    redis.lpush('topest_post', post_model)

# def posts()
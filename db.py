# -*- coding: utf-8 -*-
import pymongo
from env import *

db_url = 'mongodb+srv://{user}:{pwd}@{murl}/?retryWrites=true&w=majority'
db_name = 'tg'
db_posts = 'posts'
db_date = 'data'
db_url = db_url.format(user=db_user, pwd=db_pass, murl=db_domain)
client = pymongo.MongoClient(db_url)
database = client[db_name]
posts = database[db_posts]


def update_session(_id, base):
    set_published_query = {'$set': {'session': base}}
    database[db_date].update_one({'_id': _id}, set_published_query)


def get_session():
    return database[db_date].find_one()


def add_to_db(post_list):
    for p in post_list:
        query = {'pid': p.pid}
        if posts.count_documents(query) == 0:
            x = posts.insert_one(p.get_dic())
            print(x.inserted_id)


def get_publish_queue():
    return posts.find({"is_pub": False}).sort('pid', 1)


def should_update(_id):
    query = posts.find_one({}, sort=[('pid', -1)])
    if query is None:
        return True
    print(query['pid'])
    if len(list(query)) == 0:
        return True
    last_id = query['pid']
    return _id > last_id


def set_published(tid, eid):
    set_published_query = {'$set': {'is_pub': True, 'pub_id': eid}}
    posts.update_one({'pid': tid}, set_published_query)

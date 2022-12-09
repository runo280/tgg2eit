from Telegram import MyTelegram
import requests
import os
from post import Post
import db
import json
from env import *
import base64
from api import *
from os.path import isfile


if __name__ == "__main__":

    #get tg session
    squery = db.get_session()
    decoded_string = base64.b64decode(squery['session'])
    with open("seasion.session", "wb") as sfile:
        sfile.write(decoded_string)

    tg = MyTelegram('seasion.session', api_id,
                    api_hash, phone_number, password)

    # update db posts
    if db.should_update(tg.get_latest_post_id()):
        list_to_db = []
        for p in tg.get_latest_posts():
            post = Post(p.id)
            list_to_db.append(post)
            print(p.id)
        db.add_to_db(list_to_db)

    # publish posts

    for p in db.get_publish_queue():
        post = tg.get_message_by_id(id=p['pid'])
        print(post)
        print(post.message)
        if post.file:
            print('has file')
            filename_ = 'msgfile' + post.file.ext
            post.download_media(file=filename_)
            r = send_file(post.message, filename_)
            print(r)
            if r['ok'] == True:
                db.set_published(post.id, r['result']['message_id'])
                if os.path.exists(filename_):
                    os.remove(filename_)
        else:
            print('no file')
            r = send_message(post.message)
            print(r)
            if r['ok'] == True:
                db.set_published(post.id, r['result']['message_id'])

    #save tg session
    with open("seasion.session", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
        db.update_session(squery['_id'], b64_string)

# -*- coding: utf-8 -*-
import base64

import db
from Telegram import MyTelegram
from api import *
from post import Post
from mutil import *
import time


def set_published():
    db.set_published(post.id, r['result']['message_id'])


if __name__ == "__main__":
    # get tg session
    if not is_offline():
        session_query = db.get_session()
        decoded_string = base64.b64decode(session_query['session'])
        with open("seasion.session", "wb") as session_file:
            session_file.write(decoded_string)

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
        time.sleep(10)
        post = tg.get_message_by_id(id=p['pid'])
        print(post)
        text = post.message
        length = len(text)
        if post.file:
            print('has file')
            filename_ = 'msgfile' + post.file.ext
            post.download_media(file=filename_)
            if length < 1400:
                r = send_file(text, filename_)
                delete_msg_file(filename_)
                if r['ok']:
                    if not is_offline():
                        set_published()
                else:
                    print(r)
            else:
                r = send_file("", filename_)
                time.sleep(20)
                r2 = send_message(text)
                delete_msg_file(filename_)
                if r['ok'] and r2['ok']:
                    if not is_offline():
                        set_published()
                else:
                    print(r)
                    print(r2)
        else:
            print('no file')
            r = send_message(text)
            if r['ok']:
                if not is_offline():
                    set_published()
            else:
                print(r)

    # save tg session
    if not is_offline():
        with open("seasion.session", "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
            db.update_session(session_query['_id'], b64_string)

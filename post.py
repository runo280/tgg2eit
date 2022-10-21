# -*- coding: utf-8 -*-
class Post:
    def __init__(self, pid, is_published=False, publish_id=-1):
        self.pid = pid
        self.is_published = is_published
        self.publish_id = publish_id

    def get_dic(self):
        return {'pid': self.pid, 'is_pub': self.is_published, 'pub_id': self.publish_id}

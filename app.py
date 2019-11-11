#-*- coding:utf-8 -*-
import twitter
import threading
import datetime
import urllib
import json
import wget
import sqlite3
import cv2
import os
import numpy as np
from line import line_img

#설정 불러오기
f = open('information.json','r')
settings = json.loads(f.read())

# API설정
api = twitter.Api(consumer_key=settings["consumer_key"],
                  consumer_secret=settings["consumer_secret"],
                  access_token_key=settings["access_token_key"],
                  access_token_secret=settings["access_token_secret"])


f.close()

# 데이터베이스 테이블 생성
conn = sqlite3.connect("already_posted.db")
cur = conn.cursor()
cur.execute("""
        SELECT COUNT(*) FROM sqlite_master
        WHERE TYPE='table' AND name='posted_id'
""")

if cur.fetchone()[0] == 0:
    cur.execute("""
            create table posted_id ( id integer, media_url text, is_posted integer )
    """)

cur.close()
conn.close()

class Task:
    refresh_time = 30 
    user_name = ''

    def __init__(self, name):
        self.user_name = name

    def imageTask(self):
        conn = sqlite3.connect("already_posted.db")
        cur = conn.cursor()
        cur.execute("select * from posted_id order by id desc")
        posted_list = cur.fetchmany(20)

        mentions = api.GetMentions(count = 20)
        for i in mentions:
            posted = []
            for post in posted_list:
                posted.append(post)
            if posted != []:
                if i.AsDict()["id"] in posted_list[0]:
                    break

            tweet = i.text.replace("@" + self.user_name, "")
            if "線画抽出" in tweet:
                img = np.zeros((300, 300, 3), np.uint8)
                img[:] = (255,255,255)
                for j in i.AsDict().keys():
                    if "media" in j:
                        media = i.AsDict()["media"][0]["media_url"]
                        if(len(media) > 0):
                            filename = wget.download(media)
                            img = cv2.imread(filename)
                            img = line_img(img)
                            cv2.imwrite(filename, img)
                            id = i.AsDict()["id"]
                            api.PostUpdate("@" + i.AsDict()["user"]["screen_name"] + " 検出結果です!", media=filename, in_reply_to_status_id=id)
                            os.remove(filename)
                            sql = "insert into posted_id (id, media_url, is_posted) values ( ?, ?, ? )"
                            is_posted = (id, media, 1)
                            cur.execute(sql, is_posted)
                            conn.commit()
        cur.close()
        conn.close()
        threading.Timer(self.refresh_time, self.imageTask).start()


def main():
    task = Task(settings["user_name"])
    task.imageTask()

if __name__ == '__main__':
    main()

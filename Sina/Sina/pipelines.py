# -*- coding: utf-8 -*-
import urllib.request
import pymysql


db_host ='127.0.0.1'
db_user ='root'
db_password = '123456'
db_port ='3306'
db_name = 'sinaweibo'

class WeiboPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(user=db_user, passwd=db_password, db=db_name, host=db_host, port=int(db_port),
                             charset="utf8mb4", use_unicode=True)
        id = item["_id"]
        sel_sql = u"SELECT _id FROM user_info1 WHERE _id = " + str(id)
        cursor = db.cursor()
        cursor.execute(sel_sql)
        cam_row = cursor.fetchone()
        cursor.close()
        if not cam_row:
            # 保存图片
            # image_path ="/usr/local/Sina/ImageFile" #linux保存地址
            image_path = "D:/imagesave3/"
            filename = str(item["_id"]) + '.jpg'
            urllib.request.urlretrieve("https:" + item["Pic_Url"].replace(".50/", ".720/"),
                                       image_path+'%s' % filename)
            cursor = db.cursor()
            cursor.execute("SET NAMES utf8mb4")
            cursor.execute("""INSERT INTO user_info1 
                          (_id, nick_name, gender, info_add, signature,num_tweets,num_follows,num_fans) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                           (
                               str(item['_id']).encode('utf8'),
                               str(item['NickName']).encode('utf8'),
                               str(item['Gender']).encode('utf8'),
                               str(item['Info_Add']).encode('utf8'),
                               str(item['Signature']),
                               str(item['Num_Tweets']).encode('utf8'),
                               str(item['Num_Follows']).encode('utf8'),
                               str(item['Num_Fans']).encode('utf8'),
                           ))
            db.commit()
            cursor.close()





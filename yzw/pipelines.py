# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import pymysql
import time


class YzwPipeline:
    def __init__(self):
        self.cursor = None
        self.db = None
        self.start_time = None
        self.end_time = None

    def process_item(self, item, spider):
        for i in range(1, 5):
            item["Lesson_" + str(i)] = self.process_lesson(item["Lesson_" + str(i)])

        # ****************************************************
        # 存入数据库
        print("准备将数据存入数据库！！！")
        key_sql = "\"" + str(item['School']) + '\",\"' + str(item['College']) + '\",\"' + str(item[
                                                                                                  'Major']) + '\",\"' + str(
            item['Research_Direction']) + '\",\"' + str(item['Number']) + '\",\"' + str(
            item['Lesson_1']) + '\",\"' + str(item[
                                                  'Lesson_2']) + '\",\"' + str(
            item['Lesson_3']) + '\",\"' + str(item['Lesson_4']) + '\",\"' + str(item['Place']) + '\",\"' + str(item[
                                                                                                                   'Graduate_School']) + '\",\"' + str(
            item['Self_Scribing']) + '\",\"' + str(item['PhD']) + '\",\"' + str(item[
                                                                                    'Instructor']) + '\",\"' + str(
            item['Learning_Style']) + '\",\"' + str(item['Remarks']) + '\"'
        sql = 'insert into Admissions_Information (School_name,College,Major,Research_Direction,Number_of_People,Lesson_1,Lesson_2,Lesson_3,Lesson_4,Place,Graduate_School,Self_Scribing,PhD,Instructor,Learning_Style,Remarks) values (' + key_sql + ')'

        self.cursor.execute(sql)
        self.db.commit()
        print("已执行完成sql语句:" + sql)
        # print(sql)

        return item

    def process_lesson(self, lesson):
        lesson.replace('\n', '')
        lesson.replace('\r', '')
        lesson = lesson.strip()
        return lesson

    def open_spider(self, spider):
        self.start_time = time.time()
        # ****************************************************
        # 连接数据库
        self.db = pymysql.connect(host='localhost', user='数据库用户名', password='数据库密码', database='YZW')
        self.cursor = self.db.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        sql = "DROP TABLE IF EXISTS Admissions_Information"
        self.cursor.execute(sql)
        self.db.commit()
        sql = """
         create table Admissions_Information
(
    School_id          int unsigned not null primary key auto_increment,
    School_name        varchar(100) not null,
    College            varchar(100) not null,
    Major              varchar(100) not null,
    Research_Direction varchar(100) not null,
    Number_of_People   varchar(100) not null,
    Lesson_1           varchar(100) not null,
    Lesson_2           varchar(100) not null,
    Lesson_3           varchar(100) not null,
    Lesson_4           varchar(100) not null,
    Place              varchar(100) not null,
    Graduate_School    varchar(100) not null,
    Self_Scribing      varchar(100) not null,
    PhD                varchar(100) not null,
    Instructor         varchar(300) not null,
    Learning_Style     varchar(100) not null,
    Remarks            varchar(300) not null
)
         """
        self.cursor.execute(sql)
        self.db.commit()


    def close_spider(self, spider):
        self.end_time = time.time()
        print("finish!!!,用时共:%f" % (self.end_time - self.start_time)+'s')
        # 输入到excel表
        df = pd.read_sql('select * from Admissions_Information;',
                         con=self.db)
        df.to_excel('./招生信息.xlsx', index=False)
        # ****************************************************
        # 关闭数据库连接
        self.cursor.close()
        self.db.close()

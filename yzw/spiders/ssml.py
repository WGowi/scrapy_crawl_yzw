import re
import scrapy
from yzw.items import YzwItem
from copy import deepcopy


class SsmlSpider(scrapy.Spider):
    name = 'ssml'
    allowed_domains = ['chsi.com.cn']
    mldm = '07'  # 学科门类代码 专业学位为zyxw
    yjxkmd = '0701'  # 学科类别代码
    xxfs = '1'  # 学习方式 1为全日制，2为非全日制
    start_urls = ['https://yz.chsi.com.cn/zsml/queryAction.do']
    start_urls[0] = start_urls[0] + "?mldm=" + mldm + "&yjxkdm=" + yjxkmd + "&xxfs=" + xxfs

    def parse(self, response):
        # print("进入学校页")
        item = YzwItem()
        tr_list = response.xpath("//tbody/tr")
        for tr in tr_list:
            item["School"] = tr.xpath(".//a/text()").extract_first()
            item["Place"] = tr.xpath("./td[2]/text()").extract_first()
            item["Graduate_School"] = "是" if tr.xpath(
                "./td[3]/i[@class='iconfont ch-table-tick']").extract_first() != None else "否"
            item["Self_Scribing"] = "是" if tr.xpath(
                "./td[4]/i[@class='iconfont ch-table-tick']").extract_first() != None else "否"
            item["PhD"] = "是" if tr.xpath("./td[5]/i[@class='iconfont ch-table-tick']").extract_first() != None else "否"
            item["Detail_URL"] = "https://yz.chsi.com.cn" + tr.xpath(".//a/@href").extract_first()
            # print(item)
            # print("*"*10)
            # print(type(item["Detail_URL"]))
            yield scrapy.Request(
                url=str(item["Detail_URL"]),
                meta={"item": deepcopy(item)},
                callback=self.parse_detail,

            )
        if len(response.xpath("//li[@class='lip unable ']")) == 0:
            next_url = self.start_urls[0] + "&pageno=" + str(int(response.xpath(
                "//li[@class='lip selected']/a/text()").extract_first()) + 1)
            # print("next_url:", next_url)
            yield scrapy.Request(
                url=next_url,
                meta={'item': deepcopy(item)},
                callback=self.parse,
            )
            # print("next_url:", next_url)

    def parse_detail(self, response):
        # print("进入详情页")
        item = response.meta['item']
        tr_list = response.xpath("//tbody/tr")
        for tr in tr_list:
            item["College"] = tr.xpath("./td[2]/text()").extract_first()
            item["Major"] = tr.xpath("./td[3]/text()").extract_first()
            item["Research_Direction"] = tr.xpath("./td[4]/text()").extract_first()
            item['Learning_Style'] = tr.xpath("./td[5]/text()").extract_first()
            item['Instructor'] = "尚未确定" if tr.xpath("./td[6]//span/text()").extract_first() is None else tr.xpath(
                "./td[6]//span/text()").extract_first()
            item['Lesson_URL'] = "https://yz.chsi.com.cn" + tr.xpath("./td[8]/a/@href").extract_first()
            yield scrapy.Request(
                url=item['Lesson_URL'],
                meta={"item": deepcopy(item)},
                callback=self.parse_lesson,
            )
            if len(response.xpath("//li[@class='lip unable lip-last']")) == 0:
                next_url = item['Detail_URL'] + "&pageno=" + str(int(response.xpath(
                    "//li[@class='lip selected']/a/text()").extract_first()) + 1)
                # print("next_url:", next_url)
                yield scrapy.Request(
                    url=next_url,
                    meta={'item': deepcopy(item)},
                    callback=self.parse_detail,
                )

    def parse_lesson(self, response):
        # print("进入课程页")
        item = response.meta['item']
        item['Number'] = response.xpath("//tbody/tr[4]/td[4]/text()").extract_first()
        item['Remarks'] = "无" if response.xpath(
            "//tbody/tr[5]/td[2]/span/text()").extract_first() is None else response.xpath(
            "//tbody/tr[5]/td[2]/span/text()").extract_first()
        tbody_list = response.xpath("//div[@class='zsml-result']/table/tbody[@class='zsml-res-items']")
        # print("1" * 10)
        for tbody in tbody_list:
            item["Lesson_1"] = tbody.xpath(".//td[1]/text()").extract_first()
            item["Lesson_2"] = tbody.xpath(".//td[2]/text()").extract_first()
            item["Lesson_3"] = tbody.xpath(".//td[3]/text()").extract_first()
            item["Lesson_4"] = tbody.xpath(".//td[4]/text()").extract_first()
            # print(item)
            yield item




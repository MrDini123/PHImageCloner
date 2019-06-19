# -*- coding: utf-8 -*-
import scrapy


class ProhardverSpider(scrapy.Spider):
    name = 'prohardver'
    allowed_domains = ['prohardver.hu']
    start_urls = ['https://prohardver.hu/tema/allati_vicces_kepek/friss.html']

    def parse(self, response):
        urls = [f"https://prohardver.hu{rel_url}" for rel_url in response.xpath('//*[@id="navi_top_pages"]/div/div/ul/li/a/@href').getall()]

        for url in urls:
            yield scrapy.Request(url, self.parse_images)

    def parse_images(self, response):
        urls = []
        for url in response.xpath('//*[contains(@class, "msg")]/div[contains(@class, "text")]/p/img/@src').getall():
            if url.startswith("/"):
                urls.append(f"https://prohardver.hu{url}")
            elif "kepfeltoltes.hu" in url:
                continue
            else:
                urls.append(url)
        return {"image_urls": urls}

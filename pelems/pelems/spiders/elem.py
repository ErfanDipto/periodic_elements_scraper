import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.loader import ItemLoader
from pelems.items import PelemsItem


class ElemSpider(scrapy.Spider):
    name = "elem"
    allowed_domains = ["ptable.com"]
    start_urls = ["https://pubchem.ncbi.nlm.nih.gov/periodic-table/"]
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", 'div[class*="ptable"] div[class="element"] > button  div'),
                PageMethod("wait_for_load_state", "domcontentloaded")
                ]
        })

    def parse(self, response):
        
        # item["symbol"] = item.add_css
        
        for elem in response.css('div[class*="ptable"] div[class="element"]'):
            item = ItemLoader(item=PelemsItem(), selector=elem)
            
            item.add_css("symbol", 'button > div[data-tooltip="Symbol"]')
            item.add_css("name", 'button > div[data-tooltip="Name"]')
            item.add_css("anum", 'button  div[data-tooltip="Atomic Number"]')
            item.add_css("amass", 'button  div[data-tooltip="Atomic Mass, u"]')
            item.add_css("cgrp", 'button > div[data-tooltip="Chemical Group Block"] > span')
            
            yield item.load_item()
            
            

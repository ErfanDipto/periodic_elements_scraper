# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3, copy, json
# import copy

class GroupedElementPipeline:
    
    def __init__(self):
        self.ele_dict = {}
        
    def process_item(self, item, spider):
        
        cg = item["cgrp"]
        
        if cg not in self.ele_dict:
            self.ele_dict[cg] = {
                "elements_count": 0,
                "element": []
                            }
            
        item_copy = copy.deepcopy(item)
        del item_copy["cgrp"]
        
        self.ele_dict[cg]["elements_count"] += 1
        self.ele_dict[cg]["element"].append(dict(item_copy))
        
        return item
    
    def close_spider(self, spider):
        with open("grouped_elements.json", "w") as f:
            json.dump(self.ele_dict, f)


class PelemsPipeline:
    
    def __init__(self):
        self.con = sqlite3.connect("ptable_db.db")
        self.cursor = self.con.cursor()
        
    def open_spider(self, spider):
        self.cursor.execute("""
                            
                            CREATE TABLE IF NOT EXISTS ptable (
                                symbol TEXT PRIMARY KEY,
                                name TEXT,
                                atomic_number TEXT,
                                atomic_mass REAL,
                                chemical_group TEXT
                            );
                            
                            """)
        self.con.commit()
    
    def process_item(self, item, spider):
        
        self.cursor.execute("""
                            
                            INSERT OR IGNORE INTO ptable VALUES (?, ?, ?, ?, ?);
                            
                            """, (
                                item["symbol"],
                                item["name"],
                                item["anum"],
                                item["amass"],
                                item["cgrp"]
                            ))
        
        self.con.commit()
        
        return item
    
    def close_spider(self, spider):
        self.con.close()

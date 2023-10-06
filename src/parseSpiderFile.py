import sys
import json
args = sys.argv[1:]

# "Source" the provided settings file
with open(args[0], "r") as f:
    exec(f.read())
    
sourced_globals = dict(globals())

def is_spider_inherited(item):
    bases = []
    if hasattr(item, "__bases__"):
        bases = item.__bases__
    
    result = False
    for base in bases:
        if (base.__module__ == "scrapy.spiders" and base.__name__ == "Spider"):
            result = True
            break

    return result

def parse_spider(spiderclass):
    result = {}
    result["name"] = spiderclass.name
    result["start_urls"] = getattr(spiderclass, 'start_urls', [])
    return result

global_variables = dict(globals())


print(
    json.dumps(
        [{'class_name': item[0], **parse_spider(item[1])} for item in global_variables.items() if is_spider_inherited(item[1])],
        indent=4
    )
)
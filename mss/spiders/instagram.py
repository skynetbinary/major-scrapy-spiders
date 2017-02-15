import re
import json

from scrapy import Spider, Item, Field

from mss.utils import get_extracted


class InstagramProfileItems(Item):
    is_private = Field()
    posts = Field()
    username = Field()
    bio = Field()
    website = Field()
    profile_picture = Field()
    full_name = Field()
    total_posts = Field()
    followers = Field()
    following = Field()

class Instagram(Spider):
    name = "Instagram"
    start_urls = ["http://instagram.com/nike/"]

    download_delay = 0.5

    def parse(self, response):
        javascript = "".join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
        json_data = json.loads("".join(re.findall(r'window._sharedData = (.*);', javascript)))

        item = InstagramProfileItems()
        data = get_extracted(json_data["entry_data"]["ProfilePage"])
        item["is_private"] = data["user"]["is_private"]
        item["username"] = data["user"]["username"]
        item["full_name"] = data["user"]["full_name"]
        item["bio"] = data["user"]["biography"]
        item["profile_picture"] = data["user"]["profile_pic_url"]
        item["website"] = data["user"]["external_url"]
        item["followers"] = data["user"]["followed_by"]["count"]
        item["following"] = data["user"]["follows"]["count"]
        item["posts"] = data["user"]["media"]["nodes"]
        item["total_posts"] = data["user"]["media"]["count"]
        return item

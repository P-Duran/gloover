# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

class PricePipeline:
    vat_factor = 1.15

    def process_item(self, item, spider):
        adapter = item
        if adapter.get('price'):
            if adapter.get('price_excludes_vat'):
                adapter['price'] = adapter['price'] * self.vat_factor
            return item
        else:
            raise Exception(f"Missing price in {item}")


if __name__ == "__main__":
    important_datails = ["manufacturer", "item model number", "brand"]
    text = "Product information" \
           "Color:13.3 Inch 2K Portable Monitor Product\n" \
           "Dimensions 10.37 x 7.83 x 0.35 inches\n " \
           "Item Weight 1.65 pounds\n" \
           "Manufacturer Magedok\n " \
           "ASIN B07YCY9N31\n " \
           "Item model number 1332K-5\n " \
           "Customer Reviews\n " \
           "4.2 out of 5 stars\n " \
           "137 ratings\n" \
           "4.2 out of 5 stars\n " \
           "Best Sellers Rank #25,291 in Electronics (See Top 100 in Electronics)\n " \
           "#802 in Computer Monitors\n " \
           "Date First Available September 25, 2019\n " \
           "Feedback Would you like to tell us about a lower price?\n "
    res = {}
    for a in text.lower().split("\n"):
        for detail in important_datails:
            if detail in a:
                res[detail] = (a.replace(detail, "").strip())
    print(res)

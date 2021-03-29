from typing import List


class Product(dict):
    def __init__(self, name: str, asin: str, price: str, product_description: str, short_description: str,
                 images: List[str],
                 rating: float, number_of_reviews: int):
        self.name = name
        self.number_of_reviews = number_of_reviews
        self.rating = rating
        self.images = images
        self.short_description = short_description
        self.product_description = product_description
        self.price = price
        self.asin = asin
        dict.__init__(self, name=name,
                      number_of_reviews=number_of_reviews,
                      rating=rating,
                      images=images,
                      short_description=short_description,
                      product_description=product_description,
                      price=price,
                      asin=asin)

    @classmethod
    def from_json(cls, json_data):
        if '_id' in json_data:
            del json_data['_id']
        return Product(**json_data)

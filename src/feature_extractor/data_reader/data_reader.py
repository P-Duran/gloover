

import pandas as pd


class Review_Reader():
    def __init__(self, path):
        self.path = path
        self.plain_reviews = pd.read_json(
            path, lines=True)

    def reviews_from_asin(self, min_count=200, asin=None):
        if asin == None:
            product_asin = self.plain_reviews.asin.value_counts(
            )[self.plain_reviews.asin.value_counts() > min_count]
            big_number_reviews = self.plain_reviews[self.plain_reviews.asin ==
                                                    product_asin.index[1]]
        else:
            big_number_reviews = self.plain_reviews[self.plain_reviews.asin == asin]
        return big_number_reviews

    def asins(self, min_count=0):
        product_asin = self.plain_reviews.asin.value_counts(
        )[self.plain_reviews.asin.value_counts() > min_count]
        return product_asin
        


if __name__ == "__main__":
    # create_index()
    ''

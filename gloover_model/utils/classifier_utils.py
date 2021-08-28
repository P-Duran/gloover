import json
from datetime import datetime

from gloover_model.serialization.review import Review


def load_json_as_list_reviews(file_path: str):
    with open(file_path) as f:
        reviews = []
        for line in f:
            reviews.append(json.loads(line))

        return [Review(
            review_id=review['unixReviewTime'],
            asin=review['asin'],
            text=review['reviewText'],
            author="review['reviewerName']",
            date=datetime.now(),
            country='?',
            polarity=review['overall'],
            domain='amazon'
        ) for review in reviews]

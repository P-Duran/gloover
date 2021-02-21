import re
from urllib.parse import urlparse


class NetworkUtils:
    _URL_PATTERN = '.*\\.(?P<company>[a-z]*)\\..*'

    @classmethod
    def extract_domain(cls, url):
        domain = urlparse(url).netloc
        return domain

    @classmethod
    def extract_company_name(cls, url):
        domain = cls.extract_domain(url)
        company_name = re.search(cls._URL_PATTERN, domain).group("company")
        return company_name

import re
from urllib.parse import urlparse


class NetworkUtils:
    _URL_PATTERN = '.*\\.(?P<company>[a-z]*)\\..*'

    @classmethod
    def extract_domain(cls, url):
        domain = urlparse(url).netloc
        if not domain:
            domain = url
        return domain

    @classmethod
    def extract_company_name(cls, url):
        domain = cls.extract_domain(url)
        if re.match(cls._URL_PATTERN, domain):
            company_name = re.search(cls._URL_PATTERN, domain).group("company")
            return company_name
        else:
            raise Exception("Url was not in the correcr formar")

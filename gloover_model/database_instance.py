from gloover_model.singleton.singleton_meta import SingletonMeta
from gloover_service.utils.logger import Logger


class DatabaseInstance(metaclass=SingletonMeta):
    database = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, value=None) -> None:
        Logger.log_warning(value)
        self.database = value

from gloover_model.singleton.singleton_meta import SingletonMeta


class DatabaseInstance(metaclass=SingletonMeta):
    database = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, value=None) -> None:
        self.database = value

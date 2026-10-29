class Singleton:
    _INSTANCE = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super().__new__(cls, *kwargs, **kwargs)
        return cls._INSTANCE

    
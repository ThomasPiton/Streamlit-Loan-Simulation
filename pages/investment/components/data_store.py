class DataStore:
    _data = {}

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value

    @classmethod
    def get(cls, key, default=None):
        return cls._data.get(key, default)

    @classmethod
    def all(cls):
        return cls._data

    @classmethod
    def get_all(cls):  # Ajout de cette méthode
        return cls._data.copy()
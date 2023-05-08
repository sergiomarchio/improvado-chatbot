import unicodedata


class Dictionarizable:
    def dict(self):
        """
        default implementation returns __dict__ object
        """
        return self.__dict__


class BotException(Exception):
    def __init__(self, message=''):
        super().__init__(message)
        self.message = message


def normalize_string(string):
    return (unicodedata.normalize('NFD', string)
            .encode('ascii', 'ignore').decode()
            .lower())

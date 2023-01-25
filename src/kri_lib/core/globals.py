
class Globals:
    """
    Set your globals variable here.
    """
    API_ID = None

    def set(self, name, value):
        setattr(self, name, value)

    def unset(self, name, value=None):
        setattr(self, name, value)


GLOBALS = Globals()

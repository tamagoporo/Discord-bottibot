class Context:
    def __init__(self):
        self._bot_token = None
        
    @property
    def bot_token(self):
        return self._bot_token
        
    def set_token(self, bot_token):
        self._bot_token = bot_token
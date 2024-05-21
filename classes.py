class token:
    def __init__(self, token_id, token_time):
        self.token_id = token_id
        self.token_time = token_time
    def Update(self, new_token_id, new_token_time):
        self.token_id = new_token_id
        self.token_time = new_token_time
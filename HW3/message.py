class Message:
    def __init__(self, body, is_spam):
        self.body = body
        self.is_spam = is_spam

    def get_body(self):
        return self.body

    def is_spam(self):
        return self.is_spam

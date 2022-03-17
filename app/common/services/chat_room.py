
class ChatNamespaceService:

    @classmethod
    def generate_code(cls):
        import random
        CHARS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        code: str = ""
        for _ in range(8):
            code += random.choice(CHARS)
            if len(code) == 5:
                code += "-"
        return code
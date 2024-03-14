import re



class CaseConverter:
    # Not part of the public API!

    def __init__(self):
        self._camel_to_snake = re.compile(r'(?<!^)(?=[A-Z])')


    def camel_to_snake(self, payload: str) -> str:
        return self._camel_to_snake.sub('_', payload).lower()

    @staticmethod
    def snake_to_camel(payload: str) -> str:
        tokens = payload.split('_')
        if len(tokens) == 0:
            return ''
        else:
            return tokens[0] + ''.join(map(lambda s: s.title(), tokens[1:]))

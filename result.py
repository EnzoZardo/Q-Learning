class Result:
    def __init__(self, success: bool = True, value: object = {}, message: str = '') -> None:
        self.success: bool = success;
        self.failure: bool = not success;
        self.value = value;
        self.message = message;

class Success(Result):
    def __init__(self, value: object = {}) -> None: super().__init__(True, value);

class Error(Result):
    def __init__(self, message: str) -> None: super().__init__(False, message = message);
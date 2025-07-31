

class ImmutableAttributeError(Exception):
    """불변의 값을 수정하려 시도할때"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class JsonSerializableError(Exception):
    """값이 json 으로 파싱할수 없는 값일때"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class FunctionError(Exception):
    """주어진 값이 함수가 아닐떼"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

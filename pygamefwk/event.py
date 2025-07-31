from typing import List, Callable

class Event:
    """이 클래스는 함수들을 받아 특정상황에 실행합니다
    
    Attributes:
        lisners: A list include functions
    """
    def __init__(self):
        """이벤트를 생성한다"""
        self.lisners : List[Callable] = []
    
    def __call__(self):
        """이벤트를 호출한다"""
        self.invoke()
    
    def __len__(self):
        """이벤트 안에 등록된 함수의 갯수를 반환함

        Returns:
            int: 함수의 갯수
        """
        return len(self.lisners)
    
    def __iadd__(self, value):
        self.add_lisner(value)
    
    def __isub__(self, value):
        self.remove(value)
    
    def add_lisner(self, function: Callable):
        """함수를 인자로 받아 함수를 등록합니다.

        Args:
            function (Callable): 등록할 함수
        """
        self.lisners.append(function)
    
    def remove(self, function: Callable):
        """함수를 리스트에서 제거합니다

        Args:
            function (Callable): 제거할 함수 자체
        """
        self.lisners.remove(function)
    
    def clear(self):
        self.lisners.clear()

    def invoke(self, *arg):
        """lisners의 함수들을 실행합니다."""
        for function in self.lisners:
            function(*arg)
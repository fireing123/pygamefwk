class Input:
    """키보드랑 마우스의 입력을 확인합니다"""
    key_board = {}
    
    mouse_click = [0, 0, 0]

    KEYUPING = 0
    KEYUP = 1
    KEYDOWN = 2
    KEYDOWNING = 3

    @classmethod
    def get_key(cls, key_code: int) -> bool:
        """입력을 받는지 확인합니다

        Args:
            key_code (int): 파이게임 키 -> pygame.K_XXX

        Returns:
            bool: 키보드가 눌림 상태일떄 True
        """
        
        if cls.key_board.get(key_code, cls.KEYUPING) >= cls.KEYDOWN:
            return True
        return False
    
    @classmethod
    def get_key_down(cls, key_code: int) -> bool:
        """이 키가 눌리는 순간인지 확인합니다

        Args:
            key_code (int): 파이게임 키 -> pygame.K_XXX

        Returns:
            bool: 키보드를 누를떄 한번 True
        """
        
        if cls.key_board.get(key_code, cls.KEYUPING) == cls.KEYDOWN:
            return True
        return False
    
    @classmethod
    def get_key_up(cls, key_code: int) -> bool:
        """이 키가 더이상 입력을 받지 않는지 확인합니다

        Args:
            key_code (int): 파이게임 키 -> pygame.K_XXX

        Returns:
            bool: 키보드를 눌렀다가 떗을떄 한번 True
        """
        
        if cls.key_board.get(key_code, cls.KEYUPING) == cls.KEYUP:
            return True
        return False
    
    @classmethod
    def get_mouse(cls, button: int) -> bool:
        """클릭중인지 확인합니다

        Args:
            button (int): 마우스 버튼 0: 왼쪽, 1: 휠, 2:오른쪽 버튼 입니다

        Returns:
            bool: 마우스가 눌림 상태일떄 True
        """
        
        if cls.mouse_click[button] > Input.KEYDOWN:
            return True
        return False
    
    @classmethod
    def get_mouse_down(cls, button: int) -> bool:
        """클릭 하는 순간인지 확인합니다

        Args:
            button (int): 마우스 버튼 0: 왼쪽, 1: 휠, 2:오른쪽 버튼 입니다

        Returns:
            bool: 마우스가 눌릴떄 한번 True
        """
        
        if cls.mouse_click[button] == Input.KEYDOWN:
            return True
        return False
    
    @classmethod
    def get_mouse_up(cls, button: int) -> bool:
        """더이상 클릭을 하지 않는지 확인합니다

        Args:
            button (int): 마우스 버튼 0: 왼쪽, 1: 휠, 2:오른쪽 버튼 입니다

        Returns:
            bool: 마우스 버튼을 누르고 땟을때 True
        """
        if cls.mouse_click[button] == Input.KEYUP:
            return True
        return False
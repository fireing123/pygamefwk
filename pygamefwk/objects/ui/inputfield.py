"""
입력 필드 UI 컴포넌트 모듈

이 모듈은 pygamefwk에서 사용할 수 있는 텍스트 입력 필드와 관련된 클래스들을 제공합니다.
"""

import pygame
from typing import Optional, Tuple

from pygamefwk                           import game, util
from pygamefwk.event                     import Event
from pygamefwk.input                     import Input
from pygamefwk.objects.components.image  import ImageObject
from pygamefwk.objects.ui.text           import Text
from pygamefwk.objects.ui.ui             import UI
from pygamefwk.timertask                 import OnceTimerTask, TimerTask


class InputField(UI):
    """
    텍스트 입력 필드 UI 컴포넌트
    
    사용자가 텍스트를 입력할 수 있는 입력 필드입니다.
    커서 깜빡임, 텍스트 편집, 백스페이스 연속 삭제 등의 기능을 지원합니다.
    """
    
    def __init__(self, name: str, layer: int, tag: str, visible: bool, 
                 position: list, rotation: float, parent_name: str, scale: float, 
                 color: Tuple[int, int, int], font: str, interval: int, 
                 path: str, limit: int, fake_text: str):
        """
        InputField 초기화
        
        Args:
            name: 컴포넌트 이름
            layer: 레이어 번호
            tag: 태그
            visible: 보이기 여부
            position: 위치 [x, y]
            rotation: 회전 각도
            parent_name: 부모 컴포넌트 이름
            scale: 크기 배율
            color: 텍스트 색상 (R, G, B)
            font: 폰트 이름
            interval: 텍스트 간격
            path: 배경 이미지 경로
            limit: 최대 텍스트 길이
            fake_text: 플레이스홀더 텍스트
        """
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        # 배경 이미지 컴포넌트 추가
        image = ImageObject(self, path=path, size=(4, 4), type="topleft", follow=True, collide=True)
        self.components.append(image)

        # 입력 커서 라인 컴포넌트
        self.input_line = InputLine(name + "_line", layer, tag, False, [0, 0], 0, parent_name, scale)
        self.childrens.append(self.input_line)
        
        # 실제 텍스트 표시 컴포넌트
        self.field = Text(name + '_text', layer, tag + "_text", True, [20, -10], 0, name, scale, color, font, interval)
        self.childrens.append(self.field)

        # 플레이스홀더 텍스트 컴포넌트
        self.fake = Text(name + '_fake', layer, tag + "_fake", True, [20, -10], 0, name, scale, (128, 128, 128), font, interval)
        self.childrens.append(self.fake)
        self.fake.text = fake_text

        # 입력 필드 상태 변수들
        self.text: str = ""                    # 실제 입력된 텍스트
        self.focused: bool = False             # 포커스 상태
        self.editing_pos: int = 0              # 편집 커서 위치
        self.limit: int = limit                # 최대 텍스트 길이

        # 텍스트 편집 관련 변수들
        self.text_edit: bool = False           # 텍스트 편집 중인지 여부
        self.text_editing: str = ""            # 편집 중인 텍스트
        self.text_editing_pos: int = 0         # 편집 중인 텍스트의 위치

        # 백스페이스 연속 삭제 관련 변수들
        self.backspace: bool = False           # 백스페이스 연속 삭제 중인지 여부
        self.stay: bool = False                # 마우스가 위에 있는지 여부
        
        # 타이머들
        self.timertask = TimerTask(600)        # 커서 깜빡임 타이머
        self.backtime = TimerTask(40)          # 백스페이스 연속 삭제 타이머
        self.wait_backspace = OnceTimerTask(350)  # 백스페이스 대기 타이머
        
        # 이벤트 리스너 등록
        self.input_event = Event()
        game.event_event.add_lisner(self.event)

    def bar_reset(self) -> None:
        """
        커서 깜빡임 주기를 초기화하고 커서를 보이게 합니다.
        """
        self.timertask.reset()
        self.input_line.location.visible = True
        
    def toggle_bar(self) -> None:
        """
        커서의 보이기/숨기기를 토글합니다.
        """
        self.input_line.location.visible = not self.input_line.location.visible
    
    def toggle_backspace(self) -> None:
        """
        연속 백스페이스 삭제 모드를 토글합니다.
        """
        self.backspace = not self.backspace
    
    def insert(self, index: int, value: str) -> None:
        """
        지정된 위치에 텍스트를 삽입합니다.

        Args:
            index: 삽입할 위치
            value: 삽입할 텍스트
        """
        self.text = util.string_insert(self.text, value, index)
    
    def cut(self, range: Tuple[int, int]) -> None:
        """
        지정된 범위의 텍스트를 잘라냅니다.

        Args:
            range: 잘라낼 범위 (시작, 끝)
        """
        self.text = util.string_cut(self.text, range)
    
    def focus_insert(self, value: str) -> None:
        """
        현재 커서 위치에 텍스트를 삽입합니다.

        Args:
            value: 삽입할 텍스트
        """
        self.insert(self.editing_pos, value)
        self.set_edit_pos(len(value), add=True)
    
    def focus_cut(self, size: int) -> None:
        """
        현재 커서 위치에서 지정된 크기만큼 텍스트를 잘라냅니다.

        Args:
            size: 잘라낼 텍스트 크기
        """
        self.cut((self.editing_pos - size, self.editing_pos))
        self.set_edit_pos(size, sub=True)
        
    def set_edit_pos(self, pos: int, **kwargs) -> None:
        """
        편집 커서의 위치를 변경합니다.

        Args:
            pos: 새로운 커서 위치 또는 연산할 값
            **kwargs: 
                add (bool): True일 때 pos를 현재 위치에 더합니다
                sub (bool): True일 때 pos를 현재 위치에서 뺍니다
        """
        if kwargs.get("add"):
            pos += self.editing_pos
        elif kwargs.get("sub"):
            pos = self.editing_pos - pos
            
        length = len(self.text + self.text_editing)
        
        # 커서 위치 범위 제한
        if pos <= 0:
            self.editing_pos = 0
        elif pos > length:
            self.editing_pos = length
        else:
            self.editing_pos = pos
    
    def on_mouse_enter(self, pos) -> None:
        """마우스가 입력 필드에 진입했을 때 호출됩니다."""
        self.stay = True
    
    def on_mouse_stay(self, pos) -> None:
        """마우스가 입력 필드 위에 있을 때 호출됩니다."""
        if Input.get_mouse_down(0):
            self.focused = True
    
    def on_mouse_exit(self, pos) -> None:
        """마우스가 입력 필드를 벗어났을 때 호출됩니다."""
        self.stay = False
    
    def update(self) -> None:
        """
        입력 필드의 상태를 업데이트합니다.
        키보드 입력, 마우스 입력, 커서 깜빡임 등을 처리합니다.
        """
        if self.focused:
            # 백스페이스 키 처리
            if Input.get_key_down(pygame.K_BACKSPACE):
                pygame.key.start_text_input()
                self.wait_backspace.reset()
                if len(self.text) > 0 and self.editing_pos > 0:
                    self.focus_cut(1)
                    self.bar_reset()   

            # 삭제 키 처리
            elif Input.get_key_down(pygame.K_DELETE):
                self.cut((self.editing_pos, self.editing_pos + 1))

            # 왼쪽 화살표 키 처리
            elif Input.get_key_down(pygame.K_LEFT):
                self.set_edit_pos(1, sub=True)
                self.bar_reset()  

            # 오른쪽 화살표 키 처리
            elif Input.get_key_down(pygame.K_RIGHT):
                self.set_edit_pos(1, add=True)
                self.bar_reset()  

            # 엔터 키 처리
            elif Input.get_key_down(pygame.K_KP_ENTER) or Input.get_key_down(13):
                self.focused = False
                self.input_event.invoke(self.text)

            # 백스페이스 연속 삭제 처리
            elif Input.get_key(pygame.K_BACKSPACE):
                if self.wait_backspace.run_periodic_task():
                    self.toggle_backspace()

            elif Input.get_key_up(pygame.K_BACKSPACE):
                self.backspace = False

            # 백스페이스 연속 삭제 실행
            if self.backspace:
                if self.backtime.run_periodic_task():
                    self.focus_cut(1)
        
        # 포커스 해제 처리
        if not self.stay and Input.get_mouse_down(0):
            self.focused = False
        
        # 텍스트 표시 업데이트
        self.field.text = self.text + self.text_editing
        edit_text_pos = self.editing_pos + len(self.text_editing)
        
        if self.focused:
            # 커서 깜빡임 처리
            if self.timertask.run_periodic_task():
                self.toggle_bar()
            
            # 커서 위치 업데이트
            if self.input_line.location.visible:
                pos = self.field.get_position(edit_text_pos) + self.field.location.world_position
                pos.x += 5
                pos.y += 40
                self.input_line.location.position = pos
            self.fake.location.visible = False
        else:
            # 포커스가 없을 때 커서 숨기기
            self.input_line.location.visible = False
            if self.field.text == "":
                self.fake.location.visible = True

    def event(self, event) -> None:
        """
        pygame 이벤트를 직접 처리합니다.

        Args:
            event: pygame 이벤트 객체
        """
        if self.focused:
            if event.type == pygame.TEXTEDITING:
                # 텍스트 편집 중일 때
                if len(self.text) < self.limit:
                    self.text_edit = True
                    self.text_editing = event.text
                    self.text_editing_pos = event.start
                    self.bar_reset()
                else:
                    pygame.key.stop_text_input()
            elif event.type == pygame.TEXTINPUT:
                # 텍스트 입력 완료 시
                self.text_editing = ""
                self.text_edit = False
                if len(self.text) < self.limit:
                    self.focus_insert(event.text)
                    self.bar_reset()


class InputLine(UI):
    """
    입력 필드의 커서 라인을 표시하는 UI 컴포넌트
    """
    
    def __init__(self, name: str, layer: int, tag: str, visible: bool, 
                 position: list, rotation: float, parent_name: str, y: float):
        """
        InputLine 초기화
        
        Args:
            name: 컴포넌트 이름
            layer: 레이어 번호
            tag: 태그
            visible: 보이기 여부
            position: 위치 [x, y]
            rotation: 회전 각도
            parent_name: 부모 컴포넌트 이름
            y: 커서 라인의 높이
        """
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        
        # 커서 라인 이미지 생성
        image = ImageObject(self, surface=(5, y), type="topleft", follow=True)
        image.og_image.fill((0, 0, 0))  # 검은색으로 채움
        self.components.append(image)
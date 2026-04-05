import pygame
import os
import sys

# 어떻게든 실행되게 하는
os.chdir(
    os.path.abspath(os.path.dirname(__file__)) # 상대 경로를 이 폴더 기준으로 변경한다
)
sys.path.append("./") # 시스템 환경변수에 경로를 추가해해 pygamefwk 를 임포트 가능하게 하고

from pygamefwk import *

SCREEN_SIZE = (1200, 800)
TITLE = "Game Title"

Game.init(SCREEN_SIZE, TITLE) # 초기설정 함수

Game.import_objects("objects/", debug=None) # 입력된 경로의 파일들을 전부 가져와 게임 오브젝트 코드를  pygamefwk가 인식 가능한 상태로 만든다.
# 이코드가 필요한 이유는 오브젝트 생성방식이 pygamefwk가 관리한다. 뒤에 나오는 맵 데이터에 사용하려면 오브젝트는 등록되어야만한다.

@game.world("scene/start.json5")
def main():
    def start():
        ...
    def event(event: Event):
        ...
    def update():
        ...
    return start, event, update

main()
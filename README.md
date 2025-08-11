# pygamefwk

pygame physics의 물리 계산없고 Scene 저장 능력이 상승된 버전.

## 초기 맵 JSON 예시

### 기본 구조

```json
{
  "setting": {
    "tile": [
      ["tileset", false, ["assets/tile1.png", "assets/tile2.png", "assets/tile3.png"], 48]
    ],
    "surface": [
      ["surfaces", false, ["assets/surface1.png", "assets/surface2.png"], 1.0]
    ],
    "sprite_sheet": [
      ["player_sprites", true, "assets/player_sheet.png", 32, 16, 32],
      ["enemy_sprites", false, "assets/enemy_sheet.png", 64, 6, 64]
    ]
  },
  "objs": [
    {
      "GameObject": [
        {
          "name": "main_cam",
          "layer": 0,
          "tag": "camera",
          "visible": true,
          "position": [0, 0],
          "rotation": 0,
          "parent_name": "",
          "scale": 1.0
        }
      ]
    }
  ]
}
```

### 완전한 예시 (복사 붙여넣기용)

```json
{
  "setting": {
    "WIDTH": 800,
    "HEIGHT": 600,
    "FPS": 60,
    "tile": [
      ["tileset", false, ["assets/tiles/grass.png", "assets/tiles/stone.png", "assets/tiles/water.png"], 1.0]
    ],
    "surface": [
      ["surfaces", false, ["assets/surfaces/player.png", "assets/surfaces/enemy.png"], 1.0]
    ],
    "sprite_sheet": [
      ["player_sprites", true, "assets/sprites/player_sheet.png", 32, 16, 1.0],
      ["enemy_sprites", false, "assets/sprites/enemy_sheet.png", 64, 6, 0.5]
    ]
  },
  "objs": [
    {
      "GameObject": [
        {
          "name": "main_cam",
          "layer": 0,
          "tag": "camera",
          "visible": true,
          "position": [0, 0],
          "rotation": 0,
          "parent_name": "",
          "scale": 1.0
        }
      ]
    },
    {
      "Player": [
        {
          "name": "player",
          "layer": 1,
          "tag": "player",
          "visible": true,
          "position": [400, 300],
          "rotation": 0,
          "parent_name": "",
          "scale": 1.0
        }
      ]
    },
    {
      "Enemy": [
        {
          "name": "enemy1",
          "layer": 1,
          "tag": "enemy",
          "visible": true,
          "position": [200, 200],
          "rotation": 0,
          "parent_name": "",
          "scale": 1.0
        },
        {
          "name": "enemy2",
          "layer": 1,
          "tag": "enemy",
          "visible": true,
          "position": [600, 400],
          "rotation": 0,
          "parent_name": "",
          "scale": 1.0
        }
      ]
    }
  ]
}
```

### JSON 구조 설명

#### setting 섹션
- **WIDTH**: 화면 너비
- **HEIGHT**: 화면 높이
- **FPS**: 프레임 레이트
- **tile**: 타일 이미지들 (개별 파일)
  - `[name, is_hits, [paths...], scale]`
- **surface**: 서피스 이미지들 (개별 파일)
  - `[name, is_hits, [paths...], scale]`
- **sprite_sheet**: 스프라이트 시트 (하나의 파일에서 분할)
  - `[name, is_hits, path, tile_size, count, scale]`

#### objs 섹션
- 각 객체 타입별로 그룹화
- 각 객체는 다음 속성을 가짐:
  - **name**: 객체 이름 (고유해야 함)
  - **layer**: 레이어 번호 (0-9)
  - **tag**: 태그
  - **visible**: 보이기 여부
  - **position**: 위치 [x, y]
  - **rotation**: 회전 각도
  - **parent_name**: 부모 객체 이름 (없으면 "")
  - **scale**: 크기 배율

### 사용 방법

1. 위의 JSON 예시를 복사하여 `map.json` 파일로 저장
2. 필요한 이미지 파일들을 `assets/` 폴더에 배치
3. Scene에서 `load("map.json")` 호출

```python
from pygamefwk.scene import Scene

scene = Scene()
scene.load("map.json")
```

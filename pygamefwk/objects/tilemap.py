from uu import Error
from pygamefwk.manger import Manger
from pygamefwk.objects.gameobject import GameObject
import math

class TileMap(GameObject):
    """사분면으로 저장, 원점기준으로 계산함"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, tiles, sheet_name, sheet_type):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.tiles : list[list[list[int]]] = tiles
        if sheet_type == "tile":
            self.sheet = Manger.tile_sheet[sheet_name]
        elif sheet_type == "surface":
            self.sheet = Manger.surface_sheet[sheet_name]
        elif sheet_type == "sprite":
            self.sheet = Manger.sprite_sheet[sheet_name]
        else:
            raise Error("sheet type error")
        self.sheet_name = sheet_name
        self.size = self.sheet.size
        self.canvas = self.sheet

    def set_tile(self, xy, value):
        x, y = xy
        layer = 0
        match xy:
            case n if n[0] >= 0 and n[1] >= 1:
                y -= 1
                layer = 0
            case n if n[0] <= -1 and n[1] >= 1:
                x = -x -1
                y -= 1
                layer = 1
            case n if n[0] < 0 and n[1] < 0:
                x = -x -1
                y = -y
                layer = 2
            case n if n[0] >= 0 and n[1] < 0:
                y = -y
                layer = 3
        try:
            ly = self.tiles[layer][y]
            l = len(ly) - 1
            if l >= x:
                ly[x] = value
            else:
                m = x -l
                ly.extend([None] * m)
                ly[x] = value
        except IndexError as e:
            ly = [None] * (n[0] + 1)
            ly = [[n[0]]] = value
            l = len(self.tiles[layer]) - 1
            if l >= y:
                self.tiles[layer][y] = ly
            else:
                m = y - l
                self.tiles[layer].extend([[]] * m)
                self.tiles[layer][y] = ly

    def get_tile(self, xy):
        try:
            match xy:
                case n if n[0] >= 0 and n[1] >= 1:
                    return self.tiles[0][n[1] - 1][n[0]]
                case n if n[0] <= -1 and n[1] >= 1:
                    return self.tiles[1][n[1] - 1][-n[0] - 1]
                case n if n[0] <= -1 and n[1] <= 0:
                    return self.tiles[2][-n[1]][-n[0] - 1]
                case n if n[0] >= 0 and n[1] <= 0:
                    return self.tiles[3][-n[1]][n[0]]
        except:
            return None
    
    def render(self, surface, camera):
        """보이는 부분만 렌더링"""
        HALF_WIDTH = Manger.WIDTH / (self.size * 2)
        HALF_HEIGHT = Manger.HEIGHT / (self.size * 2)
        tile_camera = camera.location.world_position / self.size
        xrange = int(tile_camera.x - HALF_WIDTH)-1, int(tile_camera.x + HALF_WIDTH) + 2
        yrange = int(tile_camera.y - HALF_HEIGHT)-1, int(tile_camera.y + HALF_HEIGHT) + 2
        for y in range(*yrange):
            for x in range(*xrange):
                tile_n = self.get_tile((x, y))
                if tile_n != None:
                    image = self.canvas[tile_n]
                    if image != None:
                        cx = (HALF_WIDTH + x) * self.size - camera.location.world_position.x
                        cy = (HALF_HEIGHT - y) * self.size + camera.location.world_position.y
                        surface.blit(image, (math.floor(cx), math.floor(cy)))
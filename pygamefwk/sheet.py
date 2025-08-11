"""
이미지를 시작 단계에서 미리 불러오는 모듈

이 모듈은 게임에서 사용할 이미지들을 미리 로드하고 관리하는 기능을 제공합니다.
- SurfaceSheet: 개별 이미지 파일들을 관리
- TileSheet: 타일 이미지들을 관리
- SpriteSheet: 하나의 이미지 파일에서 여러 스프라이트를 분할하여 관리
"""

import pygame
from pygame import image, PixelArray, Surface
from pygame.transform import scale
from pygamefwk.objects.components.image import red
from typing import List, Tuple, Optional


class SurfaceSheet:
    """
    개별 이미지 파일들을 관리하는 시트 클래스
    
    각 이미지 파일을 개별적으로 로드하고 스케일링하여 관리합니다.
    """
    
    def __init__(self, name: str, is_hits: bool, paths: List[str], default: float):
        """
        SurfaceSheet 초기화
        
        Args:
            name: 시트 이름
            is_hits: 히트박스 이미지 생성 여부
            paths: 이미지 파일 경로 리스트
            default: 스케일 배율
        """
        self.name = name
        self.size = default
        cache = [image.load(path).convert_alpha() if path is not None else None for path in paths]
        self.images = []
        
        for surf in cache:
            if surf is None: 
                self.images.append(None)
                continue

            xs, ys = surf.get_size()
            img = scale(surf, (xs * default, ys * default))
            if is_hits:
                red[img] = scale(get_hit_image(surf), (xs * default, ys * default))
            self.images.append(img)
    
    def __len__(self) -> int:
        """이미지 개수 반환"""
        return len(self.images)
    
    def __getitem__(self, index: int):
        """인덱스로 이미지 접근"""
        if 0 <= index < len(self.images):
            return self.images[index]
        raise IndexError(f"SurfaceSheet index {index} out of range")
    
    def __iter__(self):
        """이미지들을 순회"""
        return iter(self.images)
    

class TileSheet:
    """
    타일 이미지들을 관리하는 시트 클래스
    
    각 타일 이미지를 로드하고 스케일링하여 관리합니다.
    """
    
    def __init__(self, name: str, is_hits: bool, paths: List[str], default: float):
        """
        TileSheet 초기화
        
        Args:
            name: 시트 이름
            is_hits: 히트박스 이미지 생성 여부
            paths: 타일 이미지 파일 경로 리스트
            default: 타일 크기
        """
        self.name = name
        self.size = default
        cache = [image.load(path).convert_alpha() if path is not None else None for path in paths]
        self.surfaces = []

        for img in cache:
            if img is None: 
                self.surfaces.append(None)
                continue

            scaled_img = scale(img, (default, default))
            if is_hits:
                red[scaled_img] = scale(get_hit_image(img), (default, default))
            self.surfaces.append(scaled_img)
    
    def __len__(self) -> int:
        """타일 개수 반환"""
        return len(self.surfaces)
    
    def __getitem__(self, index: int):
        """인덱스로 타일 접근"""
        if 0 <= index < len(self.surfaces):
            return self.surfaces[index]
        raise IndexError(f"TileSheet index {index} out of range")
    
    def __iter__(self):
        """타일들을 순회"""
        return iter(self.surfaces)


class SpriteSheet:
    """
    하나의 이미지 파일에서 여러 스프라이트를 분할하여 관리하는 시트 클래스
    
    스프라이트 시트 이미지에서 지정된 크기로 타일들을 분할하여 관리합니다.
    """
    
    def __init__(self, name: str, is_hits: bool, path: str, tile_size: int, count: int, default: float):
        """
        SpriteSheet 초기화
        
        Args:
            name: 시트 이름
            is_hits: 히트박스 이미지 생성 여부
            path: 스프라이트 시트 이미지 파일 경로
            tile_size: 각 타일의 크기 (width, height)
            sheet_size: 시트의 타일 개수 (columns, rows)
            default: 스케일 배율
        """
        self.name = name
        self.size = default
        self.tile_size = tile_size
        self.sheet_size = count
        
        # 스프라이트 시트 이미지 로드
        if path is not None:
            self.sheet_image = image.load(path).convert_alpha()
            
        file_row_count = self.sheet_image.get_size()[0] // tile_size

        # 타일들을 분할하여 저장
        self.sprites = []
        
        for i in range(count):
            # 타일 이미지 추출
            tile_surface = Surface((tile_size, tile_size), pygame.SRCALPHA).convert_alpha()
            tile_surface.blit(self.sheet_image, (0, 0), ((i % file_row_count) * tile_size, (i // file_row_count) * tile_size, tile_size, tile_size))
            
            scaled_tile = scale(tile_surface, (default, default))
            
            # 히트박스 이미지 생성
            if is_hits:
                red[scaled_tile] = get_hit_image(scaled_tile)
            
            self.sprites.append(scaled_tile)
    
    def __len__(self) -> int:
        """스프라이트 개수 반환"""
        return len(self.sprites)
    
    def __getitem__(self, index: int):
        """인덱스로 스프라이트 접근"""
        if 0 <= index < len(self.sprites):
            return self.sprites[index]
        raise IndexError(f"SpriteSheet index {index} out of range")
    
    def __iter__(self):
        """스프라이트들을 순회"""
        return iter(self.sprites)
    
    def get_sprite(self, index: int) -> Optional[Surface]:
        """
        지정된 인덱스의 스프라이트를 반환합니다.
        
        Args:
            index: 스프라이트 인덱스
            
        Returns:
            스프라이트 Surface 객체 또는 None
        """
        if 0 <= index < len(self.sprites):
            return self.sprites[index]
        return None

def get_hit_image(s: Surface) -> Surface:
    """
    이미지를 상대적으로 빨갛게 물들입니다.
    
    이 함수는 매우 느리므로 초기 시작 부분에 미리 사용해야 합니다.
    
    Args:
        s: 원본 Surface
        
    Returns:
        빨간색으로 처리된 Surface
    """
    f = s.copy()
    f.lock()
    p = PixelArray(f)
    h = f.get_height()
    j = f.unmap_rgb
    
    for w in range(f.get_width()):
        l = p[w]
        for y in range(h):
            t = j(l[y])
            r = t.r + 100
            o = (r % 255) // 2
            t.r = r if r < 255 else 255
            t.g = max(t.g - o, 0)
            t.b = max(t.b - o, 0)
            l[y] = t
    
    del p
    f.unlock()
    return f
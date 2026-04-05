from pygame import Rect
from pygamefwk.objects                   import Component, GameObject
from pygamefwk.objects.components.reset  import on_reset
from pygamefwk.event                     import Event
from pygame.math import Vector2 as Vector

from collections import deque
from typing import List
import math

physics_grounds: List[Rect] = []
physics_objects: List['Physics'] = []

def reset():
    physics_grounds.clear()
    physics_objects.clear()

on_reset.add_lisner(reset)

# 기존 전역 gravity(기존 코드와 호환되도록 동일 이름 유지)
gravity = 0.5

class Physics(Component):
    def __init__(self, object: GameObject, rect: Rect, **kwargs) -> None:
        # 기본 필드 (원래 틀과 호환되도록 이름들 유지)
        self.object = object
        self.rect = rect.copy()
        self.on_ground = False
        self.friction = kwargs.get("friction", 0.45)       # 지면 마찰(지수적 감쇠 계수)
        self.air_friction = kwargs.get("air_friction", 0.1) # 공기 저항(지수적 감쇠 계수)
        self.velocity = Vector(0, 0)
        self.type: str = kwargs.get('type', 'center')
        self.collision_enter_event = Event()
        self.gravity_weigth = kwargs.get("gravity_wegith", 1)  # 기존 오타명 유지
        self.gravity_effect = kwargs.get("gravity", True)

        # 추가 물리 파라미터 (옵션)
        self.mass = max(kwargs.get("mass", 1.0), 1e-6)
        self.restitution = max(kwargs.get("restitution", 0.0), 0.0)  # 반발계수
        # 드래그(지수감쇠, 속도 감소) — air_friction/ friction로 기본 동작하므로 보조용
        self.drag = kwargs.get("drag", 0.0)

        # timing
        self._last_ticks = None

        # 내부 상태
        self._pending_collisions = []  # (wall, normal)

        physics_objects.append(self)

    def delete(self):
        try:
            physics_objects.remove(self)
        except:
            pass

    # 기존 코드와 호환되도록 add_force는 즉시 velocity를 더하는 메서드로 유지
    def add_force(self, velocity: Vector):
        self.velocity += Vector(velocity)

    # 추가: 누적 force -> (현 사용성에서는 별도 사용 안해도 됨)
    def apply_force(self, force: Vector):
        # force: 픽셀/초^2 개념. 사용 시 mass로 나누어 가속에 반영하도록 확장 가능.
        # 현재 프레임에 바로 가속으로 반영 (간단하게)
        self.velocity += Vector(force) / max(self.mass, 1e-6)

    def step(self):
        """매 프레임 호출되는 메인 업데이트.
        - self.object.location.position (Vector) 를 실제 위치로 사용.
        - physics_grounds 를 벽으로 하여 Swept AABB 충돌 처리 수행.
        """
        # dt 계산 (초)
        ticks = __import__('pygame').time.get_ticks()
        if self._last_ticks is None:
            self._last_ticks = ticks
            # 초기 동기화: object 위치 -> rect
            try:
                p = self.object.location.position
                # self.type에 맞추어 rect 위치를 설정
                setattr(self.rect, self.type, (int(p.x), int(p.y)) if self.type != 'center' else (int(p.x), int(p.y)))
            except Exception:
                # fallback: rect -> location
                try:
                    self.object.location.position = Vector(self.rect.x, self.rect.y)
                except Exception:
                    pass
            return

        dt = (ticks - self._last_ticks) / 1000.0
        self._last_ticks = ticks

        if dt <= 0:
            return
        # clamp dt to avoid huge jumps
        if dt > 0.05:
            dt = 0.05

        # 현재 실수 좌표 위치
        try:
            pos = Vector(self.object.location.position.x, self.object.location.position.y)
        except Exception:
            # fallback: rect -> pos
            pos = Vector(float(self.rect.x), float(self.rect.y))
            try:
                self.object.location.position = pos
            except Exception:
                pass

        # 중력 적용 (기존 코드의 부호/규약과 호환되도록 '감소' 방식 사용)
        if self.gravity_effect:
            # 기존 코드가 self.velocity.y -= gravity * ... 사용하는 것을 고려하여 동일하게 처리
            self.velocity.y -= gravity * self.gravity_weigth * dt

        # 드래그(옵션)와 질량 기반 가속은 필요 시 apply_force 로 처리되도록 간단히 남겨둠
        if self.drag > 0:
            self.velocity *= math.exp(-self.drag * dt)

        # 충돌 검사 전에 위치 통합을 위해 이동 벡터 계산
        movement = Vector(self.velocity.x * dt, self.velocity.y * dt)

        # 초기 겹침 분리: 만약 현재 rect(실수 pos 기반)이 벽과 겹쳐있다면 분리
        for w in physics_grounds:
            if self._aabb_rect(pos.x, pos.y, self.rect.width, self.rect.height).colliderect(w):
                self._separate_overlap_pos(pos, self.rect.width, self.rect.height, w)

        # 연속 충돌 처리 (swept AABB)
        remaining = 1.0  # movement 비율 (0..1)
        iterations = 0
        encountered_any = False
        collisions = []  # (wall, normal)

        # allow up to a reasonable number of substeps per frame
        while remaining > 1e-6 and iterations < 8:
            iterations += 1
            trial_move = Vector(movement.x * remaining, movement.y * remaining)
            if trial_move.length_squared() < 1e-8:
                pos += trial_move
                break

            earliest_t = 1.0
            hit_wall = None
            hit_normal = Vector(0, 0)

            for w in physics_grounds:
                t, normal = self._swept_aabb_pos(pos, self.rect.width, self.rect.height, w, trial_move)
                if t is not None and 0.0 <= t < earliest_t:
                    earliest_t = t
                    hit_wall = w
                    hit_normal = normal

            if hit_wall is None:
                # 충돌 없음: 전체 이동
                pos += trial_move
                remaining = 0.0
                break
            else:
                # 충돌 발생: 이동의 일부(t)만큼 이동
                if earliest_t > 0:
                    pos += trial_move * earliest_t
                # 작은 스킨 오프셋으로 밀어내어 다음 반복에서 겹침을 방지
                skin = 0.001
                pos += hit_normal * skin

                # 충돌 이벤트 기록
                encountered_any = True
                collisions.append((hit_wall, hit_normal))

                # 속도에서 법선 성분 제거 및 반발 적용 (vn < 0 이면 서로 접근 중)
                vn = self.velocity.dot(hit_normal)
                if vn < 0:
                    # 법선 성분 제거 및 restitution 적용
                    self.velocity = self.velocity - hit_normal * vn * (1 + self.restitution)

                # remaining 시간 갱신
                remaining = remaining * (1.0 - earliest_t)

                # 안전 조건: 속도가 거의 0이면 중단
                if self.velocity.length_squared() < 1e-8:
                    break

        # 충돌 이벤트 호출: 각 충돌마다 타입 맵핑(0=ground,1=ceiling,2=left,3=right)
        if collisions:
            q = deque()
            for w, normal in collisions:
                collide_type = None
                if normal.y < 0:
                    collide_type = 0  # ground (밑에서 받침)
                    self.on_ground = True
                elif normal.y > 0:
                    collide_type = 1  # ceiling / top hit
                elif normal.x < 0:
                    collide_type = 2  # left
                elif normal.x > 0:
                    collide_type = 3  # right
                q.append((w, collide_type))

            # 기존 인터페이스와 동일하게 이벤트 호출
            while q:
                ground, ct = q.popleft()
                try:
                    self.collision_enter_event.invoke(ground, ct)
                except Exception:
                    # 이벤트 핸들러 문제로 루프가 끊기면 무시
                    pass

        # 최종 rect/오브젝트 위치 동기화
        # rect는 정수 픽셀로 저장
        self.rect.x = int(pos.x)
        self.rect.y = int(pos.y)
        # object.location.position 에는 실수 Vector를 저장
        try:
            self.object.location.position = Vector(pos.x, pos.y)
        except Exception:
            pass

        # 마찰(지면/공기) 적용 — 지수적 감쇠 방식으로 간략하게 구현
        if self.on_ground:
            # 지면에서는 더 강한 마찰
            self.velocity.x *= math.exp(-self.friction * dt)
            # 수직 성분은 바닥에 붙이면 매우 작게 유지
            self.velocity.y *= math.exp(-min(self.friction, 5.0) * dt)
        else:
            # 공기 저항
            self.velocity *= math.exp(-self.air_friction * dt)

        # 안정화를 위해 매우 작은 속도는 0으로
        if abs(self.velocity.x) < 1e-3:
            self.velocity.x = 0.0
        if abs(self.velocity.y) < 1e-3:
            self.velocity.y = 0.0

    # ----------------- 내부 헬퍼 -----------------
    def _aabb_rect(self, x, y, w, h) -> Rect:
        return Rect(int(x), int(y), int(w), int(h))

    def _separate_overlap_pos(self, pos: Vector, w: int, h: int, wall: Rect):
        A = Rect(int(pos.x), int(pos.y), int(w), int(h))
        B = wall
        left_pen = A.right - B.left
        right_pen = B.right - A.left
        top_pen = A.bottom - B.top
        bottom_pen = B.bottom - A.top

        pen_x = left_pen if left_pen > 0 else (right_pen if right_pen > 0 else 0)
        pen_y = top_pen if top_pen > 0 else (bottom_pen if bottom_pen > 0 else 0)

        if pen_x == 0 and pen_y == 0:
            return

        # 작은 오프셋 추가
        if pen_x < pen_y:
            if A.centerx < B.centerx:
                pos.x -= pen_x + 0.001
            else:
                pos.x += pen_x + 0.001
        else:
            if A.centery < B.centery:
                pos.y -= pen_y + 0.001
            else:
                pos.y += pen_y + 0.001

    def _swept_aabb_pos(self, pos: Vector, w: int, h: int, wall: Rect, movement: Vector):
        """
        Swept AABB between moving A (pos,w,h) moving by movement vector and static B=wall.
        반환: (entry_time, normal) or (None, None) if no collision in [0..1]
        """
        A_min_x = pos.x
        A_min_y = pos.y
        A_max_x = pos.x + w
        A_max_y = pos.y + h

        B_min_x = wall.x
        B_min_y = wall.y
        B_max_x = wall.x + wall.width
        B_max_y = wall.y + wall.height

        dx = movement.x
        dy = movement.y

        # 이미 겹쳐있는 경우(상위에서 처리)
        if (A_max_x > B_min_x and A_min_x < B_max_x and
            A_max_y > B_min_y and A_min_y < B_max_y):
            return (0.0, Vector(0, 0))

        if dx > 0.0:
            x_entry = B_min_x - A_max_x
            x_exit = B_max_x - A_min_x
        else:
            x_entry = B_max_x - A_min_x
            x_exit = B_min_x - A_max_x

        if dy > 0.0:
            y_entry = B_min_y - A_max_y
            y_exit = B_max_y - A_min_y
        else:
            y_entry = B_max_y - A_min_y
            y_exit = B_min_y - A_max_y

        tx_entry = -math.inf if abs(dx) < 1e-9 else x_entry / dx
        tx_exit  = math.inf  if abs(dx) < 1e-9 else x_exit  / dx

        ty_entry = -math.inf if abs(dy) < 1e-9 else y_entry / dy
        ty_exit  = math.inf  if abs(dy) < 1e-9 else y_exit  / dy

        entry_time = max(tx_entry, ty_entry)
        exit_time  = min(tx_exit, ty_exit)

        # 충돌 조건 검사
        if entry_time > exit_time or (tx_entry < 0 and ty_entry < 0) or (tx_entry > 1 and ty_entry > 1):
            return (None, None)
        if entry_time < 0 or entry_time > 1:
            return (None, None)

        # 법선 계산
        normal = Vector(0, 0)
        if tx_entry > ty_entry:
            normal.x = -1 if dx > 0 else 1
        else:
            normal.y = -1 if dy > 0 else 1

        return (entry_time, normal)

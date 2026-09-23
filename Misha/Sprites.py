import pygame
from math import cos, sin, radians
from settings import angle, gravity
import random

class Player:
    def __init__(self, x, y, color, is_left=False):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.width = 25
        self.height = 25
        self.vy = 0.0
        self.on_ground = False
        self.can_move = True
        self.is_left = is_left
        self.aim_center = 90.0
        self.aim_angle = self.aim_center
        self.aim_amplitude = 60.0
        self.aim_freq = 0.5
        self.aim_phase_sign = 1.0 if self.is_left else -1.0
        self.aim_time = 0.0
        self.outward_timer = 0.0
        self.outward_amount = 45.0

    def update(self, ground, dt=1 / 60, active_turn=None, bullet_fired=False):
        if not self.on_ground:
            self.vy += gravity * dt
            self.y += self.vy

        sample_points = max(3, self.width // 8)
        dy_list = []

        for i in range(sample_points):
            if sample_points == 1:
                rel_x = 0
            else:
                rel_x = int((i / (sample_points - 1)) * (self.width - 1))

            world_x = int(self.x + rel_x)
            local_x = world_x - ground.x

            if 0 <= local_x < ground.width:
                found_dy = None

                for dy in range(0, ground.height):
                    if ground.surface.get_at((local_x, dy))[3] > 0:
                        found_dy = dy
                        break

                if found_dy is not None:
                    dy_list.append(found_dy)

        if not dy_list:
            self.on_ground = False
        else:
            top_dy = min(dy_list)
            target_y = ground.y + top_dy - self.height + 1

            if self.y + self.height > ground.y + top_dy:
                self.y = target_y
                self.vy = 0.0
                self.on_ground = True
                self.can_move = False
            else:
                self.on_ground = False

        if bullet_fired:
            return

        is_current_turn = False

        if active_turn is None:
            is_current_turn = True
        else:
            if active_turn == 1 and self.is_left:
                is_current_turn = True
            if active_turn == 2 and not self.is_left:
                is_current_turn = True

        if not is_current_turn:
            return

        if self.outward_timer > 0.0:
            self.outward_timer = max(0.0, self.outward_timer - dt)
            self.aim_angle = self.aim_center - self.aim_phase_sign * self.outward_amount
        else:
            self.aim_time += dt
            angle_offset = __import__("math").sin(2 * __import__("math").pi * self.aim_freq * self.aim_time) * self.aim_amplitude
            self.aim_angle = self.aim_center + self.aim_phase_sign * angle_offset

    def trigger_outward(self, duration=0.4, amount=None):
        if amount is None:
            amount = self.outward_amount
        self.outward_amount = amount
        self.outward_timer = duration

    def move(self, dx):
        if getattr(self, "can_move", True):
            self.x += dx

    def draw(self, window):
        pygame.draw.rect(window, self.color, (int(self.x), int(self.y), self.width, self.height))

        try:
            cx = float(self.x + self.width / 2)
            cy = float(self.y + self.height / 2)
            barrel_len = 48.0
            barrel_thickness = 10.0
            rad = radians(self.aim_angle)
            dir_x = cos(rad)
            dir_y = -sin(rad)
            tip_x = cx + dir_x * barrel_len
            tip_y = cy + dir_y * barrel_len
            perp_x = -dir_y
            perp_y = dir_x
            hx = perp_x * (barrel_thickness / 2.0)
            hy = perp_y * (barrel_thickness / 2.0)
            p1 = (cx + hx, cy + hy)
            p2 = (cx - hx, cy - hy)
            p3 = (tip_x - hx, tip_y - hy)
            p4 = (tip_x + hx, tip_y + hy)
            pygame.draw.polygon(window, self.color, [p1, p2, p3, p4])
        except Exception:
            pass

    def draw_scaled(self, window, scale=1.0, y_offset=0):
        try:
            sx = int(self.x * scale)
            sy = int(self.y * scale + y_offset)
            w = max(1, int(self.width * scale))
            h = max(1, int(self.height * scale))
            pygame.draw.rect(window, self.color, (sx, sy, w, h))

            cx = float(sx + w / 2)
            cy = float(sy + h / 2)
            barrel_len = 48.0 * scale
            barrel_thickness = max(1.0, 10.0 * scale)
            rad = radians(self.aim_angle)
            dir_x = cos(rad)
            dir_y = -sin(rad)
            tip_x = cx + dir_x * barrel_len
            tip_y = cy + dir_y * barrel_len
            perp_x = -dir_y
            perp_y = dir_x
            hx = perp_x * (barrel_thickness / 2.0)
            hy = perp_y * (barrel_thickness / 2.0)
            p1 = (cx + hx, cy + hy)
            p2 = (cx - hx, cy - hy)
            p3 = (tip_x - hx, tip_y - hy)
            p4 = (tip_x + hx, tip_y + hy)
            pygame.draw.polygon(window, self.color, [p1, p2, p3, p4])
        except Exception:
            pass

class Bullet:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 10
        self.width = self.radius
        self.height = self.radius
        self.velocity = 0
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.launch_angle = None
        self.muzzle_x = None
        self.muzzle_y = None

    def set_velocity(self, velocity):
        self.velocity = velocity

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def draw_scaled(self, window, scale=1.0, y_offset=0):
        sx = int(self.x * scale)
        sy = int(self.y * scale + y_offset)
        r = max(1, int(self.radius * scale))
        pygame.draw.circle(window, self.color, (sx, sy), r)

    def reset(self):
        self.x = -20
        self.y = -20
        self.velocity = 0
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.launch_angle = None
        self.muzzle_x = None
        self.muzzle_y = None

    def launch(self, turn, player1, player2):
        shooter = player1 if turn == 1 else player2
        ang = shooter.aim_angle
        rad = radians(ang)
        vx = cos(rad)
        vy = sin(rad)
        cx = shooter.x + shooter.width / 2.0
        cy = shooter.y + shooter.height / 2.0
        muzzle_offset = max(12.0, shooter.width / 2.0 + 12.0)
        self.muzzle_x = cx + vx * muzzle_offset
        self.muzzle_y = cy - vy * muzzle_offset
        self.launch_angle = ang

    def move_with_players(self, turn, t, player1, player2):
        if self.launch_angle is not None and self.muzzle_x is not None:
            rad = radians(self.launch_angle)
            vx = cos(rad)
            vy = sin(rad)
            self.x = self.muzzle_x + self.velocity * vx * t
            self.y = self.muzzle_y - (self.velocity * vy * t - 0.5 * gravity * t**2)
        else:
            shooter = player1 if turn == 1 else player2
            ang = shooter.aim_angle
            rad = radians(ang)
            vx = cos(rad)
            vy = sin(rad)
            cx = shooter.x + shooter.width / 2.0
            cy = shooter.y + shooter.height / 2.0
            muzzle_offset = max(12.0, shooter.width / 2.0 + 12.0)
            muzzle_x = cx + vx * muzzle_offset
            muzzle_y = cy - vy * muzzle_offset
            self.x = muzzle_x + self.velocity * vx * t
            self.y = muzzle_y - (self.velocity * vy * t - 0.5 * gravity * t**2)

        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def explosion_on_ground(self, ground):
        if self.rect.colliderect(ground.rect):
            collision_x = int(self.x - ground.x)
            collision_y = int(self.y - ground.y)
            radius = 40
            ground.create_crater(collision_x, collision_y, radius)
            return float(self.x), float(self.y), radius
        return None

class Ground:
    def __init__(self, x, y, width, height, color=(90, 60, 30, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        num_internal = random.randint(2, 6)
        xs = [0]

        for i in range(1, num_internal + 1):
            frac = i / (num_internal + 1)
            xs.append(int(frac * width))

        xs.append(width)
        top_points = []
        max_scatter = max(10, int(self.height * 0.5))

        for rx in xs:
            top_y = random.randint(0, max_scatter)
            top_points.append((rx, top_y))

        top_points.sort(key=lambda p: p[0])
        polygon = []

        for p in top_points:
            polygon.append(p)

        polygon.append((width, height))
        polygon.append((0, height))
        pygame.draw.polygon(self.surface, (149, 104, 25, 255), polygon)

    def draw(self, window):
        window.blit(self.surface, (self.x, self.y))

    def draw_scaled(self, window, scale=1.0, y_offset=0):
        try:
            sx = int(self.x * scale)
            w = max(1, int(self.width * scale))
            h = max(1, int(self.height * scale))
            scaled = pygame.transform.smoothscale(self.surface, (w, h))
            sy = int(self.y * scale + y_offset)
            window.blit(scaled, (sx, sy))
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        except Exception:
            window.blit(self.surface, (self.x, self.y))

    def draw_polygon(self, points, color=None):
        pygame.draw.polygon(self.surface, color or self.color, points)

    def create_crater(self, local_x, local_y, radius):
        size = radius * 2
        temp = pygame.Surface((size, size), pygame.SRCALPHA)
        temp.fill((0, 0, 0, 0))
        pygame.draw.circle(temp, (0, 0, 0, 255), (radius, radius), radius)
        blit_x = local_x - radius
        blit_y = local_y - radius
        self.surface.blit(temp, (blit_x, blit_y), special_flags=pygame.BLEND_RGBA_SUB)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

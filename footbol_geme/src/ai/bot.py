"""
Искусственный интеллект с машиной состояний (FSM).
"""
from enum import Enum
from pygame import Vector2
from src.entities.base import Entity
from src.entities.player import Player
from src.entities.ball import Ball
import settings


class State(Enum):
    """Состояния ИИ."""
    ATTACK = "attack"
    DEFENSE = "defense"
    RETREAT = "retreat"


class Bot(Player):
    """ИИ-игрок с машиной состояний."""
    
    def __init__(self, pos: Vector2) -> None:
        """
        Инициализация бота.
        
        Args:
            pos: Начальная позиция
        """
        super().__init__(pos, settings.RED)
        self.state = State.DEFENSE
        self.kick_cooldown = 0
        self.kick_cooldown_max = 30  # Кадры до следующего удара
        # Определяем, на какой стороне находится бот (по начальной позиции)
        self.is_on_right_side = pos.x > settings.SCREEN_WIDTH // 2
        # Уровень сложности (1 - легкий, 2 - сложный)
        self.difficulty = 1  # По умолчанию легкий
    
    def set_difficulty(self, difficulty: int) -> None:
        """
        Устанавливает уровень сложности ИИ.
        
        Args:
            difficulty: Уровень сложности (1 - легкий, 2 - сложный)
        """
        self.difficulty = difficulty
    
    def update_ai(
        self,
        ball: Ball,
        player: Player,
        left_goal_x: float,
        right_goal_x: float
    ) -> None:
        """
        Обновление логики ИИ.
        
        Args:
            ball: Мяч
            player: Игрок-противник
            left_goal_x: X координата левых ворот
            right_goal_x: X координата правых ворот
        """
        self.kick_cooldown = max(0, self.kick_cooldown - 1)
        
        # Определяем СВОИ и ЧУЖИЕ ворота в зависимости от позиции бота
        if self.is_on_right_side:
            # Бот на правой стороне - его ворота справа, чужие слева
            own_goal_x = right_goal_x
            enemy_goal_x = left_goal_x
        else:
            # Бот на левой стороне - его ворота слева, чужие справа
            own_goal_x = left_goal_x
            enemy_goal_x = right_goal_x
        
        # Определяем, на чьей стороне мяч (правильно для позиции бота)
        field_center_x = (left_goal_x + right_goal_x) / 2
        if self.is_on_right_side:
            # Бот справа - мяч на его стороне, если он справа от центра
            ball_on_ai_side = ball.pos.x > field_center_x
        else:
            # Бот слева - мяч на его стороне, если он слева от центра
            ball_on_ai_side = ball.pos.x < field_center_x
        
        # На сложном уровне бот может атаковать даже если мяч на стороне противника
        # (если мяч достаточно близко к воротам противника)
        if self.difficulty == 2:
            # На сложном уровне бот атакует, если мяч близко к воротам противника
            if self.is_on_right_side:
                # Бот справа - атакует, если мяч близко к левым воротам (воротам противника)
                ball_near_enemy_goal = ball.pos.x < field_center_x and ball.pos.x < left_goal_x + 300
            else:
                # Бот слева - атакует, если мяч близко к правым воротам (воротам противника)
                ball_near_enemy_goal = ball.pos.x > field_center_x and ball.pos.x > right_goal_x - 300
            
            if ball_near_enemy_goal:
                ball_on_ai_side = True  # Считаем, что можем атаковать
        # Мяч между ботом и его воротами (правильно для обеих сторон)
        if self.is_on_right_side:
            # Бот справа - мяч между ним и воротами, если мяч между воротами и ботом
            ball_between_bot_and_goal = (ball.pos.x < self.pos.x and 
                                         ball.pos.x > own_goal_x - 50)
            ball_too_close_to_own_goal = ball.pos.x > own_goal_x - 100
        else:
            # Бот слева - мяч между ним и воротами, если мяч между воротами и ботом
            ball_between_bot_and_goal = (ball.pos.x > self.pos.x and 
                                         ball.pos.x < own_goal_x + 50)
            ball_too_close_to_own_goal = ball.pos.x < own_goal_x + 100
        
        # Мяч за спиной, если он между ботом и его воротами ИЛИ слишком близко к воротам
        ball_behind = (ball_between_bot_and_goal or ball_too_close_to_own_goal) and \
                      abs(ball.pos.y - self.pos.y) < settings.PLAYER_RADIUS * 4
        
        # Выбираем состояние
        if ball_behind:
            self.state = State.RETREAT
        elif ball_on_ai_side:
            self.state = State.ATTACK
        else:
            self.state = State.DEFENSE
        
        # Выполняем действие в зависимости от состояния
        if self.state == State.ATTACK:
            self._attack(ball, enemy_goal_x, own_goal_x)  # Бьём в чужие ворота, защищаем свои
        elif self.state == State.DEFENSE:
            self._defense(ball, player, own_goal_x)  # Защищаем свои ворота
        else:  # RETREAT
            self._retreat(ball, own_goal_x)  # Отступаем от своих ворот
    
    def _can_kick_safely(self, ball: Ball, own_goal_x: float) -> bool:
        """
        Проверяет, можно ли безопасно бить по мячу (не забить автогол).
        
        Args:
            ball: Мяч
            own_goal_x: X координата своих ворот
        
        Returns:
            True, если удар безопасен
        """
        if self.is_on_right_side:
            # Бот справа - его ворота справа
            # КРИТИЧЕСКАЯ ПРОВЕРКА 1: Мяч между ботом и его воротами (справа)
            if ball.pos.x > self.pos.x and ball.pos.x < own_goal_x + 50:
                return False  # Опасно бить!
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 2: Мяч слишком близко к воротам (справа)
            if ball.pos.x > own_goal_x - 100:
                return False  # Опасно бить!
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 3: Бот находится между мячом и воротами
            if self.pos.x < ball.pos.x and ball.pos.x > own_goal_x - 200:
                return False  # Опасно бить!
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 4: Бот должен быть правее мяча (не между мячом и воротами противника)
            if self.pos.x <= ball.pos.x:
                return False  # Бот не может бить, если он слева от мяча или на одной линии
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 5: Мяч должен быть достаточно далеко от ворот
            if ball.pos.x > own_goal_x - 150:
                return False  # Мяч слишком близко к воротам
        else:
            # Бот слева - его ворота слева
            # КРИТИЧЕСКАЯ ПРОВЕРКА 1: Мяч между ботом и его воротами (слева)
            if ball.pos.x < self.pos.x and ball.pos.x > own_goal_x:
                return False  # Опасно бить!
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 2: Мяч слишком близко к воротам (слева)
            if ball.pos.x < own_goal_x + 100:
                return False  # Опасно бить!
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 3: Бот находится между мячом и воротами
            if self.pos.x > ball.pos.x and ball.pos.x < own_goal_x + 200:
                return False  # Опасно бить!
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 4: Бот должен быть левее мяча (не между мячом и воротами противника)
            if self.pos.x >= ball.pos.x:
                return False  # Бот не может бить, если он справа от мяча или на одной линии
            
            # КРИТИЧЕСКАЯ ПРОВЕРКА 5: Мяч должен быть достаточно далеко от ворот
            if ball.pos.x < own_goal_x + 150:
                return False  # Мяч слишком близко к воротам
        
        return True
    
    def _attack(self, ball: Ball, target_goal_x: float, own_goal_x: float) -> None:
        """
        Атака: сократить дистанцию и ударить в сторону ворот игрока.
        
        Args:
            ball: Мяч
            target_goal_x: X координата ворот противника
            own_goal_x: X координата своих ворот (для проверки автогола)
        """
        # Направление к мячу
        direction_to_ball = ball.pos - self.pos
        distance_to_ball = direction_to_ball.length()
        
        if distance_to_ball < self.kick_radius and self.kick_cooldown == 0:
            # ГЛАВНАЯ ПРОВЕРКА: можно ли безопасно бить?
            if self._can_kick_safely(ball, own_goal_x):
                # Безопасный удар в сторону ворот противника
                goal_center = Vector2(target_goal_x, settings.SCREEN_HEIGHT // 2)
                kick_direction = (goal_center - ball.pos)
                if kick_direction.length() > 0:
                    kick_direction.normalize_ip()
                    # КРИТИЧЕСКАЯ ПРОВЕРКА: направление должно быть к воротам противника
                    if self.is_on_right_side:
                        # Бот справа - бьём влево (к левым воротам противника)
                        if kick_direction.x < -0.5 and self.pos.x > ball.pos.x + 20:
                            if abs(kick_direction.x) > abs(kick_direction.y):
                                ball.apply_force(kick_direction * self.kick_power)
                                self.kick_cooldown = self.kick_cooldown_max
                    else:
                        # Бот слева - бьём вправо (к правым воротам противника)
                        if kick_direction.x > 0.5 and self.pos.x < ball.pos.x - 20:
                            if kick_direction.x > abs(kick_direction.y):
                                ball.apply_force(kick_direction * self.kick_power)
                                self.kick_cooldown = self.kick_cooldown_max
        else:
            # Движемся к мячу
            if distance_to_ball > 0:
                direction_to_ball.normalize_ip()
                # На сложном уровне бот может переходить на половину противника
                if self.difficulty == 2:
                    # На сложном уровне бот активнее преследует мяч
                    self.vel += direction_to_ball * settings.PLAYER_ACCEL * 1.0
                else:
                    # На легком уровне бот не переходит на половину противника
                    field_center_x = (own_goal_x + target_goal_x) / 2
                    if self.is_on_right_side:
                        # Бот справа - не идёт левее центра
                        if ball.pos.x < field_center_x and self.pos.x < field_center_x + 50:
                            # Останавливаемся у центра
                            self.vel *= 0.8
                        else:
                            self.vel += direction_to_ball * settings.PLAYER_ACCEL * 0.8
                    else:
                        # Бот слева - не идёт правее центра
                        if ball.pos.x > field_center_x and self.pos.x > field_center_x - 50:
                            # Останавливаемся у центра
                            self.vel *= 0.8
                        else:
                            self.vel += direction_to_ball * settings.PLAYER_ACCEL * 0.8
        
        # Ограничиваем скорость
        if self.vel.length() > settings.PLAYER_MAX_SPEED:
            self.vel.scale_to_length(settings.PLAYER_MAX_SPEED)
    
    def _defense(
        self,
        ball: Ball,
        player: Player,
        own_goal_x: float
    ) -> None:
        """
        Защита: занять позицию между мячом и центром своих ворот, пытаться отобрать мяч.
        
        Args:
            ball: Мяч
            player: Игрок-противник
            own_goal_x: X координата своих ворот
        """
        goal_center = Vector2(own_goal_x, settings.SCREEN_HEIGHT // 2)
        distance_to_ball = self.pos.distance_to(ball.pos)
        
        # Если мяч близко, пытаемся его отобрать
        if distance_to_ball < self.kick_radius * 1.5:
            # Пытаемся отобрать мяч
            direction_to_ball = (ball.pos - self.pos)
            if direction_to_ball.length() > 0:
                direction_to_ball.normalize_ip()
                self.vel += direction_to_ball * settings.PLAYER_ACCEL * 0.9
            
            # Если мяч в зоне удара, отбиваем его от ворот (ТОЛЬКО если безопасно)
            if distance_to_ball < self.kick_radius and self.kick_cooldown == 0:
                # Проверяем, что мяч действительно перед воротами (не за ними)
                if self.is_on_right_side:
                    # Бот справа - ворота справа, отбиваем влево
                    if ball.pos.x < own_goal_x + 50:
                        safe_direction = Vector2(-1, 0)  # Влево, от ворот
                        if ball.pos.y < settings.SCREEN_HEIGHT // 2:
                            safe_direction.y = 0.3
                        else:
                            safe_direction.y = -0.3
                        safe_direction.normalize_ip()
                        if safe_direction.x < -0.5:
                            ball.apply_force(safe_direction * self.kick_power * 0.7)
                            self.kick_cooldown = self.kick_cooldown_max
                else:
                    # Бот слева - ворота слева, отбиваем вправо
                    if ball.pos.x > own_goal_x - 50:
                        safe_direction = Vector2(1, 0)  # Вправо, от ворот
                        if ball.pos.y < settings.SCREEN_HEIGHT // 2:
                            safe_direction.y = 0.3
                        else:
                            safe_direction.y = -0.3
                        safe_direction.normalize_ip()
                        if safe_direction.x > 0.5:
                            ball.apply_force(safe_direction * self.kick_power * 0.7)
                            self.kick_cooldown = self.kick_cooldown_max
        else:
            # Занимаем позицию между мячом и воротами
            if self.difficulty == 1:
                # Легкий уровень - ближе к воротам, не дальше 200px
                if self.is_on_right_side:
                    max_defense_x = own_goal_x - 200
                    target_x = max(goal_center.x * 0.4 + ball.pos.x * 0.6, max_defense_x)
                else:
                    max_defense_x = own_goal_x + 200
                    target_x = min(goal_center.x * 0.4 + ball.pos.x * 0.6, max_defense_x)
            else:
                # Сложный уровень - может идти дальше, но всё равно ближе к воротам
                if self.is_on_right_side:
                    max_defense_x = own_goal_x - 100  # Может быть ближе к центру
                    target_x = max(goal_center.x * 0.3 + ball.pos.x * 0.7, max_defense_x)
                else:
                    max_defense_x = own_goal_x + 100
                    target_x = min(goal_center.x * 0.3 + ball.pos.x * 0.7, max_defense_x)
            
            target_y = goal_center.y * 0.3 + ball.pos.y * 0.7
            target_pos = Vector2(target_x, target_y)
            
            direction = target_pos - self.pos
            distance = direction.length()
            
            if distance > 15:
                if direction.length() > 0:
                    direction.normalize_ip()
                    self.vel += direction * settings.PLAYER_ACCEL * 0.8
            else:
                self.vel *= 0.9
        
        # Ограничиваем скорость
        if self.vel.length() > settings.PLAYER_MAX_SPEED:
            self.vel.scale_to_length(settings.PLAYER_MAX_SPEED)
    
    def _retreat(self, ball: Ball, own_goal_x: float) -> None:
        """
        Отступ: обежать мяч по дуге, чтобы не забить автогол.
        В этом режиме бот НИКОГДА не бьет по мячу!
        
        Args:
            ball: Мяч
            own_goal_x: X координата своих ворот
        """
        # В режиме отступления бот НЕ бьет по мячу, только убегает
        distance_to_ball = self.pos.distance_to(ball.pos)
        
        # Если мяч слишком близко, убегаем быстрее
        if distance_to_ball < self.kick_radius * 2:
            # Определяем, с какой стороны обходить
            if ball.pos.y < self.pos.y:
                target_y = ball.pos.y + settings.PLAYER_RADIUS * 6
            else:
                target_y = ball.pos.y - settings.PLAYER_RADIUS * 6
            
            # Движемся в сторону от мяча и ворот (к центру поля)
            if self.is_on_right_side:
                # Бот справа - отходим влево от ворот
                target_x = max(self.pos.x - 100, own_goal_x + 50)
            else:
                # Бот слева - отходим вправо от ворот
                target_x = min(self.pos.x + 100, own_goal_x - 50)
            target_pos = Vector2(target_x, target_y)
        else:
            # Если мяч далеко, просто отходим от ворот к центру
            if self.is_on_right_side:
                target_x = max(self.pos.x - 50, own_goal_x + 100)
            else:
                target_x = min(self.pos.x + 50, own_goal_x - 100)
            target_y = settings.SCREEN_HEIGHT // 2
            target_pos = Vector2(target_x, target_y)
        
        direction = target_pos - self.pos
        if direction.length() > 0:
            direction.normalize_ip()
            self.vel += direction * settings.PLAYER_ACCEL * 0.9
        
        # Ограничиваем скорость
        if self.vel.length() > settings.PLAYER_MAX_SPEED:
            self.vel.scale_to_length(settings.PLAYER_MAX_SPEED)


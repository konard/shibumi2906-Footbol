"""
Обработка столкновений между объектами и границами поля.
"""
from pygame import Vector2
from src.entities.base import Entity
from src.entities.ball import Ball
import settings


def check_circle_circle_collision(
    entity1: Entity,
    entity2: Entity
) -> bool:
    """
    Проверяет столкновение двух круглых объектов.
    
    Args:
        entity1: Первая сущность
        entity2: Вторая сущность
    
    Returns:
        True, если объекты пересекаются
    """
    dist = entity1.pos.distance_to(entity2.pos)
    return dist < (entity1.radius + entity2.radius)


def resolve_circle_circle_collision(
    entity1: Entity,
    entity2: Entity
) -> None:
    """
    Разрешает столкновение двух круглых объектов (эластичное столкновение).
    
    Args:
        entity1: Первая сущность
        entity2: Вторая сущность
    """
    # Вектор от entity1 к entity2
    collision_vector = entity2.pos - entity1.pos
    distance = collision_vector.length()
    
    if distance == 0:
        return
    
    # Нормализуем
    normal = collision_vector / distance
    
    # Разделяем объекты, чтобы они не пересекались
    overlap = (entity1.radius + entity2.radius) - distance
    if overlap > 0:
        # Смещаем объекты
        separation = normal * (overlap / 2)
        entity1.pos -= separation
        entity2.pos += separation
    
    # Вычисляем относительную скорость
    relative_velocity = entity2.vel - entity1.vel
    velocity_along_normal = relative_velocity.dot(normal)
    
    # Не разрешаем, если объекты удаляются друг от друга
    if velocity_along_normal > 0:
        return
    
    # Коэффициент упругости
    restitution = 0.8
    
    # Импульс столкновения
    impulse = -(1 + restitution) * velocity_along_normal
    impulse /= (1 / entity1.mass + 1 / entity2.mass)
    
    # Применяем импульс
    impulse_vector = normal * impulse
    entity1.vel -= impulse_vector / entity1.mass
    entity2.vel += impulse_vector / entity2.mass


def check_wall_collision(entity: Entity) -> tuple[bool, Vector2]:
    """
    Проверяет столкновение с границами поля.
    
    Args:
        entity: Сущность для проверки
    
    Returns:
        Кортеж (столкнулся ли, нормаль к стене)
    """
    normal = Vector2(0, 0)
    collided = False
    
    # Левая стена
    if entity.pos.x - entity.radius < settings.PITCH_LEFT:
        normal = Vector2(1, 0)
        entity.pos.x = settings.PITCH_LEFT + entity.radius
        collided = True
    # Правая стена
    elif entity.pos.x + entity.radius > settings.PITCH_RIGHT:
        normal = Vector2(-1, 0)
        entity.pos.x = settings.PITCH_RIGHT - entity.radius
        collided = True
    
    # Верхняя стена
    if entity.pos.y - entity.radius < settings.PITCH_TOP:
        normal = Vector2(0, 1)
        entity.pos.y = settings.PITCH_TOP + entity.radius
        collided = True
    # Нижняя стена
    elif entity.pos.y + entity.radius > settings.PITCH_BOTTOM:
        normal = Vector2(0, -1)
        entity.pos.y = settings.PITCH_BOTTOM - entity.radius
        collided = True
    
    return collided, normal


def resolve_wall_collision(entity: Entity) -> None:
    """
    Разрешает столкновение с границами поля (отскок с потерей энергии).
    
    Args:
        entity: Сущность для обработки
    """
    collided, normal = check_wall_collision(entity)
    
    if collided and normal.length() > 0:
        # Формула отражения: v_new = v_old - 2 * v_old.dot(n) * n
        # Где v_old - текущий вектор скорости, n - нормаль к поверхности
        v_old = entity.vel
        dot_product = v_old.dot(normal)
        v_new = v_old - 2 * dot_product * normal
        
        # Применяем затухание
        entity.vel = v_new * settings.BOUNCE_DAMPING


def handle_ball_wall_collision(ball: Ball) -> None:
    """
    Обрабатывает столкновение мяча со стенами.
    
    Args:
        ball: Мяч для обработки
    """
    resolve_wall_collision(ball)


def handle_player_wall_collision(player: Entity) -> None:
    """
    Обрабатывает столкновение игрока со стенами (останавливает движение).
    
    Args:
        player: Игрок для обработки
    """
    collided, normal = check_wall_collision(player)
    
    if collided:
        # Останавливаем движение в направлении стены
        if normal.length() > 0:
            # Проецируем скорость на нормаль и вычитаем
            dot_product = player.vel.dot(normal)
            if dot_product < 0:  # Движемся к стене
                player.vel -= normal * dot_product




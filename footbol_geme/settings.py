"""
Настройки игры: константы, цвета, физические параметры.
"""

# Размеры окна
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Физика
FRICTION = 0.985  # Коэффициент трения для мяча
PLAYER_ACCEL = 0.5  # Ускорение игрока
PLAYER_MAX_SPEED = 7  # Максимальная скорость игрока
BALL_MAX_SPEED = 15  # Максимальная скорость мяча
KICK_POWER = 12  # Сила удара
KICK_RADIUS = 35  # Радиус зоны удара
BOUNCE_DAMPING = 0.85  # Потеря энергии при отскоке от стен

# Размеры игровых объектов
PLAYER_RADIUS = 22
BALL_RADIUS = 12
GOAL_WIDTH = 150
GOAL_HEIGHT = 30

# Поле
PITCH_MARGIN = 50  # Отступ от краев экрана
PITCH_WIDTH = SCREEN_WIDTH - 2 * PITCH_MARGIN
PITCH_HEIGHT = SCREEN_HEIGHT - 2 * PITCH_MARGIN
PITCH_LEFT = PITCH_MARGIN
PITCH_RIGHT = SCREEN_WIDTH - PITCH_MARGIN
PITCH_TOP = PITCH_MARGIN
PITCH_BOTTOM = SCREEN_HEIGHT - PITCH_MARGIN

# Ворота
GOAL_LEFT_Y = SCREEN_HEIGHT // 2 - GOAL_WIDTH // 2
GOAL_LEFT_X = PITCH_LEFT
GOAL_RIGHT_Y = SCREEN_HEIGHT // 2 - GOAL_WIDTH // 2
GOAL_RIGHT_X = PITCH_RIGHT

# Игровые параметры
GOAL_CELEBRATION_TIME = 2000  # Время паузы после гола в миллисекундах
GAME_DURATION = 90  # Длительность игры в секундах

# Уровни сложности ИИ
AI_DIFFICULTY_EASY = 1  # Легкий - бот играет только на своей половине
AI_DIFFICULTY_HARD = 2  # Сложный - бот играет по всему полю


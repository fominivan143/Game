import arcade

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Fireboy & Watergirl"

CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
GEM_SCALING = 0.4
BUTTON_SCALING = 0.3
LEVER_SCALING = 0.4

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
JUMP_SPEED = 20


class Player(arcade.Sprite):
    """Класс игрока"""

    def __init__(self, texture, key_up, key_down, key_left, key_right, player_type):
        super().__init__(texture, CHARACTER_SCALING)

        # Тип игрока
        self.player_type = player_type  # "fireboy" или "watergirl"

        # Управление
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right

        # Физика
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False

        # Собранные драгоценности
        self.gems_collected = 0


class MyGame(arcade.Window):
    """Основной класс игры"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Игровые сцены
        self.scene = None

        # Игроки
        self.fireboy = None
        self.watergirl = None

        # Физический движок
        self.physics_engine_fireboy = None
        self.physics_engine_watergirl = None

        # Управление
        self.keys_pressed = set()

        # Уровень
        self.level = 1
        self.game_over = False
        self.level_complete = False

        # Механики
        self.green_doors = []
        self.buttons = []
        self.levers = []
        self.gates = []

        # Текстовые объекты
        self.level_text = None
        self.fireboy_score_text = None
        self.watergirl_score_text = None
        self.controls_title = None
        self.controls_text_fireboy = None
        self.controls_text_watergirl = None
        self.restart_text = None
        self.game_over_text = None
        self.game_over_subtext = None
        self.level_complete_text = None
        self.level_complete_subtext = None
        self.instructions_text = None

        # Звуки
        self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")
        self.gem_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.button_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.door_sound = arcade.load_sound(":resources:sounds/secret2.wav")

        arcade.set_background_color(arcade.csscolor.DARK_SLATE_GRAY)

    def setup_level(self, level_num):
        """Настройка уровня"""
        self.level = level_num
        self.game_over = False
        self.level_complete = False

        # Очищаем механики
        self.green_doors.clear()
        self.buttons.clear()
        self.levers.clear()
        self.gates.clear()

        # Инициализация сцены
        self.scene = arcade.Scene()

        # Слои
        self.scene.add_sprite_list("Walls")
        self.scene.add_sprite_list("Gems")
        self.scene.add_sprite_list("Lava")
        self.scene.add_sprite_list("Water")
        self.scene.add_sprite_list("Doors")
        self.scene.add_sprite_list("Fireboy")
        self.scene.add_sprite_list("Watergirl")
        self.scene.add_sprite_list("GreenDoors")
        self.scene.add_sprite_list("Buttons")
        self.scene.add_sprite_list("Levers")
        self.scene.add_sprite_list("Gates")
        self.scene.add_sprite_list("MovingPlatforms")

        # Создание пола
        for x in range(0, SCREEN_WIDTH, 64):
            wall = arcade.Sprite(":resources:images/tiles/stoneMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Боковые стены
        for y in range(96, SCREEN_HEIGHT - 64, 64):
            wall = arcade.Sprite(":resources:images/tiles/stoneMid.png", TILE_SCALING)
            wall.center_x = 32
            wall.center_y = y
            self.scene.add_sprite("Walls", wall)

            wall = arcade.Sprite(":resources:images/tiles/stoneMid.png", TILE_SCALING)
            wall.center_x = SCREEN_WIDTH - 32
            wall.center_y = y
            self.scene.add_sprite("Walls", wall)

        # Основные платформы
        if level_num == 1:
            # Левая сторона - платформы для Fireboy
            platforms_fireboy = [
                (200, 150), (300, 150),
                (150, 280), (250, 280),
                (200, 410), (300, 410),
                (100, 540), (200, 540), (300, 540)
            ]

            for x, y in platforms_fireboy:
                wall = arcade.Sprite(":resources:images/tiles/brickBrown.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.scene.add_sprite("Walls", wall)

            # Правая сторона - платформы для Watergirl
            platforms_watergirl = [
                (700, 150), (800, 150),
                (650, 280), (750, 280), (850, 280),
                (700, 410), (800, 410),
                (700, 540), (800, 540), (900, 540)
            ]

            for x, y in platforms_watergirl:
                wall = arcade.Sprite(":resources:images/tiles/brickGrey.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.scene.add_sprite("Walls", wall)

            # Центральные соединяющие платформы
            center_platforms = [
                (400, 200, 4),
                (500, 350, 3),
                (450, 500, 2),
            ]

            for center_x, y, length in center_platforms:
                for i in range(length):
                    wall = arcade.Sprite(":resources:images/tiles/stoneCenter.png", TILE_SCALING)
                    wall.center_x = center_x - 64 + i * 64
                    wall.center_y = y
                    self.scene.add_sprite("Walls", wall)

            # Движущаяся платформа (по горизонтали)
            moving_platform = arcade.Sprite(":resources:images/tiles/grassCenter.png", TILE_SCALING)
            moving_platform.center_x = 600
            moving_platform.center_y = 250
            moving_platform.change_x = 2
            self.scene.add_sprite("MovingPlatforms", moving_platform)

            # Движущаяся платформа (по вертикали)
            moving_platform2 = arcade.Sprite(":resources:images/tiles/grassCenter.png", TILE_SCALING)
            moving_platform2.center_x = 400
            moving_platform2.center_y = 100
            moving_platform2.change_y = 1.5
            self.scene.add_sprite("MovingPlatforms", moving_platform2)

        # Создание драгоценностей
        gem_positions = []
        if level_num == 1:
            # Красные драгоценности (для Fireboy)
            gem_positions.extend([
                (180, 190, "red"),
                (280, 320, "red"),
                (200, 450, "red"),
                (100, 580, "red"),
            ])

            # Синие драгоценности (для Watergirl)
            gem_positions.extend([
                (720, 190, "blue"),
                (820, 320, "blue"),
                (700, 450, "blue"),
                (900, 580, "blue"),
            ])

            # Зеленые драгоценности (для обоих)
            gem_positions.extend([
                (380, 240, "green"),
                (500, 390, "green"),
                (450, 540, "green"),
                (600, 290, "green"),
            ])

        for x, y, color in gem_positions:
            if color == "red":
                gem = arcade.Sprite(":resources:images/items/gemRed.png", GEM_SCALING)
            elif color == "blue":
                gem = arcade.Sprite(":resources:images/items/gemBlue.png", GEM_SCALING)
            else:
                gem = arcade.Sprite(":resources:images/items/gemGreen.png", GEM_SCALING)
            gem.center_x = x
            gem.center_y = y
            self.scene.add_sprite("Gems", gem)

        # Создание лавы (опасность для Fireboy)
        lava_positions = [
            (150, 80), (250, 80), (350, 80),
            (50, 200), (50, 300), (50, 400),
        ]

        for x, y in lava_positions:
            lava = arcade.Sprite(":resources:images/tiles/lava.png", TILE_SCALING)
            lava.center_x = x
            lava.center_y = y
            self.scene.add_sprite("Lava", lava)

        # Создание воды (опасность для Watergirl)
        water_positions = [
            (850, 80), (750, 80), (650, 80),
            (950, 200), (950, 300), (950, 400),
        ]

        for x, y in water_positions:
            water = arcade.Sprite(":resources:images/tiles/water.png", TILE_SCALING)
            water.center_x = x
            water.center_y = y
            self.scene.add_sprite("Water", water)

        # Создание зеленых дверей (блокируют проход)
        green_door_positions = [
            (350, 250),
            (550, 400),
        ]

        for x, y in green_door_positions:
            # Используем дверь и красим в зеленый
            green_door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", TILE_SCALING)
            green_door.center_x = x
            green_door.center_y = y
            green_door.color = arcade.color.GREEN  # делаем зеленой
            green_door.is_closed = True
            self.scene.add_sprite("GreenDoors", green_door)
            self.green_doors.append(green_door)

        # ДОБАВЬ СОЗДАНИЕ КНОПОК - БЕЗ НИХ ИГРА НЕ РАБОТАЕТ!
        # Создание кнопок для открытия зеленых дверей
        button_positions = [
            (200, 300, 0),  # Кнопка для первой двери
            (800, 300, 1),  # Кнопка для второй двери
        ]

        for x, y, door_index in button_positions:
            button = arcade.Sprite(":resources:images/items/coinGold.png", BUTTON_SCALING)
            button.center_x = x
            button.center_y = y
            button.door_index = door_index
            button.is_pressed = False
            button.original_color = arcade.color.GOLD
            button.pressed_color = arcade.color.DARK_GOLDENROD
            self.scene.add_sprite("Buttons", button)
            self.buttons.append(button)

        # Создание ворот (открываются рычагами)
        gate_positions = [
            (250, 350, 0),
            (750, 350, 1),
        ]

        for x, y, lever_index in gate_positions:
            # Используем ящик и красим в фиолетовый
            gate = arcade.Sprite(":resources:images/tiles/boxCrate.png", TILE_SCALING * 1.2)
            gate.center_x = x
            gate.center_y = y
            gate.lever_index = lever_index
            gate.is_locked = True
            gate.color = arcade.color.PURPLE  # делаем фиолетовым
            self.scene.add_sprite("Gates", gate)
            self.gates.append(gate)

        # Создание рычагов
        lever_positions = [
            (150, 300, 0),
            (850, 300, 1),
        ]

        for x, y, gate_index in lever_positions:
            lever = arcade.Sprite(":resources:images/tiles/signRight.png", LEVER_SCALING)
            lever.center_x = x
            lever.center_y = y
            lever.gate_index = gate_index
            lever.is_active = False
            lever.original_color = arcade.color.WHITE
            lever.active_color = arcade.color.YELLOW
            self.scene.add_sprite("Levers", lever)
            self.levers.append(lever)

        # Создание дверей (финиш)
        fireboy_door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", TILE_SCALING * 1.5)
        fireboy_door.center_x = 900
        fireboy_door.center_y = 580
        self.scene.add_sprite("Doors", fireboy_door)

        watergirl_door = arcade.Sprite(":resources:images/tiles/doorClosed_mid.png", TILE_SCALING * 1.5)
        watergirl_door.center_x = 100
        watergirl_door.center_y = 580
        self.scene.add_sprite("Doors", watergirl_door)

        # Создание игроков
        self.fireboy = Player(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
                              arcade.key.W, arcade.key.S,
                              arcade.key.A, arcade.key.D, "fireboy")
        self.fireboy.center_x = 150
        self.fireboy.center_y = 300

        self.watergirl = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                arcade.key.UP, arcade.key.DOWN,
                                arcade.key.LEFT, arcade.key.RIGHT, "watergirl")
        self.watergirl.center_x = 850
        self.watergirl.center_y = 300

        self.scene.add_sprite("Fireboy", self.fireboy)
        self.scene.add_sprite("Watergirl", self.watergirl)

        self.physics_engine_fireboy = arcade.PhysicsEnginePlatformer(
            self.fireboy,
            gravity_constant=GRAVITY,
            walls=[self.scene["Walls"], self.scene["Gates"], self.scene["GreenDoors"]]
        )

        self.physics_engine_watergirl = arcade.PhysicsEnginePlatformer(
            self.watergirl,
            gravity_constant=GRAVITY,
            walls=[self.scene["Walls"], self.scene["Gates"], self.scene["GreenDoors"]]
        )

        # Создание текстовых объектов
        self.level_text = arcade.Text(
            f"Уровень: {self.level}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 18
        )

        self.fireboy_score_text = arcade.Text(
            f"Fireboy: 0 драгоценностей",
            10, SCREEN_HEIGHT - 60,
            arcade.color.RED, 18
        )

        self.watergirl_score_text = arcade.Text(
            f"Watergirl: 0 драгоценностей",
            10, SCREEN_HEIGHT - 90,
            arcade.color.BLUE, 18
        )

        self.controls_title = arcade.Text(
            "Управление:",
            SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 14
        )

        self.controls_text_fireboy = arcade.Text(
            "Fireboy: WASD, прыжок: W",
            SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60,
            arcade.color.RED, 14
        )

        self.controls_text_watergirl = arcade.Text(
            "Watergirl: Стрелки, прыжок: ↑",
            SCREEN_WIDTH - 250, SCREEN_HEIGHT - 90,
            arcade.color.BLUE, 14
        )

        self.restart_text = arcade.Text(
            "Рестарт: R, След. уровень: N",
            SCREEN_WIDTH - 250, SCREEN_HEIGHT - 120,
            arcade.color.WHITE, 14
        )

        self.instructions_text = arcade.Text(
            "Собери все драгоценности и доберись до своих дверей!",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40,
            arcade.color.LIGHT_YELLOW, 16,
            anchor_x="center"
        )

        self.game_over_text = arcade.Text(
            "ИГРА ОКОНЧЕНА!",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            arcade.color.RED, 50,
            anchor_x="center"
        )

        self.game_over_subtext = arcade.Text(
            "Нажмите R для рестарта",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
            arcade.color.WHITE, 30,
            anchor_x="center"
        )

        self.level_complete_text = arcade.Text(
            "УРОВЕНЬ ПРОЙДЕН!",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            arcade.color.GREEN, 50,
            anchor_x="center"
        )

        self.level_complete_subtext = arcade.Text(
            "Нажмите N для следующего уровня",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
            arcade.color.WHITE, 30,
            anchor_x="center"
        )

        # Сброс счетчиков драгоценностей
        self.fireboy.gems_collected = 0
        self.watergirl.gems_collected = 0

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        self.keys_pressed.add(key)

        # Прыжок Fireboy
        if key == self.fireboy.key_up and self.physics_engine_fireboy.can_jump():
            self.fireboy.change_y = JUMP_SPEED
            arcade.play_sound(self.jump_sound)

        # Прыжок Watergirl
        if key == self.watergirl.key_up and self.physics_engine_watergirl.can_jump():
            self.watergirl.change_y = JUMP_SPEED
            arcade.play_sound(self.jump_sound)

        # Рестарт уровня
        if key == arcade.key.R:
            self.setup_level(self.level)

        # Переключение уровней
        if key == arcade.key.N:
            self.setup_level(2 if self.level == 1 else 1)

        # Активация рычагов клавишей E для Fireboy и SHIFT для Watergirl
        if key == arcade.key.E:
            self.activate_lever(self.fireboy)
        if key == arcade.key.RSHIFT or key == arcade.key.LSHIFT:
            self.activate_lever(self.watergirl)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def update_player_movement(self, player, physics_engine):
        """Обновление движения игрока"""
        player.change_x = 0

        # Движение влево/вправо
        if player.key_left in self.keys_pressed:
            player.change_x = -PLAYER_MOVEMENT_SPEED
        if player.key_right in self.keys_pressed:
            player.change_x = PLAYER_MOVEMENT_SPEED

        # Обновление физики
        physics_engine.update()

        # Проверка, на земле ли игрок
        player.on_ground = physics_engine.can_jump()

    def activate_lever(self, player):
        """Активация рычага игроком"""
        for lever in self.levers:
            if arcade.check_for_collision(player, lever):
                lever.is_active = not lever.is_active
                arcade.play_sound(self.button_sound)

                # Меняем цвет рычага
                if lever.is_active:
                    lever.color = lever.active_color
                    lever.angle = 45  # Немного поворачиваем
                else:
                    lever.color = lever.original_color
                    lever.angle = 0

                # Открываем/закрываем соответствующие ворота
                for gate in self.gates:
                    if gate.lever_index == lever.gate_index:
                        gate.is_locked = not lever.is_active
                        if not gate.is_locked:
                            # Удаляем ворота из физики
                            gate.remove_from_sprite_lists()
                            arcade.play_sound(self.door_sound)

    def check_collisions(self):
        """Проверка столкновений"""
        # Проверяем столкновение с закрытыми зелеными дверями
        for door in self.green_doors:
            if door.is_closed:
                if arcade.check_for_collision(self.fireboy, door) or arcade.check_for_collision(self.watergirl, door):
                    # Игрок не может пройти через закрытую дверь
                    # Можно добавить эффект или звук
                    pass

        # Fireboy собирает драгоценности
        fireboy_gem_collisions = arcade.check_for_collision_with_list(
            self.fireboy, self.scene["Gems"]
        )
        for gem in fireboy_gem_collisions:
            gem.remove_from_sprite_lists()
            self.fireboy.gems_collected += 1
            arcade.play_sound(self.gem_sound)

        # Watergirl собирает драгоценности
        watergirl_gem_collisions = arcade.check_for_collision_with_list(
            self.watergirl, self.scene["Gems"]
        )
        for gem in watergirl_gem_collisions:
            gem.remove_from_sprite_lists()
            self.watergirl.gems_collected += 1
            arcade.play_sound(self.gem_sound)

        # Проверка нажатия кнопок
        for button in self.buttons:
            if (arcade.check_for_collision(self.fireboy, button) or
                    arcade.check_for_collision(self.watergirl, button)):
                if not button.is_pressed:
                    button.is_pressed = True
                    button.color = arcade.color.DARK_RED  # Меняем цвет на темно-красный
                    arcade.play_sound(self.button_sound)

                    # Открываем соответствующую дверь
                    if button.door_index < len(self.green_doors):
                        door = self.green_doors[button.door_index]
                        if door.is_closed:
                            door.is_closed = False
                            door.remove_from_sprite_lists()
                            arcade.play_sound(self.door_sound)

        # Fireboy касается лавы
        fireboy_lava_collisions = arcade.check_for_collision_with_list(
            self.fireboy, self.scene["Lava"]
        )
        if fireboy_lava_collisions:
            self.game_over = True

        # Watergirl касается воды
        watergirl_water_collisions = arcade.check_for_collision_with_list(
            self.watergirl, self.scene["Water"]
        )
        if watergirl_water_collisions:
            self.game_over = True

        # Проверка достижения дверей
        fireboy_door_collisions = arcade.check_for_collision_with_list(
            self.fireboy, self.scene["Doors"]
        )
        watergirl_door_collisions = arcade.check_for_collision_with_list(
            self.watergirl, self.scene["Doors"]
        )

        # Если оба игрока у дверей и собрали все драгоценности
        total_gems = len(self.scene["Gems"])
        gems_collected = self.fireboy.gems_collected + self.watergirl.gems_collected

        if (fireboy_door_collisions and watergirl_door_collisions and
                gems_collected >= total_gems):
            self.level_complete = True

    def on_update(self, delta_time):
        """Обновление игры"""
        if self.game_over or self.level_complete:
            return

        # Обновление движения игроков
        self.update_player_movement(self.fireboy, self.physics_engine_fireboy)
        self.update_player_movement(self.watergirl, self.physics_engine_watergirl)

        # Обновление движущихся платформ
        for platform in self.scene["MovingPlatforms"]:
            platform.center_x += platform.change_x
            platform.center_y += platform.change_y

            # Проверка границ для горизонтального движения
            if hasattr(platform, 'change_x'):
                if platform.center_x > 700 or platform.center_x < 500:
                    platform.change_x *= -1

            # Проверка границ для вертикального движения
            if hasattr(platform, 'change_y'):
                if platform.center_y > 200 or platform.center_y < 80:
                    platform.change_y *= -1

        # Проверка столкновений
        self.check_collisions()

        # Обновление текстовых объектов
        self.level_text.text = f"Уровень: {self.level}"
        self.fireboy_score_text.text = f"Fireboy: {self.fireboy.gems_collected} драгоценностей"
        self.watergirl_score_text.text = f"Watergirl: {self.watergirl.gems_collected} драгоценностей"

        # Границы для игроков
        self.fireboy.center_x = max(50, min(SCREEN_WIDTH - 50, self.fireboy.center_x))
        self.watergirl.center_x = max(50, min(SCREEN_WIDTH - 50, self.watergirl.center_x))
        self.fireboy.center_y = max(50, min(SCREEN_HEIGHT - 50, self.fireboy.center_y))
        self.watergirl.center_y = max(50, min(SCREEN_HEIGHT - 50, self.watergirl.center_y))

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        # Отрисовка сцены
        self.scene.draw()

        # Отрисовка текстовых объектов
        self.level_text.draw()
        self.fireboy_score_text.draw()
        self.watergirl_score_text.draw()

        self.instructions_text.draw()

        self.controls_title.draw()
        self.controls_text_fireboy.draw()
        self.controls_text_watergirl.draw()
        self.restart_text.draw()

        # Дополнительные инструкции
        extra_controls = arcade.Text(
            "Активация рычагов: Fireboy - E, Watergirl - SHIFT",
            SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150,
            arcade.color.LIGHT_YELLOW, 12
        )
        extra_controls.draw()

        # Подсказки о механике
        mechanics_hint = arcade.Text(
            "Зеленые замки открываются кнопками, красные - рычагами",
            SCREEN_WIDTH // 2, 20,
            arcade.color.LIGHT_GREEN, 14,
            anchor_x="center"
        )
        mechanics_hint.draw()

        # Отрисовка сообщений о состоянии игры
        if self.game_over:
            self.game_over_text.draw()
            self.game_over_subtext.draw()

        if self.level_complete:
            self.level_complete_text.draw()
            self.level_complete_subtext.draw()


def main():
    """Основная функция"""
    window = MyGame()
    window.setup_level(1)
    arcade.run()


if __name__ == "__main__":
    main()
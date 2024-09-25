import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    def _hash_password(self, password):
        return hash(password)

    def __repr__(self):
        return f"User(nickname='{self.nickname}', age={self.age})"

    def check_password(self, password):
        return self.password == self._hash_password(password)

class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __repr__(self):
        return f"Video(title='{self.title}', duration={self.duration}, adult_mode={self.adult_mode})"

    def __str__(self):
        return f"{self.title} ({self.duration} секунд)"

class UrTube:
    def __init__(self):
        self.users = []  # Список всех зарегистрированных пользователей
        self.videos = []  # Список всех добавленных видео
        self.current_user = None  # Текущий авторизованный пользователь

    def log_in(self, nickname, password):
        """Метод для авторизации пользователя"""
        for user in self.users:
            if user.nickname == nickname and user.check_password(password):
                self.current_user = user
                print(f"Пользователь {nickname} вошел в систему")
                return
        print("Неверный логин или пароль")

    def register(self, nickname, password, age):
        """Метод для регистрации нового пользователя"""
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} зарегистрирован и вошел в систему")

    def log_out(self):
        """Метод для выхода из учетной записи"""
        self.current_user = None
        print("Пользователь вышел из системы")

    def add(self, *videos):
        """Метод для добавления видео на платформу"""
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f"Видео '{video.title}' добавлено")
            else:
                print(f"Видео '{video.title}' уже существует")

    def get_videos(self, keyword):
        """Поиск видео по ключевому слову"""
        keyword = keyword.lower()
        return [video.title for video in self.videos if keyword in video.title.lower()]

    def watch_video(self, title):
        """Метод для воспроизведения видео"""
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        # Поиск видео по названию
        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return

                # Воспроизведение видео
                for second in range(video.time_now, video.duration):
                    print(second + 1, end=' ', flush=True)
                    time.sleep(1)  # Пауза в 1 секунду между выводом секунд
                print("Конец видео")
                video.time_now = 0  # Сброс времени просмотра
                return

        print(f"Видео '{title}' не найдено")

ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')

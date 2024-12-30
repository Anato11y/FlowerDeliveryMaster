# FlowerDelivery Master

---

## Оглавление

1. [Описание](#описание)
2. [Основные функции](#основные-функции)
3. [Требования](#требования)
4. [Установка](#установка)
5. [Использование](#использование)
6. [Использование Telegram-бота](#использование-Telegram-бота)
7. [Структура проекта](#структура-проекта)
8. [Лицензия](#лицензия)

---

## Описание

**FlowerDelivery Master** – это система управления заказами и доставки цветов. Основное назначение – обеспечить удобный интерфейс для клиентов и администраторов.

---

## Основные функции

- **Каталог:** Просмотр доступных товаров, добавление в корзину.
- **Корзина:** Управление заказами (добавление, удаление, изменение количества).
- **История заказов:** Просмотр выполненных заказов.
- **Отзывы:** Оставление отзывов о продукции.
- **Аналитика:** Отчёты о продажах и заказах.
- **Telegram-бот:** Уведомления о новых заказах и изменении статусов.

---

## Требования

- **Python:** 3.10+
- **Django:** 5.0+
- **База данных:** SQLite (по умолчанию)
- **Дополнительно:** Виртуальное окружение (рекомендуется)

---

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone <ссылка на ваш репозиторий>
   cd FlowerDeliveryMaster

2. Создайте и активируйте виртуальное окружение:
 
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   
4. Выполните миграции базы данных:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   
5. Создайте суперпользователя для доступа к админ-панели:

   ```bash
   python manage.py createsuperuser

---
## Использование

1. Запустите сервер разработки:

   ```bash
   python manage.py runserver

2. Перейдите по адресу http://127.0.0.1:8000/ в вашем браузере, чтобы открыть главную страницу приложения.
3. Для входа в админ-панель используйте http://127.0.0.1:8000/admin/.

---
## Использование Telegram-бота

1. Получите токен бота через BotFather.
2. Добавьте токен и ваш CHAT_ID в файл telegram_bot_app/bot.py
   
   ```python
   BOT_TOKEN = 'ваш_токен'
   CHAT_ID = 'ваш ID'
3. Запустите Telegram-бота:
   ```bash
   python manage.py run_bot
Telegram-бот будет доступен для получения уведомлений и взаимодействия.

---
## Структура проекта

  ```bash
   
   flowerdelivery_master/
├── analytics_app/                    # Приложение аналитики
│   ├── migrations/                   # Миграции базы данных
│   ├── static/                       # Статические файлы (CSS, JS)
│   ├── templates/                    # Шаблоны HTML для аналитики
│   │   └── dashboard.html            # Страница дашборда аналитики
│   ├── __init__.py                   # Инициализация приложения
│   ├── admin.py                      # Конфигурация панели администратора
│   ├── apps.py                       # Конфигурация приложения
│   ├── models.py                     # Модели данных (не используется)
│   ├── tests.py                      # Тесты для приложения
│   ├── urls.py                       # Маршруты для приложения аналитики
│   └── views.py                      # Представления для аналитики
├── flowerdelivery_master/            # Основные настройки проекта
│   ├── __init__.py                   # Инициализация
│   ├── asgi.py                       # Конфигурация ASGI
│   ├── settings.py                   # Основные настройки проекта
│   ├── urls.py                       # Главные маршруты проекта
│   └── wsgi.py                       # Конфигурация WSGI
├── flowers/                          # Папка для загрузки изображений товаров
├── main_app/                         # Основное приложение
│   ├── migrations/                   # Миграции базы данных
│   ├── static/                       # Статические файлы
│   ├── templates/                    # Шаблоны HTML
│   │   ├── base.html                 # Базовый HTML-шаблон
│   │   └── index.html                # Главная страница
│   ├── __init__.py                   # Инициализация
│   ├── admin.py                      # Конфигурация администратора
│   ├── apps.py                       # Конфигурация приложения
│   ├── models.py                     # Модели (Profile, Flower)
│   ├── tests.py                      # Тесты
│   ├── urls.py                       # Маршруты приложения
│   └── views.py                      # Представления главной страницы
├── orders_app/                       # Приложение для управления заказами
│   ├── migrations/                   # Миграции базы данных
│   ├── static/                       # Статические файлы
│   ├── templates/                    # Шаблоны HTML
│   │   ├── orders_app/               # Страницы заказов
│   │   │   ├── cart.html             # Страница корзины
│   │   │   ├── catalog.html          # Каталог товаров
│   │   │   └── history.html          # История заказов
│   │   └── registration/             # Шаблоны регистрации
│   │       ├── login.html            # Страница входа
│   │       └── register.html         # Страница регистрации
│   ├── __init__.py                   # Инициализация
│   ├── admin.py                      # Конфигурация администратора
│   ├── apps.py                       # Конфигурация приложения
│   ├── models.py                     # Модели (Order, OrderItem)
│   ├── signals.py                    # Сигналы Django
│   ├── tests.py                      # Тесты
│   ├── urls.py                       # Маршруты приложения
│   └── views.py                      # Представления заказов
├── reviews_app/                      # Приложение для отзывов
│   ├── migrations/                   # Миграции базы данных
│   ├── static/                       # Статические файлы
│   ├── templates/                    # Шаблоны отзывов
│   │   ├── add.html                  # Страница добавления отзыва
│   │   └── list.html                 # Список отзывов
│   ├── __init__.py                   # Инициализация
│   ├── admin.py                      # Конфигурация администратора
│   ├── apps.py                       # Конфигурация приложения
│   ├── models.py                     # Модели отзывов
│   ├── tests.py                      # Тесты
│   ├── urls.py                       # Маршруты приложения
│   └── views.py                      # Представления отзывов
├── telegram_bot_app/                 # Приложение Telegram-бота
│   ├── management/                   # Команды управления
│   ├── migrations/                   # Миграции базы данных
│   ├── __init__.py                   # Инициализация
│   ├── admin.py                      # Конфигурация администратора
│   ├── apps.py                       # Конфигурация приложения
│   ├── bot.py                        # Telegram-бот
│   ├── models.py                     # Модели (не используются)
│   ├── tests.py                      # Тесты
│   └── views.py                      # Представления (не используются)
├── __init__.py                       # Инициализация проекта
├── db.sqlite3                        # Файл базы данных SQLite
├── manage.py                         # Управление проектом
└── requirements.txt                  # Зависимости проекта

  ```


---
## Лицензия
Проект распространяется под лицензией MIT. Подробности можно найти в файле LICENSE.


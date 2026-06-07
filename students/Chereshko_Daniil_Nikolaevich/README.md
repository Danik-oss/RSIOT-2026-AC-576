# Лабораторная работа 01 — Контейнеризация и Docker

## Вариант №23

### Студент
- ФИО: Черешко Даниил Николаевич
- Группа: АС-576
- № студенческого: 220250
- Email: danikgad1q9@mail.ru
- GitHub username: Danik-oss
- Вариант №: 23
- Дата выполнения: 07.06.2026
- ОС: Windows 10 22H2

## Описание решения

Проект реализован как Python/Flask сервис с вариантом №23.

- Стек: Python/Flask
- Порт приложения: `9043`
- Health endpoint: `/live`
- Зависимость: Redis
- Volume: `data_w23`
- UID внутри контейнера: `65532`
- Тег образа: `rsiot-v23:stu-220250-v23`
- Сервисный slug: `as-576-220250-v23`

## Файлы

- `task_01/src/app.py` — Flask-приложение с Redis и graceful shutdown
- `task_01/src/Dockerfile` — multi-stage Dockerfile с пользователем UID 65532
- `task_01/src/docker-compose.yml` — Docker Compose с Redis и volume `data_w23`
- `task_01/src/requirements.txt` — Python зависимости
- `task_01/src/.dockerignore` — исключения для сборки
- `task_01/doc/README.md` — отчёт по заданию

## Запуск

1. Перейти в папку проекта:
   ```bash
   cd students/Chereshko_Daniil_Nikolaevich/task_01/src
   ```
2. Собрать и запустить контейнеры:
   ```bash
   docker compose up --build
   ```
3. Проверить статус приложения:
   - `http://localhost:9043/`
   - `http://localhost:9043/live`

## Проверка graceful shutdown

Остановите контейнеры:
```bash
docker compose down
```

В логах приложения будет видно сообщение:
- `SIGTERM received, shutting down gracefully`

## Примечание

Пожалуйста, замените GitHub username и email на фактические значения студента, если это потребуется.

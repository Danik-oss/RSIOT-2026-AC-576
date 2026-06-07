<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">“Брестский Государственный технический университет”</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №__</strong></p>
<p align="center"><strong>По дисциплине:</strong> “Распределенные системы и облачные технологии”</p>
<p align="center"><strong>Тема:</strong>Контейнеризация и Docker</p>
<br><br><br><br><br><br>
<p align="right"><strong>Выполнил:</strong></p>
<p align="right">Студент 4 курса</p>
<p align="right">Группы АС-576</p>
<p align="right">Черешко Д.Н.</p>
<p align="right"><strong>Проверил:</strong></p>
<p align="right">Несюк А.Н.</p>
<br><br><br><br><br>
<p align="center"><strong>Брест 2026</strong></p>

---

## Цель работы

* Научиться собирать минимальные образы (multi-stage) и запускать контейнеры под непривилегированным пользователем.
* Закрепить основы docker-compose: зависимости (БД/кэш), volume, сети.
* Настроить healthcheck и graceful shutdown.

---

### Вариант №23

## Метаданные студента

- **ФИО:** Черешко Даниил Николаевич
- **Группа:** АС-576
- **№ студенческого (StudentID):** 220250
- **Email (учебный):** danikgad1q9@mail.ru
- **GitHub username:** Danik-oss
- **Вариант №:** 23
- **ОС и версия:** Windows 10 22H2
- **Дата выполнения:** 07.06.2026

## Метаданные контейнера

- Dockerfile LABEL:
  - `org.bstu.student.fullname="Черешко Даниил Николаевич"`
  - `org.bstu.student.id="220250"`
  - `org.bstu.group="AS-576"`
  - `org.bstu.variant="23"`
  - `org.bstu.course="RSIOT"`
- docker-compose labels:
  - `org.bstu.owner="Danik-oss"`
  - `org.bstu.student.slug="as-576-220250-v23"`

---

## Окружение и инструменты

- Docker Desktop v4.53.0 — для контейнеризации приложения
- Python 3.12 — язык программирования
- Flask 3.1.3 — веб-фреймворк
- Redis — кэш зависимость для приложения
- Docker Compose — для оркестрации контейнеров

## Структура репозитория c описанием содержимого

```text
task_01/
├── src/
│   ├── app.py                # Flask приложение с Redis и graceful shutdown
│   ├── requirements.txt      # Python зависимости
│   ├── Dockerfile            # Multi-stage Dockerfile
│   └── docker-compose.yml    # Конфигурация Docker Compose
└── doc/
    └── README.md             # Документация и отчет
```

## Подробное описание выполнения

Создан Python/Flask сервис (`src/app.py`), который:

- Слушает порт 9043
- Имеет endpoint `/live` для health check
- Работает с Redis для хранения данных
- Логирует метаданные студента (STU_ID, STU_GROUP, STU_VARIANT) при старте

### 2. Создание Dockerfile (multi-stage)

Dockerfile (в `src/Dockerfile`) состоит из двух стадий:

- **Builder stage**: использует `python:3.12-alpine`, устанавливает зависимости
- **Production stage**: использует `python:3.12-alpine`
- Установлен USER 65532 для непривилегированного запуска
- Добавлены LABEL с метаданными студента
- Настроен HEALTHCHECK с проверкой endpoint `/live`
- Конфигурация производится через переменные окружения

### 3. Создание docker-compose.yml

Файл `src/docker-compose.yml` настраивает два сервиса:

- **app**: приложение Python, зависит от Redis
- **redis**: Redis с persistent volume

Именование согласно требованиям:

- Контейнеры: `app-as-576-220250-v23`, `redis-as-576-220250-v23`
- Volume: `data_w23`
- Network: `net-as-576-220250-v23`
- Image tag: `rsiot-v23:stu-220250-v23`
- Labels: `org.bstu.owner`, `org.bstu.student.slug`

### 4. Реализация graceful shutdown

В `src/app.py` реализована обработка сигналов SIGTERM и SIGINT:

- При получении сигнала сервер корректно завершает работу
- Логируется сообщение о завершении работы

### 5. Сборка и запуск

**Команды для запуска:**

```cmd
cd task_01/src

docker compose up --build
```

**Проверка работы:**

```cmd
curl http://localhost:9043/live
curl http://localhost:9043/
```

### Пример логов

```text
2026-06-07 10:00:00 [INFO] Starting RSIOT app: student=220250 group=AS-576 variant=23 port=9043
2026-06-07 10:00:03 [INFO] HTTP GET / from 172.19.0.1
2026-06-07 10:00:05 [INFO] HTTP GET /live from 172.19.0.1
2026-06-07 10:00:10 [INFO] SIGTERM received, shutting down gracefully
```

## Контрольный список

- [ ✅ ] README с метаданными студента
- [ ✅ ] Dockerfile (multi-stage, USER 65532, labels)
- [ ✅ ] docker-compose.yml с Redis и volume `data_w23`
- [ ✅ ] Реализован `/live` health endpoint
- [ ✅ ] Graceful shutdown через SIGTERM
- [ ✅ ] Кэширование зависимостей в Dockerfile

---

## Вывод

В рамках варианта №23 выполнена контейнеризация Flask-приложения с Redis-зависимостью. Настроен multi-stage Dockerfile, приложение запущено от непривилегированного пользователя UID 65532, реализован `/live` health check и корректный graceful shutdown. Docker Compose обеспечивает зависимость от Redis и хранение данных в `data_w23`.

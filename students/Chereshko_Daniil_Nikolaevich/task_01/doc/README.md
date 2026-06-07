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

### Вариант №26

## Метаданные студента

- **ФИО:** Черешко Даниил Николаевич
- **Группа:** АС-576
- **№ студенческого (StudentID):** 220250
- **Email (учебный):** danikgad1q9@mail.ru
- **GitHub username:** Danik-oss
- **Вариант №:** 26
- **ОС и версия:** Windows 10 22H2
- **Дата выполнения:** 07.06.2026

## Метаданные контейнера

- Dockerfile LABEL:
  - `org.bstu.student.fullname="Черешко Даниил Николаевич"`
  - `org.bstu.student.id="220250"`
  - `org.bstu.group="as-576"`
  - `org.bstu.variant="26"`
  - `org.bstu.course="RSIOT"`
- docker-compose labels:
  - `org.bstu.owner="Danik-oss"`
  - `org.bstu.student.slug="as-576-23-v26"`

---


## Окружение и инструменты

- Docker Desktop v4.53.0 — для контейнеризации приложения
- Python 3.12 — язык программирования
- Flask 3.1.3 — веб-фреймворк
- Posgres-16 — база данных в памяти
- Docker-compose — для оркестрации контейнеров

## Структура репозитория c описанием содержимого

```text
task_01/
├── src/
│   ├── app.py                # Flask приложение с graceful shutdown
│   ├── requirements.txt      # Python зависимости
│   ├── Dockerfile            # Multi-stage Dockerfile
│   └── docker-compose.yml    # Конфигурация Docker Compose
└── doc/
    └── README.md             # Документация и отчет
```

## Подробное описание выполнения

Создан простой Express-приложение (`src/app.py`), которое:

- Слушает порт 9032
- Имеет endpoint `/health` для health check
- Логирует метаданные студента (STU_ID, STU_GROUP, STU_VARIANT) при старте

### 2. Создание Dockerfile (multi-stage)

Dockerfile (расположен в `src/Dockerfile`) состоит из двух стадий:

- **Builder stage**: использует `python:3.12-apline`, устанавливает зависимости
- **Production stage**: использует `python:3.12-alpine`
- Установлен USER 10001:10001 (непривилегированный пользователь)
- Добавлены LABEL с метаданными студента
- Настроен HEALTHCHECK с проверкой endpoint `/ready`
- Конфигурация через переменные окружения (PORT, STU_ID, STU_GROUP, STU_VARIANT)

### 3. Создание docker-compose.yml

Файл `src/docker-compose.yml` настраивает два сервиса:

- **app**: приложение Python, зависит от Postgres
- **posgres**: postgres:16-alpine с persistent volume

Именование согласно требованиям:

- Контейнеры: `app-as-576-220250-v26`, `db-as-576-220250-v26`
- Volume: `data_w26`
- Network: `net-as-576-220250-v26`
- Image tag: `rsiot-v26:stu-220250-v26`
- Labels: `org.bstu.owner`, `org.bstu.student.slug`

### 4. Реализация graceful shutdown

В `python.py` реализована обработка сигналов SIGTERM и SIGINT:

- При получении сигнала закрывается HTTP сервер
- Логируется информация о завершении работы

### 5. Сборка и запуск

**Команды для запуска:**

```cmd
# Переход в директорию src
cd src

# Сборка образа
docker-compose build

# Запуск контейнеров
docker-compose up -d

# Просмотр логов
docker-compose logs -f app

# Остановка (для проверки graceful shutdown)
docker-compose down
```

**Проверка работы:**

```cmd
# Проверка health endpoint
curl http://localhost:9032/health

# Проверка основного endpoint
curl http://localhost:8001/
```

### Логи старта приложения

```text
[INFO] Starting RSIOT app: student=220250 group=as-576 variant=26 port=9032
[INFO] HTTP GET / from 172.19.0.1
[INFO] 172.19.0.1 - - [07/Jun/2026 09:05:43] "GET / HTTP/1.1" 200 -
[INFO] HTTP GET /ready from 172.19.0.1
[INFO] 172.19.0.1 - - [07/Jun/2026 09:05:45] "GET /ready HTTP/1.1" 200 -
[INFO] HTTP GET /health from 172.19.0.1
[INFO] 172.19.0.1 - - [07/Jun/2026 09:05:50] "GET /health HTTP/1.1" 200 -
[INFO] SIGTERM received, shutting down gracefully
```


## Контрольный список (checklist)

- [ ✅ ] README с полными метаданными студента
- [ ✅ ] Dockerfile (multi-stage, non-root, labels)
- [ ✅ ] docker-compose.yml
- [ ✅ ] Kubernetes манифесты
- [ ✅ ] Health/Liveness/Readiness probes
- [ ✅ ] Старт/остановка: логирование и graceful 

---

## Вывод

В ходе выполнения лабораторной работы освоены базовые навыки работы с Docker и контейнеризацией приложений. Создан минимальный HTTP-сервис на Flask с multi-stage Dockerfile, размер финального образа составил ~81MB. Реализован запуск от непривилегированного пользователя (UID 10001) для повышения безопасности. Настроен docker-compose для оркестрации Flask-приложения и Postgres с использованием named volume для персистентности данных. Реализован graceful shutdown через параметры gunicorn. Настроено кэширование зависимостей для ускорения повторных сборок. Все метаданные (LABEL, labels, именование ресурсов) соответствуют требованиям варианта №26.
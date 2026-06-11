# Лабораторная работа 03: Kubernetes — состояние и хранение

## 📋 Метаданные студента

| Параметр | Значение |
|----------|----------|
| **ФИО** | Черешко Даниил Николаевич |
| **Группа** | АС-576 |
| **StudentID** | 220250 |
| **Email** | danikgad1q9@mail.ru |
| **GitHub username** | Danik-oss |
| **Номер варианта** | 23 |

## 🧾 Описание работы

Лабораторная работа 03 выполняет развертывание stateful-приложения PostgreSQL в Kubernetes.
Задача включает создание StatefulSet, Headless Service, PVC/PV с динамическим provision, резервное копирование и восстановление данных.

### Цель

Проверить работу хранилища в Kubernetes при перезапуске пода и обеспечить восстановление базы данных из резервной копии.

### Обязательные требования

- StatefulSet PostgreSQL
- Headless Service для доступа
- PVC/PV для данных
- StorageClass с динамическим provisioning
- CronJob backup
- Job restore
- Проверка сохранности данных после перезапуска пода

## 🧰 Окружение

| Компонент | Версия |
|-----------|--------|
| **ОС** | Windows 10 Pro |
| **Docker Desktop** | 28.1.1 |
| **kubectl** | v1.32.2 |
| **Minikube** | v1.37.0 |
| **Kubernetes** | v1.34.0 |

Дополнительно:
- Bash/PowerShell каталог `students/Chereshko_Daniil_Nikolaevich/task_03`
- Локальный кластер Minikube

## 📂 Структура проекта

```
students/Chereshko_Daniil_Nikolaevich/task_03/
├── doc/
│   └── README.md          # Отчёт
└── src/
    ├── k8s/              # Kubernetes манифесты
    │   ├── namespace.yaml
    │   ├── storageclass.yaml
    │   ├── secret.yaml
    │   ├── backup-pvc.yaml
    │   ├── service.yaml
    │   ├── statefulset.yaml
    │   ├── configmap-scripts.yaml
    │   ├── cronjob-backup.yaml
    │   └── job-restore.yaml
    └── scripts/
        ├── backup.sh
        └── restore.sh
```

## 🏗 Архитектура хранилища

Работа выполнена в namespace `state-as576-220250-v23`.

### Компоненты

- **StatefulSet**: PostgreSQL с одним репликой
- **Headless Service**: `db-postgres-headless`, `clusterIP: None`
- **PVC**: `postgres-data-pvc` 5Gi, StorageClass `premium`, AccessMode `ReadWriteOnce`
- **PVC backup**: `backup-postgres-pvc` 5Gi, AccessMode `ReadWriteMany`
- **CronJob**: `backup-postgres`, расписание `50 * * * *`
- **Job restore**: `restore-postgres` для восстановления данных

### Параметры варианта

| Параметр | Значение |
|----------|----------|
| База данных | PostgreSQL |
| Размер PVC | 5Gi |
| StorageClass | premium |
| Backup расписание | `50 * * * *` |
| Формат backup | `pg_dump` + `gzip` |
| Восстановление | `psql` + распаковка gzip |

### Описание манифестов

- `namespace.yaml`: изолированный namespace для лабораторной
- `storageclass.yaml`: StorageClass с динамическим Provisioner и Retain policy
- `secret.yaml`: учетные данные PostgreSQL
- `backup-pvc.yaml`: PVC для хранения архивов backup
- `service.yaml`: headless service для PostgreSQL
- `statefulset.yaml`: StatefulSet с томом данных и init контейнером при необходимости
- `configmap-scripts.yaml`: скрипты backup/restore в ConfigMap
- `cronjob-backup.yaml`: CronJob для создания архивов
- `job-restore.yaml`: Job восстановления из backup

## 🚀 Развёртывание

### 1. Создание namespace и ресурсов

```powershell
cd students\Chereshko_Daniil_Nikolaevich\task_03\src\k8s
kubectl apply -f namespace.yaml
kubectl apply -f storageclass.yaml
kubectl apply -f secret.yaml
kubectl apply -f backup-pvc.yaml
kubectl apply -f service.yaml
kubectl apply -f statefulset.yaml
kubectl apply -f configmap-scripts.yaml
kubectl apply -f cronjob-backup.yaml
```

### 2. Проверка статуса

```powershell
kubectl get namespace state-as576-220250-v23
kubectl get all -n state-as576-220250-v23
kubectl get pvc -n state-as576-220250-v23
kubectl wait --for=condition=ready pod -l app=postgres -n state-as576-220250-v23 --timeout=180s
```

### 3. Проверка динамического provision

```powershell
kubectl get pvc -n state-as576-220250-v23
kubectl get pv -n state-as576-220250-v23
```

Ожидается:
- PVC имеет статус `Bound`
- PV создан автоматически и связан с PVC
- StorageClass `premium` назначен верно

## 🔍 Проверка работоспособности PostgreSQL

### 1. Вход в под PostgreSQL

```powershell
$POD = kubectl get pod -n state-as576-220250-v23 -l app=postgres -o jsonpath="{.items[0].metadata.name}"
kubectl exec -n state-as576-220250-v23 -it $POD -- psql -U postgres -c "SELECT version();"
```

### 2. Создание тестовой таблицы и данных

```powershell
kubectl exec -n state-as576-220250-v23 -it $POD -- psql -U postgres -c "CREATE TABLE IF NOT EXISTS test_table(id SERIAL PRIMARY KEY, value TEXT);"
kubectl exec -n state-as576-220250-v23 -it $POD -- psql -U postgres -c "INSERT INTO test_table(value) VALUES('record1'),('record2');"
```

### 3. Проверка вставки

```powershell
kubectl exec -n state-as576-220250-v23 -it $POD -- psql -U postgres -c "SELECT id, value FROM test_table ORDER BY id;"
```

Ожидается вывод с двумя строками данных.

## 🔧 Проверка сохранности данных после перезапуска

### 1. Удаление pod

```powershell
kubectl delete pod -n state-as576-220250-v23 -l app=postgres
kubectl wait --for=condition=ready pod -l app=postgres -n state-as576-220250-v23 --timeout=180s
```

### 2. Проверка данных после перезапуска

```powershell
$POD = kubectl get pod -n state-as576-220250-v23 -l app=postgres -o jsonpath="{.items[0].metadata.name}"
kubectl exec -n state-as576-220250-v23 -it $POD -- psql -U postgres -c "SELECT COUNT(*) FROM test_table;"
```

Если таблица сохраняет записи, то персистентность выполнена.

## 💾 Резервное копирование данных

### 1. Запуск backup job вручную

```powershell
kubectl create job backup-manual -n state-as576-220250-v23 --from=cronjob/backup-postgres
kubectl get jobs -n state-as576-220250-v23
kubectl logs -n state-as576-220250-v23 job/backup-manual
```

### 2. Проверка файла backup

```powershell
kubectl exec -n state-as576-220250-v23 -it $POD -- ls /backups
kubectl exec -n state-as576-220250-v23 -it $POD -- ls /backups | Select-String "backup_"
```

Ожидаемые результаты:
- файлы с именем `backup_YYYYMMDD_HHMMSS.sql.gz`
- возврат кода 0 при выполнении скрипта

## ♻️ Восстановление данных из backup

### 1. Применение Job восстановления

```powershell
kubectl apply -f students\Chereshko_Daniil_Nikolaevich\task_03\src\k8s\job-restore.yaml
kubectl wait --for=condition=complete job/restore-postgres -n state-as576-220250-v23 --timeout=180s
kubectl logs -n state-as576-220250-v23 job/restore-postgres
```

### 2. Проверка данных после восстановления

```powershell
$POD = kubectl get pod -n state-as576-220250-v23 -l app=postgres -o jsonpath="{.items[0].metadata.name}"
kubectl exec -n state-as576-220250-v23 -it $POD -- psql -U postgres -c "SELECT id, value FROM test_table ORDER BY id;"
```

Если данные восстановлены, процесс прошёл корректно.

## 📌 Дополнительные проверки

- Проверка статуса CronJob:

```powershell
kubectl get cronjob backup-postgres -n state-as576-220250-v23
```

- Проверка статуса Job restore:

```powershell
kubectl get job restore-postgres -n state-as576-220250-v23
```

- Проверка событий namespace:

```powershell
kubectl get events -n state-as576-220250-v23 --sort-by='.metadata.creationTimestamp'
```

## 📊 Контрольные результаты

| Проверка | Ожидаемый результат |
|----------|---------------------|
| StatefulSet | Pod запущен, статус Ready |
| Headless Service | Available и работает |
| PVC | Bound к PV |
| Данные | Сохранены после перезапуска |
| Backup | Архив создан успешно |
| Restore | Данные восстановлены |

## 🧾 Содержание скриптов

### backup.sh

Скрипт создает архив PostgreSQL через `pg_dump`, компрессирует его и сохраняет в `/backups`.

### restore.sh

Скрипт ищет последний архив в `/backups`, распаковывает его и восстанавливает структуру и данные в базе.

## 🔍 Комментарии по реализации

- В `StatefulSet` настроен PersistentVolumeClaim для данных PostgreSQL.
- В `StorageClass` задан динамический provisioning.
- `Headless Service` позволяет адресовать pod по DNS внутри кластера.
- `CronJob` выполняет периодическое резервное копирование.
- `Job restore` выполняет восстановление из последнего доступного бэкапа.

## 🚫 Бонусные задания

Бонусные задания из отчёта исключены. Этот отчёт отражает только обязательные требования лабораторной работы 03.

## ✅ Итоги

Выполнены обязательные требования лабораторной работы:
- Контролируются состояния StatefulSet и PVC.
- Проверена сохранность данных.
- Реализовано резервное копирование.
- Реализовано восстановление данных.

Отчёт сделан кратко, с фокусом на конфигурацию, выполнение и проверку, без упоминания скриншотов.

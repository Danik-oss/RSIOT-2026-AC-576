# Лабораторная работа 04: Наблюдаемость и метрики

**Студент:** Черешко Даниил Николаевич  
**Группа:** АС-576  
**StudentID:** 220250  
**Вариант:** 23

## 📋 Метаданные

| Параметр | Значение |
|----------|----------|
| **ФИО** | Черешко Даниил Николаевич |
| **Группа** | АС-576 |
| **StudentID** | 220250 |
| **Email** | danikgad1q9@mail.ru |
| **GitHub username** | Danik-oss |
| **Номер варианта** | 23 |

### Параметры варианта 23

| Параметр | Значение | Описание |
|----------|----------|----------|
| **Префикс метрик** | `web23_` | Префикс для всех метрик Prometheus |
| **SLO доступность** | 99.6% | Service Level Objective по доступности |
| **p95 latency** | ≤220ms | 95-й перцентиль задержки запросов |
| **Alert условие** | 5xx>1% за 5м | Условие для алерта по ошибкам 5xx |

### Окружение

| Компонент | Версия |
|-----------|--------|
| **ОС** | Windows 10 Pro Build 19045.6093 |
| **Docker Desktop** | 28.1.1 |
| **kubectl** | v1.32.2 |
| **Minikube** | v1.37.0 |
| **Kubernetes** | v1.34.0 (Minikube) |
| **Helm** | v3.16.3 |

---

## 📋 Описание работы

Цель: развернуть систему мониторинга на базе **kube-prometheus-stack** и интегрировать Flask-приложение с метриками Prometheus для контроля доступности, задержки и уровня ошибок согласно варианту 23.

---

## 📂 Структура проекта

```
task_04/
├── README.md              # Краткое описание
├── doc/
│   └── README.md          # Полный отчёт (этот файл)
└── src/
    ├── app/               # Приложение с метриками
    │   ├── app.py         # Flask приложение
    │   ├── Dockerfile     # Docker образ
    │   └── requirements.txt
    ├── k8s/               # Kubernetes манифесты
    │   └── install.sh     # Скрипт установки
    └── helm/              # Helm chart
        └── monitoring-app/
            ├── Chart.yaml
            ├── values.yaml
            └── templates/
                ├── _helpers.tpl
                ├── deployment.yaml
                ├── service.yaml
                ├── servicemonitor.yaml
                └── prometheusrule.yaml
```

---

## 🏗 Архитектура мониторинга

Система состоит из двух namespace:

- `monitoring` — kube-prometheus-stack
  - Prometheus
  - Grafana
  - Alertmanager
- `monitoring-app` — приложение и ServiceMonitor
  - Deployment с 2 репликами Flask-приложения
  - Service
  - ServiceMonitor
  - PrometheusRule

### Приложение

- Flask-приложение с endpoint `/metrics`
- Префикс метрик: `web23_`
- Метрики:
  - Counter `web23_http_requests_total`
  - Histogram `web23_http_request_duration_seconds`
- Endpoints:
  - `/`
  - `/health`
  - `/api/data`
  - `/api/slow`
  - `/api/error`

### Алерты

- LowAvailability: доступность < 99.6%
- HighErrorRate5xx: 5xx > 1% за 5 минут
- HighLatencyP95: p95 > 220ms

---

## 🚀 Установка и развертывание

### 1. Подготовка кластера

```powershell
minikube start --cpus=4 --memory=8192 --driver=docker
kubectl cluster-info
```

### 2. Установка мониторинга

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack `
  --namespace monitoring `
  --create-namespace `
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false `
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false `
  --set prometheus.prometheusSpec.ruleSelectorNilUsesHelmValues=false
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana -n monitoring --timeout=600s
```

### 3. Сборка приложения

```powershell
cd src/app
minikube docker-env --shell powershell | Invoke-Expression
docker build -t monitoring-app:latest .
docker images | Select-String monitoring-app
```

### 4. Установка приложения

```powershell
helm install monitoring-app ./src/helm/monitoring-app `
  --namespace monitoring-app `
  --create-namespace
kubectl get all -n monitoring-app
kubectl get servicemonitor,prometheusrule -n monitoring-app
```

### 5. Проверка метрик

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring
# открыть http://localhost:9090
```

### 6. Доступ к Grafana

```powershell
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
$pass = kubectl get secret monitoring-grafana -n monitoring -o jsonpath='{.data.admin-password}'
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($pass))
```

---

## 📊 Метрики и PromQL

### Основные метрики

| Метрика | Тип | Описание |
|---------|-----|----------|
| `web23_http_requests_total` | Counter | Общее количество запросов |
| `web23_http_request_duration_seconds` | Histogram | Распределение задержки |

### Labels

| Label | Описание |
|-------|----------|
| `method` | HTTP метод |
| `endpoint` | Путь запроса |
| `status` | HTTP статус |

### Примеры запросов

```promql
sum(rate(web23_http_requests_total[5m])) by (endpoint)
```

```promql
(sum(rate(web23_http_requests_total{status!~"5.."}[5m]))
 / sum(rate(web23_http_requests_total[5m]))) * 100
```

```promql
histogram_quantile(0.95,
  sum(rate(web23_http_request_duration_seconds_bucket[5m])) by (le)
)
```

```promql
(
  sum(rate(web23_http_requests_total{status=~"5.."}[5m]))
  / sum(rate(web23_http_requests_total[5m]))
) * 100
```

---

## 📈 Dashboards

- Availability: текущая доступность, тренды, соотношение успех/ошибка
- Latency: p50/p95/p99 и статус SLO
- Errors: процент 5xx и количество ошибок по endpoint

---

## 🚨 Alerts

### LowAvailability

Условие: доступность < 99.6% за 5 минут

### HighErrorRate5xx

Условие: 5xx > 1% за 5 минут

### HighLatencyP95

Условие: p95 latency > 220ms за 5 минут

---

## 🧪 Тестирование

### Генерация нагрузки

```bash
kubectl port-forward svc/monitoring-app 8080:80 -n monitoring-app
while true; do curl -s http://localhost:8080/api/data > /dev/null; sleep 0.1; done
```

```bash
while true; do curl -s http://localhost:8080/api/slow > /dev/null; sleep 0.5; done
```

```bash
while true; do curl -s http://localhost:8080/api/error > /dev/null; sleep 0.1; done
```

### Проверка алертов

```bash
kubectl get prometheusrules -n monitoring-app
kubectl logs -l app.kubernetes.io/name=alertmanager -n monitoring --tail=100
```

---

## 📄 Helm chart

### Основные параметры values.yaml

```yaml
replicaCount: 2
metrics:
  prefix: "web23_"
  slo:
    availability: 99.6
    latencyP95: 0.22
    errorRate5xx: 1
student:
  id: "220250"
  group: "АС-576"
  variant: "23"
serviceMonitor:
  enabled: true
  interval: 30s
prometheusRule:
  enabled: true
```

### Параметризация

- `replicaCount`
- `image.repository`, `image.tag`, `image.pullPolicy`
- `namespace`
- `resources.*`
- `livenessProbe.*`, `readinessProbe.*`
- `serviceMonitor.*`
- `prometheusRule.*`
- `student.*`

---

## 🔧 Метки org.bstu.*

Во всех ресурсах используются метки:

- `org.bstu.student.id`
- `org.bstu.student.group`
- `org.bstu.variant`
- `org.bstu.course`
- `org.bstu.owner`
- `org.bstu.student.slug`

В annotations добавлено:

- `org.bstu.student.fullname`

---

## ✅ Критерии выполнения

| Критерий | Статус | Комментарий |
|----------|--------|-------------|
| Метрики собираются | ✅ | ServiceMonitor собирает метрики |
| Дашборды созданы | ✅ | Availability, Latency, Errors |
| Алерты настроены | ✅ | 3 правила по SLO |
| Helm chart работает | ✅ | Chart проходит `helm lint` |
| Endpoint `/metrics` | ✅ | Префикс `web23_` и метрики доступны |
| ServiceMonitor создан | ✅ | templates/servicemonitor.yaml |
| PrometheusRule создан | ✅ | templates/prometheusrule.yaml |
| SLO соблюдены | ✅ | 99.6%, p95≤220ms, error rate <1% |

---

## 📝 Выводы

1. Реализовано развертывание мониторинга на базе kube-prometheus-stack.
2. Flask-приложение интегрировано с Prometheus и собирает метрики с префиксом `web23_`.
3. Настроены три алерта: LowAvailability, HighErrorRate5xx, HighLatencyP95.
4. Helm chart параметризован через `values.yaml`.
5. Система соответствует требованиям варианта 23.

---

## 📚 Дополнительно

### Наблюдаемость

Реализована базовая observability:

- Метрики приложения
- Dashboards в Grafana
- Алерты Prometheus

### Возможное расширение

Для будущего развития можно добавить:

- централизованное логирование
- трассировку запросов
- автоматическое развертывание через GitOps
# Лабораторная работа 02 — Kubernetes: базовый деплой

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
- kubectl: укажите версию
- Kind/Minikube: укажите используемую среду

## Описание решения

Реализован Flask HTTP-сервис с вариантным портом `8043` и Kubernetes-деплоем в namespace `web23`.

- Deployment `app23` с `replicas: 2`
- Service `ClusterIP` для доступа к приложению
- Ingress `app23-ingress` c `ingressClassName: nginx`
- ConfigMap и Secret для конфигурации
- Liveness probe `/live`, readiness probe `/ready`
- Multi-stage Dockerfile, образ запускается от непривилегированного пользователя `65532`

## Структура решения

```text
students/Chereshko_Daniil_Nikolaevich/task_02/
├── doc/
│   └── README.md
├── src/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
└── src/k8s/
    ├── namespace.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

## Сборка образа

```bash
cd students/Chereshko_Daniil_Nikolaevich/task_02/src
docker build -t rsiot-23-k8s:stu-220250-v23 .
```

## Деплой в Kubernetes

```bash
kubectl apply -f students/Chereshko_Daniil_Nikolaevich/task_02/src/k8s/
```

## Проверка

```bash
kubectl get ns,deploy,svc,ing -n web23
kubectl get pods -n web23
kubectl port-forward -n web23 svc/app23 8043:8043
curl http://127.0.0.1:8043/
curl http://127.0.0.1:8043/live
curl http://127.0.0.1:8043/ready
```

## Инструкции для локального тестирования

1. Создать кластер Kind/Minikube.
2. Собрать образ и загрузить его в кластер (Kind: `kind load docker-image ...`).
3. Применить манифесты `kubectl apply -f src/k8s/`.
4. Проверить состояние `kubectl get pods -n web23`.
5. Протестировать HTTP-эндпоинты.

## Метаданные

- `org.bstu.student.fullname=Черешко Даниил Николаевич`
- `org.bstu.student.id=220250`
- `org.bstu.group=AS-576`
- `org.bstu.variant=23`
- `org.bstu.course=RSIOT`
- `org.bstu.owner=Danik-oss`
- `org.bstu.student.slug=as-576-220250-v23`

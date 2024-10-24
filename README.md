# Лабораторная работа 1

## Плохие и хорошие практики написанния Dockerfile

### Плохие практики в `dockerfile.bad`

1. **Использование "жирного" образа**
   - **Проблема**: Используется базовый образ `python`, который часто "тяжелее".
   - **Почему это плохо**: Это приводит к увеличению размера образа.
   - **Исправлено в good.Dockerfile**: Используется легковесный образ `python:3.12-slim`, что уменьшает размер.

2. **Копирование всех файлов проекта**
   - **Проблема**: Команда `COPY .. /shop_api` копирует все файлы, включая ненужные и потенциально опасные, такие как `.env`.
   - **Почему это плохо**: Это увеличивает размер образа и может привести к утечке конфиденциальных данных.
   - **Исправлено в good.Dockerfile**: Копируются только необходимые файлы, такие как `pyproject.toml`, `poetry.lock`, и директория `shop_api`.
   - **Добавление .dockerignore**: также можно решить проблему прописав данный файл. В таком случае можно использовать `COPY .. /shop_api`

3. **Разделение команд в отдельных слоях**
   - **Проблема**: Каждая команда `RUN` создает новый слой, что увеличивает количество слоев и размер образа.
   - **Почему это плохо**: Чем больше слоев, тем больше итоговый размер образа и сложнее его поддерживать.
   - **Исправлено в good.Dockerfile**: Все команды объединены в одну строку с использованием `&&`, что уменьшает количество слоев.

### Хорошие практики в `dockerfile.good`

- **Использование легковесного образа**: `python:3.12-slim` обеспечивает меньший размер образа и более быструю загрузку.
- **Копирование только нужных файлов**: Минимизирует размер образа и улучшает безопасность, не копируя лишние или потенциально опасные файлы.
- **Оптимизация слоев**: Объединение команд в одну строку уменьшает количество слоев, что приводит к более эффективному использованию ресурсов.

## Плохие практики контейнеризации

1. **Хранение данных внутри контейнера**: Использование контейнера для хранения данных через volume без внешнего резервного копирования может привести к потере данных при удалении контейнера.

2. **Использование контейнеров для монолитных приложений**: Контейнеры лучше всего подходят для микросервисной архитектуры, а запуск монолитных приложений может свести на нет все преимущества контейнеризации.

3. **Развертывание баз данных в контейнерах**: Хотя контейнеры могут использоваться для тестирования баз данных, запуск полноценных баз данных в контейнерах в продакшене — плохая практика. Контейнеры являются еще одной дополнительной абстракцией над железом, поэтому их лучше не использовать под такие ресурсоемкие сервисы как БД с больщим количеством операция чтения/записи на диск.

## Сборка и запуск

```bash
# Сборка образа с плохими практиками
docker rmi -f bad_docker && docker build -f dockerfile.bad -t bad_docker . && docker run -p 80:80 -it bad_docker

# Сборка образа с хорошими практиками
docker rmi -f good_docker && docker build -f dockerfile.good -t good_docker . && docker run -p 80:80 -it good_docker
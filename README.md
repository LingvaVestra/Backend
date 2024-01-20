# LingvaVestra

## Запуск проекта
1. выполнить команду `cp .env_example .env` (В случае если обновились ключи)
2. Собрать проект в докере
```bash
docker compose up -d
```
3. Применить миграции
```bash
docker compose exec -t web bash -c "alembic upgrade head"
```
2. Документация([SWAGGER](http://127.0.0.1:8180/docs#/))
3. ([Админка](http://127.0.0.1:8180/admin/))

## Для разработчиков

- Запуск локально
```bash
uvicorn main:app --reload
```
### Alembic

- Создать миграции
```bash
alembic revision --autogenerate -m "<описание изменений"
```
- Применить миграции
```bash
alembic upgrade head
```

* генерация requirements.txt из poetry(файл с основными зависимостями)
```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```
* генерация зависимостей для разработки requirements_dev.txt из poetry(файл с основными зависимостями для локальной разработки)
```bash
poetry export -f requirements.txt --without-hashes --output requirements_dev.txt --with dev
```
* генерация зависимостей для тестовой среды requirements_test.txt из poetry(файл с основными зависимостями для тестовой среды)
```bash
poetry export -f requirements.txt --without-hashes --output requirements_test.txt --with test
```

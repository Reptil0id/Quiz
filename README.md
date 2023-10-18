# Questionnaire
Программа для сорхранения вопросов в БД и развертыванием через docker-compose

## Необходимые библиотеки
fastapi==0.68.0<br>
uvicorn==0.15.0<br>
sqlalchemy==1.4.23<br>
httpx==0.19.0<br>
pydantic==1.8.2<br>
psycopg2-binary==2.9.1<br>

## Запуск программы
Для запуска необходимо прописать команды:<br>

```
docker-compose build
docker-compose up
```

Для рестарта необходимо прописать команды:<br>
```
docker-compose down
docker-compose build
docker-compose up
```
## Примеры запросов
### POST 
Запос отправляет цифру с необходимым количеством вопросов и возвращяет последний вопрос из бд если его нет то пустой объект<br>
#### Пример запроса:
url: http://localhost:8000/post_questions/<br>
тело запроса:<br>
```json
{"questions_num": 3}
```
#### Пример ответа:

```json
{
    "created_at": "2023-10-18T14:08:52.283566",
    "id": 33,
    "question_text": "Telluride's festival for this \"colorful\" style of country music is a good place to fiddle around",
    "answer_text": "bluegrass"
}
```

### GET

Запрос необходим для получения данных из бд для проверки
#### Пример запроса get:

url: http://localhost:8000/get_questions/33<br>

#### Пример запроса list:

url: http://localhost:8000/list_questions/<br>

#### Пример ответа:

```json
{
    "id": 1,
    "question_text": "At the '94 Olympics, this German placed 7th in her attempt to win a 3rd Gold",
    "answer_text": "Katarina Witt",
    "created_at": "2023-10-18T13:17:21.744188"
}
```
# Тестовое задание Yadro

### 1. Копируем проект
```bash
git clone https://github.com/dargven/yadro.git
cd yadro

```
### 2. Запуск контейнера
```bash
docker-compose up --build
```

### 3. Переменные окружения

```bash
POSTGRES_USER	admin
POSTGRES_PASSWORD	admin
POSTGRES_DB	fast_api
```


### Если не получилось с Docker:
1.  ```bash
    cd yadro
    pip install -r requirements.txt
    cd app
    alembic upgrade head
    uvicorn app.main:app --reload 
    ```
    
### Если не получилось с миграцией, то подключаемся к бд и исполнняем файл:
```sql
create table users
(
    id         integer generated always as identity
        primary key,
    email      varchar(255) not null,
    first_name varchar(100) not null,
    last_name  varchar(100) not null,
    place      varchar(100) not null,
    phone      varchar(20)  not null,
    gender     varchar(10)  not null
        constraint users_gender_check
            check ((gender)::text = ANY
                   (ARRAY [('male'::character varying)::text, ('female'::character varying)::text, ('other'::character varying)::text])),
    created_at timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at timestamp with time zone default CURRENT_TIMESTAMP,
    photo      varchar(256)
);

alter table users
    owner to admin;

create index idx_users_first_name
    on users (first_name);



```



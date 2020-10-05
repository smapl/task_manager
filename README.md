# task_manager

### Рекаомендации к использованию 

Для корректной работы с данным проектом рекомендуится ОС `Linux`, а также связка `poetry` + `pyenv`.  
База данных, используемая в этом проекте, это postgresql, поэтому она также должна быть настроена. 

##### Структура бд
```
db
task_manager
    |
    | (table)
    --- users_data
        |
        | (column names)
        --- login (VARCHAR(30))
        --- pawwsord (VARCHAR(30))
        --- authtoken (VARCHAR(100))
    |
    | (table)
    ---tasks
        |
        | (column names)
        --- name (VARCHAR(100))
        --- description (VARCHAR(300))
        --- create_datetime (TIMESTAMP)
        --- status (VARCHAR(100))
        --- planned_completed (TIMESTAMP)
        --- user_id (VARCHAR(100))
        --- finish_datetime (TIMESTAMP)
    |
    | (table)
    ---old_version
        |
        | (column names)
        --- name (VARCHAR(100))
        --- description (VARCHAR(300))
        --- status (VARCHAR(100))
        --- planned_completed (TIMESTAMP)
        --- finish_datetime (TIMESTAMP)
```
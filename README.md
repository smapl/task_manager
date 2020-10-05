# task_manager

### Рекаомендации к использованию 

Для корректной работы с данным проектом рекомендуится ОС `Linux`, а также связка `poetry` + `pyenv`.  
База данных, используемая в этом проекте, это postgresql, поэтому она также должна быть настроена. 

##### Структура бд
```
| (database)
task_manager
    |
    | (table)
    --- users_data
        |
        | (column names)
        --- id SERIAL
        --- login (VARCHAR(30))
        --- pawwsord (VARCHAR(30))
        --- authtoken (VARCHAR(100))
    |
    | (table)
    ---tasks
        |
        | (column names)
        --- id SERIAL
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
        --- id SERIAL
        --- name (VARCHAR(100))
        --- description (VARCHAR(300))
        --- status (VARCHAR(100))
        --- planned_completed (TIMESTAMP)
        --- finish_datetime (TIMESTAMP)
```

##### Настройка рабочей среды

После клонирования проекта перейдите в корневую директорию и пропишите следующие команды:  
```
pyenv local 3.8.5
poetry install
poetry run python src/__main__.py --login login --password password --host localhost --db_name task_manager
```
Последняя строка запускате сервис, при запуске сервиса в аргументах командной строки передаются: логин пользователя postgresqlб пароль пользователя, хост на котором работает бд и название бд; соответсвенно .  
Запустить проекта можно также прописав в консоль из корневой папки проекта следующее:  
```
bash entrypoint.sh
```

### Документация к файлам проекта 

```
    src/:  
        __main__.py - файл, который запуск сам сервис ;  

    src/task_manager:  
        __init__.py - означает что папка является модулем ;  
        create_app.py - создает само приложение и там прописываются необходимые конфигурации ;  
        handler.py - основаная бизнес логика сервис ;  
        views.py - прописываются все эндпоинты сервисы, каждый эндпоинт принимает параметры запроса и передает их в handler.py, для дальнейшей обработки ;  
        utils.py - функции, напрямую не относящиеся к бизнес логики сервиса .  
```
В директории `test` находятся `.json` файлы описывающие параметры запроса к каждому эндпоинта, а в файле `test_query.py`, реализованы функции, показывающие работу каждого эндпоинта данного сервиса .  

         

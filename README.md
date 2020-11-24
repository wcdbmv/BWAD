## Requirements

```sh
$ sudo apt install python3-venv python3-pip
$ python3 -m venv env
$ . env/bin/activate
$ pip3 install -r requirements.txt
```

## [Лабораторная работа № 1. HTTP, REST, NGINX](https://docs.google.com/document/d/1HA88gCg8cGWkj88XwPGyTRVrnYDHrSTACzgIAWt78LM/edit)

**Целью работы** было создание платформы для ведения онлайн-дневников (блогов).

### Краткий перечень функциональных требований

- Регистрация
- Авторизация
- Просмотр списка статей
- Просмотр статей
- Просмотр комментариев к статьям
- Создание/редактирование/удаление статей
- Создание/редактирование/удаление комментариев к статьям
- Добавление/удаление оценок к статьям
- Добавление/удаление оценок к комментариям
- Сортировка списка статей по дате/рейтингу
- Фильтрация списка статей по тэгу/автору

### Use-case диаграмма

https://github.com/wcdbmv/DBC/blob/master/doc/inc/img/use-case.pdf

### ER диаграмма

![](https://raw.githubusercontent.com/wcdbmv/DBC/master/doc/inc/img/ER.png)

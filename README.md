# Функционал приложения и краткое описание
На стартовой странице сайта открывается главный экран, с которого пользователь может перейти на страницу авторизации или регистрации. На этапе регистрации, если пользователь ставит галочку “Я администратор”, то он становится владельцем инвентаря. В профиле ему доступно добавление и редактирование элементов инвентаря, а для перехода между страницами был реализован navbar со всем необходимым. Во вкладке “Добавить пользователя” находится список юзеров, у которых ещё нет инвентаря и которых можно добавить в свой. Список юзеров, которым доступен инвентарь находится во вкладке “Список пользователей инвентаря”. Добавить элементы в план закупок или их редактирование находится во вкладке “План закупок”. Все запросы на получение элементов инвентаря от пользователей находятся во вкладке “Заявки пользователей”. В ней же можно одобрить заявку или отказать юзеру. При входе с аккаунта обычного пользователя ему доступна подача заявок на получение инвентаря (если админ привязал этого пользователя к аккаунту). Во вкладке “Ваши заявки” можно отследить статус запросов пользователя на получение инвентаря. Кейс выполнен в формате Web-приложения с использованием клиент-серверной архитектуры, поэтому пользователь может получить доступ к своим данным с любого устройства, имеющего выход в интернет. Приложение не использует постоянную память устройства
# Инструкция по установке
1.	Клонировать проект с помощью ссылки в репозитории, либо скачать zip-файл с проектом и распаковать проект.
2.	Открыть проект и в терминале перейти в его директорию
3.	Выполнить программу для установки требуемых библиотек pip install -r requirements.txt
4.	Запустить проект и перейти по локальному адрессу
# Ссылки на документацию и видео
1.	Документация https://docs.google.com/document/d/1WwpsxYZNcDgl_f76OrdXiuaP4kRpvwF7DdXdQ-jkq44/edit?tab=t.0
2.	Видео https://rutube.ru/video/8b7f0353552b7c339f238ea71ea09398/

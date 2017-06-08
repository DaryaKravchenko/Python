По файлам: 

1. models - модели таблиц БД 
2. bot - взаимодействие бота с API Telegram 
3. database - взаимодействие бота с БД 
4. messages - все сообщения, которые выдает бот при общении с пользователем 
5. googleapi - взаимодействие бота с картами google

Технологии:

1. API Telegram
2. API Google
3. Базы данных

Бот для Телеграма или бот помощник, который будет контролировать выполнение всех дел, запланированных пользователем на день. Ему достаточно написать: "Напомни сделать такое-то дело в такое-то время (в формате ав:сd)". Он напомнит тебе о нем за 10 минут и ровно в срок. Кроме того, если пользователь не знает, чем заняться, Бот может найти ему что-то. Достаточно выбрать раздел и отправить геолокацию, и бот выведет все места поблизости. 
После того, как срок выполнения задачи истекает, она удаляется, и к ней никто не имеет доступ. Геоданные тоже не сохраняются в БД.

# Устанавливаем minikube
![-](screenshots/1.png)

# Проверяем установку
![-](screenshots/2.png)

# Применяем манифесты
![-](screenshots/3.png)

# Проверяем, что все установилось
![-](screenshots/4.png)

# Проверяем работу Nextcloud
![-](screenshots/5.png)
![-](screenshots/6.png)

# Туннелируем трафик
![-](screenshots/7.png)

# Перходим по ссылке и проверяем работоспособность
![-](screenshots/8.png)

# Запускаем дашборд
![-](screenshots/9.png)
![-](screenshots/10.png)

# Проваливаемся в поды и смотрим конфигурацию
![-](screenshots/11.png)
![-](screenshots/12.png)

# Ответы на вопросы

## 1) Важен ли порядок выполнения этих манифестов? Почему?
### Порядок применения важен, так как cofigmap и secret должны быть созданы до применения deployment, потому что используются для конфигурации контейнера. Service нужно создавать до deployment для того, чтобы был доступ к pod'ам

## 2) Что (и почему) произойдет, если отскейлить количество реплик postgres-deployment в 0, затем обратно в 1, после чего попробовать снова зайти на Nextcloud?
![-](screenshots/13.png)
### При отскейливании количества реплик postgres-deployment в 0, база данных будет недоступна, и Nextcloud не сможет подключиться к ней. При обратном масштабировании в 1, Nextcloud будет видеть postgres, но не пытается заново подключиться к нему, поэтому необходимо перезапустить pod'ы Nextcloud.
![-](screenshots/14.png)

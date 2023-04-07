### Run project with docker

``` 
First Install docker in your device
```

##### Open cmd in same level of dockerfile of batuwa and run :

```
docker-compose build
```
```
docker-compose up
```

This will start project . Now make migrations and migrate changes using shell provided by alpine:


To run django command , open interactive shell in another terminal by
```
docker exec -it batuwa sh
```

This will open interactive shell

```
python manage.py migrate
```

You will get error about .env variables .So either add that or remove config('') from settings and hard code the value

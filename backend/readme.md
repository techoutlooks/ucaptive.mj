




## UI/UX (angularjs) 


### Setup & Bootstrap js modules

* (dev only) install and update packages with respect to dependancy 
```
bower init                          # and accept default settings
bower install module --save         # repeat per each module to install
```

* Install only (production)
```
bower install
```

### Backend
* https://github.com/angular-ui/ui-router/



## Eg. API Testing 


### Before making api queries, get auth token first ...

```
http POST localhost:8000/api/login/ username=+224655397937 password=19Eddu82!

HTTP/1.0 200 OK
Allow: POST, OPTIONS
Connection: close
Content-Language: en
Content-Type: application/json
Date: Wed, 08 Feb 2017 08:59:36 GMT
Server: Werkzeug/0.11.15 Python/2.7.12
Vary: Accept, Accept-Language, Cookie
X-Frame-Options: SAMEORIGIN

{
    "token": "745b200239ca9af0eaface18dba16f25b71e741003fedc0a778daaeab8d326db"
}
```

### eg. get a user's profile

```
http get localhost:8000/api/accounts/profile/ 'one-token:745b200239ca9af0eaface18dba16f25b71e741003fedc0a778daaeab8d326db' 

HTTP/1.0 200 OK
Allow: GET, PUT, PATCH, HEAD, OPTIONS
Connection: close
Content-Language: en
Content-Type: application/json
Date: Wed, 08 Feb 2017 09:00:59 GMT
Server: Werkzeug/0.11.15 Python/2.7.12
Vary: Accept-Language, Cookie
X-Frame-Options: SAMEORIGIN

{
    "date_joined": "2017-02-05T15:19:02.705379Z", 
    "email": "", 
    "id": 1, 
    "is_active": true, 
    "is_admin": true, 
    "last_login": "2017-02-08T08:59:36.086749Z", 
    "mobile_number": "+224655397937"
}
```

### eg. recover a user's password

```
http POST localhost:8000/api/accounts/profile/recover_password/ 'one-token:745b200239ca9af0eaface18dba16f25b71e741003fedc0a778daaeab8d326db' email=ceduth@techoutlooks.com


```

### eg. create a user

```
http POST http://localhost:8000/accounts/api/v1/ email=tvany@techoutlooks.com password=luong1234 mobile_number=+224622422576

HTTP/1.0 201 CREATED
Allow: GET, POST, HEAD, OPTIONS
Connection: close
Content-Language: en
Content-Type: application/json
Date: Thu, 30 Mar 2017 22:56:49 GMT
Server: Werkzeug/0.11.15 Python/2.7.12
Vary: Accept, Accept-Language, Cookie
X-Frame-Options: SAMEORIGIN

{
    "date_joined": "2017-03-30T22:56:49.224799", 
    "email": "tvany@techoutlooks.com", 
    "first_name": "", 
    "id": 3, 
    "is_active": true, 
    "is_admin": false, 
    "last_login": null, 
    "last_name": "", 
    "mobile_number": "+224622422576"
}


```

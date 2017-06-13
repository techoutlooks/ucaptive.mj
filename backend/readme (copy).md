




## Angularjs 

### Setup & Bootstrap
sudo npm install --global bower gulp 
cd ~/apps/ucaptive.mj/frontend/ && npm install gulp
npm install

serve frontend site (browsersync)
gulp serve

### Doc
* https://github.com/angular-ui/ui-router/



## Eg. API Testing 

* Get auth token first,
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

* then, subsequent api queries

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

```
http POST localhost:8000/api/accounts/profile/recover_password/ 'one-token:745b200239ca9af0eaface18dba16f25b71e741003fedc0a778daaeab8d326db' email=ceduth@techoutlooks.com


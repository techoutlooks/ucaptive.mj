# ucaptive.mj

Captive enrolment portal (uCaptive, 2016-2017) was a project by the Guinea Ministry of Youth in partnership with UNICEF. 
It intends to generate a shared database to recruit and profile young people by tracking their connection to 
the City's WiFi Hotspot (32 access points across Conakry). On successful completion of a compulsory survey, 
users are granted free Internet access across the city, using the mobile number and password they registered 
as part of the questionnaire.

## Features

- Centralized storage and management of router configuration and user crendentials.
- Displays heartbeats of the 32 routers deployed across Conakry in the City map (status, traffic usage per location).
- Export user records to CSV, XLSX
  
## Stack

- Python/Django MVT
- AngularJS Single Page Application (SPA) displaying a Single-Sign-On widget
- [Google Maps API](https://developers.google.com/maps) integration
- [FreeRADIUS](https://freeradius.org/) v3 AAA integration
- [Mikrotik](https://mikrotik.com/) router integration

## Doc

* Django [Backend](./backend/readme.md#backend)
* AnguarJS [Frontend](./backend/readme.md#uiux-angularjs)


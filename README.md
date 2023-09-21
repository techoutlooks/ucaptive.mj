# ucaptive.mj

Captive enrolment portal (uCaptive, 2016-2017) was a project by the Guinea Ministry of Youth in partnership with UNICEF. 
It intends to generate a shared database to recruit and profile young people by tracking their connection to 
the City's WiFi Hotspot (32 access points across Conakry). On successful completion of a compulsory survey, 
users are granted free Internet access across the city, using the mobile number and password they registered 
as part of the questionnaire.

## Features

- Centralized storage and management of router configuration and user crendentials.
- Displays heartbeats of the 32 routers deployed across Conakry (status, traffic usage per location).
- Django admin views to export user records as CSV, XLSX
  
## Stack

- Python/Django MVT
- Single Page Application (SPA) displaying a Single-Sign-On widget
- [Google Maps API](https://developers.google.com/maps) integration
- [FreeRADIUS](https://freeradius.org/) v3 AAA integration
- [Mikrotik](https://mikrotik.com/) router integration

## Doc

* [Backend](./backend/readme.md#backend)
* [Frontend](./backend/readme.md#uiux-angularjs)


/*jshint esversion: 6 */

import angular from 'angular';

let djrosModule = angular.module('app.djros', ['ngCookies',]);

import djrosConstants from './config/djros.constants';
import djrosConfig from './config/djros.config';
import {MikrotikHotspotCookieService} from './services/cookie.service';
import {MikrotikHotspotUserService} from './services/mikrotik-user.service';
import CapsManService from './services/capsman.service';


djrosModule
    .constant('djrosConstants', djrosConstants)
    .config(djrosConfig)

    .service('HotspotCookie', MikrotikHotspotCookieService)
    .service('HotspotUser', MikrotikHotspotUserService)

    .service('CapsMan', CapsManService);


export default djrosModule;

/**
 * Created by ceduth on 3/12/17.
 */

import angular from 'angular';
import {BaseApi} from './base-api.service';
import {MikrotikHotspotUserService} from './mikrotik-user.service'

let servicesModule = angular.module('app.services', ['restangular']);

servicesModule
    .service('BaseApi', BaseApi)
    .service('MikrotikHotspotUser', MikrotikHotspotUserService);

export default servicesModule;
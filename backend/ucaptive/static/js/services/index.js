/**
 * Created by ceduth on 3/12/17.
 */

import angular from 'angular';
import {BaseApi} from './base-api.service';
import {MikrotikUserService} from './mikrotik-user.service'

let servicesModule = angular.module('app.services', ['restangular']);

servicesModule
    .service('BaseApi', BaseApi)
    .service('MikrotikUser', MikrotikUserService);

export default servicesModule;
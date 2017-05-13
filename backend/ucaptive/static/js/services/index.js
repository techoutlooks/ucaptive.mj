/**
 * Created by ceduth on 3/12/17.
 */

import angular from 'angular';
import {BaseApi} from './base-api.service';

let servicesModule = angular.module('app.services', ['restangular']);

servicesModule
    .service('BaseApi', BaseApi);

export default servicesModule;
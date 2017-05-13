import angular from 'angular';

let djrosModule = angular.module('app.djros', []);

import djrosConstants from './config/djros.constants';
import djrosConfig from './config/djros.config';
import {MikrotikHotspotUserService} from './services/mikrotik-user.service';
import CapsManService from './services/capsman.service';


djrosModule
    .constant('djrosConstants', djrosConstants)
    .config(djrosConfig)
    .service('MikrotikHotspotUser', MikrotikHotspotUserService)
    .service('CapsMan', CapsManService);

export default djrosModule;

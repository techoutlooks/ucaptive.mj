import angular from 'angular';

let djrosModule = angular.module('app.djros', []);

import djrosConstants from './config/djros.constants';
import djrosConfig from './config/djros.config';
import CapsManService from './services/capsman.service';

djrosModule
    .constant('djrosConstants', djrosConstants)
    .config(djrosConfig)
    .service('CapsMan', CapsManService);

export default djrosModule;

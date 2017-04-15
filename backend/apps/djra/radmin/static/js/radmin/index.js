import angular from 'angular';

let radminModule = angular.module('app.radmin', []);

import RadminConstants from './config/radmin.constants';
import radminConfig from './config/radmin.config';
import RadUserService from './services/raduser.service';
import RadminCtrl from './controllers/radmin.controller';

radminModule
    .constant('RadminConstants', RadminConstants)
    .config(radminConfig)
    .service('RadUser', RadUserService)
    .controller('RadminCtrl', RadminCtrl);

export default radminModule;

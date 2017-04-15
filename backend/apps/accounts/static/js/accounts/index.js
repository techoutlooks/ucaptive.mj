import angular from 'angular';

let authModule = angular.module('app.accounts', ['ui.bootstrap','ngCookies', 'restangular']);

import AuthConstants from './config/auth.constants';
import AuthConfig from './config/auth.config';
import ProfileConfig from './config/profile.config';
import JWT from './services/jwt.service';
import Auth from './services/auth.service';
import AuthCtrl from './controllers/auth.controller';
import AuthProvidersCtrl from './controllers/auth-providers.controller';
import ProfileCtrl from './controllers/profile.controller';
import ProfileService from './services/profile.service';

authModule
    .constant('AuthConstants', AuthConstants)
    // UI-Router config settings
    .config(AuthConfig)
    .config(ProfileConfig)

    // Servicess
    .service('JWT', JWT)
    .service('User', Auth)
    .service('Profile', ProfileService)

    // Controllers
    .controller('AuthCtrl', AuthCtrl)
    .controller('AuthProvidersCtrl', AuthProvidersCtrl)
    .controller('ProfileCtrl', ProfileCtrl);

export default authModule;
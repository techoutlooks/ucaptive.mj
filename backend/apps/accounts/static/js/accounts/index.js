import angular from 'angular';

let authModule = angular.module('app.accounts', ['ui.bootstrap','ngCookies', 'restangular']);


// TODO: move to one_auth
import AuthConstants from './config/auth.constants';
import AuthConfig from './config/auth.config';
import JWT from './services/jwt.service';
import Auth from './services/auth.service';
import ProfileConfig from './config/profile.config';
import AuthCtrl from './controllers/auth.controller';
import AuthProvidersCtrl from './controllers/auth-providers.controller';

// accounts
import accountsConstants from './config/accounts.constants';
import AccountsService from './services/accounts.service';
import ProfileCtrl from './controllers/profile.controller';
import ProfileService from './services/profile.service';

authModule
    .constant('AuthConstants', AuthConstants)
    .constant('accountsConstants', accountsConstants)
    // UI-Router config settings
    .config(AuthConfig)
    .config(ProfileConfig)

    // Services
    .service('JWT', JWT)
    .service('User', Auth)
    .service('Profile', ProfileService)
    .service('Accounts', AccountsService)

    // Controllers
    .controller('AuthCtrl', AuthCtrl)
    .controller('AuthProvidersCtrl', AuthProvidersCtrl)
    .controller('ProfileCtrl', ProfileCtrl);

export default authModule;
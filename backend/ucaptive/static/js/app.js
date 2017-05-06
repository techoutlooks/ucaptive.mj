/*
    npm install --save-dev angular angular-ui-router angular-sanitize \
        angular-bootstrap angular-cookies angular-ui-select underscore \
        restangular oclazyload

 */

import angular from 'angular';


/* Create and bootstrap application
 * Importing sub modules also registers them.
 * Import paths are relative to browserify's 'paths' option (Cf. gulpfile)
 * todo: make sure django-compressor (my CompressorMixin) recognizes those paths too.
 */
import 'layout';
import 'accounts';
import 'services';
import 'radmin';
import 'djros';

const requires = [
    'ui.router',
    'oc.lazyLoad',
    'ngCookies',
    'djng.forms',

    'app.services',
    'app.layout',
    'app.accounts',
    
    'app.radmin',
    'app.djros'
];


// Import our app config files
import AppConstants from './config/app.constants';
import AppConfig from './config/app.config';
import AppRun from './config/app.run';

window.app = angular.module('app', requires);
angular.module('app').constant('AppConstants', AppConstants);
angular.module('app').config(AppConfig);
angular.module('app').run(AppRun);

// angular.bootstrap(document, ['app'], {
//     strictDi: true
// });










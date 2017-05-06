function AuthConfig(AuthConstants, $stateProvider, $httpProvider) {
    'ngInject';

    $stateProvider

    .state('app.' + AuthConstants.USER_LOGIN, {
        url: '/login/',
        controller: 'AuthCtrl as $ctrl',
        templateUrl: '/accounts/signin/',
        title: 'Sign in',
        resolve: {
            auth: function(User) {
                return User.ensureAuthIs(false);
            }
        }
    })

    .state('app.' + AuthConstants.USER_LOGOUT, {
        url: '/logout/',
        template: '<div data-ng-init="$ctrl.logout()"></div>',
        controller: 'AuthCtrl as $ctrl',
        title: 'Log out',
        resolve: {
            auth: function(User) {
                return User.ensureAuthIs(false);
            }
        }

        //todo: resolve?
    })
                    
    .state('app.' + AuthConstants.USER_REGISTER, {
        url: '/register/',
        controller: 'AuthCtrl as $ctrl',
        templateUrl: '/accounts/register/',
        title: 'Sign up',
        // resolve: {
        //   deps: ['$ocLazyLoad', function($ocLazyLoad) {
        //     return $ocLazyLoad.load('/static/admin/js/jquery.min.js').then(function() {
        //       return $ocLazyLoad.load([{
        //         insertBefore: '#load_styles_before',
        //         files: ['/static/autocomplete_light/vendor/select2/dist/css/select2.css',
        //             '/static/autocomplete_light/select2.css'
        //         ]},{
        //         serie: true,
        //         files: [
        //             '/static/autocomplete_light/jquery.init.js',
        //             '/static/autocomplete_light/autocomplete.init.js',
        //             '/static/autocomplete_light/vendor/select2/dist/js/select2.full.js',
        //             '/static/autocomplete_light/select2.js']
        //         }
        //       ]);
        //     });
        //   }],
        //   auth: function(User) {
        //     return User.ensureAuthIs(false);
        //   }
        // }
        resolve: {
            auth: function(User) {
                return User.ensureAuthIs(false);
            }
        }
    })

};

export default AuthConfig;

/*jshint esversion: 6 */

function AuthConfig(AuthConstants, $stateProvider, $httpProvider) {
    'ngInject';

    $stateProvider

    .state('app.' + AuthConstants.USER_LOGIN, {
        url: '/login/?mac&ip&username&linkOrig&linkLogin',
        controller: 'AuthCtrl as $ctrl',
        templateUrl: '/accounts/login/',                                                // rendered by my NgUserLogin Django template view
        title: 'Sign in',
        params: {                                                                       // params as sent by Mikrotik login script
            mac: { value: '', squash: true },                                           // client's mac
            ip: { value: '', squash: true },                                            // client's ip
            username: { value: '', squash: true },                                      // client's username
            linkOrig: {                                                                 // url originally requested by user
                value: AuthConstants.redirectSuccessDefaultUrl,                         // before being proxy checked by Mikrotik
                squash: true
            },
            // linkLogin: {
            //     value: 'https://www.google.com/',
            //     squash: true
            // },
            error: {value: '', squash: true}
        },
        resolve: {                                                                      // disallow going to state ie., prevent login,
            auth: function(User, HotspotUser, $state) {                                 // if and only if user if already
                return User.ensureAuthIs(false).then((backendAuth) => {                 // is logged in to backend (backendAuth==false) AND
                    HotspotUser.ensureAuthIs(false).then((mikrotikAuth) => {            // simultaneously logged in to Mikrotik Hotstpot (mikrotikAuth==false)
                        console.log('Enforce login... BACKEND_NOT_LOGGED='+backendAuth + ' / MK_NOT_LOGGED='+mikrotikAuth);
                        if (!backendAuth && !mikrotikAuth) {
                            $state.go('app.home'); 
                        }
                    });
                });
            }
        }
    })

    .state('app.' + AuthConstants.USER_LOGOUT, {
        url: '/logout/',
        template: '<div data-ng-init="$ctrl.logout()"></div>',
        controller: 'AuthCtrl as $ctrl',
        title: 'Sign out',
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
    });

}

export default AuthConfig;

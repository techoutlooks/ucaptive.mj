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
        resolve: {
            auth: function(User) {
                return User.ensureAuthIs(false);
            }
        }
    })

};

export default AuthConfig;

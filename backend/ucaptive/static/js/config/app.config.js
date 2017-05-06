// import authInterceptor from '../../../../apps/accounts/static/js/accounts/auth.interceptor'
import authInterceptor from 'accounts/auth.interceptor';


function AppConfig($httpProvider, $stateProvider, $locationProvider, $urlRouterProvider,
                   $interpolateProvider, $ocLazyLoadProvider) {
    'ngInject';


    /* --
     Inject one-token to every request
     ------------------------------------------------------------*/
    $httpProvider.interceptors.push(authInterceptor);


    /* --
    Configure template processors. Eg.: '{{..}}' (Django) vs '[[..]]' (angularjs)
     ------------------------------------------------------------*/
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $ocLazyLoadProvider.config({
        debug: false,
        events: false
    });


    /* --
    If you don't want hashbang routing, uncomment this line.
    Our tutorial will be using hashbang routing though :)
    ------------------------------------------------------------*/
    // $locationProvider.html5Mode(true);
    $stateProvider
    .state('app', {
        abstract: true,
        template: '<app-header></app-header><div ui-view class="container"></div><app-footer></app-footer>',
        resolve: {
            auth: function (User) {
                User.verifyAuth();
            }
        }
    });
    $urlRouterProvider.otherwise('/home/');

}

export default AppConfig;

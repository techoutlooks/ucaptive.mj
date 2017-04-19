function LayoutConfig($stateProvider, $httpProvider) {
    'ngInject';

    $stateProvider

    /*--
     Partials (served by Django from the layout app)
     -------------------------------------------*/
    // .state('app.home', {
    //     url: '/home/',
    //     controller: 'CarouselCtrl as $ctrl',
    //     templateUrl: '/home/'
    // })
    .state('app.home', {
        url: '/home/',
        controller: 'LayoutCtrl as $ctrl',
        templateUrl: '/about/'
    })
    .state('app.maps', {
        url: '/maps/',
        templateUrl: '/maps/',
        resolve: {
            deps: ['$ocLazyLoad', function($ocLazyLoad) {
                return $ocLazyLoad.load('/static/js/map3.js');
            }]
        }
    })
    .state('app.news', {
        url: '/news/',
        templateUrl: '/news/'
    })
    .state('app.services', {
        url: '/services/',
        templateUrl: '/services/'
    })
    .state('app.projects', {
        url: '/projects/',
        templateUrl: '/projects/'
    })

    /*--
     External pages
     -----------------------------------*/
    .state('ureport', {
        url: 'https://guinea.ureport.in/',
        external: true
    })
    .state('facebook', {
        url: 'https://www.facebook.com/techoutlooks-sarl',
        external: true
    })
    .state('twitter', {
        url: 'https://www.twitter.com/techoutlooks',
        external: true
    })
    .state('github', {
        url: 'https://www.github.com/techoutlooks',
        external: true
    })
    .state('linkedin', {
        url: 'https://www.linkedin.com/company/techoutlooks-sarl',
        external: true
    })
};

export default LayoutConfig;

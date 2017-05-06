function djrosConfig(djrosConstants, $stateProvider, $httpProvider) {
    'ngInject';

    $stateProvider

    .state('app.djros', {
        abstract: true,
        url: '/djros',
        template: '<div ui-view></div>'
    });
};

export default djrosConfig;

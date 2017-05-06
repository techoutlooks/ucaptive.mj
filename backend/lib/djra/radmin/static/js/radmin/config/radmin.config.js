function radminConfig(RadminConstants, $stateProvider, $httpProvider) {
    'ngInject';

    $stateProvider

    .state('app.radmin', {
        abstract: true,
        url: '/radmin',
        template: '<div ui-view></div>'
    })

    // list views
    .state('app.radmin.home', {
        templateUrl: '/radmin/',
        title: 'Radmin Home'
    })
    .state('app.radmin.users', {
        url: '/users/',
        templateUrl: '/radmin/users/',
        title: 'Users'
    })
    .state('app.radmin.groups', {
        url: '/groups/',
        templateUrl: '/radmin/groups/',
        title: 'Create User'
    })
    .state('app.radmin.'+ RadminConstants.USER_CREATE, {
        url: '/users/create/',
        templateUrl: '/radmin/users/create/',
        title: 'Create User'
    })
    .state('app.radmin.' + RadminConstants.GROUP_CREATE, {
        url: '/groups/create/',
        templateUrl: '/radmin/groups/create/',
        title: 'Create Group'
    })

    // edit views
    .state('app.radmin.' + RadminConstants.USER_DETAIL, {
        url: '/user/@:username/',
        templateUrl: function($stateParams) {
            return'/radmin/user/+' + $stateParams.username + '/';
        },
        controller: 'RadminCtrl as $ctrl',
        title: 'Save User Detail',
        resolve: {
          raduser: function(RadUser, $state, $stateParams) {
            return RadUser.get('', $stateParams.username).then(
              (raduser) => raduser,
              (err) => $state.go('app.home')
            )
          }
        }
    })
    .state('app.radmin.' + RadminConstants.GROUP_DETAIL, {
        url: '/group/@:username/',
        templateUrl: '/radmin/group/@:groupname/',
        title: 'Group Detail'
    })
    .state('app.radmin.user_sessions', {
        url: '/radmin/user/@:username/sessions/',
        templateUrl: '/radmin/user/@:username/sessions/',
        title: 'User Sessions'
    })
};

export default radminConfig;

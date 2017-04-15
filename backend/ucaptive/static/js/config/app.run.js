/**
 * @name run
 * @desc Update xsrf $http headers to align with Django's defaults
 */
 function AppRun(JWT, AppConstants, $rootScope, $state, $log) {
  'ngInject';

    // $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    // $http.defaults.xsrfCookieName = 'csrftoken';

  /* --
    Change page title based on state
   ------------------------------------------------------------*/
    $rootScope.$on('$stateChangeSuccess', (event, toState) => {
        $rootScope.setPageTitle(toState.title);
    });

    // Helper method for setting the page's title
    $rootScope.setPageTitle = (title) => {
    $rootScope.pageTitle = '';
    if (title) {
        $rootScope.pageTitle += title;
        $rootScope.pageTitle += ' \u2014 ';
    }
    $rootScope.pageTitle += AppConstants.appName;
    };

    /*--
     On every state change verify that exists logged in user,
     else display modal.
     ------------------------------------------------------------
    $rootScope.Identity= JWT.get();
    $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
        let requireLogin = toState.data.requireLogin;

        if (requireLogin && typeof $rootScope.Identity === 'undefined') {
            event.preventDefault();

            ModalSvc().showModal({
                headerText: 'Login required',
                bodyText: 'Please pick your login service below:',
                bodyTemplateUrl: '/accounts/auth_providers/'
            },
                modalOptions).then(function (result) {
                $log.info('Modal success. Results:' +result);
                $state.go("user.signin");
            });
        }

        // doStats();
    });
     */
}



export default AppRun;

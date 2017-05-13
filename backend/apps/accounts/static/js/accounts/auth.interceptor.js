function authInterceptor(JWT, AppConstants, $window, $q) {
  'ngInject'

  return {
    // automatically attach Authorization header
    request: function(config) {
      if(config.url.indexOf(AppConstants.apiHost) === 0 && JWT.get()) {
        // config.headers.Authorization = 'one-token ' + JWT.get();
        config.headers['one-token'] = JWT.get();

      }

      return config;
    },

    // Handle 401
    responseError: function(rejection) {
      if (rejection.status === 401) {
        // clear any JWT token being stored
        JWT.destroy();
        // do a hard page refresh
        $window.location.reload();
      }
      return $q.reject(rejection);
    }

  }
}

export default authInterceptor;

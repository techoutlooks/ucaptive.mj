/*
  Catch http request originated in this angular app only !
 */

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

    responseError: function(rejection) {

      // Handle 401
      if (rejection.status === 401) {
        JWT.destroy();                    // clear any JWT token being stored
        $window.location.reload();        // do a hard page refresh
      }

      return $q.reject(rejection);
    }
  };
}

export default authInterceptor;

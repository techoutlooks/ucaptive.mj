/*jshint esversion: 6 */

const AppConstants = {

    // Network hosts
    // apiHost: 'http://ucaptivemj.cloud.com.gn',
    apiHost: 'http://ucaptivemj.cloud.com.gn:8000',
    mikrotikHost: 'http://mjrouter.cloud.com.gn',


    // Service routes
    profileUrl: 'accounts/api/v1/profile/',
    djraApiUrl: '/djra/api/v1/radusers/',

    //Redirects & Resources
    mikrotikRedirectUrl: '/mk-success',
    wifiIconBaseUrl: '/static/img/icon',

    // External urls
    ureportApiUrl: 'https://guinea.ureport.in/',
    twitterApiUrl: null,
    facebookApiUrl: null,

    // Constants. eg.: dict keys, etc...
    jwtKey: 'jwtToken',

    appName: 'uCaptive',
    identity: 'Identity'                            // currently logged in user
};

export default AppConstants;

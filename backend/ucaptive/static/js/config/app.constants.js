const AppConstants = {
    apiUrl: 'http://localhost:8000',
    // mikrotikUrl: 'https://mjrouter.cloud.com.gn',
    mikrotikUrl: 'https://192.168.0.2',

    twitterApiUrl: null,
    facebookApiUrl: null,

    profileUrl: 'accounts/api/v1/profile/',
    mikrotikRedirectUrl: '/mk-success',

    jwtKey: 'jwtToken',
    appName: 'uCaptive',
    identity: 'Identity'                        // currently logged in user
};

export default AppConstants;

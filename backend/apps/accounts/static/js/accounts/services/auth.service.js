import {BaseApi} from 'services/base-api.service';

// todo: firebase auth

class Auth extends BaseApi {
    constructor(JWT, Restangular, AppConstants, AuthConstants, $http, $state, $q, $window, $timeout) {
        'ngInject';
        super(Restangular);

        // protected
        this._JWT = JWT;
        this._AppConstants = AppConstants;
        this._AuthConstants = AuthConstants;
        this._$http = $http;
        this._$state = $state;
        this._$q = $q;
        this._$window = $window;
        this._$timeout = $timeout;

        // public
        this.apiUrl = this._AppConstants.apiUrl;
        this.api = this.setup(this.apiUrl);
        this.current = null;
    }


    ////////////////////


    attemptAuth(type, credentials) {
    /**
     * @name attemptAuth
     * @desc Try to authenticate user and update BaseApi with token globally.
     * @param {string} username The username entered by the user
     * @param {string} password The password entered by the user
     * @returns {Promise}. Token is returned in success handler.
     * @memberOf app.accounts.services.accounts
     */
        /*
            POST /accounts/api/v1/login Log in a user
            POST /accounts/api/v1/      Creates a user
         */
        let LOGIN_WAIT = 50;
        let self = this;
        let promise;

        // register, then auto login after 'wait' millisecs; or quit.
        // authenticate, save auth token; and return user id.
        // we wait a little bit for register to return before logging in.
        switch(type){

            case 'registerwithfirebase':

            case 'loginwithfirebase':
                break;

            case 'register':
                promise = this.register(credentials).then(
                    (res) => {
                        self._$timeout( () => {
                            promise = this.login(credentials);
                        }, LOGIN_WAIT);
                    }
                );
                break;

            case 'login':
                promise = this.login(credentials);
                break;

            default:
                promise = this._$q.reject('Method ' + type + ' is not implemented/allowed.');
        }

        return promise;
    }


    register(credentials) {
        return this.api.all(this._AuthConstants.authApiUrl ).post(credentials).then(
            (res) => {
                this.current = res;
                return res;
        })
    }

    login(credentials) {
        return this.api.all(this._AuthConstants.authApiUrl + 'login/').post(credentials).then(
            (res) => {
                this._JWT.save(res.token);
                this.getIdentity().then(
                    (res) => {
                        this.current = res;
                        return res;
                    },
                );
            });
    };

    update(fields) {
        return this._$http({
            url: this._AppConstants.apiUrl + '/user',
            method: 'PUT',
            data: {user: fields}
        }).then(
            (res) => {
                this.current = res.data.user;
                return res.data.user;
            }
        )
    }

    logout() {
    /**
     * @name logout
     * @desc Log out the current user
     * @returns {None}
     * @memberOf app.accounts.services.accounts
     */
        this.current = null;
        this._JWT.destroy();
        this._$state.go(this._$state.$current, null, {reload: true});
    }

    verifyAuth() {
        let deferred = this._$q.defer();

        // check for JWT token
        if (!this._JWT.get()) {
            deferred.resolve(false);
            return deferred.promise;
        }

        if (this.current) {
            deferred.resolve(true);

        } else {
            this.getIdentity().then((res) => {
                if(res) {
                    this.current = res;
                    deferred.resolve(true);
                } else {
                    this._JWT.destroy();
                    deferred.resolve(false);
                }
            });
        }
        return deferred.promise;
    }

    ensureAuthIs(bool) {
        let deferred = this._$q.defer();

        this.verifyAuth().then((authValid) => {
            if (authValid !== bool) {
                this._$state.go('app.home')
                deferred.resolve(false);
            } else {
                deferred.resolve(true);
            }

        });

        return deferred.promise;
    }

    getIdentity() {
    /**
     * @name getIdentity
     * @desc Request full user identity. Assumes request headers set with valid token.
     * @returns {promise}
     * @memberOf app.accounts.services.Auth
     */
        let deferred = this._$q.defer();
        this.api.one(this._AuthConstants.authApiUrl + 'profile/').get().then(
            (res) => {
                deferred.resolve(res);
            },
            (err) => {
                deferred.resolve(false);
            }
        );
        return deferred.promise;
    }

}

export default Auth;

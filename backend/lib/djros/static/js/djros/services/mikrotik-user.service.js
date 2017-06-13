/* jshint esversion: 6 */

class MikrotikHotspotUserService {
    constructor(AppConstants, djrosConstants, User, HotspotCookie, $http, $q, $httpParamSerializerJQLike, $cookies) {
    'ngInject;'

        this._User = User;
        this._AppConstants = AppConstants;
        this._djrosConstants = djrosConstants;
        this._$http = $http;
        this._$q = $q;
        this._$httpParamSerializerJQLike = $httpParamSerializerJQLike;
        this._HotspotCookie = HotspotCookie;
    }

    login(credentials, redirectUrl){
        return this._$http({
            url: this._AppConstants.mikrotikHost + '/login',
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            data: this._$httpParamSerializerJQLike(Object.assign({}, credentials, {dst: redirectUrl, popup:'true'}))
     }).then(
        (res) => {
            let authCookie = res.config.headers.hasOwnProperty('Set-Cookie');
            if (authCookie) {
                this._HotspotCookie.save(this._HotspotCookie.parseCookie(this._HotspotCookie.authCookieName, authCookie));
                return res;
            } else return this._$q.reject("Error attempting to login via Mk Hotspot API ! Details: "+JSON.stringify(res));
                    },
        (err) => err
    )}


    verifyAuth() {
    /*
     *   if login required by Hotspot, ie. we're not logged in anymore,
     *   we need to auto login again.
     */
        let deferred = this._$q.defer();
            this._$http({
                url: this._AppConstants.mikrotikHost + '/status',
                method: 'GET',
                headers: {
                  'LoginID': this._HotspotCookie.get()
                }
            }).then(

                (res) => {

                    switch (res.status.toString()){
                        case '200':
                            deferred.resolve(true);
                            break;
                        default:
                            deferred.resolve(false);
                    }
                },

                (err) => {
                    this._HotspotCookie.destroy();
                    deferred.resolve(false);
                }
            );
        return deferred.promise;
    }

    ensureAuthIs(bool, toStateIfFailed=null) {
        let deferred = this._$q.defer();

        this.verifyAuth().then((authValid) => {
            if (authValid !== bool) {
                if (toStateIfFailed) { this._$state.go(toStateIfFailed);}
                deferred.resolve(false);
            } else {
                deferred.resolve(true);
            }

        });

        return deferred.promise;
    }
}

export {MikrotikHotspotUserService};


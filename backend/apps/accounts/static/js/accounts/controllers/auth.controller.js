/**
 *
 * Created by ceduth on 3/2/17.
 * @namespace app.accounts
 * @desc Controller for authentication (login, logout)
 */

/*jshint esversion: 6 */

// import AuthApi from 'accounts';

class AuthCtrl {
    constructor(User, RadUser, HotspotUser, AuthConstants, RadminConstants,
                $http, $state, $scope, $window, $timeout, $stateParams, djangoForm) {
        'ngInject';

        var vm = this;

        this._User = User;
        this._RadUser = RadUser;
        this._HotspotUser = HotspotUser;
        this._AuthConstants = AuthConstants;
        this._RadminConstants = RadminConstants;
        this._$http = $http;

        this._$state = $state;
        this._$scope = $scope;
        this._$window = $window;
        this._$timeout = $timeout;
        this._$stateParams = $stateParams;

        // FIXME: Do something with me (djangoForm service at django-angular)
        this._djangoForm = djangoForm;

        this.title = $state.current.title;
        this.authType = $state.current.name.replace('app.', '');

        // load country choices
        var Guinea = 1;
        this.getRegions(Guinea).then((regions) => {
            this.regions = regions;
        });

    }

    regionChanged() {
        this.getCities(this.profile.region).then(
            (cities) => {
                this.citys = cities;
            });
    }

    /* TODO: create DjangoAutoCompleteLightService in sub module app.layout.dal
     with getCountries(), getRegions(), getCities()
     get GET url dynamically from <select.../> attrs,
     eg. data-autocomplete-light-url="/en/cities/region-autocomplete/"

     */
    getCountries() {
        return this._$http.get('/cities/country-autocomplete/').then((res) => res.data.results);
    }

    getRegions(country) {
        return this._$http.get('/cities/region-autocomplete/', {
            params: {
                forward: {country: country}
            }
        }).then((res) => res.data.results);
    }

    getCities(region) {
        return this._$http.get('/cities/city-autocomplete/', {
            params: {
                forward: {region: region}
            }
        }).then((res) => res.data.results);
    }


    /* Create and/or log in a user vs. both Django & Mikrotik.

     * User creation: First create Django user, if succeeds, create Radius account.
     * Login: Anyway, Auth service (attemptAuth) will automatically login new/existing user vs. Django.
     * Finally, the new or existing user is logged in to Mikrotik; then redirected to the originally requested page.
     */
    submitForm(form_name) {
        this.isSubmitting = true;

        // gather all user data form
        var userData = this.credentials || {};
        userData['profile'] = this.profile;

        // create and/or login user
        this._User.attemptAuth(this.authType, userData).then(
            (res) => {
                switch (this.authType) {
                    case this._AuthConstants.USER_REGISTER:
                        this._RadUser.doCreateUpdateDestroyUser(this._RadminConstants.USER_CREATE, this.credentials).then(
                            (res) => submitHotstpotForm(this._$stateParams.linkOrig),
                            (err) => this.err(err)
                        );  break;

                    case this._AuthConstants.USER_LOGIN:
                        submitHotstpotForm(this._$stateParams.linkOrig); break;

                    default:
                        this.errors = {NotImplementedError: [this.authType + 'is not implemented']};
                }
            },
            // User service promise-chains errors to the next (below) handler
            // restframework.serializers.Serializer.errors matches this properly.
            // eg. ngRepeat expects to find collection in 'this.errors', not str !!
            (err) => {
                this.err(err);
            }
        );


        var submitHotstpotForm = (redirectUrl) => {
        /*  Call Mikrotik Hostpot HTTP Auth API.
         *  Only login for now; eg. GET /login?username=username&password=password HTTP/1.0
         *  No support for Hotspot account creation through the Web UI.
         */
            this._HotspotUser.login(this.credentials, redirectUrl).then(
                (res) => {
                    // normally not needed, assumned done already in _HotspotUser.login()
                    this._$window.location.assign(redirectUrl);
                },
                (err) => {
                    this.err(err);
                }
            );
        };
    }

    logout() {
        this._User.logout();
        // this._$state.go('app.home');
    };

    err(msg) {
        this.isSubmitting = false;
        if (msg.data) {
            this.errors = msg.data.exception;
            Object.assign(this.errors, {errors: msg.data.errors});
        } else {
            console.log('authCtrl::err()  msg='+msg);
            this.errors = msg;
        }
    }
}

export default AuthCtrl;



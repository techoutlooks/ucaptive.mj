/**
 * Created by ceduth on 3/2/17.
 * @namespace app.accounts
 * @desc Controller for authentication (login, logout)
 */

// import AuthApi from 'accounts';

class AuthCtrl {
    constructor(User, RadUser, MikrotikHotspotUser, AuthConstants, RadminConstants,
                $http, $state, $scope, $window, $timeout, djangoForm) {
        'ngInject';

        var vm = this;

        this._User = User;
        this._RadUser = RadUser;
        this._MikrotikHotspotUser = MikrotikHotspotUser;
        this._AuthConstants = AuthConstants;
        this._RadminConstants = RadminConstants;
        this._$http = $http;

        this._$state = $state;
        this._$scope = $scope;
        this._$window = $window;
        this._$timeout = $timeout;
        this._djangoForm = djangoForm;

        this.title = $state.current.title;
        this.authType = $state.current.name.replace('app.', '');

        // load country choices
        var Guinea = 1;
        this.getRegions(Guinea).then((regions) => {
            this.regions = regions;
        });

    }

    regionChanged(){
        this.getCities(this.profile.region).then(
            (cities) => {
                this.citys = cities;
            });
    }

    // Get countries, regions, cities from django-autocomplete-light
    getCountries() {
        return this._$http.get('/cities/country-autocomplete/').then((res) => res.data.results );
    }
    getRegions(country) {
        return this._$http.get('/cities/region-autocomplete/', {params: {
            forward: {country: country}
        }}).then((res) => res.data.results );
    }
    getCities(region) {
        return this._$http.get('/cities/city-autocomplete/', {params: {
            forward: {region: region}
        }}).then((res) => res.data.results);
    }



    /* Create and/or log in a user vs. both Django & Mikrotik.

     * User creation: First create Django user, if succeeds, create Radius account.
     * Login: Anyway, Auth service (attemptAuth) will automatically login new/existing user vs. Django.
     * Finally, the new or existing user is logged in to Mikrotik; then redirected to the home page.
     */
    submitForm(form_name) {
        this.isSubmitting = true;

        // gather all user data form
        var userData = this.credentials || {};
        userData['profile'] = this.profile;
        console.log(JSON.stringify(userData));

        // create and/or login user
        this._User.attemptAuth(this.authType, userData).then(
            (res) => {
                switch(this.authType) {
                    case this._AuthConstants.USER_REGISTER:
                        this._RadUser.doCreateUpdateDestroy(this._RadminConstants.USER_CREATE, this.credentials).then(
                            (res) => {
                                this._MikrotikHotspotUser.login(this.authType, this.credentials).then(
                                    (res) => { this._$state.go('app.home') },
                                    (err) => { this.err(err) }
                                )
                            },
                            (err) => this.err(err)
                        );
                        break;

                    case this._AuthConstants.USER_LOGIN:
                        this._MikrotikHotspotUser.login(this.credentials).then(
                            (res) => { this._$state.go('app.home') },
                            (err) => { this.err(err) }
                        )
                        break;

                    default:
                        this.errors = {NotImplementedError: [this.authType + 'is not implemented']}

                }
            },
            // User service promise-chains errors to the next (below) handler
            // restframework.serializers.Serializer.errors matches this properly.
            // eg. ngRepeat expects to find collection in 'this.errors', not str !!
            (err) => {
                this.err(err);
            }
        )
    }

    logout() {
        this._User.logout();
        // this._$state.go('app.home');
    };

    err(msg){
        console.log('Auth errors. msg: ' + JSON.stringify(msg));
        this.isSubmitting = false;
        if (msg.data) {
            this.errors = msg.data.exception;
            Object.assign(this.errors, {errors: msg.data.errors});
        } else {
            this.errors = msg;
        }
    }
}

export default AuthCtrl;



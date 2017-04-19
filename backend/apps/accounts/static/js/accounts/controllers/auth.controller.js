/**
 * Created by ceduth on 3/2/17.
 * @namespace app.accounts
 * @desc Controller for authentication (login, logout)
 */

// import AuthApi from 'accounts';

class AuthCtrl {
    constructor(User, RadUser, MikrotikHotspotUser, AuthConstants, RadminConstants,
                $state, $rootScope, $window, $timeout, djangoForm) {
        'ngInject';

        this._User = User;
        this._RadUser = RadUser;
        this._MikrotikHotspotUser = MikrotikHotspotUser;
        this._AuthConstants = AuthConstants;
        this._RadminConstants = RadminConstants;

        this._$state = $state;
        this._$rootScope = $rootScope;
        this._$window = $window;
        this._$timeout = $timeout;
        this._djangoForm = djangoForm;

        this.title = $state.current.title;
        this.authType = $state.current.name.replace('app.', '');

    }

    submitForm(form_name) {
        this.isSubmitting = true;

        this._User.attemptAuth(this.authType, this.credentials).then(
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



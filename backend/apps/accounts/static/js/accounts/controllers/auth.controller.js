/**
 * Created by ceduth on 3/2/17.
 * @namespace app.accounts
 * @desc Controller for authentication (login, logout)
 */

// import AuthApi from 'accounts';

class AuthCtrl {
    constructor(User, RadUser, MikrotikUser, AuthConstants, $state, $rootScope, $window, $timeout, djangoForm) {
        'ngInject';

        this._User = User;
        this._RadUser = RadUser;
        this._MikrotikUser = MikrotikUser;
        this._AuthConstants = AuthConstants;

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
                        this._RadUser.doCreateUpdateDestroy(this._AuthConstants.USER_CREATE, this.credentials).then(
                            (res) => {
                                this._MikrotikUser.login(this.authType, this.credentials).then(
                                    (res) => { this._$state.go('app.home') },
                                    (err) => { this.err(err) }
                                )
                            },
                            (err) => this.err(err)
                        );
                        break;

                    case this._AuthConstants.USER_LOGIN:
                        this._MikrotikUser.login(this.authType, this.credentials).then(
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
        this.isSubmitting = false;  
        this.errors = msg.data.exception;
        console.log('Auth errors: ' + JSON.stringify(msg.data));
        Object.assign(this.errors, {errors: msg.data.errors});
    }
}

export default AuthCtrl;



/**
 * AuthProvidersCtrl
 * @namespace app.accounts.controllers.auth-providers.controller
 */


class AuthProvidersCtrl {
/**
 * @name auth
 * @desc Displays the list of auth providers in a ui-bootstrap.
 * @return: {Promise}
 */

    constructor($scope, $log) {
        'ngInject';

        this.authProviders = [
            {id: 1, name: 'Login'},
            {id: 2, name: 'Facebook'},
            {id: 3, name: 'Twitter'},
            {id: 4, name: 'Google+'},
            {id: 5, name: 'Instagram'},
        ];
        this.selected = {value: this.authProviders[0]};
    }
}

export default AuthProvidersCtrl;
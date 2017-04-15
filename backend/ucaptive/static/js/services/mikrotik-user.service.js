
class MikrotikUserService {
    constructor(User, AppConstants, $http) {
    'ngInject;'

    this._User = User;
    this._AppConstants = AppConstants;
    this._$http = $http;
    }

    login(credentials){
        return this._$http({
            url: this._AppConstants.mikrotikUrl + '/login',
            method: 'POST',
            data: {
                username: credentials.username,
                password: credentials.password,
                dst: this._AppConstants.mikrotikRedirectUrl,
            }
        }).then(
            (res) => {
                console.log('Mikrotik login success '+JSON.stringify(res.data));
                return res.data;
            }
        )
    }
}

export {MikrotikUserService}


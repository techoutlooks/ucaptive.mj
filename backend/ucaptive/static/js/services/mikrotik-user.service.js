
class MikrotikHotspotUserService {
    constructor(User, AppConstants, $http, $httpParamSerializerJQLike) {
    'ngInject;'

    this._User = User;
    this._AppConstants = AppConstants;
    this._$http = $http;
    this._$httpParamSerializerJQLike = $httpParamSerializerJQLike;
    }

    login(credentials){
        return this._$http({
            url: this._AppConstants.mikrotikUrl + '/login',
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            data: this._$httpParamSerializerJQLike(credentials)
        }).then(
            (res) => {
                console.log('MikrotikHotspotUserService:: login success '+JSON.stringify(res.data));
                return res.data;
            },
            (data, status, headers, config) => {
                console.log('MikrotikHotspotUserService:: Hotstpot login success '+JSON.stringify(status));
                return "Login to Mikrotik hotspot failed with status " + status;
            }
        )
    }
}

export {MikrotikHotspotUserService}


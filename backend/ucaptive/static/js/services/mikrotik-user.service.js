
class MikrotikUserService {
    constructor(User, AppConstants, $http) {
    'ngInject;'

    this._User = User;
    this._AppConstants = AppConstants;
    this._$http = $http;
    }

    login(credentials){
        return this._$http({
            method: 'POST',
            url: this._AppConstants.mikrotikUrl + '/login',
	    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
	    transformRequest: function(obj) {
		var str = [];
		for(var p in obj)
		str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
		return str.join("&");
	    },
	    data: {
                username: credentials.username,
                password: credentials.password,
                dst: this._AppConstants.mikrotikRedirectUrl
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


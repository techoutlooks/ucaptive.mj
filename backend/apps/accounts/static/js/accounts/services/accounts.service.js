
import {BaseApi} from 'services/base-api.service';


export default class AccountsService extends BaseApi {
    constructor(JWT, Restangular, AppConstants, accountsConstants,
                $http) {
        'ngInject;'
        super(Restangular);

        // protected
        this._JWT = JWT;
        this._AppConstants = AppConstants;
        this._accountsConstants = accountsConstants;
        this._$http = $http;
    }


    // GET /reporter/api/v1/                    --> all ureporters.UReporter
    // GET /reporter/api/v1/{mobile_number}/    --> single UReporter
    get(username) {
        var route = username || ''; var trailingSlash = username? '/': '';

        return this._$http({
            url: this._AppConstants.apiUrl + this._accountsConstants.apiUrl + route + trailingSlash,
            headers: { "Api-Key": this._accountsConstants.apiKey},
            method: 'GET'
        }).then((res) => res.data, (err) => []);
    }
}


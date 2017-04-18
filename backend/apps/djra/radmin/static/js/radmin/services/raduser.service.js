export default class RadUserService {
  constructor (AppConstants, RadminConstants, $http) {
    'ngInject';

    this._AppConstants = AppConstants;
    this._RadminConstants = RadminConstants;
    this._$http = $http;

  }

  // get single raduser or all radusers
  get(type, username) {
    let route = (type === 'radusers')? '': '?username='+username;
    console.log("route =="+ this._AppConstants.apiUrl + '/djra/api/v1/radusers/' + route)
    return this._$http({
      url: this._AppConstants.apiUrl + '/djra/api/v1/radusers/' + route,
      method: 'GET'
    }).then(
        (res) => {
            console.log('getId success '+JSON.stringify(res.data));
            return res.data;
        });
  }


    //  Create, Update, Destroy a single user.
    //  PUT, DELETE, UPDATE  /djra/api/v1/radusers/{username}/$
    doCreateUpdateDestroy(method, data) {
        let route = '';

        switch (method){
            case this._RadminConstants.USER_CREATE:
                method = 'POST';
                break;
            case this._RadminConstants.USER_DELETE:
                method = 'DELETE';
                break;
            case 'update_user':
                method = 'PUT'; route = data.username + '/';
                break;
        }


        return this._$http({
            url: this._AppConstants.apiUrl + '/djra/api/v1/radusers/' + route,
            method: method,
            data: data
        }).then(
            (res) => {
                console.log('getId success '+JSON.stringify(res.data));
                return res.data;
            }
        )
    }


}

/*jshint esversion: 6 */

export default class CapsManService {
  constructor (AppConstants, djrosConstants, $http) {
    'ngInject';

    this._AppConstants = AppConstants;
    this._djrosConstants = djrosConstants;
    this._$http = $http;

  }

  // get single cap or all caps at all orgs
  getCaps(macAddress) {
    let route =  macAddress || '';
    let endsWithSlash = macAddress? '/':'';

    return this._$http({
      url: this._AppConstants.apiHost + '/' + this._djrosConstants.djrosCapApiUrl + route + endsWithSlash,
      method: 'GET'
    }).then(
        (res) => res.data,
        (err) => []
        );
  }

  // get single radio or all radios connected on all caps
  // radio interface = djros.Radio.{interface, mac_address}; defaults to 'interface'
  getRadios(radioInterface) {
    let route =  radioInterface || '';
    let endsWithSlash = radioInterface? '/':'';

    return this._$http({
      url: this._AppConstants.apiHost + '/' + this._djrosConstants.djrosRadioApiUrl + route + endsWithSlash,
      method: 'GET'
    }).then(
        (res) => res.data,
        (err) => []
        );
  }
}
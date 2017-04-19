/**
 * Created by ceduth on 3/2/17.
 * layout
 * @namespace app.layout.controllers
 */


class LayoutCtrl {
    constructor(AppConstants, LayoutConstants, $rootScope, $scope, $window, $state,
                uiGmapGoogleMapApi, gmarkers) {
        'ngInject';

        this._$rootScope = $rootScope;
        this._$scope = $scope;
        this._$window = $window;
        this._AppConstants = AppConstants;

        // public members
        this.title = $state.current.title;
        this.authType = $state.current.name.replace('app.', '');
        this.test = this._$rootScope.header; //'test string';
        this.Identity = this._$window.localStorage[this._AppConstants.identity];

        this.map = {center: {latitude: 9.6230792, longitude: -13.6318499}, zoom: 12};
        this.options = { scrollwheel: false };
        this.markers = [];


        // load gmap markers asynchronously
        uiGmapGoogleMapApi.then(
            (maps) => gmarkers.getAll().then((res) => {
                this.markers = this.updateWiFiStatus(gmarkers.markers, LayoutConstants.WIFI);
            })
        );
    }

    updateWiFiStatus(markers, status) {
        for(let key in markers) {
            let url = this._AppConstants.wifiIconBaseUrl + '/wifi-' + status + '.png';
            if (markers.hasOwnProperty(key)) markers[key]["options"]["icon"] = url;
            else console.log("Failed loading maps icon from " + url)
        }
        return markers;
    }

}

export default  LayoutCtrl;




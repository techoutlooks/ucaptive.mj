/**
 * Created by ceduth on 3/2/17.
 * layout
 * @namespace app.layout.controllers
 */


class LayoutCtrl {
    constructor(AppConstants, LayoutConstants, djrosConstants,
                $rootScope, $scope, $window, $state, $q, $interval,
                uiGmapGoogleMapApi,
                Accounts, CapsMan, gmarkers) {
        'ngInject';

        // services
        var originalSetInterval = $interval;
        this._$interval = function(fn, delay, runImmediately) {
            if(runImmediately) fn();
            originalSetInterval(fn, delay);
        };
        this._$rootScope = $rootScope;
        this._$scope = $scope;
        this._$window = $window;
        this._$q = $q;
        this._LayoutConstants = LayoutConstants;
        this._djrosConstants = djrosConstants;
        this._AppConstants = AppConstants;
        this._CapsMan = CapsMan;
        this._Accounts = Accounts;


        // public members
        this.title = $state.current.title;
        this.authType = $state.current.name.replace('app.', '');
        this.test = this._$rootScope.header; //'test string';
        this.Identity = this._$window.localStorage[this._AppConstants.identity];

        // map
        this.map = {center: {latitude: 9.6230792, longitude: -13.6318499}, zoom: 12};
        this.options = { scrollwheel: false };
        this.markers = [];

        // global stats figures
        this.countDeployedCaps = 0;
        this.countDeployedRadios = 0;
        this.countUReporters = 0;


        // load gmap markers asynchronously,
        // every MARKER_REFRESH_TIMEOUT seconds,
        // and set their wifi status: disabled, bound, running, inactive.
        uiGmapGoogleMapApi.then(
            (maps) => gmarkers.getAll().then(() => {
                this._$interval( () => {
                    this.setWiFiStatus(gmarkers.markers).then(
                        (updatedMarkers) => {
                            this.markers = updatedMarkers;
                        }
                    );
                }, this._djrosConstants.MARKER_REFRESH_TIMEOUT, true
                );
            })
        );

        // publish stats markers asynchronously,
        // every MARKER_REFRESH_TIMEOUT seconds,
        this._$interval( ()=> {
                this.getCapsCount().then((count) => this.countDeployedCaps = count);
                this.getRadiosCount().then((count) => this.countDeployedRadios = count);
                this.getUReportersCount().then((count) => this.countUReporters = count);
            }, this._djrosConstants.STATS_REFRESH_TIMOUT, true
        );
    }

    // get num ureporters,
    // Cf. Django's app.accounts.UReporters
    getUReportersCount() {
        return this._Accounts.get().then((ureporters) => ureporters.length);
    }

    // get total num radios on all caps,
    // radio = currently connected capsman client (pc, smartphone, etc.)
    getRadiosCount() {
        return this._CapsMan.getRadios().then((radios) => radios.length);
    }

    // get num hotspots,
    // ie. caps
    getCapsCount() {
        return this._CapsMan.getCaps().then((caps) => caps.length);
    }

    // Update all given markers asynchronously
    // returns promise
    setWiFiStatus(markers) {
        let deferred = this._$q.defer();
        let markersComplete = 0;

        for(let key in markers) {
            if (markers.hasOwnProperty(key)) {
                this.setCapStatus(markers[key]).then(
                    (updatedMarker) => {
                        markers[key] = updatedMarker;
                        markersComplete++;
                        if (markersComplete === markers.length) deferred.resolve(markers);
                    }
                );
            }
        }
        return deferred.promise;
    }

    // update single marker asynchronously with Cap status
    // returns promise, and updated marker as args to success handler.
    setCapStatus(marker) {
        return this._CapsMan.getCaps(marker.id).then(
            (status) => {
                /* eg. status returned from CapsMan service (Cf my.DjROS)

                 [{
                 "bound": true,
                 "current_channel": "2412/20-Ce/gn(30dBm)",
                 "disabled": false,
                 "inactive": false,
                 "name": "CAP MJE M_MATOTO SXT",
                 "radio_mac": "D4:CA:6D:B7:A1:D7",
                 "running": true
                 }, ...]
                 */

                // set icon
                var iconId = status.running ? this._LayoutConstants.WIFI_UP : this._LayoutConstants.WIFI_DOWN;
                var iconUrl = this._AppConstants.wifiIconBaseUrl + '/wifi-' + iconId + '.png';
                marker.options.icon = iconUrl;

                return marker;
            }
        );
    }

}

export default LayoutCtrl;




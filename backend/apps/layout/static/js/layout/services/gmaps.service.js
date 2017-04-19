
/**
* MapMarkersService: Service that returns Google Maps markers from json file.
* @namespace cms.modal.services
*/

export default class MapMarkersService {
    constructor($q, $http) {
        'ngInject';

        var output = {};
        var markerUrl = '/static/gmaps/markers.json';
        output.getAll = function () {
            output.markers = [];
            return $http.get(markerUrl).then(
                (res) => { output.markers = res.data; return res; },
                (err) => { console.log("Failed loading gmaps markers from " + markerUrl + "Error: " + err); return err; }
            );
        };
        return output;

    }
}

/**
 * Created by ceduth on 3/12/17.
 *
 * BaseApi (Prototype)
 * @namespace app.services
 */


class BaseApi {

    constructor(Restangular) {
        'ngInject;'

        this._$restangular = Restangular;
        this.apiUrl = "http://localhost:8000/undefined/url";
    }

    setup(apiUrl) {
    /**
     * @name setup
     * @desc Factory that pre-configures a restangular service.
     * @param {baseUrl} Base url of api server
     * @returns {Restangular}. Pre-configured restangular service (normally $injected).
     * @memberOf app.services
     */
        this.apiUrl = apiUrl;
        return this._$restangular.withConfig(
            (config) => {
                config.setBaseUrl(apiUrl);
                config.setDefaultHeaders({
                    'X-Requested-With': 'XMLHttpRequest',
                    // 'one-token': this._$cookies.getObject('one-token')
            });
        })


    }

}

export {BaseApi};

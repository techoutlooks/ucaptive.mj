/* jshint esversion: 6 */

class MikrotikHotspotCookieService {
    constructor(djrosConstants, $window) {
        'ngInject';

        this._djrosConstants = djrosConstants;
        this._$window = $window;
    }

    save(token) {
        this._$window.localStorage[this._djrosConstants.authCookieName] = token;
    }

    get() {
        return this._$window.localStorage[this._djrosConstants.authCookieName];
    }

    destroy() {
        this._$window.localStorage.removeItem(this._djrosConstants.authCookieName);
    }

    parseCookie(name, cookie) {
        var cookiestring=RegExp(""+name+"[^;]+").exec(cookie);                                    // Get name followed by anything except a semicolon
        return unescape(!!cookiestring ? cookiestring.toString().replace(/^[^=]+./,"") : "");     // Return everything after the equal sign, or an empty string if the cookie name not found
    }


}


export {MikrotikHotspotCookieService};

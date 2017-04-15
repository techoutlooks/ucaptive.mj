/**
 * Created by ceduth on 3/2/17.
 * layout
 * @namespace app.layout.controllers
 */



class LayoutCtrl {
    constructor(AppConstants, $rootScope, $window, $state) {
        'ngInject';

        this._$rootScope = $rootScope;
        this._$window = $window;
        this._AppConstants = AppConstants;

        this.title = $state.current.title;
        this.authType = $state.current.name.replace('app.', '');
        this.test = this._$rootScope.header; //'test string';
        this.Identity = this._$window.localStorage[this._AppConstants.identity];
        console.log("Identity=="+ this.Identity);

    }

}

export default  LayoutCtrl;




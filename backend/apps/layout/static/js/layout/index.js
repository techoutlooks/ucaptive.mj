import angular from 'angular';

let layoutModule = angular.module('app.layout', ['ngAnimate', 'ngSanitize', 'ui.bootstrap', 'uiGmapgoogle-maps']);

import LayoutConstants from './config/layout.constants';
import LayoutConfig from './config/layout.config';
import ModalSvc from './services/modal.service';
import MapMarkersService from './services/gmaps.service'
import LayoutCtrl from './controllers/layout.controller';
import CarouselCtrl from './controllers/carousel.controller';
import ShowAuthed from './components/show-authed.directive';
import AppHeader from './components/header.component';
import AppFooter from './components/footer.component';
import ListErrors from './components/list-errors.component';

layoutModule

    // Constants
    .constant('LayoutConstants', LayoutConstants)

    // Config
    .config(function(uiGmapGoogleMapApiProvider) {
        uiGmapGoogleMapApiProvider.configure({
            key: 'AIzaSyDD85eI1-uiNlsFDnsdh3t7dP0sNjTW2c4',
            v: '3.20', //defaults to latest 3.X anyhow
            libraries: 'weather,geometry,visualization'
        });
    })
    .config(LayoutConfig)

    // Services
    .service('ModalSvc', ModalSvc)
    .service('gmarkers', MapMarkersService)

    // Controllers
    .controller('LayoutCtrl', LayoutCtrl)
    .controller('CarouselCtrl', CarouselCtrl)

    // Components
    .directive('showAuthed', ShowAuthed)
    .component('appHeader', AppHeader)
    .component('appFooter', AppFooter)
    .component('listErrors', ListErrors);

export default layoutModule;

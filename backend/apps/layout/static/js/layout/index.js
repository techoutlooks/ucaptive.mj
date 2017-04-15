import angular from 'angular';

let layoutModule = angular.module('app.layout', ['ngAnimate', 'ngSanitize', 'ui.bootstrap']);

import LayoutConfig from './layout.config';
import ModalSvc from './services/modal.service';
import LayoutCtrl from './controllers/layout.controller';
import CarouselCtrl from './controllers/carousel.controller';
import ShowAuthed from './components/show-authed.directive';
import AppHeader from './components/header.component';
import AppFooter from './components/footer.component';
import ListErrors from './components/list-errors.component';

layoutModule

    // Config
    .config(LayoutConfig)

    // Services
    .service('ModalSvc', ModalSvc)

    // Controllers
    .controller('LayoutCtrl', LayoutCtrl)
    .controller('CarouselCtrl', CarouselCtrl)

    // Components
    .directive('showAuthed', ShowAuthed)
    .component('appHeader', AppHeader)
    .component('appFooter', AppFooter)
    .component('listErrors', ListErrors);

export default layoutModule;

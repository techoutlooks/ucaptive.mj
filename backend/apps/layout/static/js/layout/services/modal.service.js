/**
* modalSvc: Modal Service
* @namespace cms.modal.services
*/

class ModalSvc {
    constructor($uibModal) {
        'ngInject';

        this._$uibModal = $uibModal;
        this.modalDefaults = {
            backdrop: true,
            keyboard: true,
            modalFade: true,
            templateUrl: '/modal/'
        };

        this.modalOptions = {
            closeButtonText: 'Close',
            actionButtonText: 'OK',
            headerText: 'Proceed?',
            bodyText: 'Perform this action?',

            /* Template included inside of modal body.
             - bodyTemplateUrl: url of template to ng-include.
             body's template providing app may eventually define a controller of its own, no use case.
             */
            bodyTemplateUrl: '/body.html',
        };
    }

    showModal(customModalDefaults, customModalOptions) {
        if (!customModalDefaults) customModalDefaults = {};
        customModalDefaults.backdrop = 'static';
        return this.show(customModalDefaults, customModalOptions);
    };

    show(customModalDefaults, customModalOptions) {
        //Create temp objects to work with since we're in a singleton service
        var tempModalDefaults = {};
        var tempModalOptions = {};

        //Map angular-ui modal custom defaults to modal defaults defined in service
        angular.extend(tempModalDefaults, this.modalDefaults, customModalDefaults);

        //Map modal.html $scope custom properties to defaults defined in service
        angular.extend(tempModalOptions, this.modalOptions, customModalOptions);

        if (!tempModalDefaults.controller) {
            tempModalDefaults.controller = function ($scope, $uibModalInstance) {
                this.modalOptions = tempModalOptions;
                this.modalOptions.ok = function (result) {
                    $uibModalInstance.close(result);
                };
                this.modalOptions.close = function (result) {
                    $uibModalInstance.dismiss('cancel');
                };
            }
        }

        return $uibModal.open(tempModalDefaults).result;
    };

}

export default ModalSvc;

class ListErrorsCtrl {
    constructor($scope) {
        'ngInject';
    }

    formatErrors(err){
        if (typeof this.errors === 'string' || this.errors instanceof String) {
            err = new Array(err);
        }
        return err;
    }
}

let ListErrors = {
    bindings: {
        errors: '='
    },
    scope: true,
    controller: ListErrorsCtrl,
    template: `   
    <ul class="error-messages" ng-show="$ctrl.errors">
      <div ng-repeat="(field, errors) in $ctrl.errors">
        <li ng-repeat="error in $ctrl.formatErrors(errors)"> 
          [[field]]: [[error]]
        </li>
      </div>
    </ul>
    `
}

export default ListErrors;

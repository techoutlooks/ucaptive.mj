"use strict";
var core_1 = require("@angular/core");
var _ = require('lodash');
exports.RESTANGULAR = new core_1.OpaqueToken('restangularWithConfig');
function RestangularFactory(config) {
    var configObj = {
        fn: config[0],
        arrServices: [],
    };
    if (_.isArray(config[0])) {
        configObj = {
            arrServices: config[0],
            fn: config[1]
        };
    }
    return configObj;
}
exports.RestangularFactory = RestangularFactory;
//# sourceMappingURL=ng2-restangular.config.js.map
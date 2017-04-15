import { ModuleWithProviders, OpaqueToken } from '@angular/core';
export declare const CONFIG_OBJ: OpaqueToken;
export declare class RestangularModule {
    constructor(parentModule: RestangularModule);
    static forRoot(config1?: any, config2?: any): ModuleWithProviders;
}

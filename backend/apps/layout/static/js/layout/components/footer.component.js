class AppFooterCtrl {
  constructor(AppConstants) {
    'ngInject';
    this.appName = AppConstants.appName;

    // Get today's date to generate the year
    this.date = new Date();
  }
}

let AppFooter = {
  controller: AppFooterCtrl,
  templateUrl: '/footer/'
};

export default AppFooter;

class AppHeaderCtrl {
  constructor(AppConstants, User, $scope) {
    'ngInject';

    this.appName = AppConstants.appName;
    this.currentUser = User.current;

    $scope.$watch('User.current', (newUser) => {
      this.currentUser = newUser;
    })
  }
}

let AppHeader = {
  controller: AppHeaderCtrl,
  templateUrl: '/header/'
};

export default AppHeader;

class RadminCtrl {
    constructor(raduser, RadUser, $state) {
        'ngInject';

        this._RadUser = RadUser;
        this._$state = $state;
        this.title = $state.current.title;

        this.raduser = raduser;

        console.log("raduser 1= "+ JSON.stringify(this.raduser));
        console.log("data 1 = " +JSON.stringify(this.data));

    }

    // GET, PUT, DELETE username
    submitForm() {
        console.log("raduser 2= "+ JSON.stringify(this.raduser));
        console.log("submitForm.data = " +JSON.stringify(this.data));

        this.isSubmitting = true;
        this._RadUser.edit('update_user', this.data).then(
            (res) => this._$state.go('app.radmin.home'),
            (err) => {
              this.isSubmitting = false;
              this.errors = err.data.errors;
            }
        )
    }
}


export default RadminCtrl;
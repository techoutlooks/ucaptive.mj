


    accounts.$inject = [];

        /**
        * @name register
        * @desc Try to register a new user
        * @param {string} username The username entered by the user
        * @param {string} password The password entered by the user
        * @param {string} email The email entered by the user
        * @returns {Promise}
        * @memberOf app.accounts.services.accounts
        */
        function register(email, password, username) {
          return BaseApi.post('/api/v1/accounts/', {
            username: username,
            password: password,
            email: email
          });
        }

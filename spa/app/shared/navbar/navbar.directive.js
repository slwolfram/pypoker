(function () {
    'use strict';

    angular
        .module('app')
        .directive('navbar', Directive);

    function Directive() {
        return {
            restrict: 'E',
            templateUrl: 'app/shared/navbar/navbar.view.html',
            controller: Controller
        };
    }

    function Controller(LoginService) {
        var vm = this;
        checkLogin();
        vm.checkLogin = checkLogin;
        

        function checkLogin() {
            LoginService.checkLogin(function(result) {
                if (result === true) {
                    vm.loggedIn = true;
                } else {
                    vm.loggedIn = false;
                }
            });
        }


        function logout() {
            LoginService.logout();
        }

    }
}());
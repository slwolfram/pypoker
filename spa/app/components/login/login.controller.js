(function() {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', Controller);

    function Controller($location, LoginService) {
        var vm = this;
        vm.login = login;
        initController();

        function initController() {
            LoginService.logout();
        }

        function login() {
            vm.loading = true;
            LoginService.login(vm.username, vm.password, function(result) {
                if (result === true) {
                    $location.path('/');
                } else {
                    vm.error = 'Username or Password is incorrect';
                    vm.loading = false;
                }
            })
        }
    }
})();
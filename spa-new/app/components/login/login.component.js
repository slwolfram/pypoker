(function() {
    'use strict';

    angular
        .module('app')
        .component('login', {
            templateUrl: 'app/components/login/login.view.html',
            controller: Controller,
            controllerAs: 'vm'
        });


    function Controller($location, $scope, LoginService) {
        var vm = this;
        vm.login = login;
        vm.logout = logout;
        initController();

        function initController() {
            vm.logout();
        }

        function login() {
            vm.loading = true;
            LoginService.login(vm.username, vm.password, function(result) {
                console.log(result);
                if ('success' in result) {
                    $scope.$emit('loginChange', {"state": true});
                    $location.path('/');
                } else {
                    if (result.error === null)
                        vm.error = "Couldn't access the server. Please try again later.";
                    else
                        vm.error = 'Invalid credentials.';
                    vm.loading = false;
                }
            });
        }

        function logout() {
            LoginService.logout();
            $scope.$emit('loginChange', {"state": false});
        }
    }
})();
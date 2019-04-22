(function () {
    'use strict';

    angular
        .module('app')
        .component('navbar', {
            templateUrl: 'app/components/navbar/navbar.view.html',
            controller: Controller,
            controllerAs: 'vm'
        });


    function Controller($scope, LoginService) {
        var vm = this;
        vm.checkLogin = checkLogin;
        vm.loggedIn = false;
        checkLogin();

        $scope.$on('switchLoginStatus', function(event, obj) {
            console.log('navbar controller: switching login status');
            vm.loggedIn = obj.state;
        });


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
(function() {
    'use strict';

    angular
        .module('appGame')
        .component('player', {
            templateUrl: 'app/game/components/player/player.view.html',
            controller: Controller,
            controllerAs: 'vm',
            bindings: {
<<<<<<< HEAD
                seatId: '@',
                gameId: '<'
=======
                seatId: '@'
>>>>>>> 6b526b2baae0c5453fe57c6193eb2bf04f11e2c8
            }
        });


<<<<<<< HEAD
    function Controller(GameService) {
        var vm = this;
        vm.seated = false;
        vm.$onInit = () => {
            console.log(vm.seatId);
            console.log(vm.gameId);
            vm.joinGame = joinGame;
        };


        function joinGame() {
            GameService.joinGame(vm.gameId, vm.seatId, function (result) {
                if ('success' in result) {
                    $scope.$emit('updateGame');
                } else {
                    $location.path('/');
                }
            });
        }
=======
    function Controller($attrs) {
        var vm = this;
        vm.seated = false;
        console.log($attrs.seatid);
>>>>>>> 6b526b2baae0c5453fe57c6193eb2bf04f11e2c8
    }
}());
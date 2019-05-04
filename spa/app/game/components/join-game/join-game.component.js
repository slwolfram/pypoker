(function() {
    'use strict';

    angular
        .module('appGame')
        .component('joinGame', {
            templateUrl: 'app/game/components/join-game/join-game.view.html',
            controller: Controller,
            controllerAs: 'vm',
        });


    function Controller($stateParams, GameService) {
        console.log('joingame');
        var vm = this;
        vm.joinGame = joinGame;
        vm.getGame = getGame;
        vm.$onInit = () => {
            getGame($stateParams.gameID);
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


        function getGame(gameId) {
            GameService.getGame(gameId, function(result) {
                if ('success' in result) {
                    vm.game = result.success.data;
                } else {
                }
            });
        }
    }
}());
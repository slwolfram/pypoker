(function() {
    'use strict';

    angular
        .module('appGame')
        .component('game', {
            templateUrl: 'app/game/components/game/game.view.html',
            controller: Controller,
            controllerAs: 'vm'
        });


    function Controller($stateParams, GameService) {
        var vm = this;
        vm.gameIdentifier = $stateParams.gameID;
        vm.getGameState = getGameState;
        getGameState(vm.gameIdentifier);


        function getGameState(gameIdentifier) {
            GameService.getGameState(gameIdentifier, function(result) {
                console.log(result);
                if ('success' in result) {
                    vm.game = result.success.data;
                } else {

                }
            });
        }
    }
}());
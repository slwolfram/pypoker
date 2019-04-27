(function() {
    'use strict';

    angular
        .module('appGame')
        .component('player', {
            templateUrl: 'app/game/components/player/player.view.html',
            controller: Controller,
            controllerAs: 'vm',
            bindings: {
                seatId: '@'
            }
        });


    function Controller($attrs) {
        var vm = this;
        vm.seated = false;
        console.log($attrs.seatid);
    }
}());
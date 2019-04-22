(function() {
    'use strict';

    angular
        .module('app')
        .component('player', {
            templateUrl: 'app/components/player/player.view.html',
            controller: Controller,
            controllerAs: 'vm'
        });


    function Controller() {
        var vm = this;
    }
}());
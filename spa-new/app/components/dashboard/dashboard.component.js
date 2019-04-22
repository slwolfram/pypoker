(function() {
  'use strict';

  angular
    .module('app')
    .component('dashboard', {
      templateUrl: 'app/components/dashboard/dashboard.view.html',
      controller: Controller,
      controllerAs: 'vm'
    });


  function Controller(GameService) {
    var vm = this;
    vm.getGames = getGames;
    initController();


    function initController() {
      getGames();
    }
    

    function getGames() {
      GameService.getGames(function(result) {
        if ('success' in result) {
          console.log(result);
          vm.games = result.success.data;
        } else {

        }
      });
    }
  }
}());
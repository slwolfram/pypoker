(function() {
  'use strict';

  angular
    .module('app')
    .component('dashboard', {
      templateUrl: 'app/core/components/dashboard/dashboard.view.html',
      controller: Controller,
      controllerAs: 'vm'
    });


  function Controller(DashboardService) {
    var vm = this;
    vm.getGames = getGames;
    initController();


    function initController() {
      getGames();
    }
    

    function getGames() {
      DashboardService.getGames(function(result) {
        if ('success' in result) {
          console.log(result);
          vm.games = result.success.data;
        } else {

        }
      });
    }
  }
}());
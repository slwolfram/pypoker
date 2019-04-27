(function () {
  'use strict';

  angular
    .module('app')
    .component('home', {
      templateUrl: 'app/core/components/home/home.view.html',
      controller: Controller,
      controllerAs: 'vm'
    });


  function Controller() {
    var vm = this;
    vm.NumSeats = 6;
  }
})();
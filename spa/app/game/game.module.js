(function () {
    'use strict';

    angular
        .module('appGame', ['ui.router', 'ngMessages', 'ngStorage'])
        .config(config)
        .run(run);


    function config($stateProvider) {

        // app routes
        $stateProvider
            .state('game', {
                url: '/game/:gameID',
                component: 'game'
            });
    }


    function run($rootScope, $location, $localStorage) {
        $rootScope.$on(
            '$locationChangeStart', function(event, next, current) {
            var publicPages = ['/game'];
            var location = $location.path();
            if ($location.path().includes('/game/')) {
                location = '/game';
            }
            var restrictedPage = (
                publicPages.indexOf(location) === -1);
            if (restrictedPage && !$localStorage.currentUser) {
                $location.path('/login');
            }
        });
    }
})();
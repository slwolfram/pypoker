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
<<<<<<< HEAD
            })
            .state('join', {
                url: '/game/:gameID/join',
                component: 'joinGame'
            })
            .state('joinSeat', {
                url: '/game/:gameID/join/:seatID',
                component: 'joinGame'
=======
>>>>>>> 6b526b2baae0c5453fe57c6193eb2bf04f11e2c8
            });
    }


    function run($rootScope, $location, $localStorage) {
        $rootScope.$on(
<<<<<<< HEAD
            'updateGame', function(event) {
                console.log('Broadcasting game update');
                $rootScope.$broadcast('updateGame');
            }
        );
=======
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
>>>>>>> 6b526b2baae0c5453fe57c6193eb2bf04f11e2c8
    }
})();
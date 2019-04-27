(function () {
    'use strict';

    angular
        .module('app', ['appGame', 'ui.router', 'ngMessages', 'ngStorage', 'smart-table'])
        .config(config)
        .run(run);


    function config($stateProvider, $urlRouterProvider) {
        // default route
        $urlRouterProvider.otherwise("/");

        // app routes
        $stateProvider
            .state('home', {
                url: '/',
                component: 'home'
            })
            .state('login', {
                url: '/login',
                component: 'login'
            })
            .state('register', {
                url: '/register',
                component: 'register'
            })
            .state('dashboard', {
                url: '/dashboard',
                component: 'dashboard'
            });
    }


    function run($rootScope, $http, $location, $localStorage) {
        // keep user logged in after page refresh
        if ($localStorage.currentUser) {
            $http.defaults.headers.common.Authorization = (
                'Bearer ' + $localStorage.currentUser.token);
        }

        // redirect to login page if not logged in and trying
        // to access a restricted page
        $rootScope.$on(
            '$locationChangeStart', function(event, next, current) {
            var publicPages = ['/login', '/register', '/dashboard'];
            var location = $location.path();
            if ($location.path().includes('/user/')) {
                location = '/user';
            }
            var restrictedPage = (
                publicPages.indexOf(location) === -1);
            if (restrictedPage && !$localStorage.currentUser) {
                $location.path('/login');
            }
        });

        $rootScope.$on(
            'loginChange', function(event, obj) {
                console.log('Broadcasting login change');
                $rootScope.loggedIn = obj.state;
                $rootScope.$broadcast(
                    'switchLoginStatus', {'state': obj.state});
            }
        );
    }


})();
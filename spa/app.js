angular.module('PyPoker', [
    'ngMessages',
    'ngRoute',
    'PyPoker.dashboard',
    'PyPoker.login'
]).
config(['$locationProvider', '$routeProvider', 
    function($locationProvider, $routeProvider) {
        $locationProvider.hashPrefix('!');
        $routeProvider.otherwise({redirectTo: '/dashboard'});
}]);
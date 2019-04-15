var dashboard = angular.module('PyPoker.games', ['ngRoute']);
dashboard.config(function($routeProvider) {
  $routeProvider.when('/games', {
    templateUrl: 'app/components/games/games.view.html',
    controller: 'GamesCtrl'
  });
});
dashboard.controller('GamesCtrl', function($scope, $http) {
    var url = "http://localhost:5000/api/games/all";
    $http.get(url).success( function(response) {
        console.log(response.data);
        $scope.games = response.data;
     });
});
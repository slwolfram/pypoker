var dashboard = angular.module('PyPoker.dashboard', ['ngRoute']);
dashboard.config(function($routeProvider) {
  $routeProvider.when('/dashboard', {
    templateUrl: 'app/components/dashboard/dashboardView.html',
    controller: 'DashboardCtrl'
  });
});
dashboard.controller('DashboardCtrl', function($scope, $http) {
    var url = "http://localhost:5000/api/games/all";
    $http.get(url).success( function(response) {
        console.log(response.data);
        $scope.games = response.data;
     });
});
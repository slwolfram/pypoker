var app = angular.module('pypoker', []);

app.controller('gameController', function($scope, $http) {
    var url = "http://localhost:5000/api/games/all";
    $http.get(url).success( function(response) {
        console.log(response.data);
        $scope.games = response.data;
     });
});

app.controller('userController', function($scope) {

});
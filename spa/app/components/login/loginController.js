var login = angular.module('PyPoker.login', ['ngRoute']);
login.config(function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'app/components/login/loginView.html',
    controller: 'LoginCtrl'
  });
});

login.controller('LoginCtrl', function($scope, $http) {
    $scope.submit = function() {
        console.log("You pressed the button.");
        var username = $scope.username;
        var password = $scope.password;
        console.log(username);
        console.log(password);
        $http({
            method: 'POST',
            url: 'http://localhost:5000/api/auth/login',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {
                Identifier: username,
                Password: password
            }
        })
        .then(function successCallback(response) {
            console.log(response);
        }, function errorCallback(response) {
            console.log(response);
        });
    };
});
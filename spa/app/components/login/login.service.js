(function () {
    'use strict';

    angular
        .module('app')
        .factory('LoginService', Service);

    function Service($http, $localStorage) {
        var service = {};

        service.login = login;
        service.logout = logout;
        service.checkLogin = checkLogin;

        return service;


        function login(username, password, callback) {
            $http.post(
                'http://localhost:5000/api/auth/login', {
                    Identifier: username, Password: password}, {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    transformRequest: function(obj) {
                        var str = [];
                        for(var p in obj)
                        str.push(encodeURIComponent(p) + "=" + 
                            encodeURIComponent(obj[p]));
                        return str.join("&");
                    }
                }
            ).then(function(response) {
                console.log(response);
                console.log(response.data.token);
                $localStorage.currentUser = {
                    username: username, 
                    token: response.data.token
                };
                callback(true);
            }).catch(function(error) {
                console.log(error);
                callback(false);
            });
        }


        function logout() {
            delete $localStorage.currentUser;
            $http.defaults.headers.common.Authorization = '';
        }


        function checkLogin(callback) {
            console.log($localStorage.currentUser);
            if ($localStorage.currentUser === undefined || 
                $localStorage.currentUser === null) {
                return callback(false);
            } 
            $http.get(
                'http://localhost:5000/api/auth/check-login', {
                    headers: {
                        'Authentication': $localStorage.currentUser.token
                    }
                }
            ).then(function(response) {
                console.log('user is logged in!');
                callback(true);
            }).catch(function(error) {
                console.log('user is not logged in!');
                callback(false);
            });
        }
    }
})();
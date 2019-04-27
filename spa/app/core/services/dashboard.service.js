(function() {
    'use strict';

    angular
        .module('app')
        .factory('DashboardService', Service);

    function Service($http) {
        var service = {};
        service.getGames = getGames;
        service.getGameState = getGameState;

        return service;


        function getGames(callback) {
            $http.get("http://localhost:5000/api/games/all"
                ).then(function(response) {
                    callback({'success': response.data});
                }).catch(function(response) {
                    callback({'error': response.data});
                });
        }


        function getGameState(gameIdentifier, callback) {
            $http.get("http://localhost:5000/api/games/" + gameIdentifier
            ).then(function(response) {
                callback({'success': response.data});
            }).catch(function(response) {
                callback({'error': response.data});
            });
        }

        function joinGame(gameIdentifier, callback) {
            if ($localStorage.currentUser === undefined || 
                $localStorage.currentUser === null) {
                return callback(false);
            } 
            $http.get(
                'http://localhost:5000/api/game/join' + gameIdentifier, {
                    headers: {
                        'Authentication': $localStorage.currentUser.token
                    }
                }
            ).then(function(response) {
                callback({'success': response});
            }).catch(function(response) {
                callback({'error': response});
            });
        }
    }
}());
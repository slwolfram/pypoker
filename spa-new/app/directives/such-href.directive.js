(function() {
    'use strict';

    angular
        .module('app')
        .directive('suchHref', Directive);

    function Directive($location) {

        return {
            link: function (scope, element, attr) {
                element.attr('style', 'cursor:pointer');
                element.on('click', function(){
                    console.log('clicked!');
                    $location.path(attr.suchHref)
                    scope.$apply();
                });
            }
        };
    }
}());
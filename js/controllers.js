'use strict';

var app = angular.module('main', ['ngRoute']);

app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });

app.controller('mainController', function($scope, $http) {
    $scope.stockPrice = "Stock Price";

    $scope.buttonClicked = function() {
        $http({
                method: 'POST',
                url: '/query',
                data: {
                    stockName: $scope.inputStockName
                }
            }).then(function(response) {
                console.log(response);
                $scope.stockPrice = response.data;
            }, function(error) {
                console.log(error);
            });
    }

});
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


$('#datepicker').daterangepicker({
    "startDate": "03/30/2017",
    "endDate": "04/05/2017",
    "minDate": "02/01/2016",
    "maxDate": "02/01/2017"
}, function(start, end, label) {
  console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
});
'use strict';

var app = angular.module('main', ['ngRoute', 'chart.js']);

app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });
//Chart configuration
app.config(['ChartJsProvider', function (ChartJsProvider) {
    // Configure all charts
    ChartJsProvider.setOptions({
      chartColors: ['#FF5252', '#FF8A80'],
      responsive: true
    });
    // Configure all line charts
    ChartJsProvider.setOptions('line', {
      showLines: false
    });
  }])

app.controller('mainController', function($scope, $http) {
    //Test module
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

app.controller('hisController', ['$scope', '$timeout', function($scope, $http, $filter, $timeout) {
    $scope.stocks = [{name: 'Select a Company', value: '', notAnOption: true},
                    {name: 'Apple', value: 'AAPL'},
                    {name : 'Alibaba', value: 'BABA'},
                    {name : 'Baidu', value: 'BIDU'},
                    {name : 'Yahoo', value: 'YHOO'},
                    {name: 'Google', value: 'GOOG'}];

    $scope.stockName = $scope.stocks[0];
    
    //Load datepicker
    $scope.load = function() {
        $('input[name="daterange"]').daterangepicker({
        "startDate": "02/01/2016",
        "endDate": "02/01/2017",
        "minDate": "02/01/2016",
        "maxDate": "02/01/2017"
    }, function(start, end, label) {
    console.log("New date range selected: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ")");
    });
   };
    $scope.load();

    //Historical data query
    $scope.hisQuery = function() {
        console.log('------------------------------------');
        console.log($scope.stockName.value + $scope.dateRange1);
        console.log('------------------------------------');
        $http({
                method: 'POST',
                url: '/hisData',
                data: {
                    stockName: $scope.stockName.value,
                    dateRange: $scope.dateRange1
                }
            }).then(function(response) {
                console.log(response);
                $scope.stockData = response.data;
            }, function(error) {
                console.log(error);
            });
    }

    //Stock chart
    $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
    $scope.series = ['Series A', 'Series B'];
    $scope.data = [
        [65, 59, 80, 81, 56, 55, 40],
        [28, 48, 40, 19, 86, 27, 90]
    ];
    $scope.onClick = function (points, evt) {
        console.log(points, evt);
    };
    
    // Simulate async data update
    // $timeout(function () {
    //     $scope.data = [
    //     [28, 48, 40, 19, 86, 27, 90],
    //     [65, 59, 80, 81, 56, 55, 40]
    //     ];
    // }, 3000);

}]);

app.controller('preController', function($scope, $http) {

});

app.controller('groupController', function($scope, $http) {

});


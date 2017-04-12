// written by: Jingyuan Li
// assisted by:
// debugged by: Jingyuan Li
'use strict';

var app = angular.module('main', ['ngRoute', 'chart.js']);



app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('//').endSymbol('//');
});
//Chart configuration
// app.config(['ChartJsProvider', function (ChartJsProvider) {
//     // Configure all charts
//     ChartJsProvider.setOptions({
//         chartColors: ['#4caf50', '#0c7cd5'],
//         type: ['line', 'bar'],
//         responsive: true,
//         scales: {
//             yAxes: [{
//                 type: "linear",
//                 position: "left",
//                 id: "y-axis-1",
//             }, {
//                 type: "linear",
//                 position: "right",
//                 id: "y-axis-2",
//             }],
//         }
//     });
//     // Configure all line charts
//     ChartJsProvider.setOptions('line', {
//         showLines: true
//     });
// }])

app.controller('mainController', function ($scope, $http) {
    //Test module
    $scope.stockPrice = "Stock Price";
    $scope.buttonClicked = function () {
        $http({
            method: 'POST',
            url: '/query',
            data: {
                stockName: $scope.inputStockName
            }
        }).then(function (response) {
            console.log(response);
            $scope.stockPrice = response.data;
        }, function (error) {
            console.log(error);
        });
    }

});

app.controller('hisController', function ($scope, $http, $filter, $timeout) {
    var stockData, stockTime = [],
        stockPrice = [],
        stockVolume = [];

    //The selector
    $scope.stocks = [{
            name: 'Select a Company',
            value: '',
            notAnOption: true
        },
        {
            name: 'Apple',
            value: 'AAPL'
        },
        {
            name: 'Alibaba',
            value: 'BABA'
        },
        {
            name: 'Baidu',
            value: 'BIDU'
        },
        {
            name: 'Yahoo',
            value: 'YHOO'
        },
        {
            name: 'Google',
            value: 'GOOG'
        }
    ];
    $scope.stockName = $scope.stocks[0];

    //Load datepicker
    $scope.load = function () {
        $('input[name="daterange"]').daterangepicker({
            "startDate": "02/01/2016",
            "endDate": "02/01/2017",
            "minDate": "02/01/2016",
            "maxDate": "02/01/2017"
        }, function (start, end, label) {
            console.log("New date range selected: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ")");
        });
    };

    var data = {
                    labels: stockTime,
                    datasets: [{
                        type: 'line',
                        label: 'Price',
                        // xAxisID: 'Time',
                        yAxisID: 'A',
                        // yAxesGroup: 'price',
                        fill: false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#4caf50',
                        pointBackgroundColor:'#4caf50',
                        backgroundColor:'#4caf50',
                        pointRadius: 2,
                        pointBorderColor:'#f9f9f9',
                        pointHoverBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBorderColor: '#f9f9f9',
                        // pointBorderColor: '#4caf50',
                        // pointRadius: '2',
                        data: [stockPrice]
                    },
                    {
                        type: 'bar',
                        label: 'Volume',
                        // xAxisID: 'Time',
                        yAxisID: 'B',
                        // yAxesGroup: 'volume',
                        borderColor: '#0c7cd5',
                        hoverBorderColor: '#0c7cd5',
                        hoverBorderWidth: 2,
                        backgroundColor: '#0c7cd5',
                        data: [stockVolume]
                    }]
                };
    var options = {
                    tooltips:{
                        backgroundColor: 'rgba(245,245,245,0.8)',
                        titleFontColor: '#666666',
                        bodyFontColor: '#666666',
                        bodySpacing: 3,
                    },
                    scales: {
                        xAxes:[{
                            gridLines:{
                                display: false
                            },
                        }],
                        yAxes: [{
                            id: 'A',
                            type: 'linear',
                            position: 'left',
                            gridLines:{
                                display: false
                            },
                            ticks: {
                                beginAtZero: false
                            }
                        },
                        {
                            id: 'B',
                            type: 'linear',
                            position: 'right',
                            gridLines:{
                                display: false
                            },
                            ticks: {
                                beginAtZero: false
                            }
                        }],
                        fontFamily: "'Lato', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'"
                    },
                    legend: {
                        display: true
                    }
                };
    var ctx = $('#myChart');
    var hisChart = new Chart(ctx, {
        type: 'bar',
        // data: data,
        options: options
    });
    $scope.load();

    //Historical data query
    $scope.hisQuery = function () {
        console.log('-------------Query Data-------------');
        console.log($scope.stockName.value + $scope.dateRange1);
        console.log('------------------------------------');
        $http({
            method: 'POST',
            url: '/hisData',
            data: {
                stockName: $scope.stockName.value,
                dateRange: $scope.dateRange1
            }
        }).then(function (response) {
            stockData = response.data;
            console.log('------------stockData---------------');
            console.log(stockData);
            console.log('------------------------------------');
            for (var i = 0; i < stockData.length; i++) {
                stockTime[i] = stockData[i].date;
                stockPrice[i] = stockData[i].close;
                stockVolume[i] = stockData[i].volume;
                console.log('-------------stockPrice-------------');
                console.log(stockPrice);
                console.log('------------------------------------');
            }
            //Stock chart data(angular)
            // $scope.labels = stockTime;
            // $scope.series = ['Price', 'Volume'];
            // $scope.chartdata = [stockPrice, stockVolume];
            console.log('============================');
            console.log();

            //Render a stock chart(jquery)
            var ctx = $('#myChart');
            var hisChart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: options
            });
            
            hisChart.data.datasets[0].data = stockPrice;
            hisChart.data.datasets[1].data = stockVolume;
            hisChart.data.labels = stockTime;
            hisChart.update();
            // ctx.data.datasets[0].data = stockVolume;
            // ctx.data.labels = stockTime;
            // ctx.update();
        }, function (error) {
            console.log(error);
        });
    }



    // $scope.onClick = function (points, evt) {
    //     console.log(points, evt);
    // };

    // Simulate async data update
    // $timeout(function () {
    //     $scope.data = [
    //     [28, 48, 40, 19, 86, 27, 90],
    //     [65, 59, 80, 81, 56, 55, 40]
    //     ];
    // }, 3000);

});

app.controller('preController', function ($scope, $http) {

});

app.controller('groupController', function ($scope, $http) {

});
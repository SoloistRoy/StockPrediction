// written by: Jingyuan Li
// assisted by: Yiran Sun
// debugged by: Jingyuan Li, Yiran Sun
'use strict';

var app = angular.module('main', ['ngRoute', 'chart.js']);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('//').endSymbol('//');
});

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
            }).then(function(response) {
                console.log(response);
                // pass data in json, a[0]: one piece, a[1]: json data
                var dataSet = response.data;
                var data = dataSet[1]
                $scope.stockPrice = data;
            }, function(error) {
                console.log(error);
            });
    }

});

app.controller('hisController', function ($scope, $http, $filter) {
    var stockData, stockTime = ["1900-01-01","1900-01-02","1900-01-03","1900-01-04","1900-01-05","1900-01-06"],
        stockPrice = [0,0,0,0,0,0],
        stockVolume = [0,0,0,0,0,0],
        clickCount = 0;

    //The selector
    $scope.stocks = [{
            name: 'Select a Company',
            value: '',
            notAnOption: true
        },
        {
            name: 'Apple Inc.',
            value: 'AAPL'
        },
        {
            name: 'Alibaba Group',
            value: 'BABA'
        },
        {
            name: 'Baidu, Inc',
            value: 'BIDU'
        },
        {
            name: 'Yahoo! Inc.',
            value: 'YHOO'
        },
        {
            name: 'Google (Alphabet Inc.)',
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
        var ctx = $('#myChart');
        // prerender chart
        var hisChart = new Chart(ctx, {
            type: 'bar',
            data: chartdata,
            options: options
        });
    }; 
   

    //chart configuration
    var chartdata = {
                    labels: stockTime,
                    datasets: [{
                        type: 'line',
                        label: 'Price',
                        yAxisID: 'A',
                        fill: false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#69b04a',
                        pointBackgroundColor:'#69b04a',
                        backgroundColor:'#69b04a',
                        pointRadius: 2,
                        pointBorderColor:'#f9f9f9',
                        pointHoverBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBorderColor: '#f9f9f9',
                        data: [stockPrice]
                    },
                    {
                        type: 'bar',
                        label: 'Volume',
                        yAxisID: 'B',
                        borderColor: '#a4d9f1',
                        hoverBorderColor: '#49b2e3',
                        hoverBorderWidth: 2,
                        backgroundColor: '#a4d9f1',
                        data: [stockVolume]
                    }]
                };
    var options = {
                    tooltips: {
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
                                beginAtZero: true
                            }
                        }],
                        fontFamily: "'Lato', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'"
                    },
                    legend: {
                        display: true
                    }
                };

    var ctx = $('#myChart');
    // prerender chart
    var hisChart = new Chart(ctx, {
        type: 'bar',
        data: chartdata,
        options: options
    });

     $scope.load();
    //Scroll Top button
    $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('.floatbtn').fadeIn();
            } else {
                $('.floatbtn').fadeOut();
            }
        });
        $('.floatbtn').click(function () {
            $("html, body").animate({ scrollTop: 0 }, 1000);
            return false;
        });

    //Historical data query
    $scope.hisQuery = function () {
        clickCount++;
        $("html, body").animate({ scrollTop: 95 }, 500);
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
            //Initialize data in each query
            stockPrice = [0];
            stockVolume = [0];
            stockTime = ["1900-01-01"];
            stockData = response.data;
            $scope.tableData = response.data;
            console.log('------------stockData---------------');
            console.log(stockData);
            console.log('------------------------------------');
            for (var i = 0; i < stockData.length; i++) {
                stockTime[i] = stockData[i].date;
                stockPrice[i] = stockData[i].close;
                stockVolume[i] = stockData[i].volume;
            }
            console.log('------------------------------------');
            console.log(clickCount);
            console.log('------------------------------------');
            console.log(hisChart);
                //Update chart
                hisChart.data.datasets[0].data = stockPrice;
                hisChart.data.datasets[1].data = stockVolume;
                hisChart.data.labels = stockTime;
                hisChart.update();
            console.log(hisChart);
            
            console.log("New data: ");
            console.log(stockPrice);
            console.log(stockTime);
            
        }, function (error) {
            console.log(error);
        });
    }
});

app.controller('preController', function ($scope, $http) {
    var stockData, stockTime = ["1900-01-01","1900-01-02","1900-01-03","1900-01-04","1900-01-05","1900-01-06"],
        stockPrice = [0,0,0,0,0,0],
        stockVolume = [0,0,0,0,0,0];

    //The selector
    $scope.stocks = [{
            name: 'Select a Company',
            value: '',
            notAnOption: true
        },
        {
            name: 'Apple Inc.',
            value: 'AAPL'
        },
        {
            name: 'Alibaba Group',
            value: 'BABA'
        },
        {
            name: 'Baidu, Inc',
            value: 'BIDU'
        },
        {
            name: 'Yahoo! Inc.',
            value: 'YHOO'
        },
        {
            name: 'Google (Alphabet Inc.)',
            value: 'GOOG'
        }
    ];
    $scope.terms = [
        {
            name: '5 Day',
            value: 5
        },
        {
            name: '10 Day',
            value: 10
        },
        {
            name: '15 Day',
            value: 15
        }
    ];
    $scope.inputStockName = $scope.stocks[0];
    $scope.inputPredictTerm = $scope.terms[0];

    //chart configuration
    var chartdata = {
                    labels: stockTime,
                    datasets: [{
                        type: 'line',
                        label: 'Price',
                        yAxisID: 'A',
                        fill: false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#6b73d6',
                        pointBackgroundColor:'#6b73d6',
                        backgroundColor:'#6b73d6',
                        pointRadius: 2,
                        pointBorderColor:'#f9f9f9',
                        pointHoverBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBorderColor: '#f9f9f9',
                        data: [stockPrice]
                    },
                    {
                        type: 'bar',
                        label: 'Volume',
                        yAxisID: 'B',
                        borderColor: '#cdeaf7',
                        // hoverBorderColor: '#794DDA',
                        hoverBorderWidth: 2,
                        backgroundColor: '#cdeaf7',
                        data: [stockVolume]
                    }]
                };
    var options = {
                    tooltips: {
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
                                beginAtZero: true
                            }
                        }],
                        fontFamily: "'Lato', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'"
                    },
                    legend: {
                        display: true
                    }
                };
    var ctx = $('#myChart');
    //prerender chart
    var hisChart = new Chart(ctx, {
        type: 'bar',
        data: chartdata,
        options: options
    });

    //Scroll Top button
    $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('.floatbtn').fadeIn();
            } else {
                $('.floatbtn').fadeOut();
            }
        });
        $('.floatbtn').click(function () {
            $("html, body").animate({ scrollTop: 0 }, 1000);
            return false;
        });

    $scope.prediction = "Prediction";
    $scope.preQuery = function () {
        $http({
                method: 'POST',
                url: '/getPre',
                data: {
                    stockName: $scope.inputStockName.value,
                    datePicker: $scope.inputPredictTerm.value
                }
            }).then(function(response) {
                $("html, body").animate({ scrollTop: 97 }, 500);
                //Initialize data in each query
                stockPrice = [0];
                stockVolume = [0];
                stockTime = ["1900-01-01"];
                stockData = response.data;
                $scope.tableData = response.data;
                console.log('------------stockData---------------');
                console.log(stockData);
                console.log('------------------------------------');
                for (var i = 0; i < stockData.length; i++) {
                    stockTime[i] = stockData[i].date;
                    stockPrice[i] = stockData[i].close;
                    stockVolume[i] = stockData[i].volume;
                }
                
                // Update chart
                hisChart.data.datasets[0].data = stockPrice;
                hisChart.data.datasets[1].data = stockVolume;
                hisChart.data.labels = stockTime;
                console.log("New data: ");
                console.log(stockPrice);
                console.log(stockTime);
                hisChart.update();

                console.log(response.data);
                $scope.prediction = response.data;
            }, function(error) {
                console.log(error);
            });
    }
});

app.controller('groupController', function ($scope, $http) {

});
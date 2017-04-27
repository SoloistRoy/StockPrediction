// written by: Jingyuan Li
// assisted by: Yiran Sun
// debugged by: Jingyuan Li, Yiran Sun
'use strict';

var app = angular.module('main', ['ngRoute', 'chart.js']);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('//').endSymbol('//');
});

app.controller('mainController', function ($scope, $interval, $http) {
    // Get real time data
    var getdata;
    $http({
            method: 'GET',
            url: '/realTime'
        }).then(function(response) {
            console.log(response);
            $scope.realData = response.data;
        }, function(error) {
            console.log(error);
        });
    console.log("getdata!");
    getdata = $interval(function() {
        $http({
            method: 'GET',
            url: '/realTime'
        }).then(function(response) {
            console.log(response);
            $scope.realData = response.data;
        }, function(error) {
            console.log(error);
        });
    }, 30000);
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
    var stockData, indData, dateData,
        stockTime = ["1900-01-01","1900-01-02","1900-01-03","1900-01-04","1900-01-05","1900-01-06"],
        stockPrice = [0,0,0,0,0,0],
        stockPrice2 = [0,0,0,0,0,0],
        indPrice = [0,0,0,0,0,0],
        indTime = ["1900-01-01","1900-01-02","1900-01-03","1900-01-04","1900-01-05","1900-01-06"],
        stockVolume = [0,0,0,0,0,0],
        dateTime = ["1900-01-01","1900-01-02","1900-01-03","1900-01-04","1900-01-05","1900-01-06"],
        datePrice = [0,0,0,0,0,0],
        dateVolume = [0,0,0,0,0,0],
        overbought = [0,0,0,0,0,0],
        oversold = [0,0,0,0,0,0],
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
        },
        {
            name: 'Chase Corporation',
            value: 'CCF'
        },
        {
            name: 'Bank of America Corporation',
            value: 'BAC'
        },
        {
            name: 'Facebook, Inc.',
            value: 'FB'
        },
        {
            name: 'Twitter, Inc.',
            value: 'TWTR'
        },
        {
            name: 'New Oriental Education & Technology Group Inc.',
            value: 'EDU'
        }
    ];
    $scope.indicators = [{
            name: 'Select an Indicator',
            value: '',
            notAnOption: true
        },
        {
            name: 'SMA (Simple Moving Average)',
            value: 'SMA'
        },
        {
            name: 'EMA (Exponential Moving Average)',
            value: 'EMA'
        },
        {
            name: 'RSI (Relative Strength Index)',
            value: 'RSI'
        },
        // {
        //     name: 'MACD (Moving Average Convergence/Divergence)',
        //     value: 'MACD'
        // }
    ];
    $scope.stockName = $scope.stocks[0];
    $scope.indicatorName = $scope.indicators[0];

    //Load datepicker
    $scope.load = function () {
        var end = moment();
        $('input[name="daterange"]').daterangepicker({
            "startDate": "01/01/2016",
            "endDate": end,
            "minDate": "01/01/2016",
            "maxDate": end
        }, function (start, end, label) {
            console.log("New date range selected: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ")");
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
                        pointRadius: 0.5,
                        pointBorderColor:'#69b04a',
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
                    onClick: function(e){
                        var element = this.getElementAtEvent(e);
                        if(element.length > 0){
                            var dateDate = stockTime[element[0]._index];
                            $scope.datetimeDate = dateDate;
                            $http({
                                method: 'POST',
                                url: '/dateQuery',
                                data: {
                                    stockName: $scope.stockName.value,
                                    stockDate: dateDate
                                }
                            }).then(function (response) {
                                console.log(response.data);
                                $scope.dateTBData = response.data;

                                //Initialize data in each query
                                datePrice = [0];
                                dateVolume = [0];
                                dateTime = ["1900-01-01"];
                                dateData = response.data;

                                if (dateData == "VOID") {  /////////////////////// In this case, pop a alert instead of a graph///////////////////////////////
                                    console.log("VOID")
                                    window.alert("There is no data at this day!");
                                }
                                else{
                                    console.log('------------------------------------');
                                    console.log(dateData);
                                    console.log('------------------------------------');
                                    
                                    for (var i = 0; i < dateData.length; i++) {
                                        dateTime[i] = dateData[i].time;
                                        datePrice[i] = dateData[i].price;
                                        dateVolume[i] = dateData[i].volume;
                                    }
                                    //Update chart
                                    mdlChart.data.datasets[0].data = datePrice;
                                    // mdlChart.data.datasets[1].data = dateVolume;
                                    mdlChart.data.labels = dateTime;
                                    mdlChart.update();
                                    $('#myModal').modal('show');
                                }
                                
                            }, function (error) {
                                console.log(error);
                            });
                        }
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
    var indChartdata = {
                    labels: indTime,
                    datasets: [{
                        type: 'line',
                        label: 'Indicator',
                        fill: false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#00a7ee',
                        pointBackgroundColor:'#00a7ee',
                        backgroundColor:'#00a7ee',
                        pointRadius: 0.5,
                        pointBorderColor:'#00a7ee',
                        pointHoverBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBorderColor: '#f9f9f9',
                        data: [indPrice]
                    }
                    ,{
                        type: 'line',
                        label: 'date Price',
                        fill: false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#69b04a',
                        pointBackgroundColor:'#69b04a',
                        backgroundColor:'#69b04a',
                        pointRadius: 0.5,
                        pointBorderColor:'#69b04a',
                        pointHoverBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBorderColor: '#f9f9f9',
                        data: [stockPrice2]
                    },
                    {
                        type:'line',
                        label: 'Overbought',
                        fill:false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#be0712',
                        pointBackgroundColor:'#be0712',
                        backgroundColor:'#be0712',
                        pointBorderColor:'#be0712',
                        pointHoverBorderColor: '#be0712',
                        pointRadius: 0,
                        pointHoverBorderWidth: 0,
                        pointHoverRadius: 0,
                        data:[overbought],
                        hidden: true
                    },
                    {
                        type:'line',
                        label: 'Oversold',
                        fill:false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#fc0d1b',
                        pointBackgroundColor:'#fc0d1b',
                        backgroundColor:'#fc0d1b',
                        pointBorderColor:'#fc0d1b',
                        pointHoverBorderColor: '#fc0d1b',
                        pointRadius: 0,
                        pointHoverBorderWidth: 0,
                        pointHoverRadius: 0,
                        data:[oversold],
                        hidden: true
                    }
                    ]
                };
    var indOptions = {
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
                            type: 'linear',
                            position: 'left',
                            gridLines:{
                                display: false
                            },
                            ticks: {
                                beginAtZero: false
                            }
                        }
                        ],
                        fontFamily: "'Lato', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'"
                    },
                    legend: {
                        display: true
                    }
                };

    var mdlChartdata = {
                    labels: dateTime,
                    datasets: [{
                        type: 'line',
                        label: 'Price',
                        yAxisID: 'A',
                        fill: false,
                        borderJoinStyle: 'bevel',
                        lineTension: 0,
                        borderColor: '#fc0d1b',
                        pointBackgroundColor:'#fc0d1b',
                        backgroundColor:'#fc0d1b',
                        pointRadius: 0.5,
                        pointBorderColor:'#fc0d1b',
                        pointHoverBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBorderColor: '#f9f9f9',
                        data: [datePrice]
                    }
                    // ,
                    // {
                    //     type: 'bar',
                    //     label: 'Volume',
                    //     yAxisID: 'B',
                    //     borderColor: '#a4d9f1',
                    //     hoverBorderColor: '#49b2e3',
                    //     hoverBorderWidth: 2,
                    //     backgroundColor: '#a4d9f1',
                    //     data: [dateVolume]
                    // }
                    ]
                };
    var mdlOptions = {
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
                        }
                        // ,
                        // {
                        //     id: 'B',
                        //     type: 'linear',
                        //     position: 'right',
                        //     gridLines:{
                        //         display: false
                        //     },
                        //     ticks: {
                        //         beginAtZero: true
                        //     }
                        // }
                        ],
                        fontFamily: "'Lato', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'"
                    },
                    legend: {
                        display: true
                    }
                };
    var ctx = $('#myChart');
    var ctx2 = $('#myChart2');
    var ctx3 = $('#modalChart')
    // prerender chart
    var hisChart = new Chart(ctx, {
        type: 'bar',
        data: chartdata,
        options: options
    });
    var indChart = new Chart(ctx2, {
        type: 'line',
        data: indChartdata,
        options: indOptions
    });
    var mdlChart = new Chart(ctx3, {
        type: 'line',
        data: mdlChartdata,
        options: mdlOptions
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
            for (var i = 0; i < stockData.length; i++) {
                stockTime[i] = stockData[i].date;
                stockPrice[i] = stockData[i].close;
                stockVolume[i] = stockData[i].volume;
            }
            //Update chart
            hisChart.data.datasets[0].data = stockPrice;
            hisChart.data.datasets[1].data = stockVolume;
            hisChart.data.labels = stockTime;
            hisChart.update();
        }, function (error) {
            console.log(error);
        });
    }

    // Indicators data query
    $scope.indQuery = function () {
        console.log('-------------Query Data-------------');
        console.log($scope.indicatorName.value + $scope.dateRange1);
        console.log('------------------------------------');

        $http({
            method: 'POST',
            url: '/indData',
            data: {
                stockName: $scope.stockName.value,
                indicatorName: $scope.indicatorName.value,
                dateRange: $scope.dateRange1
            }
        }).then(function (response) {
            //Initialize data in each query
            indPrice = [0];
            // stockVolume = [0];
            indTime = ["1900-01-01"];
            indData = response.data;
            for (var i = 0; i < indData.length; i++) {
                indTime[i] = indData[i].date;
                indPrice[i] = indData[i].close;
            }
            var N=10;
            var indPrice2;
            // stockPrice2 = stockPrice.slice(10,stockPrice.length);
            indChart.data.datasets[2].hidden = true;
            indChart.data.datasets[3].hidden = true;
            if ($scope.indicatorName.value==='SMA')
                for (var index = 0; index < N; index++) 
                    indPrice.unshift(null);
            else if ($scope.indicatorName.value==='RSI') {
                for (var index = 0; index < 14; index++) 
                    indPrice.unshift(null);
                for (var index = 0; index < indPrice.length; index++) {
                    overbought[index] = 70;
                    oversold[index] = 30;
                }
                indChart.data.datasets[2].hidden = false;
                indChart.data.datasets[3].hidden = false;
            }
            console.log(stockPrice);
            console.log(stockPrice.length);
            console.log(indPrice.length);
            //Update chart
            indChart.data.datasets[2].data = overbought;
            indChart.data.datasets[3].data = oversold;
            indChart.data.datasets[0].data = indPrice;
            indChart.data.datasets[1].data = stockPrice;
            indChart.data.labels = stockTime;
            indChart.update();
            
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
        },
        {
            name: 'Chase Corporation',
            value: 'CCF'
        },
        {
            name: 'Bank of America Corporation',
            value: 'BAC'
        },
        {
            name: 'Facebook, Inc.',
            value: 'FB'
        },
        {
            name: 'Twitter, Inc.',
            value: 'TWTR'
        },
        {
            name: 'New Oriental Education & Technology Group Inc.',
            value: 'EDU'
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
    $scope.methods = [{
            name: 'Select a Method',
            value: '',
            notAnOption: true
        },
        {
            name: 'SVM',
            value: 'SVM'
        },
        {
            name: 'ANN',
            value: 'ANN'
        },
        {
            name: 'Lasso/Ridge',
            value: ''
        }
    ];
    $scope.inputStockName = $scope.stocks[0];
    $scope.inputPredictTerm = $scope.terms[0];
    $scope.inputPredictMethod = $scope.methods[0];

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
                        borderColor: '#f2a778',
                        pointBackgroundColor:'#f2a778',
                        backgroundColor:'#f2a778',
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
                        borderColor: '#eaeaea',
                        // hoverBorderColor: '#794DDA',
                        hoverBorderWidth: 2,
                        backgroundColor: '#eaeaea',
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
                    datePicker: $scope.inputPredictTerm.value,
                    method: $scope.inputPredictMethod.value
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

app.controller('queryController', function ($scope, $http) {
    function findCompany(params) {
        if (params==='AAPL') return 'Apple Inc. (AAPL)'
        else if (params==='BABA') return 'Alibaba Group (BABA)'
        else if (params==='BIDU') return 'Baidu, Inc. (BIDU)'
        else if (params==='YHOO') return 'Yahoo! Inc. (YHOO)'
        else if (params==='GOOG') return 'Google (Alphabet Inc.) (GOOG)'
        else if (params==='CCF') return 'Chase Corporation (CCF)'
        else if (params==='BAC') return 'Bank of America Corporation (BAC)'
        else if (params==='FB') return 'Facebook, Inc. (FB)'
        else if (params==='TWTR') return 'Twitter, Inc. (TWTR)'
        else if (params==='EDU') return 'New Oriental Education & Technology Group Inc. (EDU)'
    }
    var staData;
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
            name: 'Baidu, Inc.',
            value: 'BIDU'
        },
        {
            name: 'Yahoo! Inc.',
            value: 'YHOO'
        },
        {
            name: 'Google (Alphabet Inc.)',
            value: 'GOOG'
        },
        {
            name: 'Chase Corporation',
            value: 'CCF'
        },
        {
            name: 'Bank of America Corporation',
            value: 'BAC'
        },
        {
            name: 'Facebook, Inc.',
            value: 'FB'
        },
        {
            name: 'Twitter, Inc.',
            value: 'TWTR'
        },
        {
            name: 'New Oriental Education & Technology Group Inc.',
            value: 'EDU'
        }
    ];
    $scope.inputStockName = $scope.stocks[0];

    $scope.Query = function () {
        $http({
                method: 'POST',
                url: '/Query',
                data: {
                    stockName: $scope.inputStockName.value
                }
            }).then(function(response) {
                //Initialize data in each query
                staData = response.data;
                var company = staData[3].value;
                company = company.substring(1,company.length-1);
                var companies = company.split(', ');
                for (var index = 0; index < companies.length; index++) {
                    var temp = companies[index];
                    companies[index] = temp.substring(1,temp.length-1);
                }
                for (var index = 0; index < companies.length; index++) {
                    companies[index] = findCompany(companies[index]);
                }
                staData[3].value = companies.join(', ');
                $scope.statisticData = staData;
            }, function(error) {
                console.log(error);
            });
    }
});
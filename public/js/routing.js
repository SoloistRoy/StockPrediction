app.config(function($routeProvider, $locationProvider){
    $locationProvider.html5Mode(true);
    $routeProvider
    .when("/home", {
        templateUrl: "StockPrediction/public/partials/main.html", 
        controller: "mainController",
        activetab: "home"
    })
    .when("/historical", {
        templateUrl: "StockPrediction/public/partials/historical.html",
        controller: "hisController",
        activetab: 'historical'
    })
    .when("/prediction", {
        templateUrl: "StockPrediction/public/partials/prediction.html",
        controller: "preController",
        activetab: "prediction"
    })
    .when("/groupinfo", {
        templateUrl: "StockPrediction/public/partials/groupinfo.html",
        controller: "groupController",
        activetab: "groupinfo"
    })
    .otherwise({ redirectTo: "/home", activetab: "home" });
}).run(function ($rootScope, $route) {
        $rootScope.$route = $route;
    });
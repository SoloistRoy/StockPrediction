app.config(function($routeProvider, $locationProvider){
    $locationProvider.html5Mode(true);
    $routeProvider
    .when("/home", {
        templateURL: "partials/main.html", 
        controller: "mainController",
        activetab: "home"
    })
    .when("/historical", {
        templateURL: "historical.html",
        activetab: "historical"
    })
    .when("/prediction", {
        templateURL: "partials/prediction.html",
        activetab: "prediction"
    })
    .when("/groupinfo", {
        templateURL: "partials/groupinfo.html",
        activetab: "groupinfo"
    })
    .otherwise({ redirectTo: "/home", activetab: "home" });
}).run(function ($rootScope, $route) {
    $rootScope.$route = $route;
});
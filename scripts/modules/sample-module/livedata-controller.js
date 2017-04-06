define(['angular', './sample-module'], function(angular, sampleModule) {
	'use strict';
	return sampleModule.controller('LiveDataCtrl', ['$scope', '$http', 'PredixLiveDataService',
		function($scope, $http, PredixLiveDataService) {
	        PredixLiveDataService.getWsUrl().then(function(urlData) {
	            $scope.context = {};
				$scope.wsUrl = urlData.wsUrl + '/livestream';
	            // console.log('scope.context.wsUrl: ' + $scope.context.wsUrl);
	            $scope.context.pickerOptions =
					[
				        {
				            "sourceTagId": "Compressor-2015:CompressionRatio",
				            "meterUri": "/tag/crank-frame-compressionratio",
				            "thresholdHigh": 3,
				            "thresholdLow": 2.5,
				            "wsUrl": $scope.wsUrl + "/Compressor-2015:CompressionRatio",
				            "label": "Temperature",
				            "colorIndex": 0
				        },
				        {
				            "sourceTagId": "Compressor-2015:DischargePressure",
				            "meterUri": "/tag/crank-frame-dischargepressure",
				            "thresholdHigh": 23,
				            "thresholdLow": 0,
				            "wsUrl": $scope.wsUrl + "/Compressor-2015:DischargePressure",
				            "label": "Barometer",
				            "colorIndex": 1
				        },

				    ];
	        }, function (msg) {
	            console.log(msg);
	        });
		}]);
});

angular.module('demo', [])
  .controller('Hello', function ($scope, $http) {

    $scope.detection = false;
    $http.get('http://localhost:5000/emotion_scores/').then(function (response) {
      $scope.greeting = response.data;
      $scope.greeting.reverse();
      $scope.greeting.forEach(function (e, i, array) {
        e["time"] = timeConverter(e["time"]);
        var width = {}, height = {}, myBase64 = "data:image/jpg;base64," + e.picture[0];
        var img = new Image();
        img.src = myBase64;
        img.addEventListener('load', function () {
          width = img.width;
          height = img.height;
          var maxValue = Math.max(img.width, img.height);
          var scale = maxValue / 240;
          e.face_position.left = e.face_position.left / scale;
          e.face_position.width = e.face_position.width / scale;
          e.face_position.height = e.face_position.height / scale;
          e.face_position.top = e.face_position.top / scale;
          console.log(e);
        });

      });
    });
    $http.get('http://localhost:5000/last_happy_client/').then(function (response) {
      $scope.smile = response.data[0];
      $scope.smile["time"] = timeConverter($scope.smile["time"]);

    });

    function timeConverter(UNIX_timestamp) {
      var a = new Date(UNIX_timestamp * 1000);
      var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      var year = a.getFullYear();
      var month = months[a.getMonth()];
      var date = a.getDate();
      var hour = a.getHours();
      var min = a.getMinutes();
      var sec = a.getSeconds();
      var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
      return time;
    }

    $scope.showFaceDetection = function showFaceDetection() {
      $scope.detection = !$scope.detection;

    }
  });



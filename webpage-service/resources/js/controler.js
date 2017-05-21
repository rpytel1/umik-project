angular.module('demo', [])
  .controller('Hello', function ($scope, $http) {


    $http.get('http://localhost:5000/emotion_scores/').then(function (response) {
      $scope.greeting = response.data;
      $scope.greeting.reverse();
      $scope.greeting.forEach(function (e, i, array) {
        e["time"] = timeConverter(e["time"]);
      });
    });
    $http.get('http://localhost:5000/lasthappy/').then(function (response) {
      $scope.smile = response.data[0];
      $scope.smile["time"]=timeConverter($scope.smile["time"]);
      console.log(response.data[0]);
    });
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



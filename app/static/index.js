$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  var $this = $(this),
  label = $this.prev('label');

  if (e.type === 'keyup') {
    if ($this.val() === '') {
      label.removeClass('active highlight');
    } else {
      label.addClass('active highlight');
    }
  } else if (e.type === 'blur') {
    if( $this.val() === '' ) {
      label.removeClass('active highlight'); 
    } else {
      label.removeClass('highlight');   
    }   
  } else if (e.type === 'focus') {
    if( $this.val() === '' ) {
      label.removeClass('highlight'); 
    } else if( $this.val() !== '' ) {
      label.addClass('highlight');
    }
  }
});
  
$('.tab a').on('click', function (e) {
  e.preventDefault();
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  target = $(this).attr('href');
  $('.tab-content > div').not(target).hide();
  $(target).fadeIn(600);
});


function showLocation() {
  var mapDict = {
    "Trinity centre" : ["LS1 5AT"],
    "Train Station": ["LS1 4DY"],
    "Merrion centre": ["LS2 8NG"],
    "LRI hospital": ["LS1 3EX"],
    "UoL Edge sports centre": ["LS2 9JT"]
  };
  var geocoder = new google.maps.Geocoder();
  
  geocoder.geocode({
    address: mapDict[document.getElementById('location').value]+""
  }, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      //map.setCenter(results[0].geometry.location); //center the map over the result

      var mapOptions = {
        zoom: 15,
        center: results[0].geometry.location
      }
      map = new google.maps.Map(document.getElementById('map'), mapOptions);

      //place a marker at the location
      var marker = new google.maps.Marker({
        map: map,
        position: results[0].geometry.location
      });
      //markers.push(marker);
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}
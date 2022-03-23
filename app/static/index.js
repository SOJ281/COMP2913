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
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

function changeView() {
  var value = document.getElementById('viewType').value;
  if (value == "Weekly") {
    document.getElementById("day").value = "";
    document.getElementById("month").value = "";
    document.getElementById("year").value = "";

    document.getElementById('dayC').hidden = false;
    document.getElementById('monthC').hidden = false;
    document.getElementById('yearC').hidden = false;
  } else if (value == "Monthly") {
    document.getElementById("day").value = "-1";
    document.getElementById("month").value = "";
    document.getElementById("year").value = "";

    document.getElementById('dayC').hidden = true;
    document.getElementById('monthC').hidden = false;
    document.getElementById('yearC').hidden = false;
  } else if (value == "Yearly") {
    document.getElementById("day").value = "-1";
    document.getElementById("month").value = "-1";
    document.getElementById("year").value = "";

    document.getElementById('dayC').hidden = true;
    document.getElementById('monthC').hidden = true;
    document.getElementById('yearC').hidden = false;
  }
}

function genChart(date, data, tableName) {
  //alert(""+ data)
  
  //data = data
  date = date.replace('[', '');
  date = date.replace(']', '');
  var labels = date.split(',');

  data = data.replace('[', '');
  data = data.replace(']', '');
  var values = data.split(',');
  
  //alert(""+ values)
  //alert(""+ labels)
  const ctx = document.getElementById("myChart").getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: tableName,
            data: values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
  });
}
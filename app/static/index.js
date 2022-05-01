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

//Uses google maps geocode API to generate marker at postcode
//Refocuses map and returns
function showLocation() {
  var mapDict = {
    "Trinity centre" : ["27 Albion St, Leeds LS1 5AT"],
    "Train Station": ["New Station St, Leeds LS1 4DY"],
    "Merrion centre": ["Merrion Way, Leeds LS2 8NG"],
    "LRI hospital": ["Infirmary Square, Leicester LE1 5WW"],
    "UoL Edge sports centre": ["University of Leeds, Willow Terrace Road, Leeds LS2 9JT"]
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

//Generates chart for displaying income data
//takes x/y data as comma seperated value strings
//uses chart.js to generate table on canvas
function genChart(date, data, tableName) {
  date = date.replace('[', '');
  date = date.replace(']', '');
  date = date.replaceAll('&#39;','');
  var labels = date.split(',');

  data = data.replace('[', '');
  data = data.replace(']', '');
  data = data.replace('undefined', '');
  data.replace('&#39;','');
  var values = data.split(',');

  var total = 0;
  for (var i = 0; i < values.length; i++)
    total += parseInt(values[i]);
  document.getElementById('totalIncome').innerHTML = total;


  document.getElementById('myChart').remove(); // this is my <canvas> element
  document.getElementById('graphContainer').innerHTML = '<canvas id="myChart" style="width:80%;height:400px;"></canvas>';
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

//Shows/hides bookings in the table for income
function showBookings(duration) {
  var dict = {
    0 : "1",
    1 : "4",
    2 : "24",
    3 : "168",
    4 : "all"
  };
  if (duration != 4) {
    var elements
    for (var i = 0; i < 4; i++) {
      elements = document.getElementsByClassName(dict[i]);
      for(var l = 0; l < elements.length; l++) {
        elements[l].hidden = true;
      }
    }
    var ele = document.getElementsByClassName(dict[duration]);
    for(var i = 0; i < ele.length; i++) {
      ele[i].hidden = false;
    }
  } else {
    for (i = 0; i < 4; i++) {
      //document.getElementById(dict[i]).hidden = false;
      var elements = document.getElementsByClassName(dict[i]);
      for(var l = 0; l < elements.length; l++) {
        elements[l].hidden = false;
      }
    }
  }
}


function showCost(duration, cost) {
  duration = duration.replace('[', '');
  duration = duration.replace(']', '');
  var dura = duration.split(',');

  cost = cost.replace('[', '');
  cost = cost.replace(']', '');
  var cos = cost.split(',');

  var scrollItem = document.getElementById("duration").value+"";

  for (var i = 0; i < cos.length; i++) {
    if (parseInt(scrollItem) == parseInt(dura[i])) {
      document.getElementById("costed").innerHTML = cos[i]+"";
    }
  }
}

function loadCard(cardArray) {
  var number = document.getElementById("cardSelect").value+"";
  var index;
  for (i = 0; i < cardArray.length; i++) {
    if (cardArray[i][0] == number) {
      index = i;
      break;
    }
  }
  document.getElementById("number").value = cardArray[i][0];
  document.getElementById("security_code").value = cardArray[i][1];
  document.getElementById("expiration_date").value = cardArray[i][2];
  document.getElementById("name").value = cardArray[i][3];

}

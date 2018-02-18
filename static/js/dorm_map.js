    var lastOpenedInfoWindow = null;

      function initMap() {
          var pomona = {lat: 34.098346, lng: -117.713507};
          var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 16,
              center: pomona
          });

          function addDormToMap(dorm) {
              var contentString = '<div id="content">' +
                      '<div id="siteNotice">' +
                      '</div>' +
                      `<h1 id="firstHeading" class="firstHeading">${dorm.name}</h1>` +
                      '<div id="bodyContent">' +
                      `<p><b>Overalls:</b> ${dorm.ratings.average_rating.toFixed(2)} </p>` +
                      `<p><b>Quietness:</b> ${dorm.ratings.average_rating_quiet.toFixed(2)} </p>` +
                      `<p><b>Spaciousness:</b> ${dorm.ratings.average_rating_spacious.toFixed(2)} </p>` +
                      `<p><b>Temperature:</b> ${dorm.ratings.average_rating_temperate.toFixed(2)} </p>` +
                      `<p><b>Maintenance:</b> ${dorm.ratings.average_rating_maintained.toFixed(2)} </p>` +
                      `<p><b>Cellphone Signal:</b> ${dorm.ratings.average_rating_cellphone.toFixed(2)} </p>` +
                      `<a href="${dorm.review_url}">Read reviews</a>`+
                      '</div>' +
                      '</div>';
              var infowindow = new google.maps.InfoWindow({
                  content: contentString
              });

              lastOpenedInfoWindow = infowindow;

              var marker = new google.maps.Marker({
                  position: dorm.position,
                  map: map,
                  title: dorm.name
              });
              marker.addListener('click', function () {
                  lastOpenedInfoWindow.close();
                  infowindow.open(map, marker);
                  lastOpenedInfoWindow = infowindow;
              });
          }


          $.ajax({
              url: '',
              type: 'POST',
              data: {
                csrfmiddlewaretoken: Cookies.get('csrftoken')
              },
              success: function (data) {
                  for (var i in data) {
                      addDormToMap(data[i]);
                  }
              },
              error: function(error) {
                  console.log(error.responseText);
              }
          })
      }
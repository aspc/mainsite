      var ctx = document.getElementById("reviews_barplot").getContext("2d");
      var ratings = document.getElementsByClassName("reviews_list-rating_score");
      var distrib = {1:0, 2:0, 3:0, 4:0, 5:0};
      for (var i=0; i<ratings.length; i++) {
          var rating = parseInt(ratings[i].textContent);
          distrib[rating]++;
      }
      for(var i in distrib){
          distrib[i] = Math.round(distrib[i] / ratings.length *100);
      }
      var data = {
        labels: ["1 star", "2 star", "3 star", "4 star", "5 star"],
        datasets: [
                    {
                        label: "My First dataset",
                        fillColor: "#0071a6",
                        strokeColor: "rgba(220,220,220,0.8)",
                        highlightFill: " #6699ff",
                        highlightStroke: "rgba(220,220,220,1)",
                        data: [distrib[1], distrib[2], distrib[3], distrib[4], distrib[5]]
                    }
                ]
            };
          new Chart(ctx).Bar(data, {
                barShowStroke: false,
               scaleShowGridLines : true,
               scaleShowLabels: true,
               barValueSpacing : 1,
               scaleShowValues: true,
              tooltipTemplate: "<%= value +'%'%>"
            });
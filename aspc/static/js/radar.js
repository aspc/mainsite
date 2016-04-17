var radar = document.getElementById("reviews_radar").getContext("2d");
var misc_ratings = document.getElementById('miscellaneous_ratings').value.split(',');
for (var i in misc_ratings){
    misc_ratings[i] = Math.round(parseFloat(misc_ratings[i])*100)/100;
}

var data = {
    labels: ["Usefulness", "Engagement", "Difficulty", "Competency", "Lecture style", "Enthusiasm", "Approachability"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: misc_ratings
        }
    ]
};

var myRadarChart = new Chart(radar).Radar(data, {});
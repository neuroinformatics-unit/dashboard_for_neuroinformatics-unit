make_plot();

function make_plot() {
  let data_to_plot = [];
  for (const [key, value] of Object.entries(loc_data)) {
    data_to_plot.push({ x: value["date"], y: value["loc"] });
  }
  var canvas = document.getElementById("lines_of_code_plot");
  var ctx = canvas.getContext("2d");

  //sort the data by date
  data_to_plot.sort(function (a, b) {
    var keyA = new Date(a.x);
    var keyB = new Date(b.x);
    return keyA - keyB;
  });

  var data = {
    datasets: [
      {
        data: data_to_plot,
        showLine: true,
        pointBackgroundColor: "rgba(0,0,0,1.0)",
      },
    ],
  };

  var myChart = new Chart(ctx, {
    type: "scatter",
    data,
    options: {
      responsive: true,
      legend: {
        display: false,
      },
      title: {
        text: "Lines of Code",
        display: true,
      },
      scales: {
        yAxes: [
          {
            scaleLabel: {
              labelString: "Lines of Code",
              display: true,
            },
          },
        ],
        xAxes: [
          {
            scaleLabel: {
              labelString: "date",
              display: true,
            },
            type: "time",
            position: "bottom",
          },
        ],
      },
    },
  });
}

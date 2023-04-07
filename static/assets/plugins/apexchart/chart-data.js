'use strict';

$(document).ready(function() {


  // var options = {
  //   series:   $("#chartradial").data('chart-data'),
  //   chart: {
  //   width: '100%',
  //   type: 'pie',
  // },
  // labels:  ['Active','Pending','Ongoing','Completed','Cancelled'],
  // theme: {
  //   monochrome: {
  //     enabled: true
  //   }
  // },
  // plotOptions: {
  //   pie: {
  //     dataLabels: {
  //       offset: -5
  //     }
  //   }
  // },
  // title: {
  //   text: "Project Chart Info"
  // },
  // dataLabels: {
  //   formatter(val, opts) {
  //     const name = opts.w.globals.labels[opts.seriesIndex]
  //     return [name, val.toFixed(1) + '%']
  //   }
  // },
  // legend: {
  //   show: false
  // }
  // };

  // var chart = new ApexCharts(document.querySelector("#chartradial"), options);
  // chart.render();













// --- Project Chhart ------


var options = {
  series: [{
  name: 'No. of Projects',
  data:$("#chartradial").data('chart-data'),
  }],

  chart: {
  height: 350,
  type: 'bar',
  },
  plotOptions: {
  bar: {
    borderRadius: 10,
    columnWidth: '50%',
  }
  },
  dataLabels: {
  enabled: false
  },
  stroke: {
  width: 2
  },
  
  grid: {
  row: {
    colors: ['#fff', '#f2f2f2']
  }
  },
  xaxis: {
  labels: {
    rotate: -45
  },
  //categories: label.split(','),
  categories: ['Active', 'Pending', 'Ongoing', 'Completed', 'Cancelled'],
  
  tickPlacement: 'on'
  },
  yaxis: {
  title: {
    text: 'Number of projects',
  },
  labels: {
    formatter: function(val) {
      return val.toFixed(0);
    }
    }
  
  },
  fill: {
  type: 'gradient',
  gradient: {
    shade: 'light',
    type: "horizontal",
    shadeIntensity: 0.25,
    gradientToColors: undefined,
    inverseColors: true,
    opacityFrom: 0.85,
    opacityTo: 0.85,
    stops: [50, 0, 100]
  },
  }
  };

  var chart = new ApexCharts(document.querySelector("#chartprofile"), options);
  chart.render();

  
});
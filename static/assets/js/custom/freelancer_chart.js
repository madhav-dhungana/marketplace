

var options = {
    series: [{
    name: 'No. of Projects',
    data:$("#chartprofile").data('chart-data'),
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
    categories: [ 'Ongoing', 'Completed', 'Cancelled'],
    
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
  
    
  
<template>
    <div>
      <div id="myBarChart"></div>
    </div>
  </template>
  
  <script>
  import Plotly from 'plotly.js/dist/plotly';
  
  export default {
    name: "BarChart",
    data: () => ({
    BarPlotData: {x: [], y: []}
  }),
    props: {
      position: {
        type: String,
        required: true,
      },
      gender: {
        type: String,
        required: true,
      },
    },
    watch: {
      position: function() {
        this.BarPlotData.x = [];
        this.BarPlotData.y = [];
        this.fetchData();
      },
      gender: function() {
        this.BarPlotData.x = [];
        this.BarPlotData.y = [];
        this.fetchData();
      }
    },
    methods: {
      async fetchData() {
        const dict_pos = {'GK': '0', 'CF': '1', 'LM': '2', 'RM': '3', 'CM': '4', 'CB': '5', 'LB': '6', 'RB': '7'};
        const dict_gender = {'female': 0, 'male': '1'}
        var reqUrl = 'http://127.0.0.1:5000/ranks/' + dict_gender[this.gender] + '/' + dict_pos[this.position]
        const response = await fetch(reqUrl);
        const data = await response.json();
        console.log(data);
        data.forEach(player => {
          this.BarPlotData.x.push(player.short_name);
          this.BarPlotData.y.push(player.overall);
        });
        this.drawBarChart();
      },
      drawBarChart() {
        var trace1 = {
          x: this.BarPlotData.x,
          y: this.BarPlotData.y,
          type: 'bar',
          marker: {
            color: 'rgb(26, 118, 255)',
            opacity: 0.6,
            line: {
              color: 'rgb(8,48,107)',
              width: 1.5
            }
          }
        };
        var data = [trace1];
        var layout = {
          title: 'Ranking of ' + this.position + ' players',
          yaxis: {
            title: 'Performance',
            range: [80, 95]
          },
        };
        Plotly.newPlot('myBarChart', data, layout);
      },
      
    },
    mounted() {
      this.fetchData();
    },
  };
  </script>
  
  <style scoped>
    #myBarChart {
        position: relative;
        margin-top: -250px;
        width: 600px;
        height: 400px;
    }
  </style>
  
  
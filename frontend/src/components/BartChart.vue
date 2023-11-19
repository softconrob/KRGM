<template>
    <div>
      <div id="myBarChart"></div>
      <button @click="closeChart">Close Chart</button>
    </div>
  </template>
  
  <script>
  import Plotly from 'plotly.js/dist/plotly';
  
  export default {
    name: "BarChart",
    props: {
      data: Object,
    },
    methods: {
      drawBarChart() {
        var trace1 = {
          x: Object.keys(this.data),
          y: Object.values(this.data),
          type: 'bar',
        };
        var data = [trace1];
        var layout = {
          title: 'Ranking of players',
          xaxis: {
            title: 'Player',
          },
          yaxis: {
            title: 'Performance',
          },
        };
        Plotly.newPlot('myBarChart', data, layout);
      },
      closeChart() {
        this.$emit('close');
      },
    },
    mounted() {
      this.drawBarChart();
    },
  };
  </script>
  
  <style scoped>
    #myBarChart {
        width: 600px;
        height: 400px;
    }
  button {
    margin-top: 10px;
    cursor: pointer;
  }
  </style>
  
  
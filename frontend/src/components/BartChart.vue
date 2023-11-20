<template>
    <div>
      <div id="myBarChart"></div>
    </div>
  </template>
  
  <script>
  import Plotly from 'plotly.js/dist/plotly';
  
  export default {
    name: "BarChart",
    props: {
      position: {
        type: String,
        required: true,
      },
    },
    watch: {
      position: function() {
        this.drawBarChart();
        console.log('position changed');
      }
    },
    methods: {
      drawBarChart() {
        var trace1 = {
          x: Object.keys(this.getDataForPosition(this.position)),
          y: Object.values(this.getDataForPosition(this.position)),
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
          },
        };
        Plotly.newPlot('myBarChart', data, layout);
      },
      getDataForPosition(position) {
        const data = {
          CF: {
            'Lionel Messi': 100,
            'Cristiano Ronaldo': 90,
            'Neymar': 80,
            'Robert Lewandowski': 70,
            'Harry Kane': 60,
          },
          CM: {
            'Kevin De Bruyne': 100,
            'Luka Modric': 90,
            'N\'Golo Kanté': 80,
            'Toni Kroos': 70,
            'Paul Pogba': 60,
          },
          CB: {
            'Sergio Ramos': 100,
            'Virgil van Dijk': 90,
            'Raphael Varane': 80,
            'Gerard Piqué': 70,
            'Giorgio Chiellini': 60,
          },
          LB: {
            'Marcelo': 100,
            'Jordi Alba': 90,
            'Alex Sandro': 80,
            'David Alaba': 70,
            'Andrew Robertson': 60,
          },
          RB: {
            'Dani Alves': 100,
            'Joshua Kimmich': 90,
            'Kyle Walker': 80,
            'Sergio Roberto': 70,
            'César Azpilicueta': 60,
          },
          LM: {
            'Eden Hazard': 100,
            'Sadio Mané': 90,
            'Marco Reus': 80
          },
          RM: {
            'Mohamed Salah': 100,
            'Gareth Bale': 90,
            'Bernardo Silva': 80
          },
          GK: {
            'Jan Oblak': 100,
            'David de Gea': 90,
            'Thibaut Courtois': 80
          },
        };
        return data[position];
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
  
  
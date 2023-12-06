<template>
    <div>
      <div id="myRadarChart"></div>
    </div>
  </template>

<script>
import Plotly from 'plotly.js/dist/plotly';

export default {
    name: 'RadarChart',
    data: () => ({
        Player1: {id:0, name:'', x: [], y: []},
        Player2: {id:0, name:'', x: [], y: []},
    }),
    props: {
        player1Id: {
            type: Number,
            required: true,
        },
        player2Id: {
            type: Number,
            required: true,
        },
    },
    watch: {
        player1Id: function() {
            this.Player1.id = this.player1Id;
            this.Player1.x = [];
            this.Player1.y = [];
            this.fetchData(this.player1Id);
        },
        player2Id: function() {
            this.Player2.id = this.player2Id;
            this.Player2.x = [];
            this.Player2.y = [];
            this.fetchData(this.player2Id);
        }
    },
    methods: {
        async fetchData(playerId) {
            var reqUrl = 'http://127.0.0.1:5000/players/' + playerId;
            const response = await fetch(reqUrl);
            const data = await response.json();
            if (playerId == this.player1Id) {
                this.Player1.name = data.short_name;
                this.Player1.x = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physic', 'attacking', 'skill', 'movement', 'power', 'mentality','goalkeeping'];
                this.Player1.y = [data.pace, data.shooting, data.passing, data.dribbling, data.defending, data.physic, data.attacking, data.skill, data.movement, data.power, data.mentality, data.goalkeeping];
            } else {
                this.Player2.name = data.short_name;
                this.Player2.x = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physic', 'attacking', 'skill', 'movement', 'power', 'mentality','goalkeeping'];
                this.Player2.y = [data.pace, data.shooting, data.passing, data.dribbling, data.defending, data.physic, data.attacking, data.skill, data.movement, data.power, data.mentality, data.goalkeeping];
            }
            this.drawRadarChart();
        },

        drawRadarChart() {
            var data = [
                {
                    type: 'scatterpolar',
                    r: this.Player1.y,
                    theta: this.Player1.x,
                    fill: 'toself',
                    name: this.Player1.name,
                    marker: {
                        color: 'rgba(255, 0, 0, 0.5)',
                        symbol: 'square',
                        size: 8
                    },
                    line: {
                        color: 'rgba(255, 0, 0, 0.5)',
                        width: 3
                    }
                },
                {
                    type: 'scatterpolar',
                    r: this.Player2.y,
                    theta: this.Player2.x,
                    fill: 'toself',
                    name: this.Player2.name,
                    marker: {
                        color: 'rgba(0, 0, 255, 0.5)',
                        symbol: 'square',
                        size: 8
                    },
                    line: {
                        color: 'rgba(0, 0, 255, 0.5)',
                        width: 3
                    }
                }
            ];
            var layout = {
                polar: {
                    radialaxis: {
                        visible: true,
                        range: [0, 100]
                    },
                    tickfont: {
                        size: 15,
                        color: '#333',
                        weight: 'bold'
                    },
                },
                margin: {
                    l: 20,
                    r: 20,
                    b: 20,
                    t: 30,
                    pad: 10
                },
                showlegend: true,
                legend: {
                    x: 0.5,
                    y: 1.2,
                    orientation: "h"
                }
            };
            Plotly.newPlot('myRadarChart', data, layout);
        }
    },
    mounted() {
        this.fetchData(this.player1Id);
        this.fetchData(this.player2Id);
    }
};
</script>

<style scoped>
#myRadarChart {
    position: relative;
    margin-top: -250px;
    width: 600px;
    height: 400px;
}
</style>


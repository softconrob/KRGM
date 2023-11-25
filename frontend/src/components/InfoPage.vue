<template>
    <div class="player-info">
        <img :src= playerInfo.faceurl alt="Player Picture">
        <img :src= playerInfo.nation_flag_url alt="Player Picture">
        <div class="info-item">
            <span>{{ playerInfo.name }}</span>
            <span>Age: {{ playerInfo.age }}</span>
        </div>  
        <div class="chart" id="attribute1"></div>
        <div class="chart" id="attribute2"></div>
    </div>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
    name: 'InfoPage',
    data: () => ({
        playerInfo: {faceurl: '', name: '', age: '', nation_flag_url: ''},
    }),
    props: {
        sofifaid: {
            type: String,
            required: true
        },
    },
    watch: {
        sofifaid: function() {
            this.fetchData();
        }
    },  
    methods: {
        async fetchData() {
            var reqUrl = 'http://127.0.0.1:5000/players/' + this.sofifaid;
            const response = await fetch(reqUrl);
            const data = await response.json();
            this.playerInfo.nation_flag_url = data.nation_flag_url;
            this.playerInfo.faceurl = data.player_face_url;
            this.playerInfo.name = data.short_name;
            this.playerInfo.age = data.age;
            this.playerInfo.attributes = data.attacking;
            let attributes1 = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic'];
            let values1 = [data.pace, data.shooting, data.passing, data.dribbling, data.defending, data.physic];
            let attributes2 = ['attacking', 'skill', 'movement', 'power', 'mentality','goalkeeping'];
            let values2 = [data.attacking, data.skill, data.movement, data.power, data.mentality, data.goalkeeping];
            this.drawRadarChart("attribute1", attributes1, values1);
            this.drawRadarChart("attribute2", attributes2, values2);
        },
        drawRadarChart(chartId, k, v) {
            // draw radar chart for player attributes 
            const attributes = k;
            const values = v;
            const trace = {
                type: 'scatterpolar',
                r: values,
                theta: attributes,
                fill: 'toself',
                fillcolor: 'rgba(0, 0, 255, 0.1)',
                line: {
                    color: 'rgba(0, 0, 255, 0.5)',
                }
            };
            const layout = {
                title: {
                    font: {
                        size: 14,
                        color: '#333',
                    },
                    xref: 'paper',
                    x: 0.05,
                },
                width: 200,
                height: 200,
                margin: {
                    l: 20,
                    r: 20,
                    b: 20,
                    t: 30,
                    pad: 10
                },
                polar: {
                    radialaxis: {
                        visible: false,
                        range: [0, 100]
                    },
                    angularaxis: {
                    showticklabels: true,
                    tickfont: {
                        size: 12,
                        color: '#333',
                    }
                    }   
                },
                
                showlegend: false
            };
            Plotly.newPlot(chartId, [trace], layout);      
        },
        
    },
    mounted () {
        this.fetchData();
    }

};
</script>

<style scoped>
.player-info {
    position: fixed;
    bottom: 50px;
    width: 1200px;
    height: 250px;
    display: flex;
    justify-content: space-around; 
    align-items: center;
    background-color: aliceblue;
}
.player-info img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 20px;
}
.player-info .info-item {
    display: flex;
    flex-direction: column;
    color: #333;
}
.player-info .info-item span {
    font-size: 2em;
}
.player-info .chart {
    width: 200px;
    height: 200px;
}

</style>
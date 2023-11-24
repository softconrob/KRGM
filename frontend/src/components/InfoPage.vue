<template>
    <div class="player-info">
        <img :src="'https://cdn.sofifa.net/players/188/545/22_120.png'" alt="Player Picture">
        <div class="info-item">
            <span>Player Name</span>
            <span>Age</span>
        </div>  
        <div class="chart" id="attributeChart1"></div>
        <div class="chart" id="attributeChart2"></div>

    </div>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
    name: 'InfoPage',
    props: {
        sofifaid: {
            type: String,
            required: true
        },
    },
    watch: {
        sofifaid: function() {
            const data = this.getPlayerInfo();
            const chart1 = 'attributeChart1';
            const chart2 = 'attributeChart2';
            this.showPlayerInfo(data, chart1);
            this.showPlayerInfo(data, chart2);
            console.log(this.sofifaid);
        }
    },  
    methods: {
        showPlayerInfo(data, chart) {
            // draw radar chart for player attributes 
            const attributes = Object.keys(data.attributes);
            const values = Object.values(data.attributes);
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
                width: 200,
                height: 200,
                margin: {
                    l: 20,
                    r: 20,
                    b: 20,
                    t: 20,
                    pad: 20
                },
                polar: {
                    radialaxis: {
                        visible: false,
                        range: [0, 100]
                    },
                    angularaxis: {
                    showticklabels: true,
                    tickfont: {
                        size: 8,
                        color: '#333',
                    }
                    }   
                },
                
                showlegend: false
            };
            Plotly.newPlot(chart, [trace], layout);      
        },
        getPlayerInfo(){
            // get player info from API, currently hard coded
            const data = {
                name: 'Lionel Messi',
                age: 34,
                attributes: {
                    pace: 85,
                    shooting: 92,
                    passing: 91,
                    dribbling: 95,
                    defending: 38,
                    physical: 65,
                }
            }
            return data;

        }
    },
    mounted () {
        this.showPlayerInfo();
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
    font-size: 1.2em;
}
.player-info .chart {
    width: 150px;
    height: 150px;
}

</style>
<template>
    <div class="player-info">
        <img :src="'https://cdn.sofifa.net/players/188/545/22_120.png'" alt="Player Picture">
        <div class="info-item">
            <span>Player Name</span>
            <span>Age</span>
        </div>  
        <div id="attributeChart"></div>

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
            this.showPlayerInfo();
            console.log(this.sofifaid);
        }
    },  
    methods: {
        showPlayerInfo() {
            // draw radar chart for player attributes 
            const data = this.getPlayerInfo();
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
                width: 100,
                height: 100,
                margin: {
                    l: 0,
                    r: 0,
                    b: 0,
                    t: 0,
                    pad: 0
                },
                polar: {
                    radialaxis: {
                        visible: true,
                        range: [0, 100]
                    },
                    angularaxis: {
                    showticklabels: false,
                    }   
                },
                
                showlegend: false
            };
            Plotly.newPlot('attributeChart', [trace], layout);      
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
    width: 80%;
    height: 150px;
    display: flex;
    justify-content: space-around; 
    align-items: center;
    background-color: aliceblue;
}
.player-info img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 20px;
}
.player-info .info-item {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #333;
}
.player-info .info-item span {
    font-size: 1.2em;
    
}

</style>
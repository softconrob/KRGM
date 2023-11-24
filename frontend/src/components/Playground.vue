<template>
  <div class="container">
    <div class="playground">
      <img src="@/assets/field.jpeg" alt="Field"  />
      <Player :top="10" :left="200" :position="'CF'" @showBarChart="showBarChart"/>
      <Player :top="10" :left="350" :position="'CF'" @showBarChart="showBarChart" />
      <Player :top="100" :left="20" :position="'LM'" @showBarChart="showBarChart" />
      <Player :top="100" :left="500" :position="'RM'" @showBarChart="showBarChart" />
      <Player :top="150" :left="200" :position="'CM'" @showBarChart="showBarChart" />
      <Player :top="150" :left="350" :position="'CM'" @showBarChart="showBarChart" />
      <Player :top="250" :left="200" :position="'CB'" @showBarChart="showBarChart" />
      <Player :top="250" :left="350" :position="'CB'" @showBarChart="showBarChart" />
      <Player :top="200" :left="20" :position="'LB'" @showBarChart="showBarChart" />
      <Player :top="200" :left="500" :position="'RB'" @showBarChart="showBarChart" />
      <Player :top="300" :left="270" :position="'GK'" @showBarChart="showBarChart" />
    </div>
    <BarChart :position="selectedPosition" />
    <InfoPage :sofifaid="sofifaid" />
  </div>
  
</template>
  
  <script>
  import Player from './Player.vue';
  import BarChart from "./BartChart.vue";
  import InfoPage from "./InfoPage.vue";

  export default {
  name: 'Playground',
  prps: {
    gender: {
      type: String,
      required: true,
    },

  },
  components: {
    Player,
    BarChart,
    InfoPage
},
  data() {
    return {
      selectedPosition: 'CF',
      showChart: false,
      showPage: false,
      sofifaid: '158023',
    };
  },
  methods: {
    showBarChart(position) {
      this.showChart = true;
      this.selectedPosition = position;
      this.showPage = true;
      this.sofifaid = '158024';
    },
    
  },
};
  </script>
  
  
  <style scoped>

  .container {
    display: flex;
  }
  .playground {
    position: relative;
    margin-top: -250px;
    width: 600px; 
    height: 400px; 
    background-color: green; 
  }
  .playground img {
    transform: rotate(180deg);
    width: 100%;
    height: 100%;
  }
  </style>
  
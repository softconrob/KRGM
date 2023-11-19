<template>
  <div class="football-container">
    

    <div class="football-playground">
      <img src="@/assets/field.jpeg" alt="Field"  />
      <slot></slot>
      <Player ref="player1" :top="10" :left="200" :position="'CF'" @click="showBarChart" />
      <Player ref="player2" :top="10" :left="350" :position="'CF'" @click="showBarChart" />
      <Player ref="player3" :top="100" :left="20" :position="'LM'" @click="showBarChart" />
      <Player ref="player4" :top="100" :left="500" :position="'RM'" @click="showBarChart" />
      <Player ref="player5" :top="150" :left="200" :position="'CM'" @click="showBarChart" />
      <Player ref="player6" :top="150" :left="350" :position="'CM'" @click="showBarChart" />
      <Player :top="250" :left="200" :position="'CB'" @click="showBarChart" />
      <Player :top="250" :left="350" :position="'CB'" @click="showBarChart" />
      <Player :top="200" :left="20" :position="'LB'" @click="showBarChart" />
      <Player :top="200" :left="500" :position="'RB'" @click="showBarChart" />
      <Player :top="300" :left="270" :position="'GK'" @click="showBarChart" />
    </div>
    <!-- Bar chart component -->
    <BarChart v-if="showChart" :data="chartData" @close="closeBarChart" />
  </div>
</template>
  
  <script>
  import Player from './Player.vue';
  import BarChart from "./BartChart.vue";

  export default {
  name: 'Playground',
  components: {
    Player,
    BarChart,
  },
  data() {
    return {
      showChart: false,
      chartData: {},
    };
  },
  methods: {
    showBarChart() {
      this.showChart = true;
      this.chartData = {
        bar1: 50,
        bar2: 30,
        bar3: 70,
        bar4: 60,
        bar5: 90,

      };
    },
    closeBarChart() {
      // Set showChart to false to hide the bar chart
      this.showChart = false;
    },
  },
};
  </script>
  
  
  <style scoped>

  .football-container {
    display: flex;
  }
  .football-playground {
    position: relative;
    width: 600px; 
    height: 400px; 
    background-color: green; 
  }
  img {
    transform: rotate(180deg);
    width: 100%;
    height: 100%;
  }
  </style>
  
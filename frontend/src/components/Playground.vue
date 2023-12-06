<template>
  <div class="container">
    <div class="playground">
      <img src="@/assets/field.jpeg" alt="Field" />
      <Player
        v-for="player in players"
        :key="player.pref"
        :pref="player.pref"
        :top="player.top"
        :left="player.left"
        :position="player.position"
        :pid="player.pid"
        @showBarChart="showBarChart"
      />
    </div>
    <BarChart v-show="showBar" :position="selectedPosition" :gender="selectedGender" @showInfoPage="showInfoPage" />
    <RadarChart v-show="showRadar" :player1Id="sofifaid" :player2Id="player2Id" />
    <InfoPage v-show="showInfo" :sofifaid=sofifaid @comparePlayer="comparePlayer" />
  </div>
</template>

<script>
import Player from "./Player.vue";
import BarChart from "./BarChart.vue";
import RadarChart from "./RadarChart.vue";
import InfoPage from "./InfoPage.vue";

export default {
  name: 'Playground',
  props: {
    gender: {
      type: String,
      required: true,
    },
  },
  components: {
    Player,
    BarChart,
    InfoPage,
    RadarChart,
  },
  data() {
    return {
      selectedPosition: 'CF',
      selectedGender: 'male',
      sofifaid: 0,
      selectedPlayersRef: '',
      showBar: false,
      showRadar: false,
      showInfo: false,
      player2Id: 0,
      players: [
        { pref: 0, top: 10, left: 200, position: 'CF', pid: 0 },
        { pref: 1, top: 10, left: 350, position: 'CF', pid: 0 },
        { pref: 2, top: 100, left: 20, position: 'LM', pid: 0 },
        { pref: 3, top: 100, left: 500, position: 'RM', pid: 0 },
        { pref: 4, top: 150, left: 200, position: 'CM', pid: 0 },
        { pref: 5, top: 150, left: 350, position: 'CM', pid: 0 },
        { pref: 6, top: 250, left: 200, position: 'CB', pid: 0 },
        { pref: 7, top: 250, left: 350, position: 'CB', pid: 0 },
        { pref: 8, top: 200, left: 20, position: 'LB', pid: 0 },
        { pref: 9, top: 200, left: 500, position: 'RB', pid: 0 },
        { pref: 10, top: 300, left: 270, position: 'GK', pid: 0 },
      ],
    };
  },
  methods: {
    showBarChart(position, pref) {
      this.showRadar = false;
      this.showBar = true;
      this.selectedPosition = position;
      this.selectedPlayersRef = pref;
    },
    showInfoPage(sofifaid) {
      this.showInfo = true;
      this.sofifaid = sofifaid;
      // change the pid of the selected player
      this.players[this.selectedPlayersRef].pid = sofifaid;
      console.log(this.players[this.selectedPlayersRef].pid);
    },
    comparePlayer(pid) {
      this.showBar = false;
      this.showRadar = true;
      this.player2Id = pid;
    },
  },
  watch: {
    gender() {
      this.selectedGender = this.gender;
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

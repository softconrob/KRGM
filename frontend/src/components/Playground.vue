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
    <BarChart :position="selectedPosition" :gender="selectedGender" :playerRef="selectedPlayersRef" @showInfoPage="showInfoPage" />
    <InfoPage :sofifaid=sofifaid />
  </div>
</template>

<script>
import Player from "./Player.vue";
import BarChart from "./BarChart.vue";
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
  },
  data() {
    return {
      selectedPosition: 'CF',
      selectedGender: 'male',
      sofifaid: 158023,
      selectedPlayersRef: '',
      players: [
        { pref: 0, top: 10, left: 200, position: 'CF', pid: 0 },
        { pref: 1, top: 10, left: 350, position: 'CF', pid: 1 },
        { pref: 2, top: 100, left: 20, position: 'LM', pid: 2 },
        { pref: 3, top: 100, left: 500, position: 'RM', pid: 3 },
        { pref: 4, top: 150, left: 200, position: 'CM', pid: 4 },
        { pref: 5, top: 150, left: 350, position: 'CM', pid: 5 },
        { pref: 6, top: 250, left: 200, position: 'CB', pid: 6 },
        { pref: 7, top: 250, left: 350, position: 'CB', pid: 7 },
        { pref: 8, top: 200, left: 20, position: 'LB', pid: 8 },
        { pref: 9, top: 200, left: 500, position: 'RB', pid: 9 },
        { pref: 10, top: 300, left: 270, position: 'GK', pid: 10 },
      ],
    };
  },
  methods: {
    showBarChart(position, pref) {
      this.selectedPosition = position;
      this.selectedPlayersRef = pref;
    },
    showInfoPage(sofifaid) {
      this.sofifaid = sofifaid;
      // change the pid of the selected player
      this.players[this.selectedPlayersRef].pid = sofifaid;
      console.log(this.players[this.selectedPlayersRef].pid);
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

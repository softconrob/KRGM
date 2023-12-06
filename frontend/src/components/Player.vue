<template>
  <div class="football-player" :style="{ top: `${top}px`, left: `${left}px` }" @click="handleClick">
    <img :src=imgSrc alt="Player" />
    <span class="player-position" v-show="showPosition">{{ position }}</span>
  </div>
</template>

<script>
import { T } from 'plotly.js/dist/plotly';

export default {
  name: 'Player',
  data() {
    return {
      imgSrc: 'src/assets/player.svg',
      showPosition: true,
    };
  },
  props: {
    top: {
      type: Number,
      required: true,
    },
    left: {
      type: Number,
      required: true,
    },
    position: {
      type: String,
      default: 'forward',
    },
    pref: {
      type: Number,
      required: true,
    },
    pid: {
      type: Number,
      required: true,
    },
  },
  watch: {
    pid: function() {
      this.showPosition = false;
      this.fetchData();
  },
},
  methods: {
    handleClick() {
      // Emit a 'showBarChart' event with the player's position and reference
      this.$emit('showBarChart', this.position, this.pref );
    },
    async fetchData() {
      var reqUrl = 'http://127.0.0.1:5000/players/' + this.pid;
      const response = await fetch(reqUrl);
      const data = await response.json();
      this.imgSrc = data.player_face_url;
  },
},
  mounted() {
    this.fetchData();
  },
};

</script>

<style scoped>
.football-player {
  position: absolute;
  width: 70px;
  height: 70px;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensure the image covers the container */
}

.player-position {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 20px;
  color: white;
}
</style>

  
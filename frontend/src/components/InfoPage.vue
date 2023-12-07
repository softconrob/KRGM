<template>
    <div class="alternatives">
      <ul class="players">
        <li
          v-for="player in similarPlayers"
          :key="player.sofifa_id"
          @click="pickPlayer(player)"
          :class="{ 'selected-player': player.isSelected }"
          class="player-item"
        >
          <img :src="player.player_face_url" alt="Img" class="player-img" @error="setDefaultImage" />
          <div class="profile">
            <span class="player-name">{{ player.short_name }}</span>
            <span class="player-info">{{ player.nationality_name }} - {{ player.age }} years</span>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import Plotly from 'plotly.js/dist/plotly';
  
  export default {
    name: 'InfoPage',
    data: () => ({
      playerInfo: { faceurl: '', name: '', age: '', nation_flag_url: '' },
      similarPlayers: [],
    }),
    props: {
      sofifaid: {
        type: Number,
        required: true,
        default: 0,
      },
    },
    watch: {
      sofifaid: function () {
        this.fetchData();
      },
    },
    methods: {
      async fetchData() {
        var reqUrl1 = 'http://127.0.0.1:5000/players/' + this.sofifaid;
        const response1 = await fetch(reqUrl1);
        const data1 = await response1.json();
        this.playerInfo.nation_flag_url = data1.nation_flag_url;
        this.playerInfo.faceurl = data1.player_face_url;
        this.playerInfo.name = data1.short_name;
        this.playerInfo.age = data1.age;
        var reqUrl = 'http://127.0.0.1:5000/players/similar/' + this.playerInfo.name;
        const response = await fetch(reqUrl);
        const data = await response.json();
        this.similarPlayers = data.map((player) => ({ ...player, isSelected: false }));
      },
      pickPlayer(player) {
        this.similarPlayers.forEach((p) => (p.isSelected = false));
        // Toggle the isSelected property for the clicked player
        player.isSelected = !player.isSelected;
        this.$emit('comparePlayer', player.sofifa_id);
      },
      setDefaultImage(event) {
        event.target.src = 'src/assets/missing.jpeg';
      },
      setDefaultImageNation(event) {
        event.target.src = 'src/assets/earth.jpeg';
      },
    },
    mounted() {
      this.fetchData();
    },
  };
  </script>
  
  <style scoped>
  .alternatives {
    position: fixed;
    bottom: 50px;
    width: 1200px;
    height: 250px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: aliceblue;
    /* Use flexbox to display items in a row */
  }
  
  .players {
    list-style: none;
    display: flex;
    /* Display list items in a row */
    margin: 0;
    padding: 0;
  }
  
  .player-item {
    margin-right: 20px;
    /* Adjust the spacing between players */
  }
  
  .player-img {
    width: 100px;
    /* Adjust the image width as needed */
    height: auto;
    border-radius: 5px;
    /* Add border-radius for rounded corners */
  }
  
  .profile {
    display: flex;
    flex-direction: column;
    /* Display the player name and info in a column */
  }

    .player-info {
        display: block;
        text-align: center;
        margin-top: 5px;
        /* Adjust the spacing between image and name */
    }
  .player-name {
    display: block;
    text-align: center;
    margin-top: 5px;
    /* Adjust the spacing between image and name */
  }
  
  .selected-player {
    background-color: rgb(48, 221, 178); /* Apply a green background to selected player */
  }
  </style>
  
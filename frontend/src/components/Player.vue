<template>
    <div class="football-player" :style="{ top: `${top}px`, left: `${left}px` }" @click="handleClick">
        <img src="@/assets/player.svg" alt="Player" />
        <span class="player-position">{{ position }}</span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Player',
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
    },
    methods: {
    handleClick() {
      // Emit a 'showBarChart' event with the player's position
      this.$emit('showBarChart', this.position);
    },
  },
  };
  </script>
  
  <style scoped>
  .football-player {
    position: absolute;
    width: 60px; 
    height: 60px; 
    
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
  
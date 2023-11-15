<template>
    <div id="app">
      <Playground>
        <Player :top="10" :left="200" :position="'CF'"/>
        <Player :top="10" :left="350" :position="'CF'"/>
        <Player :top="100" :left="20" :position="'LM'"/>
        <Player :top="100" :left="500" :position="'RM'"/>
        <Player :top="150" :left="200" :position="'CM'"/>
        <Player :top="150" :left="350" :position="'CM'"/>
        <Player :top="250" :left="200" :position="'CB'"/>
        <Player :top="250" :left="350" :position="'CB'"/>
        <Player :top="200" :left="20" :position="'LB'"/>
        <Player :top="200" :left="500" :position="'RB'"/>
        <Player :top="300" :left="270" :position="'GK'"/>

      </Playground>
    </div>
  </template>
  
  <script>
  import Playground from './components/Playground.vue';
  import Player from './components/Player.vue';
  
  export default {
    name: 'App',
    components: {
      Playground,
      Player,
    },
  };
  </script>
  
  <style>
  #app {
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  </style>
  
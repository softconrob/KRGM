<template>
    <div id="app">
    <Playground> </Playground>  
    </div>
  </template>
  
  <script>
  import Playground from './components/Playground.vue';
  
  export default {
    name: 'App',
    components: {
      Playground,
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
  
<template>
    <div class="football-playground">
        <img src="@/assets/field.jpeg" alt="Field" width="600" height="360"  />
      <slot></slot>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Playground',
  };
  </script>
  
  <style scoped>
  .football-playground {
    position: relative;
    width: 600px; 
    height: 360px; 
    background-color: green; 
  }
  img {
    transform: rotate(180deg);
  }
  </style>
  
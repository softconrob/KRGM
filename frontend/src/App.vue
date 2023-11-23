<template>
  <div id="app">
    <!-- Configuration Panel -->
    <div class="panel">
      <label for="gender">Gender: </label>
      <select id="gender" v-model="gender">
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>
    </div>
    <Playground :gender="gender"></Playground>  
  </div>
</template>

<script>
import Playground from './components/Playground.vue';

export default {
  name: 'App',
  components: {
    Playground,
  },
  data() {
    return {
      gender: 'male', // default value
    };
  },
};
</script>

<style>
#app {
  text-align: center;
}
body {
  background-color: #2d4e02; 
}
.panel {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #0b4c01;
  border-radius: 5px;
  background-color: #9fd257;
  z-index: 1000; 
}
.panel label {
  font-size: 1.3em;
  color: #333;
}
.panel select {
  font-size: 1.3em;
  color: #333;
  margin-left: 10px;
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #333;
}
.panel select:focus {
  outline: none;
}
.panel select option {
  color: #333;
}
</style>

  
<template>
    <div class="player-info">
        <img :src="'https://cdn.sofifa.net/players/188/545/22_120.png'" alt="Player Picture">
        <p>Player Name</p>
        <p>Player Age</p>
        <p>Nationality</p>
        <p>Club</p>

    </div>
</template>

<script>
export default {
    props: {
        sofifaid: {
            type: String,
            required: true
        },
    }
};
</script>

<style scoped>
.player-info {
    position: fixed;
    bottom: 50px;
    width: 80%;
    display: flex;
    justify-content: space-around; 
    background-color: aliceblue;
}
</style>
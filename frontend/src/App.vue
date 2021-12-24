<template>
    <router-view/>
</template>

<script>
    export default {
        name: 'App'
    }
</script>

<style>
    body {
        margin: 0px ;
        background-color: #121212;
        color: #fff;
    }
    #app {
        font-family: Georgia, Arial, sans-serif;
        margin-left: 0px;
        margin-right: 0px;
    }

    @media only screen and (min-width: 321px) and (max-width: 768px) {
    #app {
        max-width: 100%;
        height: auto;
        position: relative;
    }

    .content {
        max-width: 300px;
        margin: 0 auto;

    }
    }
</style>
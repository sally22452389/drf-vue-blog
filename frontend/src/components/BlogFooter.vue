<template>
    <!--  br 頁尾留出位置  -->
    <br><br><br>
    <div id="footer">
        <p>icemaple.net</p>
    </div>
</template>

<script>
    export default {
        name: 'BlogFooter'
    }
</script>

<style scoped>
    #footer {
        position: fixed;
        left: 0;
        bottom: 0;
        height: 60px;
        width: 100%;
        background: lightskyblue;
        text-align: center;
        font-weight: bold;
    }
</style>
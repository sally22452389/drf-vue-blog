<template>
    <div id="header">
        <div class="grid">
            <a href="/">Icemaple drf-vue blog</a>
            <p></p>
            <div class="searchbutton">
                <SearchButton/>
            </div>
            <div class="login">

                <div v-if="hasLogin">
                    <div class="dropdown">
                        <button class="dropbtn">歡迎, {{username}} </button>
                        <div class="dropdown-content">
                            <router-link :to="{ name: 'UserCenter', params: { username: username }}">用戶中心</router-link>
                            <router-link :to="{ name: 'ArticleCreate' }" v-if="isSuperuser">發表文章</router-link>
                            <router-link to="/" v-on:click.prevent="logout()">登出</router-link>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <router-link to="/login" class="login-link">登錄</router-link>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
    import SearchButton from '@/components/SearchButton.vue';
    import authorization from '@/utils/authorization';
    export default {
        name: 'BlogHeader',
        components: {SearchButton},
        data: function () {
            return {
                username: '',
                hasLogin: false,
                isSuperuser: JSON.parse(localStorage.getItem('isSuperuser.myblog')),
            }
        },
        mounted() {
            authorization().then((data) => [this.hasLogin, this.username] = data);
        },
        methods: {
            logout() {
                localStorage.clear();
                window.location.reload(false);
            },
            refresh() {
                this.username = localStorage.getItem('username.myblog');
            }
        }
    }
</script>

<style scoped>
    /* 來源: https://www.runoob.com/css/css-dropdowns.html* /
    /* 下拉 */
    .dropbtn {
        background-color: mediumslateblue;
        color: white;
        padding: 8px 8px 30px 8px ;
        font-size: 16px;
        border: none;
        cursor: pointer;
        height: 16px;
        border-radius: 5px;
    }
    /*  <div> - 需要定位下拉内容 */
    .dropdown {
        position: relative;
        display: inline-block;
    }
    /* 下拉内容 (預設隱藏) */
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 50px;
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    /* 下拉連結 */
    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }
    /* 鼠标移上去后修改下拉菜单链接颜色 */
    .dropdown-content a:hover {
        background-color: #f1f1f1
    }
    /* 在鼠标移上去后显示下拉菜单 */
    .dropdown:hover .dropdown-content {
        display: block;
    }
    /* 当下拉内容显示后修改下拉按钮的背景颜色 */
    .dropdown:hover .dropbtn {
        background-color: darkslateblue;
    }
</style>

<style scoped>
    
    #header {
        padding-top: 0px;
        padding-bottom: 80px;
        text-align: center; 
        margin: 0 auto;
        font-weight: bold;
        background-color: ;
        
    }

    .grid {
        position: fixed;
        width: 100%;
        align-items: center;
        height: ;
        display: grid;
        grid-template-columns: 1fr 3fr 1fr 0.2fr;
        background-color: #375a7f;

        padding-top: 1rem;
        padding-bottom: 1rem;
        margin-right: 0.5rem;
        font-size: 1.5rem;
        line-height: inherit;
        white-space: nowrap;

        font-family: "Dosis", "Source Sans Pro", "Helvetica Neue", Arial, sans-serif;
        color: #273849;
    }

    .searchbutton {

    }
    .login-link {
        color: #ffffff;
        font-size: 70%;
    }

    .login {
        text-align: right;
        padding-right: 70px;
    }

    a {
        text-decoration: none;
        color: #fff;
    }
</style>
<template>

    <BlogHeader/>

    <div id="grid">
        <div id="signup">
            <h3>註冊帳號</h3>
            <form>
                <div class="form-elem">
                    <span>帳號：</span> 
                    <input v-model="signupName" type="text" placeholder="用戶名">
                </div>
                <div class="form-elem">
                    <span>密碼：</span> 
                    <input v-model="signupPwd" type="password" placeholder="密碼">
                </div>
                <div class="form-elem">
                    <button v-on:click.prevent="signup">提交</button>
                </div>
            </form>
        </div>

        <div id="signin">
            <h3>登錄帳號</h3>
            <form>
                <div class="form-elem">
                    <span>帳號：</span>
                    <input v-model="signinName" type="text" placeholder="用戶名">
                </div>

                <div class="form-elem">
                    <span>密碼：</span>
                    <input v-model="signinPwd" type="password" placeholder="密碼">
                </div>

                <div class="form-elem">
                    <button v-on:click.prevent="signin">登錄</button>
                </div>
            </form>
        </div>
    </div>

    <BlogFooter/>

</template>

<script>
    import axios from 'axios';
    import BlogHeader from '@/components/BlogHeader.vue'
    import BlogFooter from '@/components/BlogFooter.vue'

    export default {
        name: 'Login',
        components: {BlogHeader, BlogFooter},
        data: function () {
            return {
                signupName: '',
                signupPwd: '',
            }
        },
        methods: {
            signup() {
                const that = this;
                axios
                    .post('/api/user/', {
                        username: this.signupName,
                        password: this.signupPwd,
                    })
                    .then(function (response) {
                        that.signupResponse = response.data;
                        alert('用戶註冊成功');
                    })
                    .catch(function (error) {
                        alert(error.message);
                        // Handling Error here...
                        // https://github.com/axios/axios#handling-errors
                    });
            },
            signin() {
                const that = this;
                axios
                    .post('/api/token/', {
                        username: this.signinName,
                        password: this.signinPwd,
                    })
                    .then(function (response) {
                        const storage = localStorage;
                        // Date.parse(...) 返回1970年1月1日UTC以來的毫秒數
                        // Token 設30min，這加上60000 ms
                        const expiredTime = Date.parse(response.headers.date) + 1800000;
                          // 設 localStorage
                        storage.setItem('access.myblog', response.data.access);
                        storage.setItem('refresh.myblog', response.data.refresh);
                        storage.setItem('expiredTime.myblog', expiredTime);
                        storage.setItem('username.myblog', that.signinName);
                        // 路由跳轉
                        // 成功後回到首頁
                        // 是否為管理員
                        axios
                            .get('/api/user/' + that.signinName + '/')
                            .then(function (response) {
                                storage.setItem('isSuperuser.myblog', response.data.is_superuser);
                                // 路由挑轉
                                that.$router.push({name: 'Home'});
                            })
                            // .catch(function () {alert('非管理員身分');})
                    })
                    .catch(function () {
                        alert('密碼錯誤');
                    })
            },
        }
    }
</script>

<style scoped>
    #signin {
        text-align: center;
    }
    #grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
    }
    #signup {
        text-align: center;
    }
    .form-elem {
        padding: 10px;
    }
    input {
        height: 25px;
        padding-left: 10px;
    }
    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: gray;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }
</style>
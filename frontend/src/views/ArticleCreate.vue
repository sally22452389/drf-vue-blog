<template>
  <BlogHeader/>
  <div id="article-create">
    <h3>發表文章</h3>
    <form>
      <div class="form-elem">
        <span>標題：</span>
        <input v-model="title" type="text" placeholder="標題">
      </div>

      <div class="form-elem">
        <span>分類：</span>
        <span
              v-for="category in categories"
              :key="category.id"
              >
          <!--樣式-->
          <button
                  class="category-btn"
                  :style="categoryStyle(category)"
                  @click.prevent="chooseCategory(category)"
                  >
            {{category.title}}
          </button>
        </span>
      </div>

      <div class="form-elem">
        <span>標籤：</span>
        <input v-model="tags" type="text" placeholder="標籤，用逗號分隔">
      </div>

      <div class="form-elem">
        <span>正文：</span>
        <textarea v-model="body" placeholder="正文" rows="20" cols="80"></textarea>
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="submit">送出</button>
      </div>
    </form>
  </div>
  <BlogFooter/>
</template>

<script>
  import BlogHeader from '@/components/BlogHeader.vue'
  import BlogFooter from '@/components/BlogFooter.vue'
  import axios from 'axios';
  import authorization from '@/utils/authorization';

  export default {
    name: 'ArticleCreate',
    components: {BlogHeader, BlogFooter},
    data: function () {
      return {
        title: '',
        body: '',
        // 分類
        categories: [],
        // 選定的分類
        selectedCategory: null,
        // 標籤
        tags: '',
      }
    },
    mounted() {
      // 頁面初始化時獲取的所有分類
      axios
        .get('/api/category/')
        .then(response => this.categories = response.data)
    },
    methods: {
      // 根據分類是否被選中，按鈕的顏色改變
      categoryStyle(category) {
        if (this.selectedCategory !== null && category.id === this.selectedCategory.id) {
          return {
            backgroundColor: 'black',
          }
        }
        return {
          backgroundColor: 'lightgrey',
          color: 'black',
        }
      },
      // 選取分類
      chooseCategory(category) {
        // 如果點擊已選取的分類，則 selectedCategory 置空
        if (this.selectedCategory !== null && this.selectedCategory.id === category.id) {
          this.selectedCategory = null
        }
        // 如果沒選中分類，則選它
        else {
          this.selectedCategory = category;
        }
      },
      // 提交
      submit() {
        const that = this;
        // 驗證
        authorization()
          .then(function (response) {
            if (response[0]) {
              // 傳給後端的字典
              let data = {
                title: that.title,
                body: that.body,
              };
              // 分類
              if (that.selectedCategory) {
                data.category_id = that.selectedCategory.id
              }
              // 標籤處理
              data.tags = that.tags
                .split(/[,，]/)
                .map(x => x.trim())
                .filter(x => x.charAt(0) !== '');

              // 發表文章發送
              // 成功後往詳細頁面
              const token = localStorage.getItem('access.myblog');
              axios
                .post('/api/article/',
                  data,
                  {
                        headers: {Authorization: 'Bearer ' + token}
                    })
                .then(function (response) {
                    that.$router.push({name: 'ArticleDetail', params: {id: response.data.id}});
              })
            }
            else {
              alert('過期，請重新登錄。')
            }
          }
        )
      }
    }
  }
</script>

<style scoped>
  .category-btn {
    margin-right: 10px;
  }
  #article-create {
    text-align: center;
    font-size: large;
  }
  form {
    text-align: left;
    padding-left: 100px;
    padding-right: 10px;
  }
  .form-elem {
    padding: 10px;
  }
  input {
    height: 25px;
    padding-left: 10px;
    width: 50%;
  }
  button {
    height: 35px;
    cursor: pointer;
    border: none;
    outline: none;
    background: steelblue;
    color: whitesmoke;
    border-radius: 5px;
    width: 60px;
  }
</style>
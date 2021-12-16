<template>
  <BlogHeader/>
  <div id="article-create">
    <h3>更新文章</h3>
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
          <!-- 樣式也可以通過:style綁定 -->
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
        <input v-model="tags" type="text" placeholder="輸入標籤，用逗號分隔">
      </div>

      <div class="form-elem">
        <span>正文：</span>
        <textarea v-model="body" placeholder="正文" rows="20" cols="80"></textarea>
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="submit">提交</button>
      </div>
      <div class="form-elem">
        <button v-on:click.prevent="deleteArticle" style="background-color: darkred">刪除</button>
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
    name: 'ArticleEdit',
    components: {BlogHeader, BlogFooter},
    data: function () {
      return {
        title: '',
        body: '',

        // 所有分類
        categories: [],
        selectedCategory: null,
        tags: '',

        articleID: null,
      }
    },
    mounted() {
      // 頁面初始化時獲取所有分類
      axios
        .get('/api/category/')
        .then(response => this.categories = response.data);

      // 如果你不希望非管理員用戶也能獲取原始 Markdown 數據
      // 必須在旁進行鑑權
      // 可根據用戶選擇不同的序列化器
      const that = this;
      axios
        .get('/api/article/' + that.$route.params.id + '/')
        .then(function (response) {
          const data = response.data;
          that.title = data.title;
          that.body = data.body;
          that.selectedCategory = data.category;
          that.tags = data.tags.join(',');
          that.articleID = data.id;
        })
    },
    methods: {
      // 根據分類是否被選中，按鈕的顏色發生變化
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
      chooseCategory(category) {
        // 如果點擊已選擇的分類，則將選擇的分類置為空
        if (this.selectedCategory !== null && this.selectedCategory.id === category.id) {
          this.selectedCategory = null
        }
        else {
          this.selectedCategory = category;
        }
      },
    
      submit() {
        const that = this;
        authorization()
          .then(function (response) {
            if (response[0]) {
              let data = {
                title: that.title,
                body: that.body,
              };

              data.category_id = that.selectedCategory ? that.selectedCategory.id : null;

              data.tags = that.tags
                .split(/[,，]/)
                .map(x => x.trim())
                .filter(x => x.charAt(0) !== '');

              const token = localStorage.getItem('access.myblog');
              axios
                .put('/api/article/' + that.articleID + '/',
                     data,
                     {
                headers: {Authorization: 'Bearer ' + token}
              })
                .then(function (response) {
                that.$router.push({name: 'ArticleDetail', params: {id: response.data.id}});
              })
            }
            else {
              alert('過期了，請重新登錄。')
            }
          }
        )
      },
      deleteArticle() {
        const that = this;
        const token = localStorage.getItem('access.myblog');
        authorization()
          .then(function (response) {
            if (response[0]) {
              axios
                .delete('/api/article/' + that.articleID + '/',
                  {
                        headers: {Authorization: 'Bearer ' + token}
                    })
                .then(() => that.$router.push({name: 'Home'}))
            }
            else {
              alert('過期了，請重新登錄。')
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
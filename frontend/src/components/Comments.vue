<template>
  <br><br>
  <hr>
  <h3>發表評論</h3>
  <!-- 評論多行文本輸入 -->
  <textarea
            v-model="message"
            :placeholder="placeholder"
            name="comment"
            id="comment-area"
            cols="60"
            rows="5"
            ></textarea>
  <div>
    <button @click="submit" class="submitBtn">留言</button>
  </div>

  <br>
  <p>已有 {{ comments.length }} 條留言</p>
  <hr>

  <!-- 渲染所有評論內容 -->
  <div
       v-for="comment in comments"
       :key="comment.id"
       >
    <div class="comments">
      <div>
        <span class="username">
          {{ comment.author.username }}
        </span>
        於
        <span class="created">
          {{ formatted_time(comment.created) }}
        </span>
        <span v-if="comment.parent">
          對
          <span class="parent">
            {{ comment.parent.author.username }}
          </span>
        </span>
        留言：
      </div>
      <div class="content">
        {{ comment.content }}
      </div>
      <div>
        <button class="commentBtn" @click="replyTo(comment)">回覆</button>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
  import axios from 'axios';
  import authorization from '@/utils/authorization';

  export default {
    name: 'Comments',
    // 通過道具 獲取當前文章
    props: { article: Object },
    data: function () {
      return {
        comments: [],
        // 評論登記綁定的文本和占位符
        message: '',
        placeholder: '留言...',
        // 評論的評論
        parentID: null
      }
    },
    // 以便更新評論
    watch: {
      article() {
        this.comments = this.article !== null ? this.article.comments : []
      }
    },
    methods: {
      submit() {
        const that = this;
        authorization()
          .then(function (response) {
            if (response[0]) {
              axios
                .post('/api/comment/',
                  {
                    content: that.message,
                    article_id: that.article.id,
                    parent_id: that.parentID,
                  },
                  {
                    headers: {Authorization: 'Bearer ' + localStorage.getItem('access.myblog')}
                  })
                .then(function (response) {
                  // 將新的評論添加到頂部
                  that.comments.unshift(response.data);
                  that.message = '';
                  alert('留言成功')
                })
            }
            else {
              alert('請登錄後評論。')
            }
        })
      },
      // 對某條評論進行評論
      replyTo(comment) {
        this.parentID = comment.id;
        this.placeholder = '對' + comment.author.username + '留言:'
      },
      // 日期顯示格式
      formatted_time: function (iso_date_string) {
        const date = new Date(iso_date_string);
        return date.toLocaleDateString() + '  ' + date.toLocaleTimeString()
      },
    }
  }
</script>

<style scoped>
  button {
    cursor: pointer;
    border: none;
    outline: none;
    color: whitesmoke;
    border-radius: 5px;
  }
  .submitBtn {
    height: 30px;
    background: steelblue;
    width: 50px;
  }
  .commentBtn {
    height: 25px;
    background: lightslategray;
    width: 50px;
  }
  .comments {
    padding-top: 10px;
  }
  .username {
    font-weight: bold;
    color: darkorange;
  }
  .created {
    font-weight: bold;
    color: darkblue;
  }
  .parent {
    font-weight: bold;
    color: orangered;
  }
  .content {
    font-size: large;
    padding: 15px;
  }
</style>
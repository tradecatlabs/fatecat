// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import App from './App'
import router from './store/router'
import common from './store/common'
import fileUtil from './store/fileUtil'
import axios from 'axios'
import {post,fetch,patch,put} from './store/https'
import AudioRecorder from 'vue-audio-recorder'


//定义全局变量
Vue.prototype.$post=post;
Vue.prototype.$fetch=fetch;
Vue.prototype.$patch=patch;
Vue.prototype.$put=put;
Vue.prototype.$axios=axios;

Vue.use(ElementUI);
Vue.use(common);
Vue.use(fileUtil);
Vue.use(AudioRecorder)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
    router,
  components: { App },
  template: '<App/>'
})

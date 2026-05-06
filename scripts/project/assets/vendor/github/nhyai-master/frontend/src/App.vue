<template>
  <div id="app">
    <keep-alive >
      <router-view v-if="$route.meta.keepAlive"></router-view>
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive"></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style>
  @import './assets/css/common.css';
  @import './assets/css/override-element-ui.css';
  @import './assets/css/video-js.min.css';
  @import './assets/css/videojs.markers.css';
</style>

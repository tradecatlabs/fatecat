<script lang="ts" setup>
const { isFullscreen, toggle } = useFullscreen()
</script>

<template>
  <button rounded p-2 hover="bg-active" @click="toggle">
    <div :class="{ 'i-gridicons:fullscreen-exit': isFullscreen, 'i-gridicons:fullscreen': !isFullscreen }" text-2xl />
  </button>
</template>

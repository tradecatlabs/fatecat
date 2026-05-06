<script lang="ts" setup>
const colorMode = useColorMode()

/**
 * 切换模式
 */
const toggleMode = (): void => {
  colorMode.value = colorMode.value === 'light' ? 'dark' : 'light'
}
</script>

<template>
  <button rounded p-2 hover="bg-active" @click="toggleMode">
    <div i-ph-sun-dim-duotone dark:i-ph-moon-stars-duotone text-2xl />
  </button>
</template>

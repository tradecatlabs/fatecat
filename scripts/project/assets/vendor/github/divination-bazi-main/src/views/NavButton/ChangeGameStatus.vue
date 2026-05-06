<script lang='ts' setup>
const state = useGlobalState()

const pauseClick = (): void => {
  state.value.gameState = 'pause'
}
</script>

<template>
  <button rounded p-2 hover="bg-active" @click="pauseClick">
    <div
      :class="{ 'i-material-symbols:play-circle-rounded': state.gameState === 'pause', 'i-material-symbols:pause-circle': state.gameState === 'start' }"
      text-2xl />
  </button>
</template>

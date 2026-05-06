<script lang="ts" setup>
import OneStep from './OneStep.vue';
import TwoStep from './TwoStep.vue';
import ThreeStep from './ThreeStep.vue';
import FourStep from './FourStep.vue';

const lunarDate = ref()
const baZi = ref()

const getlunarDate = val => {
  lunarDate.value = val ? val : null
  if (lunarDate.value) {
    baZi.value = lunarDate.value.getEightChar()
    console.log(baZi.value)
  }
}
</script>

<template>
  <div style="height: calc(100vh - 58px); overflow: auto" w-screen color-white p8 flex-center flex-wrap gap-8>
    <OneStep @get-all-data="getlunarDate" />
    <TwoStep :lunar-date="lunarDate" :ba-zi="baZi" />
    <ThreeStep :lunar-date="lunarDate" :ba-zi="baZi" />
    <FourStep />
  </div>
</template>

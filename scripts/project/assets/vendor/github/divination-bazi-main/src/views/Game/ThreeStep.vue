<script lang='ts' setup>
import StepCard from './StepCard.vue';

const props = defineProps({
  lunarDate: {
    type: Object
  },
  baZi: {
    type: Object
  }
})

const yearShiShen = ref('未知')
const monthShiShen = ref('未知')
const dayShiShen = ref('未知')
const timeShiShen = ref('未知')

const getShiShen = () => {
  yearShiShen.value = props.baZi.getYearShiShenZhi()
  monthShiShen.value = props.baZi.getMonthShiShenZhi()
  dayShiShen.value = props.baZi.getDayShiShenZhi()
  timeShiShen.value = props.baZi.getTimeShiShenZhi()
}

watch(
  () => props.lunarDate,
  () => getShiShen()
)
</script>

<template>
  <StepCard>
    <div class="title">
      第三步：分析十神
    </div>
    <div flex-center>
      <div w-130px>年十神：</div>
      <div w-400px>{{ yearShiShen }}</div>
    </div>
    <div flex-center>
      <div w-130px>月十神：</div>
      <div w-400px>{{ monthShiShen }}</div>
    </div>
    <div flex-center>
      <div w-130px>日十神：</div>
      <div w-400px>{{ dayShiShen }}</div>
    </div>
    <div flex-center>
      <div w-130px>时十神：</div>
      <div w-400px>{{ timeShiShen }}</div>
    </div>
  </StepCard>
</template>

<style scoped lang='scss'>
</style>

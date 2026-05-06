<script lang="ts" setup>
import StepCard from './StepCard.vue';
import { SolarUtil, Lunar } from 'lunar-typescript';

const emit = defineEmits(['getAllData'])

const year = ref(1990) // 默认1990年，方便选择
const yearItems = ref([1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026])
const month = ref()
const monthItems = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
const day = ref()
const dayNum = ref()
const dayItems = ref([])
const time = ref()
const timeItems = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])

const yearMonthChange = () => {
  if (year.value && month.value) {
    dayNum.value = SolarUtil.getDaysOfMonth(Number(year.value), Number(month.value))
    for (let i = 1; i <= dayNum.value; i++) {
      dayItems.value.push(i)
    }
  } else {
    dayItems.value = []
  }
}

const lunar = computed(() => {
  if (year.value && month.value && day.value && time.value) {
    const date = new Date(`${year.value}-${month.value}-${day.value} ${time.value}:00:00`)
    return Lunar.fromDate(date)
  } else {
    return null
  }
})

const yearGan = computed(() => lunar.value ? lunar.value.getYearGan() : '未')
const yearZhi = computed(() => lunar.value ? lunar.value.getYearZhi() : '知')
const monthGan = computed(() => lunar.value ? lunar.value.getMonthGan() : '未')
const monthZhi = computed(() => lunar.value ? lunar.value.getMonthZhi() : '知')
const dayGan = computed(() => lunar.value ? lunar.value.getDayGan() : '未')
const dayZhi = computed(() => lunar.value ? lunar.value.getDayZhi() : '知')
const timeGan = computed(() => lunar.value ? lunar.value.getTimeGan() : '未')
const timeZhi = computed(() => lunar.value ? lunar.value.getTimeZhi() : '知')

const returnAllData = () => {
  emit('getAllData', lunar.value)
}

watch(
  () => lunar.value,
  () => returnAllData()
)
</script>

<template>
  <StepCard>
    <div class="title">
      第一步：获取生辰八字
    </div>
    <!-- 年 -->
    <div flex-center gap-4>
      <div w-40px>年</div>
      <el-select v-model="year" placeholder="year" style="width: 120px" @change="yearMonthChange">
        <el-option v-for="item in yearItems" :key="item" :value="item" :label="`${item}年`" />
      </el-select>
      <div w-160px>干支：{{ yearGan }}{{ yearZhi }}</div>
    </div>
    <!-- 月 -->
    <div flex-center gap-4>
      <div w-40px>月</div>
      <el-select v-model="month" placeholder="month" style="width: 120px" @change="yearMonthChange">
        <el-option v-for="item in monthItems" :key="item" :value="item" :label="`${item}月`" />
      </el-select>
      <div w-160px>干支：{{ monthGan }}{{ monthZhi }}</div>
    </div>
    <!-- 日 -->
    <div flex-center gap-4>
      <div w-40px>日</div>
      <el-select v-model="day" placeholder="day" style="width: 120px">
        <el-option v-for="item in dayItems" :key="item" :value="item" :label="`${item}日`" />
      </el-select>
      <div w-160px>干支：{{ dayGan }}{{ dayZhi }}</div>
    </div>
    <!-- 时 -->
    <div flex-center gap-4>
      <div w-40px>时</div>
      <el-select v-model="time" placeholder="time" style="width: 120px">
        <el-option v-for="item in timeItems" :key="item" :value="item" :label="`${item}点`" />
      </el-select>
      <div w-160px>干支：{{ timeGan }}{{ timeZhi }}</div>
    </div>
  </StepCard>
</template>

<style scoped lang='scss'>
</style>

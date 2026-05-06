<script lang="ts" setup>
import GameNav from "@/views/Layout/GameNav.vue";
import GameContent from '@/views/Layout/GameContent.vue'
import {getAssetsFile} from '@/utils'

const state = useGlobalState()
</script>

<template>
  <main h-100dvh h-screen w-screen of-hidden bg-cover bg-center grid="~ rows-[max-content_1fr]"
        :style="{ backgroundImage: `url(${getAssetsFile(`${state.bgImage}.jpg`)})` }">
    <GameNav/>
    <GameContent/>
  </main>
</template>

import {GameInfoType} from '@/views/Type'

export const useGlobalState: () => Ref<GameInfoType> = createGlobalState(
    () => useStorage('global-state', {
        // 游戏难度
        difficulty: 'middle',
        // 当前局此
        rounds: 0,
        // 游戏状态
        gameState: 'init',
        // 背景图片
        bgImage: 'game-bg',
        // 是否显示游戏日志
        isShowGameInfo: true,
        // 游戏日志
        gameLogItems: []
    })
)

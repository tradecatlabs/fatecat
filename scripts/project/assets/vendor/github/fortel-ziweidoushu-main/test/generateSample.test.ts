import { DestinyBoard } from '../src/model/destinyBoard'
import { Ground } from '../src/model/ground'
import { DestinyConfigBuilder } from '../src/util/destinyConfigBuilder'
import { MajorStar } from '../src/model/majorStar'
import { MinorStar } from '../src/model/minorStar'
import { Temple } from '../src/model/temple'
import { BoardCriteria } from '../src/criteria/boardCriteria'
import { Element } from '../src/model/miscEnums'
import { StarDerivative } from '../src/main'

describe('Test generate sample boards', () => {
    it('Test board 1', () => {
        const destinyBoard: DestinyBoard = new DestinyBoard(DestinyConfigBuilder.withText('1952年12月15日寅時天盤女'))

        expect(destinyBoard).toBeInstanceOf(DestinyBoard)
        expect(destinyBoard.element).toBe(Element.GOLD)
        expect(destinyBoard.destinyMaster).toBe(MajorStar.MAJOR_STAR_FIRE)
        expect(destinyBoard.bodyMaster).toBe(MinorStar.MINOR_STAR_CLEVER)
        expect(destinyBoard.getCellByTemple(Temple.TEMPLE_DESTINY).ground).toBe(Ground.getByName('亥'))
        expect(destinyBoard.startControl).toBe(Ground.getByName('卯'))

        expect(BoardCriteria.fromDescription(destinyBoard, '命宮有天同,祿存,右弼,紅鸞,大耗,天巫,博士,龍德,亡神')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '兄弟宮有破軍,陀羅,天官,天虛,力士,歲破,月煞')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '夫妻宮有地空,天廚,咸池,月德,八座,恩光,青龍,小耗,咸池')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '子女宮有廉貞,文昌,龍池,台輔,天刑,小耗,官符,指背')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '財帛宮有天壽,旬空,天貴,將軍,貫索,天煞')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '疾厄宮有七殺,文曲,天福,鳳閣,解神,旬空,解神,蜚廉,天傷,奏書,喪門,災煞')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '遷移宮有天梁化祿,天鉞,天喜,孤辰,劫煞,天空,三台,蜚廉,晦氣,劫煞')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '交友宮有紫微,天相,火星,封誥,陰煞,天使,喜神,太歲,華蓋')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '事業宮有天機,巨門,左輔,天魁,天才,截空,病符,病符,息神')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '田宅宮有貪狼,天馬,天哭,截空,天月,大耗,弔客,歲驛')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '福德宮有太陽,太陰,地劫,寡宿,破碎,伏兵,天德,攀鞍')).toBe(true)
        expect(BoardCriteria.fromDescription(destinyBoard, '父母宮有武曲化忌,天府化科,擎羊,鈴星,天姚,官府,白虎,將星')).toBe(true)

        expect(JSON.stringify(destinyBoard)).toBe(
            JSON.stringify({
                config: {
                    year: 1952,
                    month: 12,
                    day: 15,
                    isLeapMonth: false,
                    yearSky: '壬',
                    yearGround: '辰',
                    monthSky: '癸',
                    monthGround: '丑',
                    daySky: '庚',
                    dayGround: '辰',
                    bornTimeGround: '寅時',
                    configType: '天盤',
                    gender: '女',
                },
                element: '金四局',
                destinyMaster: '廉貞',
                bodyMaster: '文昌',
                startControl: '卯',
                cells: [
                    {
                        sky: '壬',
                        ground: '子',
                        temples: ['父母'],
                        majorStars: ['武曲', '天府'],
                        minorStars: ['鈴星', '擎羊'],
                        miniStars: ['天姚'],
                        miscStars: ['天姚', '官府', '白虎', '將星'],
                        ageStart: 114,
                        ageEnd: 123,
                        lifeStage: '衰',
                    },
                    {
                        sky: '癸',
                        ground: '丑',
                        temples: ['福德'],
                        majorStars: ['太陽', '太陰'],
                        minorStars: ['地劫'],
                        miniStars: ['寡宿', '破碎'],
                        miscStars: ['寡宿', '破碎', '伏兵', '天德', '攀鞍'],
                        ageStart: 104,
                        ageEnd: 113,
                        lifeStage: '帝旺',
                    },
                    {
                        sky: '壬',
                        ground: '寅',
                        temples: ['田宅'],
                        majorStars: ['貪狼'],
                        minorStars: ['天馬'],
                        miniStars: ['天哭', '截空', '天月'],
                        miscStars: ['天哭', '截空', '天月', '大耗', '弔客', '歲驛'],
                        ageStart: 94,
                        ageEnd: 103,
                        lifeStage: '臨官',
                    },
                    {
                        sky: '癸',
                        ground: '卯',
                        temples: ['身宮', '事業'],
                        majorStars: ['天機', '巨門'],
                        minorStars: ['天魁', '左輔'],
                        miniStars: ['天才', '截空'],
                        miscStars: ['天才', '截空', '病符', '病符', '息神'],
                        ageStart: 84,
                        ageEnd: 93,
                        lifeStage: '冠帶',
                    },
                    {
                        sky: '甲',
                        ground: '辰',
                        temples: ['交友'],
                        majorStars: ['紫微', '天相'],
                        minorStars: ['火星'],
                        miniStars: ['封誥', '陰煞', '天使'],
                        miscStars: ['封誥', '陰煞', '天使', '喜神', '太歲', '華蓋'],
                        ageStart: 74,
                        ageEnd: 83,
                        lifeStage: '沐浴',
                    },
                    {
                        sky: '乙',
                        ground: '巳',
                        temples: ['遷移'],
                        majorStars: ['天梁'],
                        minorStars: ['天鉞'],
                        miniStars: ['天喜', '孤辰', '劫煞', '天空', '三台'],
                        miscStars: ['天喜', '孤辰', '劫煞', '天空', '三台', '蜚廉', '晦氣', '劫煞'],
                        ageStart: 64,
                        ageEnd: 73,
                        lifeStage: '長生',
                    },
                    {
                        sky: '丙',
                        ground: '午',
                        temples: ['疾厄'],
                        majorStars: ['七殺'],
                        minorStars: ['文曲'],
                        miniStars: ['天福', '鳳閣', '解神', '旬空', '解神', '蜚廉', '天傷'],
                        miscStars: ['天福', '鳳閣', '解神', '旬空', '解神', '蜚廉', '天傷', '奏書', '喪門', '災煞'],
                        ageStart: 54,
                        ageEnd: 63,
                        lifeStage: '養',
                    },
                    {
                        sky: '丁',
                        ground: '未',
                        temples: ['財帛'],
                        majorStars: [],
                        minorStars: [],
                        miniStars: ['天壽', '旬空', '天貴'],
                        miscStars: ['天壽', '旬空', '天貴', '將軍', '貫索', '天煞'],
                        ageStart: 44,
                        ageEnd: 53,
                        lifeStage: '胎',
                    },
                    {
                        sky: '戊',
                        ground: '申',
                        temples: ['子女'],
                        majorStars: ['廉貞'],
                        minorStars: ['文昌'],
                        miniStars: ['龍池', '台輔', '天刑'],
                        miscStars: ['龍池', '台輔', '天刑', '小耗', '官符', '指背'],
                        ageStart: 34,
                        ageEnd: 43,
                        lifeStage: '絕',
                    },
                    {
                        sky: '己',
                        ground: '酉',
                        temples: ['夫妻'],
                        majorStars: [],
                        minorStars: ['地空'],
                        miniStars: ['天廚', '咸池', '月德', '八座', '恩光'],
                        miscStars: ['天廚', '咸池', '月德', '八座', '恩光', '青龍', '小耗', '咸池'],
                        ageStart: 24,
                        ageEnd: 33,
                        lifeStage: '墓',
                    },
                    {
                        sky: '庚',
                        ground: '戌',
                        temples: ['兄弟'],
                        majorStars: ['破軍'],
                        minorStars: ['陀羅'],
                        miniStars: ['天官', '天虛'],
                        miscStars: ['天官', '天虛', '力士', '歲破', '月煞'],
                        ageStart: 14,
                        ageEnd: 23,
                        lifeStage: '死',
                    },
                    {
                        sky: '辛',
                        ground: '亥',
                        temples: ['命宮'],
                        majorStars: ['天同'],
                        minorStars: ['祿存', '右弼'],
                        miniStars: ['紅鸞', '大耗', '天巫'],
                        miscStars: ['紅鸞', '大耗', '天巫', '博士', '龍德', '亡神'],
                        ageStart: 4,
                        ageEnd: 13,
                        lifeStage: '病',
                    },
                ],
                bornStarDerivativeMap: { 祿: '天梁', 權: '紫微', 科: '天府', 忌: '武曲' },
            }),
        )
    })

    it('Test board 2', () => {
        const destinyBoard: DestinyBoard = new DestinyBoard(DestinyConfigBuilder.withText('1990年9月10日子時人盤男'))

        expect(destinyBoard).toBeInstanceOf(DestinyBoard)
        expect(destinyBoard.element).toBe(Element.FIRE)
        expect(destinyBoard.getCellByTemple(Temple.TEMPLE_DESTINY).ground).toBe(Ground.getByName('子'))
        expect(destinyBoard.startControl).toBe(Ground.getByName('辰'))

        expect(
            new BoardCriteria(destinyBoard).ofTemple(Temple.TEMPLE_DESTINY).hasAllStars([MajorStar.MAJOR_STAR_ENJOYMENT, MajorStar.MAJOR_STAR_MOON]),
        ).toBe(true)

        expect(destinyBoard.getMajorStarDerivative(MajorStar.MAJOR_STAR_ENJOYMENT)).toEqual(StarDerivative.PROBLEM)
    })
})

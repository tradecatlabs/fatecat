import { Ground } from '../src/model/ground'
import { Sky } from '../src/model/sky'
import { Temple } from '../src/model/temple'

describe('Test sky', () => {
    it('Test sky', () => {
        expect(Sky.get(0).displayName).toBe('甲')
        expect(Sky.get(11)).toBe(Sky.get(1))
        expect(Sky.get(21)).toBe(Sky.get(1))
        expect(Sky.get(-1)).toBe(Sky.get(9))
        expect(Sky.get(-11)).toBe(Sky.get(9))
        expect(Sky.get(5).shift(3)).toBe(Sky.get(8))
        expect(Sky.get(5).shift(-3)).toBe(Sky.get(2))
        expect(Sky.get(5).shift(13)).toBe(Sky.get(8))
        expect(Sky.get(5).shift(-13)).toBe(Sky.get(2))
        expect(Sky.get(5).equals(Sky.get(5))).toBe(true)
        expect(Sky.get(5).equals(Sky.get(7))).toBe(false)
    })
})

describe('Test ground', () => {
    it('Test ground', () => {
        expect(Ground.get(0).displayName).toBe('子')
        expect(Ground.get(13)).toBe(Ground.get(1))
        expect(Ground.get(25)).toBe(Ground.get(1))
        expect(Ground.get(-1)).toBe(Ground.get(11))
        expect(Ground.get(-13)).toBe(Ground.get(11))
        expect(Ground.get(5).shift(3)).toBe(Ground.get(8))
        expect(Ground.get(5).shift(-3)).toBe(Ground.get(2))
        expect(Ground.get(5).shift(15)).toBe(Ground.get(8))
        expect(Ground.get(5).shift(-15)).toBe(Ground.get(2))
        expect(Ground.get(5).equals(Ground.get(5))).toBe(true)
        expect(Ground.get(5).equals(Ground.get(7))).toBe(false)
    })
})

describe('Test temple', () => {
    it('Test temple', () => {
        expect(Temple.TEMPLE_BROTHER.getDisplayName()).toBe('兄弟')
        expect(Temple.TEMPLE_BROTHER.getFormalName()).toBe('兄弟宮')

        expect(Temple.getByKey('TEMPLE_HAPPINESS')).toBe(Temple.TEMPLE_HAPPINESS)
        expect(Temple.getByName('交友')).toBe(Temple.TEMPLE_FRIEND)
        expect(Temple.getByName('交友宮')).toBe(Temple.TEMPLE_FRIEND)
    })
})

import { MajorStar } from '../model/majorStar'
import { MinorStar } from '../model/minorStar'
import { MiniStar } from '../model/miniStar'
import { Star } from '../model/star'

export const starByName = (name: string): Star => {
    const star = MajorStar.getByName(name) ?? MinorStar.getByName(name) ?? MiniStar.getByName(name)
    if (!star) {
        throw new Error('star not found')
    }
    return star
}

export const starByKey = (key: string): Star => {
    const star = MajorStar.getByKey(key) ?? MinorStar.getByKey(key) ?? MiniStar.getByKey(key) ?? null
    if (!star) {
        throw new Error('star not found')
    }
    return star
}

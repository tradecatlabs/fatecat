import { calculateBazi, type BaziOutput as CoreBaziOutput } from 'taibu-core/bazi';
import { parseLongitude } from '@/lib/divination/place-resolution';

type StoredBaziBase = {
    gender?: string | null;
    birth_date?: string | null;
    birth_time?: string | null;
    birth_place?: string | null;
    longitude?: number | string | null;
    calendar_type?: string | null;
    is_leap_month?: boolean | null;
};

export function calculateBaziOutputFromStoredFields(row: StoredBaziBase): CoreBaziOutput | null {
    if (typeof row.birth_date !== 'string' || row.birth_date.trim() === '') {
        return null;
    }

    const [birthYear, birthMonth, birthDay] = row.birth_date.split('-').map(Number);
    if (!Number.isFinite(birthYear) || !Number.isFinite(birthMonth) || !Number.isFinite(birthDay)) {
        return null;
    }

    const birthTime = typeof row.birth_time === 'string' && row.birth_time.trim() !== ''
        ? row.birth_time
        : '12:00';
    const [birthHour, birthMinute] = birthTime.split(':').map(Number);
    if (!Number.isFinite(birthHour) || !Number.isFinite(birthMinute)) {
        return null;
    }

    try {
        return calculateBazi({
            gender: row.gender === 'female' ? 'female' : 'male',
            birthYear,
            birthMonth,
            birthDay,
            birthHour,
            birthMinute,
            birthPlace: row.birth_place || undefined,
            longitude: parseLongitude(row.longitude),
            calendarType: row.calendar_type === 'lunar' ? 'lunar' : 'solar',
            isLeapMonth: row.is_leap_month ?? false,
        });
    } catch {
        return null;
    }
}

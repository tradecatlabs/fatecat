
export interface TarotCardDefinition {
  name: string;
  nameChinese: string;
  number?: number;
  keywords: string[];
  reversedKeywords?: string[];
  suit: 'major' | 'wands' | 'cups' | 'swords' | 'pentacles';
  element?: string;
  astrologicalCorrespondence?: string;
}

export interface TarotSpreadDefinition {
  id: string;
  name: string;
  positions: string[];
}

export interface TarotCardResult {
  position: string;
  card: {
    name: string;
    nameChinese: string;
    keywords: string[];
  };
  orientation: 'upright' | 'reversed';
  meaning: string;
  number?: number;
  reversedKeywords?: string[];
  element?: string;
  astrologicalCorrespondence?: string;
}

// ===== 塔罗相关类型 =====

export interface TarotInput {
  spreadType?: string;
  question?: string;
  allowReversed?: boolean;
  seed?: string;
  seedScope?: string;
  birthYear?: number;
  birthMonth?: number;
  birthDay?: number;
}

export interface TarotNumerologyCard {
  number: number;
  name: string;
  nameChinese: string;
  keywords?: string[];
  element?: string;
  astrologicalCorrespondence?: string;
  year?: number;
}

export interface TarotNumerology {
  personalityCard: TarotNumerologyCard;
  soulCard: TarotNumerologyCard;
  yearlyCard: TarotNumerologyCard;
}

export interface TarotOutput {
  spreadId: string;
  spreadName: string;
  question?: string;
  seed: string;
  birthDate?: string;
  cards: TarotCardResult[];
  numerology?: TarotNumerology;
}

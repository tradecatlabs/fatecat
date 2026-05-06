import {
  BRANCH,
  FIVE_ELEMENT_SCHEME,
  GENDER,
  PALACE_HANT,
  STAR_HANT,
  STEM,
  TRANSFORMATION_HANT,
  YIN_YANG_HANS,
  ZODIAC_HANT,
} from "../../../constants";

export default {
  year: "年",
  age: "歲",
  hour: "時",
  one: YIN_YANG_HANS,
  gender: GENDER,
  stem: STEM,
  zodiac: ZODIAC_HANT,
  branch: BRANCH,
  palace: PALACE_HANT,
  star: STAR_HANT,
  transformation: TRANSFORMATION_HANT,
  fiveElementScheme: FIVE_ELEMENT_SCHEME,
} as const;

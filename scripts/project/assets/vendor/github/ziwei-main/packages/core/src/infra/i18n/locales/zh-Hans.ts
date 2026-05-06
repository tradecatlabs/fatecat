import {
  BRANCH,
  FIVE_ELEMENT_SCHEME,
  GENDER,
  PALACE_HANS,
  STAR_HANS,
  STEM,
  TRANSFORMATION_HANS,
  YIN_YANG_HANS,
  ZODIAC_HANS,
} from "../../../constants";

export default {
  year: "年",
  age: "岁",
  hour: "时",
  one: YIN_YANG_HANS,
  gender: GENDER,
  stem: STEM,
  zodiac: ZODIAC_HANS,
  branch: BRANCH,
  palace: PALACE_HANS,
  star: STAR_HANS,
  transformation: TRANSFORMATION_HANS,
  fiveElementScheme: FIVE_ELEMENT_SCHEME,
} as const;

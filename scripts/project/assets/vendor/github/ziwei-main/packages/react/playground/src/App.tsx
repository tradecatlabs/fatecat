import "./App.css";
import { colorPalette, ZiWei, ZiWeiSimulator } from "../../src";

export default function App() {
  return (
    <div>
      {/* 1994-2-16-7 */}
      <ZiWei side={800} name="xx" date="1983-5-12-5" gender="Yang" language="zh-Hant" />
      {/* <ZiWeiSimulator
        side={800}
        birthYearStemKey="Jia"
        ziweiBranchKey="Chou"
        mainPalaceBranchKey="Shen"
        language="zh-Hant"
        options={{
          showPalaceName: false,
          showSelf: false,
          showStem: false,
          showBranch: false,
          showTransformation: false,
          showLaiYin: false,
        }}
        config={{
          palaceHoroscopeFill: "transparent",
          ziweiPalaceFill: colorPalette.w8,
          palaceRectStrokeWidth: 0,
        }}
      /> */}
    </div>
  );
}

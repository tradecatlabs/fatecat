import * as fs from "fs";
import * as path from "path";
import gbNums from "./data/nums-basic.json";
import { Sex } from "./types";
import { getGoodNums } from "./utils";

fs.writeFileSync(
  path.join(__filename, "../data/good-nums.json"),
  JSON.stringify(getGoodNums(gbNums, Sex.female), null, 2)
);

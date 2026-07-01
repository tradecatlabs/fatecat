import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

export default function ThemeSelector({ currentThemeName, setCurrentThemeName }) {
  const handleThemeNameChange = (event) => {
    setCurrentThemeName(event.target.value);
  };

  return (
    <FormControl sx={{ minWidth: 120, m: 2 }}>
      <InputLabel id="theme-select-label">主题</InputLabel>
      <Select
        labelId="theme-select-label"
        id="theme-select"
        value={currentThemeName}
        label="主题"
        onChange={handleThemeNameChange}
      >
        {/* <MenuItem value="tianLan">天蓝主题</MenuItem>
        <MenuItem value="qingLv">青绿主题</MenuItem>
        <MenuItem value="chiHong">赤红主题</MenuItem>
        <MenuItem value="jinHuang">金黄主题</MenuItem> */}
        <MenuItem value="ciBai">瓷白主题</MenuItem>
        {/* <MenuItem value="yanZhi">胭脂主题</MenuItem> */}
        <MenuItem value="moHei">墨黑主题</MenuItem>
      </Select>
    </FormControl>
  );
} 
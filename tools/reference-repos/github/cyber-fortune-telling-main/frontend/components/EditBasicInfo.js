import { useEffect, useState } from "react";
import {
  Button,
  Card,
  CardContent,
  Typography,
  Box,
  Alert,
  Stack,
  TextField,
  RadioGroup,
  FormControlLabel,
  Radio,
  Select,
  MenuItem,
  Checkbox,
  FormGroup,
  FormControl,
  FormLabel,
} from "@mui/material";
import useFortuneTellingStore from "@/stores/fortuneTellingStore";

// 获取基本信息
function EditBasicInfo({ fortune_telling_uid }) {
  // 使用 Zustand store
  const {
    fortuneTellingUserInfo,
    setIsEditing,
    updateUserInfo,
    fetchEnumMappings,
    fetchFortuneTellingUserData,
    fetchFortuneSections,
    setHadUpdateUserInfoNeedRequestFortuneTellingInfo,
  } = useFortuneTellingStore();

  // 表单数据保持本地状态
  const [formData, setFormData] = useState({
    username: "",
    gender: "",
    birth_date: "",
    birth_time: "",
    height: "",
    weight: "",
    profession: "",
    constitution_type: "",
    sleep_quality: "",
    exercise_frequency: "",
    common_symptoms: [],
    dietary_preferences: [],
    body_discomfort: [],
    health_info: "",
    fortune_sections: [], // 默认为空，在加载配置后自动添加必填项
  });
  
  // 本地UI状态
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [enumMappings, setEnumMappings] = useState({});
  const [fortuneSections, setFortuneSections] = useState([]);

  // 当用户信息更新时，更新表单数据
  useEffect(() => {
    if (fortuneTellingUserInfo && fortuneSections.length > 0) {
      const userFortuneSections = fortuneTellingUserInfo.fortune_sections || [];
      // 确保必填栏目始终包含在选择中
      const requiredSections = fortuneSections.filter(section => section.required).map(section => section.key);
      const sectionsWithRequired = [...new Set([...userFortuneSections, ...requiredSections])];
      
      // 按照预定义顺序重新排列
      const allSectionKeys = fortuneSections.map(section => section.key);
      const sortedSections = allSectionKeys.filter(key => sectionsWithRequired.includes(key));
      
      setFormData({
        username: fortuneTellingUserInfo.username || "",
        gender: fortuneTellingUserInfo.gender || "",
        birth_date: fortuneTellingUserInfo.birth_date || "",
        birth_time: fortuneTellingUserInfo.birth_time || "",
        height: fortuneTellingUserInfo.height || "",
        weight: fortuneTellingUserInfo.weight || "",
        profession: fortuneTellingUserInfo.profession || "",
        constitution_type: fortuneTellingUserInfo.constitution_type || "",
        sleep_quality: fortuneTellingUserInfo.sleep_quality || "",
        exercise_frequency: fortuneTellingUserInfo.exercise_frequency || "",
        common_symptoms: fortuneTellingUserInfo.common_symptoms || [],
        dietary_preferences: fortuneTellingUserInfo.dietary_preferences || [],
        body_discomfort: fortuneTellingUserInfo.body_discomfort || [],
        health_info: fortuneTellingUserInfo.health_info || "",
        fortune_sections: sortedSections,
      });
    }
  }, [fortuneTellingUserInfo, fortuneSections]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (fieldName, value) => {
    setFormData((prev) => {
      const currentArray = prev[fieldName] || [];
      
      // 如果是必填栏目，且用户试图取消选择，则阻止操作
      if (fieldName === 'fortune_sections') {
        const section = fortuneSections.find(s => s.key === value);
        if (section?.required && currentArray.includes(value)) {
          return prev; // 不做任何更改
        }
      }
      
      let newArray;
      if (fieldName === 'fortune_sections') {
        // 对于栏目选择，需要保持预定义的顺序
        const allSectionKeys = fortuneSections.map(section => section.key);
        
        if (currentArray.includes(value)) {
          // 取消选择
          newArray = currentArray.filter(item => item !== value);
        } else {
          // 添加选择
          newArray = [...currentArray, value];
        }
        
        // 按照预定义顺序重新排列
        newArray = allSectionKeys.filter(key => newArray.includes(key));
      } else {
        // 其他字段保持原有逻辑
        newArray = currentArray.includes(value)
          ? currentArray.filter(item => item !== value)
          : [...currentArray, value];
      }
      
      return { ...prev, [fieldName]: newArray };
    });
  };

  const handleSubmit = async (e) => {
    e && e.preventDefault && e.preventDefault();
    setLoading(true);
    setSuccess(null);
    setError(null);
    
    // 验证栏目选择：确保至少有必填栏目
    const requiredSections = fortuneSections.filter(section => section.required).map(section => section.key);
    const finalSections = [...new Set([...formData.fortune_sections, ...requiredSections])];
    
    if (finalSections.length < 1) {
      setError("系统错误：没有可用的占卜栏目");
      setLoading(false);
      return;
    }
    
    // 确保必填栏目始终包含在提交数据中，并按照预定义顺序排列
    const sectionsWithRequired = [...new Set([...formData.fortune_sections, ...requiredSections])];
    
    // 按照预定义顺序重新排列
    const allSectionKeys = fortuneSections.map(section => section.key);
    const sortedSections = allSectionKeys.filter(key => sectionsWithRequired.includes(key));
    
    const submitFormData = {
      ...formData,
      fortune_sections: sortedSections
    };
    
    try {
      const result = await updateUserInfo(submitFormData, fortuneTellingUserInfo);
      
      if (result.success) {
        setSuccess("保存成功！");
        // 重新获取用户数据以确保数据同步
        await fetchFortuneTellingUserData(fortune_telling_uid);
        
        // 设置标志位，表示用户信息已更新，需要重新请求算命信息
        setHadUpdateUserInfoNeedRequestFortuneTellingInfo(true);

        setIsEditing(false);
      } else {
        setError(result.error || "保存失败，请重试。");
      }
    } catch (error) {
      setError("保存失败，请重试。");
    } finally {
      setLoading(false);
    }
  };

  const loadEnumMappings = async () => {
    try {
      const mappings = await fetchEnumMappings();
      setEnumMappings(mappings);
    } catch (error) {
      console.error('获取枚举映射失败:', error);
      setEnumMappings({});
    }
  };

  const loadFortuneSections = async () => {
    try {
      const sections = await fetchFortuneSections();
      setFortuneSections(sections);
    } catch (error) {
      console.error('获取栏目配置失败:', error);
      setFortuneSections([]);
    }
  };

  useEffect(() => {
    loadEnumMappings();
    loadFortuneSections();
    // 如果没有用户信息，获取用户数据
    if (!fortuneTellingUserInfo?.username) {
      fetchFortuneTellingUserData(fortune_telling_uid);
    }
  }, [fortune_telling_uid, fortuneTellingUserInfo?.username, fetchFortuneTellingUserData]);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        py: { xs: 4, md: 8 },
      }}
    >
      <Card
        sx={{
          maxWidth: 500,
          mx: "auto",
          borderRadius: 4,
          boxShadow: "0 4px 32px 0 #FFD70044",
          border: "2px solid #FFD700",
          background: "#000000",
          mb: 3,
        }}
      >
        <CardContent>
          <form onSubmit={handleSubmit}>
            <Stack spacing={3} mt={3}>
              <TextField
                name="username"
                label="用户名"
                value={formData.username}
                onChange={handleChange}
                fullWidth
                required
                variant="outlined"
                InputProps={{
                  sx: {
                    color: "#000",
                    backgroundColor: "#FFD700",
                    borderRadius: 2,
                    fontSize: 18,
                    height: 56,
                  },
                }}
                InputLabelProps={{
                  sx: {
                    color: "#000",
                    fontWeight: "bold",
                    "&.MuiInputLabel-shrink": {
                      backgroundColor: "#FFD700",
                      color: "#000",
                      px: 0.5,
                      borderRadius: 1,
                      zIndex: 1,
                    },
                  },
                }}
              />
              <RadioGroup
                row
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                sx={{
                  justifyContent: "center",
                  backgroundColor: "#FFD700",
                  borderRadius: 2,
                  px: 2,
                  py: 1,
                  mb: 1,
                }}
              >
                <FormControlLabel
                  value="male"
                  control={
                    <Radio
                      sx={{ color: "#000", "&.Mui-checked": { color: "#000" } }}
                    />
                  }
                  label={
                    <span style={{ color: "#000", fontWeight: "bold" }}>
                      男♂
                    </span>
                  }
                />
                <FormControlLabel
                  value="female"
                  control={
                    <Radio
                      sx={{ color: "#000", "&.Mui-checked": { color: "#000" } }}
                    />
                  }
                  label={
                    <span style={{ color: "#000", fontWeight: "bold" }}>
                      女♀
                    </span>
                  }
                />
              </RadioGroup>
              <TextField
                name="birth_date"
                label="出生日期"
                type="date"
                value={formData.birth_date}
                onChange={handleChange}
                fullWidth
                required
                variant="outlined"
                InputLabelProps={{
                  shrink: true,
                  sx: {
                    color: "#000",
                    fontWeight: "bold",
                    "&.MuiInputLabel-shrink": {
                      backgroundColor: "#FFD700",
                      color: "#000",
                      px: 0.5,
                      borderRadius: 1,
                      zIndex: 1,
                    },
                  },
                }}
                InputProps={{
                  sx: {
                    color: "#000",
                    backgroundColor: "#FFD700",
                    borderRadius: 2,
                    fontSize: 18,
                    height: 56,
                  },
                }}
              />
              <TextField
                name="birth_time"
                label="出生时间"
                type="time"
                value={formData.birth_time}
                onChange={handleChange}
                fullWidth
                required
                variant="outlined"
                InputLabelProps={{
                  shrink: true,
                  sx: {
                    color: "#000",
                    fontWeight: "bold",
                    "&.MuiInputLabel-shrink": {
                      backgroundColor: "#FFD700",
                      color: "#000",
                      px: 0.5,
                      borderRadius: 1,
                      zIndex: 1,
                    },
                  },
                }}
                InputProps={{
                  sx: {
                    color: "#000",
                    backgroundColor: "#FFD700",
                    borderRadius: 2,
                    fontSize: 18,
                    height: 56,
                  },
                }}
              />
              
              <Typography
                variant="subtitle1"
                sx={{ 
                  color: "#FFD700", 
                  fontWeight: "bold", 
                  textAlign: "center",
                  mt: 2,
                  mb: 1 
                }}
              >
                可选信息
              </Typography>
              
              <Select
                name="height"
                value={formData.height}
                onChange={handleChange}
                fullWidth
                displayEmpty
                variant="outlined"
                sx={{
                  color: "#000",
                  backgroundColor: "#FFD700",
                  borderRadius: 2,
                  fontSize: 18,
                  height: 56,
                  "& .MuiSelect-select": {
                    paddingTop: "16px",
                    paddingBottom: "16px",
                  },
                  "& .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#FFD700",
                  },
                }}
              >
                <MenuItem value="" sx={{ color: "#666" }}>
                  选择身高
                </MenuItem>
                {Array.from({ length: 201 }, (_, i) => {
                  const height = (50 + i) / 100; // 0.50m to 2.50m
                  return (
                    <MenuItem key={height} value={height}>
                      {height.toFixed(2)}米
                    </MenuItem>
                  );
                })}
              </Select>
              
              <Select
                name="weight"
                value={formData.weight}
                onChange={handleChange}
                fullWidth
                displayEmpty
                variant="outlined"
                sx={{
                  color: "#000",
                  backgroundColor: "#FFD700",
                  borderRadius: 2,
                  fontSize: 18,
                  height: 56,
                  "& .MuiSelect-select": {
                    paddingTop: "16px",
                    paddingBottom: "16px",
                  },
                  "& .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#FFD700",
                  },
                }}
              >
                <MenuItem value="" sx={{ color: "#666" }}>
                  选择体重
                </MenuItem>
                {Array.from({ length: 196 }, (_, i) => {
                  const weight = 5 + i; // 5kg to 200kg
                  return (
                    <MenuItem key={weight} value={weight}>
                      {weight}公斤
                    </MenuItem>
                  );
                })}
              </Select>
              
              <TextField
                name="profession"
                label="职业"
                value={formData.profession}
                onChange={handleChange}
                fullWidth
                variant="outlined"
                placeholder="可选填写您的职业或工作领域..."
                InputProps={{
                  sx: {
                    color: "#000",
                    backgroundColor: "#FFD700",
                    borderRadius: 2,
                    fontSize: 18,
                    height: 56,
                  },
                }}
                InputLabelProps={{
                  sx: {
                    color: "#000",
                    fontWeight: "bold",
                    "&.MuiInputLabel-shrink": {
                      backgroundColor: "#FFD700",
                      color: "#000",
                      px: 0.5,
                      borderRadius: 1,
                      zIndex: 1,
                    },
                  },
                }}
              />
              
              <Typography
                variant="subtitle1"
                sx={{ 
                  color: "#FFD700", 
                  fontWeight: "bold", 
                  textAlign: "center",
                  mt: 3,
                  mb: 1 
                }}
              >
                健康状况评估
              </Typography>
              
              <Select
                name="constitution_type"
                value={formData.constitution_type}
                onChange={handleChange}
                fullWidth
                displayEmpty
                variant="outlined"
                sx={{
                  color: "#000",
                  backgroundColor: "#FFD700",
                  borderRadius: 2,
                  fontSize: 18,
                  height: 56,
                  "& .MuiSelect-select": {
                    paddingTop: "16px",
                    paddingBottom: "16px",
                  },
                  "& .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#FFD700",
                  },
                }}
              >
                <MenuItem value="" sx={{ color: "#666" }}>
                  选择体质类型
                </MenuItem>
                {Object.entries(enumMappings.constitution_type || {}).map(([value, label]) => (
                  <MenuItem key={value} value={value} sx={{ fontSize: "14px" }}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
              
              <Select
                name="sleep_quality"
                value={formData.sleep_quality}
                onChange={handleChange}
                fullWidth
                displayEmpty
                variant="outlined"
                sx={{
                  color: "#000",
                  backgroundColor: "#FFD700",
                  borderRadius: 2,
                  fontSize: 18,
                  height: 56,
                  "& .MuiSelect-select": {
                    paddingTop: "16px",
                    paddingBottom: "16px",
                  },
                  "& .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#FFD700",
                  },
                }}
              >
                <MenuItem value="" sx={{ color: "#666" }}>
                  选择睡眠质量
                </MenuItem>
                {Object.entries(enumMappings.sleep_quality || {}).map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
              
              <Select
                name="exercise_frequency"
                value={formData.exercise_frequency}
                onChange={handleChange}
                fullWidth
                displayEmpty
                variant="outlined"
                sx={{
                  color: "#000",
                  backgroundColor: "#FFD700",
                  borderRadius: 2,
                  fontSize: 18,
                  height: 56,
                  "& .MuiSelect-select": {
                    paddingTop: "16px",
                    paddingBottom: "16px",
                  },
                  "& .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#FFD700",
                  },
                }}
              >
                <MenuItem value="" sx={{ color: "#666" }}>
                  选择运动频率
                </MenuItem>
                {Object.entries(enumMappings.exercise_frequency || {}).map(([value, label]) => (
                  <MenuItem key={value} value={value}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
              
              <FormControl component="fieldset" sx={{ mt: 2 }}>
                <FormLabel component="legend" sx={{ color: "#FFD700", fontWeight: "bold", mb: 1 }}>
                  常见症状 (可多选)
                </FormLabel>
                <FormGroup row>
                  {["失眠", "头痛", "胃痛", "便秘", "腹泻", "疲劳", "心悸", "咳嗽", "腰痛", "关节痛"].map((symptom) => (
                    <FormControlLabel
                      key={symptom}
                      control={
                        <Checkbox
                          checked={formData.common_symptoms.includes(symptom)}
                          onChange={() => handleCheckboxChange("common_symptoms", symptom)}
                          sx={{ color: "#FFD700", "&.Mui-checked": { color: "#FFD700" } }}
                        />
                      }
                      label={<span style={{ color: "#FFD700", fontSize: "14px" }}>{symptom}</span>}
                    />
                  ))}
                </FormGroup>
              </FormControl>
              
              <FormControl component="fieldset" sx={{ mt: 2 }}>
                <FormLabel component="legend" sx={{ color: "#FFD700", fontWeight: "bold", mb: 1 }}>
                  饮食偏好 (可多选)
                </FormLabel>
                <FormGroup row>
                  {["偏爱辛辣", "偏爱甜食", "偏爱油腻", "偏爱生冷", "偏爱热食", "清淡饮食", "素食主义", "不规律饮食"].map((preference) => (
                    <FormControlLabel
                      key={preference}
                      control={
                        <Checkbox
                          checked={formData.dietary_preferences.includes(preference)}
                          onChange={() => handleCheckboxChange("dietary_preferences", preference)}
                          sx={{ color: "#FFD700", "&.Mui-checked": { color: "#FFD700" } }}
                        />
                      }
                      label={<span style={{ color: "#FFD700", fontSize: "14px" }}>{preference}</span>}
                    />
                  ))}
                </FormGroup>
              </FormControl>
              
              <FormControl component="fieldset" sx={{ mt: 2 }}>
                <FormLabel component="legend" sx={{ color: "#FFD700", fontWeight: "bold", mb: 1 }}>
                  身体不适部位 (可多选)
                </FormLabel>
                <FormGroup row>
                  {["头部", "颈部", "肩部", "背部", "腰部", "腹部", "腿部", "脚部", "手部", "胸部"].map((part) => (
                    <FormControlLabel
                      key={part}
                      control={
                        <Checkbox
                          checked={formData.body_discomfort.includes(part)}
                          onChange={() => handleCheckboxChange("body_discomfort", part)}
                          sx={{ color: "#FFD700", "&.Mui-checked": { color: "#FFD700" } }}
                        />
                      }
                      label={<span style={{ color: "#FFD700", fontSize: "14px" }}>{part}</span>}
                    />
                  ))}
                </FormGroup>
              </FormControl>
              
              <TextField
                name="health_info"
                label="补充说明"
                multiline
                rows={2}
                value={formData.health_info}
                onChange={handleChange}
                fullWidth
                variant="outlined"
                placeholder="其他需要说明的健康情况..."
                InputProps={{
                  sx: {
                    color: "#000",
                    backgroundColor: "#FFD700",
                    borderRadius: 2,
                    fontSize: 16,
                  },
                }}
                InputLabelProps={{
                  sx: {
                    color: "#000",
                    fontWeight: "bold",
                    "&.MuiInputLabel-shrink": {
                      backgroundColor: "#FFD700",
                      color: "#000",
                      px: 0.5,
                      borderRadius: 1,
                      zIndex: 1,
                    },
                  },
                }}
              />
              
              <Typography
                variant="subtitle1"
                sx={{ 
                  color: "#FFD700", 
                  fontWeight: "bold", 
                  textAlign: "center",
                  mt: 3,
                  mb: 1 
                }}
              >
                占卜栏目选择
              </Typography>
              
              <Typography
                variant="body2"
                sx={{ 
                  color: "#FFD700", 
                  textAlign: "center",
                  mb: 2,
                  fontSize: "14px",
                  opacity: 0.8
                }}
              >
                选择您希望包含在算命结果中的栏目
                {fortuneSections.filter(section => section.required).length > 0 && (
                  <span>（{fortuneSections.filter(section => section.required).map(section => section.label).join('、')}会自动包含）</span>
                )}
              </Typography>
              
              <Stack direction="row" spacing={2} justifyContent="center" sx={{ mb: 2 }}>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => {
                    // 选择所有栏目（包括必填和可选）
                    const allSectionKeys = fortuneSections.map(s => s.key);
                    setFormData(prev => ({ 
                      ...prev, 
                      fortune_sections: allSectionKeys
                    }));
                  }}
                  sx={{
                    borderColor: "#FFD700",
                    color: "#FFD700",
                    fontSize: "12px",
                    "&:hover": {
                      borderColor: "#F4C430",
                      color: "#F4C430",
                    },
                  }}
                >
                  全选
                </Button>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => {
                    const requiredSections = fortuneSections.filter(section => section.required).map(section => section.key);
                    setFormData(prev => ({ 
                      ...prev, 
                      fortune_sections: requiredSections // 只保留必填栏目
                    }));
                  }}
                  sx={{
                    borderColor: "#FFD700",
                    color: "#FFD700",
                    fontSize: "12px",
                    "&:hover": {
                      borderColor: "#F4C430",
                      color: "#F4C430",
                    },
                  }}
                >
                  全不选
                </Button>
              </Stack>
              
              <FormControl component="fieldset" sx={{ mt: 1 }}>
                <Typography
                  variant="caption"
                  sx={{ 
                    color: "#FFD700", 
                    textAlign: "center",
                    mb: 1,
                    display: "block"
                  }}
                >
                  已选择 {formData.fortune_sections.filter(key => !fortuneSections.find(s => s.key === key)?.required).length} 个可选栏目
                </Typography>
                <FormGroup>
                  {fortuneSections.filter(section => !section.required).map((section) => {
                    return (
                      <FormControlLabel
                        key={section.key}
                        control={
                          <Checkbox
                            checked={formData.fortune_sections.includes(section.key)}
                            onChange={() => handleCheckboxChange("fortune_sections", section.key)}
                            sx={{ 
                              color: "#FFD700", 
                              "&.Mui-checked": { color: "#FFD700" },
                              "& .MuiSvgIcon-root": { fontSize: 20 }
                            }}
                          />
                        }
                        label={
                          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                            <span style={{ fontSize: "16px" }}>{section.icon}</span>
                            <Box>
                              <Typography variant="body2" sx={{ color: "#FFD700", fontWeight: "bold" }}>
                                {section.label}
                              </Typography>
                              <Typography variant="caption" sx={{ color: "#FFD700", opacity: 0.7 }}>
                                {section.description}
                              </Typography>
                            </Box>
                          </Box>
                        }
                        sx={{ 
                          mb: 1, 
                          backgroundColor: "rgba(255, 215, 0, 0.1)",
                          borderRadius: 1,
                          px: 1,
                          py: 0.5,
                          mr: 0,
                        }}
                      />
                    );
                  })}
                </FormGroup>
              </FormControl>
              
              <Stack
                direction="row"
                spacing={2}
                justifyContent="space-between"
                sx={{ mt: 3 }}
              >
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  disabled={loading}
                  sx={{
                    fontWeight: "bold",
                    backgroundColor: "#FFD700",
                    color: "#000",
                    border: "2px solid #FFD700",
                    borderRadius: 2,
                    height: 56,
                    fontSize: 18,
                    mt: 1,
                    "&:hover": {
                      backgroundColor: "#FFC300",
                      color: "#000",
                      border: "2px solid #FFD700",
                    },
                    "&.Mui-disabled": {
                      backgroundColor: "#FFD700",
                      color: "#333",
                      opacity: 0.7,
                      border: "2px solid #FFD700",
                    },
                  }}
                >
                  {loading ? "加载中..." : "保存"}
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => setIsEditing(false)}
                  sx={{
                    borderColor: "#FFD700",
                    color: "#FFD700",
                    borderRadius: 2,
                    height: 56,
                    fontWeight: "bold",
                    fontSize: 18,
                    "&:hover": {
                      borderColor: "#F4C430",
                      color: "#F4C430",
                    },
                  }}
                >
                  取消
                </Button>
              </Stack>
              {success && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  {success}
                </Alert>
              )}
              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
            </Stack>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
}

export default EditBasicInfo; 
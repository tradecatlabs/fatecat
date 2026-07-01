import { useState, useEffect } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  Typography,
  Box,
  Container,
  Stack,
  TextField,
  Button,
  Alert,
  RadioGroup,
  FormControlLabel,
  Radio,
} from "@mui/material";
import { useRouter } from "next/router";
import FortuneMasterAvatar from "../components/FortuneMasterAvatar";


const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:11337";
const API_TOKEN = process.env.NEXT_PUBLIC_API_TOKEN || "";

// 格式化时间为 HH:mm:ss.SSS
function formatBirthTime(time) {
  if (!time) return "";
  if (/^\d{2}:\d{2}:\d{2}\.\d{3}$/.test(time)) return time;
  if (/^\d{2}:\d{2}:\d{2}$/.test(time)) return time + ".000";
  return time + ":00.000";
}

export default function Register() {
  const [formData, setFormData] = useState({
    username: "",
    gender: "",
    birth_date: "",
    birth_time: "",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);
  const [displayedGreeting, setDisplayedGreeting] = useState("");
  const [isTyping, setIsTyping] = useState(true);
  const router = useRouter();

  // 问候语配置
  const greetings = {
    morning: "(^_^) / 早上好",
    noon: "(^o^) / 中午好", 
    afternoon: "(＾▽＾) / 下午好",
    evening: "(｡◕‿◕｡) / 晚上好",
    night: "(￣o￣) . z Z / 夜深了"
  };

  // 根据时间获取问候语
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) {
        return greetings.morning;
    } else if (hour >= 12 && hour < 14) {
        return greetings.noon;
    } else if (hour >= 14 && hour < 18) {
        return greetings.afternoon;
    } else if (hour >= 18 && hour < 22) {
        return greetings.evening;
    } else {
        return greetings.night;
    }
  };

  // 人类打字效果
  useEffect(() => {
    const fullText = getGreeting() + "，开始占卜吧！";
    let index = 0;
    setDisplayedGreeting("");
    setIsTyping(true);

    const typeNextChar = () => {
      if (index < fullText.length) {
        const char = fullText[index];
        setDisplayedGreeting(prev => prev + char);
        index++;

        // 计算下一个字符的延迟时间，模拟人类打字节奏
        let delay;
        
        // 标点符号后稍微停顿长一点
        if (char === '，' || char === '。' || char === '！' || char === '？') {
          delay = 200 + Math.random() * 300; // 200-500ms
        }
        // 空格稍微快一点
        else if (char === ' ') {
          delay = 50 + Math.random() * 50; // 50-100ms
        }
        // 表情符号稍微慢一点
        else if (/[\(\)\^_\-\.\|\/zZ￣o◕‿｡＾▽]/.test(char)) {
          delay = 80 + Math.random() * 120; // 80-200ms
        }
        // 普通字符：基础时间 + 随机变化
        else {
          delay = 60 + Math.random() * 100; // 60-160ms
        }

        setTimeout(typeNextChar, delay);
      } else {
        setIsTyping(false);
      }
    };

    // 开始打字前稍微等一下
    setTimeout(typeNextChar, 500);

    return () => {
      // 清理函数不需要特别处理，因为我们使用的是setTimeout
    };
  }, []);

  // 检查必填字段是否都已填写
  const isFormValid = formData.username.trim() !== '' && 
                     formData.gender !== '' && 
                     formData.birth_date !== '' && 
                     formData.birth_time !== '';

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(null);
    setError(null);
    try {
      const fortune_telling_uid = `uid-${Date.now()}-${Math.floor(Math.random()*10000)}`;
      const submitData = {
        ...formData,
        birth_time: formatBirthTime(formData.birth_time),
        fortune_telling_uid,
      };
      
      await axios.post(
        `${API_BASE_URL}/api/fortune-telling-users`,
        {
          data: submitData,
        },
        {
          headers: {
            Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined,
          },
        }
      );
      setSuccess("开始占卜成功！");
      setFormData({ 
        username: "", 
        gender: "", 
        birth_date: "", 
        birth_time: "", 
      });
      router.push(`/linkMe/${fortune_telling_uid}`);
    } catch (err) {
      setError("开始占卜失败，请重试。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{`
        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }
      `}</style>
      <Box
        sx={{
          minHeight: "100vh",
          backgroundImage:
            "linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.6)), url('/api/random-desk-decor-bg')",
          backgroundSize: { xs: 'cover', md: 'cover' },
          backgroundRepeat: "no-repeat",
          backgroundPosition: { xs: 'center', md: 'center' },
          py: { xs: 4, md: 8 },
        }}
      >
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingBottom: 4, paddingTop: 4 }}>
        <FortuneMasterAvatar size={120} />
      </Box>

      <Container maxWidth="sm">
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
            <Typography
              variant="h5"
              gutterBottom
              sx={{ 
                textAlign: "center", 
                fontWeight: "bold", 
                color: "#FFD700",
                minHeight: "3em", // 保持固定高度避免布局跳动
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexWrap: "wrap"
              }}
            >
              {displayedGreeting}
              {isTyping && (
                <span
                  style={{
                    display: "inline-block",
                    width: "2px",
                    height: "1.2em",
                    backgroundColor: "#FFD700",
                    marginLeft: "2px",
                    animation: "blink 1s infinite"
                  }}
                />
              )}
            </Typography>
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
                      color: '#000',
                      fontWeight: 'bold',
                      '&.MuiInputLabel-shrink': {
                        backgroundColor: '#FFD700',
                        color: '#000',
                        px: 0.5,
                        borderRadius: 1,
                        zIndex: 1,
                      }
                    }
                  }}
                />
                <RadioGroup
                  row
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  sx={{
                    justifyContent: 'center',
                    backgroundColor: '#FFD700',
                    borderRadius: 2,
                    px: 2,
                    py: 1,
                    mb: 1,
                  }}
                >
                  <FormControlLabel
                    value="male"
                    control={<Radio sx={{ color: '#000', '&.Mui-checked': { color: '#000' } }} />}
                    label={<span style={{ color: '#000', fontWeight: 'bold' }}>男♂</span>}
                  />
                  <FormControlLabel
                    value="female"
                    control={<Radio sx={{ color: '#000', '&.Mui-checked': { color: '#000' } }} />}
                    label={<span style={{ color: '#000', fontWeight: 'bold' }}>女♀</span>}
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
                  InputLabelProps={{ shrink: true, sx: {
                    color: '#000',
                    fontWeight: 'bold',
                    '&.MuiInputLabel-shrink': {
                      backgroundColor: '#FFD700',
                      color: '#000',
                      px: 0.5,
                      borderRadius: 1,
                      zIndex: 1,
                    }
                  }}}
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
                  InputLabelProps={{ shrink: true, sx: {
                    color: '#000',
                    fontWeight: 'bold',
                    '&.MuiInputLabel-shrink': {
                      backgroundColor: '#FFD700',
                      color: '#000',
                      px: 0.5,
                      borderRadius: 1,
                      zIndex: 1,
                    }
                  }}}
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
                
                {/* 必填字段提示 */}
                {!isFormValid && (
                  <Typography
                    variant="body2"
                    sx={{
                      color: "#FFD700",
                      textAlign: "center",
                      mt: 2,
                      opacity: 0.8,
                      fontStyle: "italic",
                    }}
                  >
                    请完成以下必填信息：
                    {!formData.username.trim() && " 用户名"}
                    {!formData.gender && " 性别"}
                    {!formData.birth_date && " 出生日期"}
                    {!formData.birth_time && " 出生时间"}
                  </Typography>
                )}
                
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  disabled={loading || !isFormValid}
                  sx={{
                    fontWeight: "bold",
                    backgroundColor: isFormValid ? "#FFD700" : "#666",
                    color: isFormValid ? "#000" : "#999",
                    border: `2px solid ${isFormValid ? "#FFD700" : "#666"}`,
                    borderRadius: 2,
                    height: 56,
                    fontSize: 18,
                    mt: 1,
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      backgroundColor: isFormValid ? '#FFC300' : '#666',
                      color: isFormValid ? '#000' : '#999',
                      border: `2px solid ${isFormValid ? "#FFD700" : "#666"}`,
                    },
                    '&.Mui-disabled': {
                      backgroundColor: isFormValid ? '#FFD700' : '#666',
                      color: isFormValid ? '#333' : '#999',
                      opacity: isFormValid ? 0.7 : 0.5,
                      border: `2px solid ${isFormValid ? "#FFD700" : "#666"}`,
                    },
                  }}
                >
                  {loading ? "信息录入中..." : isFormValid ? "开始占卜" : "请填写完整信息"}
                </Button>
                {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
                {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
              </Stack>
            </form>
          </CardContent>
        </Card>
      </Container>
    </Box>
    </>
  );
}

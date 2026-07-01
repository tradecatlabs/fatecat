import { useEffect, useState } from "react";
import {
  Button,
  Card,
  CardContent,
  Typography,
  Box,
  Alert,
  Stack,
  Chip,
  Collapse,
} from "@mui/material";
import LoadingSpinner from "@/components/LoadingSpinner";
import fortuneTellingUidStyles from "@/pages/linkMe/fortune_telling_uid.module.css";
import getZodiacByDate from "@/tools/getZodiacByDate";
import getChineseTraditionalTime from "@/tools/getChineseTraditionalTime";
import getChineseTraditionalDate from "@/tools/getChineseTraditionalDate";
import EditIcon from "@mui/icons-material/Edit";
import useFortuneTellingStore from "@/stores/fortuneTellingStore";
import SettingsIcon from "@mui/icons-material/Settings";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";

function ShowBasicInfo({ fortune_telling_uid }) {
  // 使用 Zustand store
  const {
    fortuneTellingUserInfo,
    getFortuneTellingUserInfoLoading,
    getFortuneTellingUserInfoError,
    isStreaming,
    loading,
    genderEmoji,
    setIsEditing,
    fetchFortuneSections,
  } = useFortuneTellingStore();

  // 本地状态用于计算的值
  const [zodiac, setZodiac] = useState("");
  const [chineseTraditionalTime, setChineseTraditionalTime] = useState("");
  const [chineseTraditionalDate, setChineseTraditionalDate] = useState("");
  const [fortuneSections, setFortuneSections] = useState([]);
  
  // 折叠状态
  const [isExpanded, setIsExpanded] = useState(false);

  // 根据出生日期获取生肖
  useEffect(() => {
    if (fortuneTellingUserInfo && fortuneTellingUserInfo.birth_date) {
      setZodiac(getZodiacByDate(fortuneTellingUserInfo.birth_date));
    }
  }, [fortuneTellingUserInfo?.birth_date]);

  // 根据birth_time 获取中国传统时间 getChineseTraditionalTime
  useEffect(() => {
    if (fortuneTellingUserInfo && fortuneTellingUserInfo.birth_time) {
      setChineseTraditionalTime(
        getChineseTraditionalTime(fortuneTellingUserInfo.birth_time)
      );
    }
  }, [fortuneTellingUserInfo?.birth_time]);

  // 根据birth_date 获取中国传统日期 getChineseTraditionalDate
  useEffect(() => {
    if (fortuneTellingUserInfo && fortuneTellingUserInfo.birth_date) {
      setChineseTraditionalDate(
        getChineseTraditionalDate(fortuneTellingUserInfo.birth_date)
      );
    }
  }, [fortuneTellingUserInfo?.birth_date]);

  // 获取栏目配置
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
    loadFortuneSections();
  }, []);

  // 获取用户选择的栏目信息
  const getSelectedSections = () => {
    if (!fortuneTellingUserInfo?.fortune_sections || !fortuneSections.length) {
      return [];
    }
    
    return fortuneSections.filter(section => 
      fortuneTellingUserInfo.fortune_sections.includes(section.key)
    );
  };

  const selectedSections = getSelectedSections();

  // 检查是否有详细信息可以显示
  const hasDetailedInfo = () => {
    if (!fortuneTellingUserInfo) return false;
    
    return !!(
      fortuneTellingUserInfo.height ||
      fortuneTellingUserInfo.weight ||
      fortuneTellingUserInfo.profession ||
      fortuneTellingUserInfo.constitution_type ||
      fortuneTellingUserInfo.sleep_quality ||
      fortuneTellingUserInfo.exercise_frequency ||
      (fortuneTellingUserInfo.common_symptoms && fortuneTellingUserInfo.common_symptoms.length > 0) ||
      (fortuneTellingUserInfo.dietary_preferences && fortuneTellingUserInfo.dietary_preferences.length > 0) ||
      (fortuneTellingUserInfo.body_discomfort && fortuneTellingUserInfo.body_discomfort.length > 0) ||
      fortuneTellingUserInfo.health_info
    );
  };

  return (
    <Box
      sx={{
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        mt: 2,
      }}
    >
      <Card
        sx={{
          width: "100%",
          maxWidth: 400,
          borderRadius: 4,
          boxShadow: "0 4px 32px 0 #FFD70044",
          border: "2px solid #FFD700",
          background: "rgba(255,255,255,0.95)",
          mb: 3,
        }}
      >
        <CardContent>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              mb: 2,
            }}
          >
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                color: "#1A237E",
                fontWeight: 700,
                textAlign: "center",
                mb: 0,
              }}
            >
              基本信息
            </Typography>
            {/* 移除原本标题旁的设置按钮 */}
          </Box>
          {getFortuneTellingUserInfoLoading && (
            <Box display="flex" justifyContent="center" my={2}>
              <LoadingSpinner />
            </Box>
          )}
          {getFortuneTellingUserInfoError && (
          <Alert severity="error">
            {getFortuneTellingUserInfoError?.message || 
             getFortuneTellingUserInfoError?.toString() || 
             "获取用户信息失败"}
          </Alert>
        )}
          {!getFortuneTellingUserInfoLoading &&
            !getFortuneTellingUserInfoError &&
            fortuneTellingUserInfo && (
              <Stack spacing={2}>
                <Stack direction="row" spacing={1}>
                  <Typography
                    className={fortuneTellingUidStyles["user-info-title"]}
                    sx={{ fontWeight: 600, color: "#1A237E" }}
                  >
                    姓名：
                  </Typography>
                  <Typography
                    className={`${fortuneTellingUidStyles["username"]} ${fortuneTellingUidStyles["user-info-value"]}`}
                  >
                    {fortuneTellingUserInfo.username}
                  </Typography>
                </Stack>
                <Stack direction="row" spacing={1}>
                  <Typography
                    className={fortuneTellingUidStyles["user-info-title"]}
                    sx={{ fontWeight: 600, color: "#1A237E" }}
                  >
                    性别：
                  </Typography>
                  <Typography
                    className={fortuneTellingUidStyles["user-info-value"]}
                    key={fortuneTellingUserInfo.gender}
                  >
                    {fortuneTellingUserInfo.gender === "male"
                      ? "♂ " + genderEmoji
                      : "♀ " + genderEmoji}
                  </Typography>
                </Stack>
                <Stack direction="row" spacing={1}>
                  <Typography
                    className={fortuneTellingUidStyles["user-info-title"]}
                    sx={{ fontWeight: 600, color: "#1A237E" }}
                  >
                    生日：
                  </Typography>
                  <Typography
                    className={`${fortuneTellingUidStyles["birth_date"]} ${fortuneTellingUidStyles["user-info-value"]}`}
                  >
                    {fortuneTellingUserInfo.birth_date} {chineseTraditionalDate}{" "}
                    {zodiac}
                  </Typography>
                </Stack>
                <Stack direction="row" spacing={1}>
                  <Typography
                    className={fortuneTellingUidStyles["user-info-title"]}
                    sx={{ fontWeight: 600, color: "#1A237E" }}
                  >
                    时间：
                  </Typography>
                  <Typography
                    className={`${fortuneTellingUidStyles["birth-time"]} ${fortuneTellingUidStyles["user-info-value"]}`}
                  >
                    {fortuneTellingUserInfo.birth_time} {chineseTraditionalTime}
                  </Typography>
                </Stack>
                
                {/* 展开/收起按钮 */}
                {hasDetailedInfo() && (
                  <Box sx={{ display: "flex", justifyContent: "center", mt: 1 }}>
                    <Button
                      variant="text"
                      size="small"
                      onClick={() => setIsExpanded(!isExpanded)}
                      sx={{
                        color: "#1A237E",
                        fontSize: "12px",
                        textTransform: "none",
                        minWidth: 0,
                      }}
                      endIcon={isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                    >
                      {isExpanded ? "收起信息" : "更多信息"}
                    </Button>
                  </Box>
                )}

                {/* 可折叠的详细信息区域 */}
                <Collapse in={isExpanded}>
                  <Stack spacing={2} sx={{ mt: 2 }}>
                    {fortuneTellingUserInfo.height && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          身高：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.height}米
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.weight && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          体重：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.weight}公斤
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.profession && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          职业：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.profession}
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.constitution_type && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          体质：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.constitution_type_label || fortuneTellingUserInfo.constitution_type}
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.sleep_quality && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          睡眠：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.sleep_quality_label || fortuneTellingUserInfo.sleep_quality}
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.exercise_frequency && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          运动：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.exercise_frequency_label || fortuneTellingUserInfo.exercise_frequency}
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.common_symptoms && fortuneTellingUserInfo.common_symptoms.length > 0 && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          症状：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.common_symptoms.join(", ")}
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.dietary_preferences && fortuneTellingUserInfo.dietary_preferences.length > 0 && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          饮食：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.dietary_preferences.join(", ")}
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.body_discomfort && fortuneTellingUserInfo.body_discomfort.length > 0 && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          不适：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                        >
                          {fortuneTellingUserInfo.body_discomfort.join(", ")}
                        </Typography>
                      </Stack>
                    )}
                    {fortuneTellingUserInfo.health_info && (
                      <Stack direction="row" spacing={1}>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-title"]}
                          sx={{ fontWeight: 600, color: "#1A237E" }}
                        >
                          补充：
                        </Typography>
                        <Typography
                          className={fortuneTellingUidStyles["user-info-value"]}
                          sx={{ 
                            whiteSpace: "pre-wrap",
                            wordBreak: "break-word",
                            maxWidth: "200px"
                          }}
                        >
                          {fortuneTellingUserInfo.health_info}
                        </Typography>
                      </Stack>
                    )}
                  </Stack>
                </Collapse>
                
                {/* 显示用户勾选的栏目 */}
                {selectedSections.length > 0 && (
                  <Box sx={{ mt: 3, pt: 2, borderTop: "1px solid #E0E0E0" }}>
                    <Typography
                      variant="subtitle2"
                      sx={{ 
                        fontWeight: 600, 
                        color: "#1A237E",
                        mb: 1.5,
                        textAlign: "left"
                      }}
                    >
                      占卜栏目
                    </Typography>
                    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, justifyContent: "flex-start" }}>
                      {selectedSections.map((section) => (
                        <Chip
                          key={section.key}
                          label={
                            <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                              <span style={{ fontSize: "12px" }}>{section.icon}</span>
                              <span style={{ fontSize: "12px", fontWeight: 500 }}>
                                {section.label}
                              </span>
                            </Box>
                          }
                          size="small"
                          sx={{
                            backgroundColor: "#1A237E",
                            color: "white",
                            fontSize: "11px",
                            height: "24px",
                            "& .MuiChip-label": {
                              px: 1,
                              py: 0.5,
                            },
                            "&:hover": {
                              backgroundColor: "#303F9F",
                            },
                          }}
                        />
                      ))}
                    </Box>
                    <Typography
                      variant="caption"
                      sx={{ 
                        color: "#666",
                        textAlign: "left",
                        display: "block",
                        mt: 1,
                        fontSize: "10px"
                      }}
                    >
                      共选择 {selectedSections.length} 个栏目
                    </Typography>
                  </Box>
                )}
                {/* 在底部居中显示设置按钮 */}
                {!isStreaming && (
                  <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                    <Button
                      variant="outlined"
                      size="medium"
                      startIcon={<SettingsIcon />}
                      sx={{ 
                        color: "#1A237E",
                        borderColor: "#1A237E",
                        borderRadius: "20px",
                        px: 3,
                        py: 1,
                        fontSize: "14px",
                        fontWeight: 500,
                        textTransform: "none",
                        boxShadow: "0 2px 4px rgba(26, 35, 126, 0.1)",
                        transition: "all 0.2s ease-in-out",
                        "&:hover": {
                          backgroundColor: "#1A237E",
                          color: "white",
                          borderColor: "#1A237E",
                          boxShadow: "0 4px 8px rgba(26, 35, 126, 0.2)",
                          transform: "translateY(-1px)",
                        },
                        "&:active": {
                          transform: "translateY(0px)",
                          boxShadow: "0 2px 4px rgba(26, 35, 126, 0.1)",
                        }
                      }}
                      disabled={loading || isStreaming}
                      onClick={() => setIsEditing(true)}
                    >
                      编辑信息
                    </Button>
                  </Box>
                )}
              </Stack>
            )}
        </CardContent>
      </Card>
    </Box>
  );
}

export default ShowBasicInfo; 
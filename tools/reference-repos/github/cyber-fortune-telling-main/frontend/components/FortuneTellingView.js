import {
  Button,
  Card,
  CardContent,
  Typography,
  Box,
  Alert,
  Stack,
} from "@mui/material";
import { motion } from "framer-motion";
import styles from "@/styles/Markdown.module.css";
import LoadingSpinner from "@/components/LoadingSpinner";
import FortuneMasterAvatar from "@/components/FortuneMasterAvatar";
import StyledMarkdown from "@/components/StyledMarkdown";
import EditBasicInfo from "@/components/EditBasicInfo";
import ShowBasicInfo from "@/components/ShowBasicInfo";
import useFortuneTellingStore from "@/stores/fortuneTellingStore";

// 创建占卜视图组件
function FortuneTellingView({ fortune_telling_uid }) {
  // 使用 Zustand store
  const {
    isEditing,
    loading,
    error,
    isStreaming,
    fortuneData,
    streamingText,
    allowRunFortuneTellingRequest,
    desktopDecoration,
    genderEmoji,
    setSpiritualPractice,
    requestFortuneTellingInfo,
  } = useFortuneTellingStore();

  return (
    <Stack spacing={3} alignItems="center">
      <Box sx={{ height: 20 }} />
      <FortuneMasterAvatar size={120} />

      {isEditing ? (
        <EditBasicInfo fortune_telling_uid={fortune_telling_uid} />
      ) : (
        <>
          <ShowBasicInfo fortune_telling_uid={fortune_telling_uid} />

          {loading && <LoadingSpinner />}
          {error && <Alert severity="error">{error}</Alert>}

          {(isStreaming || fortuneData) && (
            <Card sx={{ maxWidth: 800, width: "100%", margin: "20px" }}>
              <CardContent>
                <div className={styles["waving-container"]}>
                  <Typography
                    variant="h5"
                    gutterBottom
                    className={`${
                      isStreaming ? styles["mystical-title"] : ""
                    } ${styles["wave-text"]}`}
                    sx={{ textAlign: "center", fontWeight: "bold" }}
                  >
                    {[..."✨满血大圆满玄乎儿大师曰"].map((char, index) => (
                      <span key={index}>{char}</span>
                    ))}
                  </Typography>
                </div>
                <StyledMarkdown
                  content={
                    isStreaming ? streamingText : fortuneData.textResponse
                  }
                />
              </CardContent>
            </Card>
          )}

          <Stack direction="row" spacing={2}>
            {!fortuneData && !isStreaming && allowRunFortuneTellingRequest ? (
              <Button
                variant="contained"
                onClick={() => requestFortuneTellingInfo(fortune_telling_uid)}
                disabled={loading || isStreaming}
              >
                开始占卜
              </Button>
            ) : desktopDecoration ? (
              <Button
                variant="contained"
                onClick={() => {
                  console.log("进入玄修");
                  setSpiritualPractice(true);
                }}
                sx={{
                  position: "fixed",
                  top: 20,
                  right: 20,
                  zIndex: 1000,
                }}
              >
                玄修 {genderEmoji}
              </Button>
            ) : null}
          </Stack>
          <Box sx={{ height: 10 }} />
        </>
      )}
    </Stack>
  );
}

export default FortuneTellingView; 
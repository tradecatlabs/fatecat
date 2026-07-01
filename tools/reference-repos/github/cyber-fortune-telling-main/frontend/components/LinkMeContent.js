import { useEffect } from "react";
import { Box, Button } from "@mui/material";
import moment from "moment";
import SignInCalendar from "@/components/SignInCalendar";
import ChatInput from "@/components/ChatInput";
import ChatMarkdownStack from "@/components/ChatMarkdownStack";
import SpiritualPracticeView from "@/components/SpiritualPracticeView";
import FortuneTellingView from "@/components/FortuneTellingView";
import useFortuneTellingStore from "@/stores/fortuneTellingStore";

function LinkMeContent({ fortune_telling_uid }) {
  // 使用 Zustand store
  const {
    // 状态
    fortuneTellingUserInfo,
    loading,
    error,
    isEditing,
    streamingText,
    isStreaming,
    spiritualPractice,
    desktopDecoration,
    tips,
    currentTip,
    animationKey,
    getFortuneTellingUserInfoError,
    getFortuneTellingUserInfoLoading,
    allowRunFortuneTellingRequest,
    conversationId,
    prompt,
    newAIResponse,
    newAIResponseIsStreaming,
    chatInputDisabled,
    requestFortuneTellingInfoDone,
    genderEmoji,
    conversationHistory,
    currentChatList,
    showInput,
    historyOpen,
    fortuneData,
    REFRESH_HOUR,
    REFRESH_MINUTE,
    CHECK_INTERVAL,
    hadUpdateUserInfoNeedRequestFortuneTellingInfo,
    
    // 方法
    setIsEditing,
    setPrompt,
    setSpiritualPractice,
    setHistoryOpen,
    setCurrentTip,
    setAnimationKey,
    setHadUpdateUserInfoNeedRequestFortuneTellingInfo,
    
    // 异步操作
    fetchFortuneTellingUserData,
    requestFortuneTellingInfo,
    getConversationId,
    sendPrompt,
    
    // 计算属性
    isUserInfoComplete,
    updateShowInputStatus,
    
    // 初始化方法
    initializeGenderEmoji,
    
    // 重置方法
    reset,
  } = useFortuneTellingStore();

  // 检查用户信息是否完整，并自动触发占卜
  useEffect(() => {
    console.log("检查用户信息是否完整==", fortuneTellingUserInfo);
    if (fortuneTellingUserInfo && isUserInfoComplete()) {
      // 如果信息完整且没有正在进行的请求，并且还没有占卜数据，自动触发占卜
      if (!loading && !isStreaming && !fortuneData && !requestFortuneTellingInfoDone) {
        requestFortuneTellingInfo(fortune_telling_uid);
      }
    }
  }, [fortuneTellingUserInfo, loading, isStreaming, fortuneData, requestFortuneTellingInfoDone, fortune_telling_uid]);

  // 页面加载完成后自动获取用户数据
  useEffect(() => {
    if (isEditing === false) {
      fetchFortuneTellingUserData(fortune_telling_uid);
    }
  }, [isEditing, fortune_telling_uid]);

  // 监听用户信息更新后需要重新请求算命信息的标志
  useEffect(() => {
    if (isEditing === false && hadUpdateUserInfoNeedRequestFortuneTellingInfo) {
      // 用户信息已更新，需要重新请求算命信息
      console.log("用户信息已更新，正在重新请求算命信息...");
      requestFortuneTellingInfo(fortune_telling_uid);
      // 重置标志位
      setHadUpdateUserInfoNeedRequestFortuneTellingInfo(false);
    }
  }, [isEditing, hadUpdateUserInfoNeedRequestFortuneTellingInfo, fortune_telling_uid]);

  // 当占卜请求完成时，获取对话ID
  useEffect(() => {
    if (requestFortuneTellingInfoDone && !conversationId) {
      // 延迟1秒再获取conversation_id
      setTimeout(() => {
        getConversationId(fortune_telling_uid);
      }, 1000);
    }
  }, [requestFortuneTellingInfoDone, conversationId, fortune_telling_uid]);

  // 初始化性别表情
  useEffect(() => {
    if (fortuneTellingUserInfo?.gender) {
      initializeGenderEmoji();
    }
  }, [fortuneTellingUserInfo?.gender]);

  // 更新显示输入框状态
  useEffect(() => {
    updateShowInputStatus();
  }, [conversationHistory, currentChatList]);

  // 使用useEffect来管理动画和tip更新
  useEffect(() => {
    if (tips.length > 0 && spiritualPractice) {
      // 立即设置第一个随机tip
      const randomIndex = Math.floor(Math.random() * tips.length);
      setCurrentTip(tips[randomIndex]);

      // 设置定时器每10秒更新一次动画和tip
      const interval = setInterval(() => {
        const newRandomIndex = Math.floor(Math.random() * tips.length);
        setCurrentTip(tips[newRandomIndex]);
        setAnimationKey((prev) => prev + 1); // 强制重新渲染动画
      }, 10000);

      // 清理定时器
      return () => clearInterval(interval);
    }
  }, [tips, spiritualPractice, setCurrentTip, setAnimationKey]);

  // 监听本地时间，特定时刻刷新页面
  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const todayStr = `${now.getFullYear()}-${
        now.getMonth() + 1
      }-${now.getDate()}`;
      const lastRefresh = localStorage.getItem("lastAutoRefresh");

      if (
        now.getHours() === REFRESH_HOUR &&
        now.getMinutes() === REFRESH_MINUTE &&
        lastRefresh !== todayStr
      ) {
        localStorage.setItem("lastAutoRefresh", todayStr);
        console.log("时间符合条件刷新页面");
        window.location.reload();
      }
    }, CHECK_INTERVAL);
    return () => clearInterval(interval);
  }, [REFRESH_HOUR, REFRESH_MINUTE, CHECK_INTERVAL]);

  // 组件卸载时重置状态
  useEffect(() => {
    return () => {
      reset();
    };
  }, [reset]);

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundImage:
          "linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.6)), url('/api/random-desk-decor-bg')",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
      }}
    >
      {spiritualPractice === false && (
        <>
          <FortuneTellingView
            genderEmoji={genderEmoji}
            fortune_telling_uid={fortune_telling_uid}
            isEditing={isEditing}
            setIsEditing={setIsEditing}
            fortuneTellingUserInfo={fortuneTellingUserInfo}
            getFortuneTellingUserInfoLoading={getFortuneTellingUserInfoLoading}
            getFortuneTellingUserInfoError={getFortuneTellingUserInfoError}
            loading={loading}
            error={error}
            isStreaming={isStreaming}
            fortuneData={fortuneData}
            streamingText={streamingText}
            allowRunFortuneTellingRequest={allowRunFortuneTellingRequest}
            desktopDecoration={desktopDecoration}
            requestFortuneTellingInfo={() => requestFortuneTellingInfo(fortune_telling_uid)}
            setSpiritualPractice={setSpiritualPractice}
          />

          {/* 创建一个折叠历史记录的div, 点击可以展开，默认折叠 */}
          {conversationId && conversationHistory.length > 0 && (
            <Box sx={{ my: 2, maxWidth: 800, mx: "auto" }}>
              <Button
                variant="outlined"
                onClick={() => setHistoryOpen(!historyOpen)}
                sx={{
                  mb: 1,
                  color: "#FFD700",
                  borderColor: "#FFD700",
                  fontWeight: "bold",
                }}
                fullWidth
              >
                {historyOpen
                  ? "收起历史对话"
                  : `展开历史对话（${conversationHistory.length}条）`}
              </Button>
              {historyOpen && (
                <Box
                  sx={{
                    maxHeight: 400,
                    overflowY: "auto",
                    border: "1px solid #FFD700",
                    borderRadius: 2,
                    p: 1,
                    background: "rgba(0,0,0,0.05)",
                  }}
                >
                  {conversationHistory.map((item, index) => {
                    return (
                      <ChatMarkdownStack
                        genderEmoji={genderEmoji}
                        username={fortuneTellingUserInfo.username}
                        key={"conversationHistory" + index}
                        item={item}
                      />
                    );
                  })}
                </Box>
              )}
            </Box>
          )}
          
          {/* 当前的对话记录 */}
          <div className="currentChatList">
            {currentChatList.map((item, index) => {
              return (
                <ChatMarkdownStack
                  genderEmoji={genderEmoji}
                  username={fortuneTellingUserInfo.username}
                  key={"currentChatList" + index}
                  item={item}
                />
              );
            })}
          </div>

          {newAIResponse && newAIResponseIsStreaming === true && (
            <ChatMarkdownStack item={{ content: newAIResponse }} />
          )}

          <div
            style={{
              height: "100px",
            }}
          >
            {showInput === false ? (
              <div
                style={{
                  textAlign: "center",
                  fontSize: "20px",
                  color: "#FFD700",
                  position: "fixed",
                  bottom: 0,
                  left: 0,
                  right: 0,
                  zIndex: 1000,
                  background: "rgba(0,0,0,0.5)",
                  padding: "10px 0",
                }}
              >
                明天见
              </div>
            ) : null}
          </div>

          {/* 创建一个Input 和一个发送按钮的组合 */}
          {conversationId &&
            newAIResponseIsStreaming === false &&
            showInput === true && (
              <ChatInput
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onSend={sendPrompt}
                disabled={chatInputDisabled}
              />
            )}

          {/* 签到浮窗组件 */}
          {/* <SignInCalendar
            fortune_telling_uid={fortune_telling_uid}
          /> */}
        </>
      )}

      {spiritualPractice === true && (
        <SpiritualPracticeView
          tips={tips}
          currentTip={currentTip}
          animationKey={animationKey}
          desktopDecoration={desktopDecoration}
          setSpiritualPractice={setSpiritualPractice}
        />
      )}
    </div>
  );
}

export default LinkMeContent; 
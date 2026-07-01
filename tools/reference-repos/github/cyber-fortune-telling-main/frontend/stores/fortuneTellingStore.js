import { create } from 'zustand';
import axios from 'axios';
import moment from 'moment';
import getGenderEmoji from '@/tools/getGenderEmoji';
import extractDesktopDecoration from '@/tools/extractDesktopDecoration';
import extractFortuneTips from '@/tools/extractFortuneTips';
import formatBirthTime from '@/tools/formatBirthTime';

// API 配置
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:11337";
const API_TOKEN = process.env.NEXT_PUBLIC_API_TOKEN || "";

const useFortuneTellingStore = create((set, get) => ({
  // ============ 用户信息相关状态 ============
  fortuneTellingUserInfo: {},
  setFortuneTellingUserInfo: (info) => set({ fortuneTellingUserInfo: info }),
  
  // ============ 加载状态 ============
  loading: false,
  error: null,
  isStreaming: false,
  getFortuneTellingUserInfoLoading: false,
  getFortuneTellingUserInfoError: null,
  
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  setIsStreaming: (isStreaming) => set({ isStreaming }),
  setGetFortuneTellingUserInfoLoading: (loading) => set({ getFortuneTellingUserInfoLoading: loading }),
  setGetFortuneTellingUserInfoError: (error) => set({ getFortuneTellingUserInfoError: error }),

  // ============ 占卜数据 ============
  fortuneData: null,
  streamingText: "",
  allowRunFortuneTellingRequest: false,
  requestFortuneTellingInfoDone: false,
  
  setFortuneData: (data) => set({ fortuneData: data }),
  setStreamingText: (text) => set({ streamingText: text }),
  setAllowRunFortuneTellingRequest: (allow) => set({ allowRunFortuneTellingRequest: allow }),
  setRequestFortuneTellingInfoDone: (done) => set({ requestFortuneTellingInfoDone: done }),

  // ============ UI 状态 ============
  isEditing: false,
  spiritualPractice: false,
  showInput: true,
  historyOpen: false,
  
  setIsEditing: (editing) => set({ isEditing: editing }),
  setSpiritualPractice: (practice) => set({ spiritualPractice: practice }),
  setShowInput: (show) => set({ showInput: show }),
  setHistoryOpen: (open) => set({ historyOpen: open }),

  // ============ 用户信息更新后需要重新请求算命信息的标志 ============
  hadUpdateUserInfoNeedRequestFortuneTellingInfo: false,
  
  setHadUpdateUserInfoNeedRequestFortuneTellingInfo: (need) => set({ hadUpdateUserInfoNeedRequestFortuneTellingInfo: need }),

  // ============ 对话相关 ============
  conversationId: "",
  conversationHistory: [],
  currentChatList: [],
  prompt: "",
  newAIResponse: "",
  newAIResponseIsStreaming: false,
  chatInputDisabled: false,
  
  setConversationId: (id) => set({ conversationId: id }),
  setConversationHistory: (history) => set({ conversationHistory: history }),
  setCurrentChatList: (list) => set({ currentChatList: list }),
  setPrompt: (prompt) => set({ prompt }),
  setNewAIResponse: (response) => set({ newAIResponse: response }),
  setNewAIResponseIsStreaming: (streaming) => set({ newAIResponseIsStreaming: streaming }),
  setChatInputDisabled: (disabled) => set({ chatInputDisabled: disabled }),
  
  addToCurrentChatList: (message) => set((state) => ({
    currentChatList: [...state.currentChatList, message]
  })),

  // ============ 装饰和提示 ============
  desktopDecoration: "",
  tips: [],
  currentTip: "",
  animationKey: 0,
  genderEmoji: "",
  
  setDesktopDecoration: (decoration) => set({ desktopDecoration: decoration }),
  setTips: (tips) => set({ tips }),
  setCurrentTip: (tip) => set({ currentTip: tip }),
  setAnimationKey: (key) => set({ animationKey: key }),
  setGenderEmoji: (emoji) => set({ genderEmoji: emoji }),

  // ============ 栏目配置 ============
  fortuneSections: [],
  selectedSections: [],
  
  setFortuneSections: (sections) => set({ fortuneSections: sections }),
  setSelectedSections: (sections) => set({ selectedSections: sections }),

  // ============ 常量 ============
  MAX_CHAT_LIST_LENGTH: 30,
  REFRESH_HOUR: 0,
  REFRESH_MINUTE: 0 + Math.floor(Math.random() * 5),
  CHECK_INTERVAL: 30000,

  // ============ 计算属性 ============
  isUserInfoComplete: () => {
    const { fortuneTellingUserInfo } = get();
    const { username, gender, birth_date, birth_time } = fortuneTellingUserInfo;
    return Boolean(username && gender && birth_date && birth_time);
  },

  shouldHideInput: () => {
    const { conversationHistory, currentChatList, MAX_CHAT_LIST_LENGTH } = get();
    return conversationHistory.length + currentChatList.length > MAX_CHAT_LIST_LENGTH;
  },

  // ============ 异步操作 ============
  
  // 获取用户信息
  fetchFortuneTellingUserData: async (fortune_telling_uid) => {
    const { setGetFortuneTellingUserInfoLoading, setGetFortuneTellingUserInfoError, setFortuneTellingUserInfo } = get();
    
    try {
      setGetFortuneTellingUserInfoLoading(true);
      setGetFortuneTellingUserInfoError(null);

      const response = await axios.get(
        `${API_BASE_URL}/api/fortune-telling-users?username=*&filters[fortune_telling_uid][$eq]=${fortune_telling_uid}&date=${moment().format("YYYY-MM-DD")}`,
        {
          headers: {
            Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined,
          },
        }
      );
      
      setFortuneTellingUserInfo(response.data.data[0]);
      console.log("设置用户信息==", response.data.data[0]);
    } catch (err) {
      setGetFortuneTellingUserInfoError(err);
    } finally {
      setGetFortuneTellingUserInfoLoading(false);
    }
  },

  // 获取对话ID和历史记录
  getConversationId: async (fortune_telling_uid) => {
    const { 
      fortuneTellingUserInfo, 
      setConversationId, 
      setConversationHistory, 
      setChatInputDisabled 
    } = get();
    
    if (
      fortuneTellingUserInfo.username &&
      fortuneTellingUserInfo.gender &&
      fortuneTellingUserInfo.birth_date &&
      fortuneTellingUserInfo.birth_time
    ) {
      const response = await fetch(
        `${API_BASE_URL}/api/anything-request/getConversationIdAndHistory?fortune_telling_uid=${fortune_telling_uid}&stream=true&date=${moment().format(
          "YYYY-MM-DD"
        )}&birth_date=${fortuneTellingUserInfo.birth_date}&username=${
          fortuneTellingUserInfo.username
        }&gender=${fortuneTellingUserInfo.gender}&birth_time=${
          fortuneTellingUserInfo.birth_time
        }`,
        {
          headers: {
            Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined,
          },
        }
      );
      const data = await response.json();
      setConversationId(data.conversation_id);
      setConversationHistory(data.conversation_history);
      setChatInputDisabled(false);
    }
  },

  // 发送提示消息
  sendPrompt: async () => {
    const {
      prompt,
      conversationId,
      setPrompt,
      addToCurrentChatList,
      setNewAIResponseIsStreaming,
      setNewAIResponse,
      setChatInputDisabled
    } = get();

    if (prompt.length === 0) return;

    addToCurrentChatList({ role: "user", content: prompt });
    
    const response = await fetch(
      `${API_BASE_URL}/api/anything-request/getAnswerFromLLM`,
      {
        method: "POST",
        body: JSON.stringify({
          conversationId: conversationId,
          prompt: prompt,
        }),
        headers: {
          Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined,
        },
      }
    );
    setPrompt("");

    setNewAIResponseIsStreaming(true);
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let accumulatedText = "";
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        setNewAIResponse(accumulatedText);
        setChatInputDisabled(false);
        setNewAIResponseIsStreaming(false);
        break;
      }
      const text = decoder.decode(value);
      buffer += text;
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          try {
            if (line === "data: [DONE]") {
              setNewAIResponse(accumulatedText);
              addToCurrentChatList({ role: "assistant", content: accumulatedText });
              setChatInputDisabled(false);
              setNewAIResponseIsStreaming(false);
              break;
            }
            const jsonData = JSON.parse(line.slice(6));
            if (jsonData.content) {
              accumulatedText += jsonData.content;
              setNewAIResponse(accumulatedText);
            }
          } catch (e) {
            console.log("Parsing error:", e);
            setNewAIResponseIsStreaming(false);
            continue;
          }
        }
      }
    }
  },

  // 开始占卜请求
  requestFortuneTellingInfo: async (fortune_telling_uid) => {
    const {
      fortuneTellingUserInfo,
      setRequestFortuneTellingInfoDone,
      setLoading,
      setError,
      setStreamingText,
      setIsStreaming,
      setNewAIResponseIsStreaming,
      setFortuneData,
      setDesktopDecoration,
      setTips
    } = get();

    setRequestFortuneTellingInfoDone(false);
    console.log("开始占卜");
    
    try {
      setLoading(true);
      setError(null);
      setStreamingText("");
      setIsStreaming(true);
      
      const response = await fetch(
        `${API_BASE_URL}/api/anything-request?fortune_telling_uid=${fortune_telling_uid}&date=${moment().format(
          "YYYY-MM-DD"
        )}`,
        {
          headers: {
            Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined,
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setNewAIResponseIsStreaming(true);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = "";
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          setIsStreaming(false);
          setLoading(false);
          setNewAIResponseIsStreaming(false);
          const decorationSrc = extractDesktopDecoration(accumulatedText);
          if (decorationSrc) {
            setDesktopDecoration(decorationSrc);
          }
          break;
        }

        const text = decoder.decode(value);
        buffer += text;
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              if (line === "data: [DONE]") {
                setFortuneData({ textResponse: accumulatedText });
                const decorationSrc = extractDesktopDecoration(accumulatedText);
                if (decorationSrc) {
                  setDesktopDecoration(decorationSrc);
                }
                const extractedTips = extractFortuneTips(accumulatedText);
                if (extractedTips.length > 0) {
                  setTips(extractedTips);
                }
                setRequestFortuneTellingInfoDone(true);
                break;
              }
              const jsonData = JSON.parse(line.slice(6));
              if (jsonData.content) {
                accumulatedText += jsonData.content;
                setStreamingText(accumulatedText);
              }
            } catch (e) {
              console.log("Parsing error:", e);
              continue;
            }
          }
        }
      }
    } catch (err) {
      setError("Failed to fetch data");
      console.error("Streaming error:", err);
      setIsStreaming(false);
      setLoading(false);
    }
  },

  // 更新用户信息
  updateUserInfo: async (formData, fortuneTellingUserInfo) => {
    try {
      if (!fortuneTellingUserInfo || !fortuneTellingUserInfo.documentId) {
        throw new Error("无效的用户信息");
      }
      
      const submitData = {
        ...formData,
        birth_time: formatBirthTime(formData.birth_time),
      };
      
      // 处理空字段
      if (submitData.height === "") delete submitData.height;
      if (submitData.weight === "") delete submitData.weight;
      if (submitData.profession === "") delete submitData.profession;
      if (submitData.constitution_type === "") delete submitData.constitution_type;
      if (submitData.sleep_quality === "") delete submitData.sleep_quality;
      if (submitData.exercise_frequency === "") delete submitData.exercise_frequency;
      if (submitData.health_info === "") delete submitData.health_info;
      
      // 处理数组字段
      if (submitData.common_symptoms.length === 0) delete submitData.common_symptoms;
      if (submitData.dietary_preferences.length === 0) delete submitData.dietary_preferences;
      if (submitData.body_discomfort.length === 0) delete submitData.body_discomfort;
      if (submitData.fortune_sections && submitData.fortune_sections.length === 0) delete submitData.fortune_sections;
      
      await axios.put(
        `${API_BASE_URL}/api/fortune-telling-users/${fortuneTellingUserInfo.documentId}`,
        {
          data: submitData,
        },
        {
          headers: {
            Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined,
          },
        }
      );
      
      return { success: true };
    } catch (error) {
      return { success: false, error: "保存失败，请重试。" };
    }
  },

  // 获取枚举映射
  fetchEnumMappings: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/fortune-telling-users/enum-mappings`);
      return response.data.data;
    } catch (error) {
      console.error('获取枚举映射失败:', error);
      return {};
    }
  },

  // 获取栏目配置
  fetchFortuneSections: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/fortune-telling-users/fortune-sections`);
      return response.data.data;
    } catch (error) {
      console.error('获取栏目配置失败:', error);
      return [];
    }
  },

  // 初始化性别表情
  initializeGenderEmoji: () => {
    const { fortuneTellingUserInfo, setGenderEmoji } = get();
    if (fortuneTellingUserInfo && fortuneTellingUserInfo.gender) {
      setGenderEmoji(getGenderEmoji(fortuneTellingUserInfo.gender));
    }
  },

  // 检查和更新显示输入框状态
  updateShowInputStatus: () => {
    const { shouldHideInput, setShowInput } = get();
    setShowInput(!shouldHideInput());
  },

  // 重置所有状态
  reset: () => set({
    fortuneTellingUserInfo: {},
    loading: false,
    error: null,
    isStreaming: false,
    getFortuneTellingUserInfoLoading: false,
    getFortuneTellingUserInfoError: null,
    fortuneData: null,
    streamingText: "",
    allowRunFortuneTellingRequest: false,
    requestFortuneTellingInfoDone: false,
    isEditing: false,
    spiritualPractice: false,
    showInput: true,
    historyOpen: false,
    hadUpdateUserInfoNeedRequestFortuneTellingInfo: false,
    conversationId: "",
    conversationHistory: [],
    currentChatList: [],
    prompt: "",
    newAIResponse: "",
    newAIResponseIsStreaming: false,
    chatInputDisabled: false,
    desktopDecoration: "",
    tips: [],
    currentTip: "",
    animationKey: 0,
    genderEmoji: "",
    fortuneSections: [],
    selectedSections: [],
  }),
}));

export default useFortuneTellingStore; 
import { useRef, useState } from 'react';
import { Box, InputBase, IconButton, Paper } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

/**
 * ChatInput 聊天输入框组件
 * @param {string} value - 输入框的值
 * @param {function} onChange - 输入变化时的回调
 * @param {function} onSend - 发送消息的回调
 * @param {boolean} disabled - 是否禁用输入框
 */
export default function ChatInput({ value, onChange, onSend, disabled, setChatInputDisabled }) {
  const inputRef = useRef();
  const [showFAQ, setShowFAQ] = useState(false);
  const [inputError, setInputError] = useState('');
  const commonQuestions = [
    '玄乎儿大师，我最近会遇到什么好运？',
    '玄乎儿大师，有什么需要注意的事情吗？',
    '玄乎儿大师，我的事业/学业怎么样？',
    '玄乎儿大师，我今日塔罗运势如何？',
    '玄乎儿大师，我今日星座运势如何？',
    '玄乎儿大师，今天适合听什么歌'
  ];
  const MAX_LENGTH = 50;

  // 统一的发送处理函数
  const handleSend = () => {
    if (value.trim() && !disabled) {
      onSend();
      setChatInputDisabled(true);
    }
  };

  // 处理回车发送
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // 处理常见问题点击
  const handleQuestionClick = (question) => {
    if (onChange) {
      onChange({ target: { value: question } });
    }
    setShowFAQ(false);
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  // 处理输入变化，限制最大长度
  const handleInputChange = (e) => {
    let val = e.target.value;
    if (val.length > MAX_LENGTH) {
      val = val.slice(0, MAX_LENGTH);
      setInputError(`最多只能输入${MAX_LENGTH}个字符`);
      // 触发onChange，确保外部value也被截断
      if (onChange) onChange({ target: { value: val } });
    } else {
      setInputError('');
      if (onChange) onChange(e);
    }
  };

  return (
    <Box
      sx={{
        position: 'fixed',
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 2000,
        display: 'flex',
        justifyContent: 'center',
        pb: { xs: 1, md: 3 },
        background: 'transparent',
        pointerEvents: disabled ? 'none' : 'auto',
      }}
    >
      <Box sx={{ position: 'relative', width: { xs: '98vw', sm: 500 }, maxWidth: '98vw' }}>
        {/* 常见问题浮窗 */}
        {showFAQ && (
          <Paper
            elevation={4}
            sx={{
              position: 'absolute',
              left: 0,
              right: 0,
              bottom: '100%',
              mb: 1,
              zIndex: 2100,
              p: 1,
              display: 'flex',
              flexWrap: 'wrap',
              gap: 1,
              background: '#fff',
            }}
          >
            {commonQuestions.map((q, idx) => (
              <Box
                key={idx}
                onClick={() => handleQuestionClick(q)}
                sx={{
                  px: 1.5,
                  py: 0.5,
                  borderRadius: 2,
                  background: '#f5f5f5',
                  cursor: 'pointer',
                  fontSize: 15,
                  color: '#333',
                  '&:hover': { background: '#e0e0e0' },
                }}
              >
                {q}
              </Box>
            ))}
          </Paper>
        )}
        <Paper
          elevation={6}
          sx={{
            display: 'flex',
            alignItems: 'center',
            width: '100%',
            borderRadius: 4,
            px: 2,
            py: 1,
            background: '#fff',
            flexDirection: 'column', // 使提示信息显示在输入框下方
          }}
        >
          <Box sx={{ width: '100%', display: 'flex', alignItems: 'center' }}>
            <InputBase
              inputRef={inputRef}
              value={value}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="我是玄乎儿，为你照亮前路"
              multiline
              maxRows={4}
              disabled={disabled}
              onFocus={() => setShowFAQ(true)}
              onBlur={() => setTimeout(() => setShowFAQ(false), 150)}
              sx={{
                flex: 1,
                fontSize: 18,
                px: 1,
                color: '#222',
                background: 'transparent',
              }}
            />
            <IconButton
              color="primary"
              onClick={handleSend}
              disabled={disabled || !value.trim()}
              sx={{ ml: 1 }}
            >
              <SendIcon />
            </IconButton>
          </Box>
          {inputError && (
            <Box sx={{ color: 'red', fontSize: 14, mt: 0.5, width: '100%', textAlign: 'left' }}>{inputError}</Box>
          )}
        </Paper>
      </Box>
    </Box>
  );
} 
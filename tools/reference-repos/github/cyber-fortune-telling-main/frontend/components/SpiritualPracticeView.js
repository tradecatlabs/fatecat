import { useState, useEffect } from "react";
import { Box, IconButton, Typography, Paper, List, ListItem, ListItemText } from "@mui/material";
import { motion } from "framer-motion";
import goFullScreen from "@/tools/getFullScreen";
import exitFullScreen from "@/tools/exitFullScreen";
import FullscreenIcon from "@mui/icons-material/Fullscreen";
import FullscreenExitIcon from "@mui/icons-material/FullscreenExit";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";
import useFortuneTellingStore from "@/stores/fortuneTellingStore";
import moment from "moment";
// DualTime 组件
function DualTimeComponent({ desktopDecoration, tips, currentTip, animationKey }) {
  const [currentTime, setCurrentTime] = useState(new Date());
  
  // 屏幕方向状态管理
  const [isLandscape, setIsLandscape] = useState(() => {
    if (typeof window !== 'undefined') {
      return window.innerWidth > window.innerHeight;
    }
    return false;
  });
  
  // 番茄钟状态管理
  const [pomodoroTime, setPomodoroTime] = useState(25 * 60); // 25分钟（秒）
  const [breakTime, setBreakTime] = useState(5 * 60); // 5分钟（秒）
  const [currentSession, setCurrentSession] = useState(25 * 60); // 初始为25分钟
  const [isRunning, setIsRunning] = useState(false);
  const [isBreak, setIsBreak] = useState(false);
  
  // 今日完成周期管理
  const [todayCycles, setTodayCycles] = useState(() => {
    if (typeof window !== 'undefined') {
      const today = new Date().toLocaleDateString('zh-CN');
      const savedData = localStorage.getItem('pomodoroTodayCycles');
      
      if (savedData) {
        try {
          const data = JSON.parse(savedData);
          // 如果是今天的数据，则返回保存的周期数
          if (data.date === today) {
            return data.cycles;
          }
        } catch (e) {
          console.error('读取番茄钟数据失败:', e);
        }
      }
      
      // 如果没有数据或不是今天的数据，则返回0
      return 0;
    }
    return 0;
  });

  // 保存今日周期到localStorage
  const saveTodayCycles = (cycles) => {
    if (typeof window !== 'undefined') {
      const today = new Date().toLocaleDateString('zh-CN');
      const data = {
        date: today,
        cycles: cycles,
        lastUpdated: new Date().toISOString()
      };
      localStorage.setItem('pomodoroTodayCycles', JSON.stringify(data));
    }
  };

  // 检查并更新今日周期（处理跨日期情况）
  const checkAndUpdateTodayCycles = () => {
    if (typeof window !== 'undefined') {
      const today = new Date().toLocaleDateString('zh-CN');
      const savedData = localStorage.getItem('pomodoroTodayCycles');
      
      if (savedData) {
        try {
          const data = JSON.parse(savedData);
          // 如果保存的不是今天的数据，重置为0
          if (data.date !== today) {
            setTodayCycles(0);
            saveTodayCycles(0);
          }
        } catch (e) {
          console.error('检查番茄钟数据失败:', e);
          setTodayCycles(0);
          saveTodayCycles(0);
        }
      }
    }
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      // 每分钟检查一次日期变化
      checkAndUpdateTodayCycles();
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // 监听屏幕方向变化
  useEffect(() => {
    const handleOrientationChange = () => {
      // 延迟一点检查，确保屏幕尺寸已更新
      setTimeout(() => {
        setIsLandscape(window.innerWidth > window.innerHeight);
      }, 100);
    };

    const handleResize = () => {
      setIsLandscape(window.innerWidth > window.innerHeight);
    };

    if (typeof window !== 'undefined') {
      // 监听屏幕方向变化事件
      window.addEventListener('orientationchange', handleOrientationChange);
      // 监听窗口大小变化事件
      window.addEventListener('resize', handleResize);
      
      return () => {
        window.removeEventListener('orientationchange', handleOrientationChange);
        window.removeEventListener('resize', handleResize);
      };
    }
  }, []);

  // 番茄钟定时器
  useEffect(() => {
    let interval = null;
    if (isRunning && currentSession > 0) {
      interval = setInterval(() => {
        setCurrentSession(currentSession => currentSession - 1);
      }, 1000);
    } else if (currentSession === 0) {
      // 时间到了，切换状态
      if (isBreak) {
        // 休息结束，开始新的工作周期
        setCurrentSession(pomodoroTime);
        setIsBreak(false);
        // 休息结束后增加今日完成周期
        const newCycles = todayCycles + 1;
        setTodayCycles(newCycles);
        saveTodayCycles(newCycles);
      } else {
        // 工作结束，开始休息
        setCurrentSession(breakTime);
        setIsBreak(true);
      }
      setIsRunning(false);
    }
    return () => clearInterval(interval);
  }, [isRunning, currentSession, pomodoroTime, breakTime, isBreak, todayCycles]);

  const formatTime = (date) => {
    return date.toLocaleTimeString('zh-CN', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const formatDate = (date) => {
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'long'
    });
  };

  const formatPomodoroTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };



  const getProgress = () => {
    const totalTime = isBreak ? breakTime : pomodoroTime;
    return ((totalTime - currentSession) / totalTime) * 100;
  };

  // 获取扇形角度（基于30分钟制表盘）
  const getSectorAngle = () => {
    const remainingSeconds = currentSession;
    // 将剩余秒数转换为分钟
    const remainingMinutes = remainingSeconds / 60;
    // 30分钟制表盘，每分钟12度 (360° ÷ 30分钟 = 12度/分钟)
    const angle = remainingMinutes * 12;
    return angle;
  };



  return (
    <Box
      sx={{
        display: 'flex',
        width: '100%',
        height: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        gap: isLandscape ? 6 : 2, // 横屏时增大间距
        padding: isLandscape ? 3 : 1, // 横屏时增大内边距
        flexDirection: isLandscape ? 'row' : 'column', // 横屏时水平布局，竖屏时垂直布局
        transform: isLandscape ? 'scale(1.2)' : 'scale(1)', // 横屏时放大整体尺寸
        transformOrigin: 'center',
        transition: 'all 0.3s ease-in-out', // 平滑过渡效果
        '@media (max-width: 600px)': {
          gap: isLandscape ? 4 : 0,
          padding: isLandscape ? 2 : 0.1,
        },
      }}
    >
      {/* 左侧计时器 */}
      <Box
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: isLandscape ? { xs: 1, sm: 2, md: 3 } : { xs: 0.2, sm: 1, md: 2 }, // 横屏时增大内边距
          maxWidth: isLandscape ? { xs: '500px', sm: '600px', md: '700px' } : { xs: 'calc(100% - 16px)', sm: '380px', md: '400px' }, // 横屏时增大最大宽度
          minHeight: isLandscape ? { xs: '200px', sm: '250px', md: '300px' } : { xs: '120px', sm: '150px', md: '170px' }, // 横屏时增大最小高度
          width: isLandscape ? 'auto' : { xs: 'calc(100% - 16px)', md: 'auto' }, // 横屏时自适应宽度
          margin: isLandscape ? '0 16px' : { xs: '16px 8px 4px 8px', md: '0 16px 0 16px' }, // 横屏时调整边距
        }}
      >
        <Typography
          variant="h2"
          sx={{
            color: '#FFD700',
            fontWeight: 'bold',
            textShadow: '0 0 20px rgba(255, 215, 0, 0.8)',
            marginBottom: isLandscape ? { xs: 2, sm: 2.5, md: 3 } : { xs: 1, sm: 1.5, md: 2 }, // 横屏时增大下边距
            fontFamily: 'monospace',
            fontSize: isLandscape ? { xs: '3rem', sm: '4rem', md: '5rem' } : { xs: '2rem', sm: '2.5rem', md: '3rem' }, // 横屏时增大字体
          }}
        >
          {formatTime(currentTime)}
        </Typography>
        <Typography
          variant="h6"
          sx={{
            color: '#FFD700',
            textAlign: 'center',
            opacity: 0.9,
            fontSize: isLandscape ? { xs: '1.2rem', sm: '1.5rem', md: '1.8rem' } : { xs: '0.9rem', sm: '1rem', md: '1.25rem' }, // 横屏时增大字体
            marginBottom: isLandscape ? { xs: 1, sm: 1.5, md: 2 } : { xs: 0.5, sm: 1, md: 1.5 }, // 横屏时增大下边距
          }}
        >
          {formatDate(currentTime)}
        </Typography>
        
        {/* 显示修行提示 */}
        {tips.length > 0 && (
          <motion.div
            key={animationKey}
            style={{
              marginTop: window.innerWidth <= 600 ? '6px' : '8px', // 进一步减少修行提示上边距
              maxWidth: '100%',
              padding: window.innerWidth <= 600 ? '5px' : '10px', // 减少内边距
              backgroundColor: 'rgba(255, 215, 0, 0.1)',
              borderRadius: '8px',
              border: '1px solid #FFD700',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
            }}
            initial={{ opacity: 0, y: -10 }}
            animate={{
              opacity: [0, 1, 1, 0],
              y: [-10, 0, 0, -10],
              transition: {
                duration: 10,
                repeat: 0,
                ease: 'easeInOut',
                times: [0, 0.1, 0.9, 1],
              },
            }}
          >
            <Typography
              variant="body1"
              sx={{
                color: '#FFD700',
                textAlign: 'center',
                fontWeight: 'bold',
                textShadow: '0 0 10px rgba(255, 215, 0, 0.3)',
                fontSize: { xs: '0.85rem', sm: '1rem' }, // 移动端稍小字体
              }}
            >
              {currentTip}
            </Typography>
          </motion.div>
        )}
      </Box>

      {/* 右侧番茄钟 */}
      <Box
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          maxWidth: isLandscape ? { xs: '500px', sm: '600px', md: '700px' } : { xs: 'calc(100% - 16px)', sm: '380px', md: '400px' }, // 横屏时增大最大宽度
          position: 'relative',
          width: isLandscape ? 'auto' : { xs: 'calc(100% - 16px)', md: 'auto' }, // 横屏时自适应宽度
          margin: isLandscape ? '0 16px' : { xs: '-60px 8px 32px 8px', md: '-40px 16px 0 16px' }, // 横屏时调整边距
        }}
      >
        {/* 番茄钟主体 */}
        <Box
          component={motion.div}
          sx={{
            position: 'relative',
            width: isLandscape ? 'min(85%, 400px)' : 'min(85%, 300px)', // 横屏时增大表盘尺寸
            height: isLandscape ? 'min(85%, 400px)' : 'min(85%, 300px)', // 横屏时增大表盘尺寸
            aspectRatio: '1/1',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            filter: 'drop-shadow(0 0 20px rgba(255, 215, 0, 0.5))',
            '@media (max-width: 600px)': {
              width: isLandscape ? 'min(85%, 350px)' : 'min(85%, 280px)', // 横屏时移动端也增大表盘
              height: isLandscape ? 'min(85%, 350px)' : 'min(85%, 280px)',
            },
          }}
          animate={{
            scale: [1, 1.01, 1],
            filter: [
              'drop-shadow(0 0 20px rgba(255, 215, 0, 0.5))',
              'drop-shadow(0 0 30px rgba(255, 215, 0, 0.8))',
              'drop-shadow(0 0 20px rgba(255, 215, 0, 0.5))',
            ],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: 'easeInOut',
            times: [0, 0.5, 1],
          }}
        >
          {/* 背景圆 */}
          <Box
            sx={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              borderRadius: '50%',
              background: 'radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%)',
              border: '3px solid rgba(255, 215, 0, 0.6)',
              boxShadow: '0 0 20px rgba(255, 215, 0, 0.3), inset 0 0 20px rgba(255, 215, 0, 0.1)',
              overflow: 'hidden',
            }}
          >
            {/* 桌面装饰背景图 */}
            {desktopDecoration && (
              <Box
                component="img"
                src={desktopDecoration}
                alt="修行圣物"
                sx={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  width: '70%',
                  height: '70%',
                  objectFit: 'contain',
                  opacity: 0.9, // 进一步提高透明度让图片更清晰
                  filter: 'brightness(1.2) contrast(1.2) saturate(1.2)', // 进一步增强对比度和饱和度
                  zIndex: 1,
                }}
              />
            )}
            
            {/* 轻微遮罩层 */}
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                background: 'radial-gradient(circle, rgba(0, 0, 0, 0.05) 0%, rgba(0, 0, 0, 0.2) 100%)',
                zIndex: 2,
              }}
            />
          </Box>
          
          {/* 倒计时扇形 - 祖母绿内环 */}
          <Box
            sx={{
              position: 'absolute',
              width: '85%',
              height: '85%',
              borderRadius: '50%',
              background: `conic-gradient(
                from 0deg,
                rgba(0, 200, 81, 0.4) 0deg,
                rgba(0, 200, 81, 0.4) ${getSectorAngle()}deg,
                transparent ${getSectorAngle()}deg,
                transparent 360deg
              )`,
              maskImage: 'radial-gradient(circle, transparent 60%, black 65%, black 100%)',
              WebkitMaskImage: 'radial-gradient(circle, transparent 60%, black 65%, black 100%)',
              top: '7.5%',
              left: '7.5%',
              zIndex: 15,
              transition: 'background 0.5s ease-in-out',
              opacity: 1,
              boxShadow: '0 0 15px rgba(0, 200, 81, 0.5)',
            }}
          />
          

          

          

          
          {/* 刻度 */}
          {[...Array(12)].map((_, i) => (
            <Box
              key={i}
              sx={{
                position: 'absolute',
                width: '2px',
                height: '8%',
                backgroundColor: '#FFD700',
                borderRadius: '2px',
                transformOrigin: 'bottom center',
                transform: `rotate(${i * 30}deg)`,
                top: '5%',
                opacity: 0.6,
                boxShadow: '0 0 3px rgba(255, 215, 0, 0.5)',
                zIndex: 3, // 降低刻度线层级，让扇形在上方
              }}
            />
          ))}
          
          {/* 数字刻度 - 30分钟制表盘（顺时针显示） */}
          {[
            { num: 0, angle: 0 },     // 12点位置
            { num: 5, angle: 60 },    // 2点位置
            { num: 10, angle: 120 },  // 4点位置
            { num: 15, angle: 180 },  // 6点位置
            { num: 20, angle: 240 },  // 8点位置
            { num: 25, angle: 300 }   // 10点位置
          ].map(({ num, angle }) => (
            <Typography
              key={num}
              sx={{
                position: 'absolute',
                color: '#FFD700',
                fontSize: { xs: '12px', sm: '14px' },
                fontWeight: 'bold',
                textShadow: '0 0 8px rgba(255, 215, 0, 0.9), 0 0 15px rgba(0, 0, 0, 0.9)',
                transform: `rotate(${angle}deg) translate(0, -130px) rotate(${-angle}deg)`,
                transformOrigin: 'center',
                zIndex: 10,
                backgroundColor: 'rgba(0, 0, 0, 0.6)',
                padding: '2px 6px',
                borderRadius: '4px',
                border: '1px solid rgba(255, 215, 0, 0.5)',
                minWidth: '16px',
                textAlign: 'center',
              }}
            >
              {num}
            </Typography>
          ))}
          
          {/* 中心时间显示 */}
          <Typography
            sx={{
              color: '#FFD700',
              fontWeight: 'bold',
              fontFamily: 'monospace',
              textShadow: '0 0 20px rgba(255, 215, 0, 0.8), 0 0 5px rgba(0, 0, 0, 0.9)',
              zIndex: 20, // 提高时间显示层级，确保在所有元素上方
              userSelect: 'none',
              backgroundColor: 'rgba(0, 0, 0, 0.6)', // 增加背景透明度提高可读性
              padding: isLandscape ? { xs: '8px 16px', sm: '12px 20px' } : { xs: '6px 12px', sm: '8px 16px' }, // 横屏时增大内边距
              borderRadius: '12px',
              fontSize: isLandscape ? { xs: '3rem', sm: '4rem', md: '5rem' } : { xs: '2.2rem', sm: '2.8rem', md: '3.5rem' }, // 横屏时增大字体
            }}
          >
            {formatPomodoroTime(currentSession)}
          </Typography>
        </Box>
        
        {/* 周期计数和控制按钮组合 */}
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: { xs: 2, sm: 3 }, // 周期计数和按钮之间的间距
            marginTop: { xs: 0.5, sm: 1.5 },
            marginBottom: { xs: 4, sm: 2 },
          }}
        >
          {/* 周期计数 */}
          <Typography
            variant="body1"
            sx={{
              color: '#FFD700',
              textAlign: 'center',
              fontSize: { xs: '12px', sm: '14px' },
              fontWeight: 'bold',
              textShadow: '0 0 5px rgba(255, 215, 0, 0.5)',
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              padding: { xs: '4px 8px', sm: '8px 16px' },
              borderRadius: '16px',
              border: '1px solid #FFD700',
              maxWidth: { xs: '200px', sm: '250px' },
            }}
          >
            今日完成 {todayCycles} 个周期
          </Typography>
          
          {/* 控制按钮 */}
          <Box
            onClick={toggleTimer}
            sx={{
              backgroundColor: 'rgba(255, 215, 0, 0.15)',
              color: '#FFD700',
              border: '3px solid #FFD700',
              borderRadius: '50px', // 圆角长条形
              width: isLandscape ? { xs: 240, sm: 280 } : { xs: 180, sm: 220 }, // 横屏时增大宽度
              height: isLandscape ? { xs: 80, sm: 90 } : { xs: 60, sm: 70 }, // 横屏时增大高度
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: isLandscape ? { xs: 2, sm: 2.5 } : { xs: 1.5, sm: 2 }, // 横屏时增大间距
              fontSize: isLandscape ? { xs: '2.2rem', sm: '2.8rem' } : { xs: '1.8rem', sm: '2.2rem' }, // 横屏时增大图标尺寸
              boxShadow: '0 0 15px rgba(255, 215, 0, 0.4), 0 0 30px rgba(255, 215, 0, 0.2)',
              transition: 'all 0.3s ease',
              cursor: 'pointer',
              userSelect: 'none',
              '&:hover': {
                backgroundColor: 'rgba(255, 215, 0, 0.25)',
                boxShadow: '0 0 20px rgba(255, 215, 0, 0.6), 0 0 40px rgba(255, 215, 0, 0.3)',
                transform: 'scale(1.05)',
              },
              '&:active': {
                transform: 'scale(0.95)',
              },
            }}
          >
            {isRunning ? <PauseIcon /> : <PlayArrowIcon />}
            <Typography
              sx={{
                fontSize: isLandscape ? { xs: '20px', sm: '24px' } : { xs: '16px', sm: '18px' }, // 横屏时增大文字尺寸
                fontWeight: 'bold',
                color: '#FFD700',
                textShadow: '0 0 5px rgba(255, 215, 0, 0.5)',
              }}
            >
              {isRunning ? '暂停' : '开始'}
            </Typography>
          </Box>
        </Box>

      </Box>
    </Box>
  );
}

// 创建玄修视图组件
function SpiritualPracticeView({
  tips,
  currentTip,
  animationKey,
  desktopDecoration,
  setSpiritualPractice,
}) {

   const {
    fortuneTellingUserInfo,
  } = useFortuneTellingStore();
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [viewMode, setViewMode] = useState(() => {
    // 从 localStorage 读取保存的模式，如果没有则使用 'dualtime' 作为默认值
    // 支持的模式: 'easy' | 'dualtime'
    if (typeof window !== 'undefined') {
      const savedMode = localStorage.getItem('spiritualPracticeViewMode');
      return savedMode || 'dualtime';
    }
    return 'dualtime';
  });
  const [showMenu, setShowMenu] = useState(false);

  const allWeeks = 90 * 52; // 假设活到90岁，每年52周
  const [weeksLeft, setWeeksLeft] = useState(null);
  const [weeksLived, setWeeksLived] = useState(null);
  
  useEffect(() => {

    console.log('fortuneTellingUserInfo changed:', fortuneTellingUserInfo);
    // get birthday by fortuneTellingUserInfo , and calculate if a people live to 90 years, how many weeks left
    if (fortuneTellingUserInfo && fortuneTellingUserInfo.birth_date) {
      const birthday = moment(fortuneTellingUserInfo.birth_date, 'YYYY-MM-DD');
      const now = moment();
      const age = now.year() - birthday.year();
      const weeksLived = age * 52 + Math.floor(now.diff(birthday.clone().year(now.year()), 'weeks', true));
      const weeksLeft = allWeeks - weeksLived;
      setWeeksLeft(weeksLeft > 0 ? weeksLeft : 0);
      setWeeksLived(weeksLived > 0 ? weeksLived : 0);
    } else {
      setWeeksLeft(null);
      setWeeksLived(null);
    }



  }, [fortuneTellingUserInfo]);


  // 切换模式并保存到 localStorage
  const handleViewModeChange = (newMode) => {
    setViewMode(newMode);
    if (typeof window !== 'undefined') {
      localStorage.setItem('spiritualPracticeViewMode', newMode);
    }
  };

  return (
    <Box
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1,
        backgroundImage:
          "linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.6)), url('/api/random-desk-decor-bg')",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
      }}
    >
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 0, // 确保遮罩在内容后面,
      }}>
        <div>
          {/* Canvas-based life weeks grid - much more performant */}
          <div style={{
            position: 'absolute',
            left : 0,
            right: 0,
            top: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.01)',
            zIndex: 0,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '10px',
            overflow: 'auto',
            opacity: 0.4
          }}>
            {weeksLived !== null && weeksLeft !== null && (
              <canvas
                ref={(canvas) => {
                  if (canvas) {
                    const ctx = canvas.getContext('2d');
                    const width = canvas.width;
                    const height = canvas.height;

                    // Clear canvas
                    ctx.clearRect(0, 0, width, height);

                    // Calculate grid dimensions
                    const cols = 52;
                    const rows = 90;
                    const cellWidth = width / cols;
                    const cellHeight = height / rows;

                    // Draw grid cells
                    for (let row = 0; row < rows; row++) {
                      for (let col = 0; col < cols; col++) {
                        const index = row * cols + col;
                        const isLived = index < weeksLived;
                        const isLeft = index >= weeksLived && index < weeksLived + weeksLeft;

                        if (isLived || isLeft) {
                          ctx.fillStyle = isLived ? '#CCCCCC' : '#FFD700';
                          ctx.globalAlpha = 0.5;
                          ctx.fillRect(
                            col * cellWidth + 0.5,
                            row * cellHeight + 0.5,
                            cellWidth - 1,
                            cellHeight - 1
                          );
                          ctx.globalAlpha = 1;
                        } else {
                          // Draw border for future weeks
                          ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
                          ctx.lineWidth = 1;
                          ctx.strokeRect(
                            col * cellWidth + 0.5,
                            row * cellHeight + 0.5,
                            cellWidth - 1,
                            cellHeight - 1
                          );
                        }
                      }
                    }
                  }
                }}
                style={{
                  width: '100%',
                  height: '100%',
                  maxWidth: '100%',
                  maxHeight: '100%',
                  aspectRatio: '52 / 90'
                }}
                width={520}
                height={900}
                title={`Life Grid: ${weeksLived} weeks lived, ${weeksLeft} weeks left`}
              />
            )}
          </div>
        </div>
        <div style={{
          height: '40px',
          position: 'absolute',
          bottom: '10px',
          left: 0,
          right: 0,
          textAlign: 'center',
          color: '#FFD700',
          fontSize: '14px',
          fontWeight: 'bold',
          textShadow: '0 0 5px rgba(255, 215, 0, 0.5)',
          zIndex: 1, // 确保文字在遮罩前面
        }}>     
          如果我能活到90岁; 一共能活 {allWeeks} 周，剩余 {weeksLeft} 周，已度过 {weeksLived} 周
        </div>

        
      </div>
      {/* 左侧菜单 */}
      {!isFullScreen && (
        <>
          {/* 菜单按钮 */}
          <IconButton
            onClick={() => setShowMenu(!showMenu)}
            sx={{
              position: "fixed",
              top: { xs: 60, sm: 80 }, // 移动端位置稍高
              left: { xs: 10, sm: 20 }, // 移动端稍微靠左
              zIndex: 2001,
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              color: '#FFD700',
              border: '2px solid #FFD700',
              width: { xs: 40, sm: 48 }, // 响应式大小
              height: { xs: 40, sm: 48 },
              '&:hover': {
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
              },
            }}
          >
            {showMenu ? <CloseIcon /> : <MenuIcon />}
          </IconButton>

          {/* 菜单面板 */}
          {showMenu && (
            <motion.div
              initial={{ x: -300, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -300, opacity: 0 }}
              transition={{ duration: 0.3 }}
              style={{
                position: "fixed",
                top: window.innerWidth <= 600 ? 110 : 130, // 移动端位置调整
                left: window.innerWidth <= 600 ? 10 : 20, // 移动端稍微靠左
                zIndex: 2000,
                width: window.innerWidth <= 600 ? 160 : 200, // 移动端宽度稍小
              }}
            >
              <Paper
                sx={{
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  border: '2px solid #FFD700',
                  borderRadius: 2,
                }}
              >
                <List>
                  <ListItem
                    button
                    onClick={() => {
                      handleViewModeChange('easy');
                      setShowMenu(false);
                    }}
                    sx={{
                      backgroundColor: viewMode === 'easy' ? 'rgba(255, 215, 0, 0.2)' : 'transparent',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 215, 0, 0.1)',
                      },
                    }}
                  >
                    <ListItemText
                      primary="简单模式"
                      primaryTypographyProps={{
                        color: '#FFD700',
                        fontWeight: viewMode === 'easy' ? 'bold' : 'normal',
                      }}
                    />
                  </ListItem>
                  <ListItem
                    button
                    onClick={() => {
                      handleViewModeChange('dualtime');
                      setShowMenu(false);
                    }}
                    sx={{
                      backgroundColor: viewMode === 'dualtime' ? 'rgba(255, 215, 0, 0.2)' : 'transparent',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 215, 0, 0.1)',
                      },
                    }}
                  >
                    <ListItemText
                      primary="DualTime模式"
                      primaryTypographyProps={{
                        color: '#FFD700',
                        fontWeight: viewMode === 'dualtime' ? 'bold' : 'normal',
                      }}
                    />
                  </ListItem>
                </List>
              </Paper>
            </motion.div>
          )}
        </>
      )}

      {/* 右上角全屏按钮 */}
      {isFullScreen === false && (
        <IconButton
          color="primary"
          onClick={() => {
            setIsFullScreen(true);
            goFullScreen();
          }}
          sx={{
            position: "fixed",
            top: { xs: 10, sm: 20 }, // 响应式位置
            right: { xs: 10, sm: 20 }, // 响应式位置
            zIndex: 1000,
            width: { xs: 40, sm: 48 }, // 响应式大小
            height: { xs: 40, sm: 48 },
          }}
        >
          <FullscreenIcon sx={{ 
            fontSize: { xs: 24, sm: 32 }, // 响应式图标大小
            color: "#FFD700" 
          }} />
        </IconButton>
      )}
      {isFullScreen === true && (
        <IconButton
          color="primary"
          onClick={() => {
            setIsFullScreen(false);
            exitFullScreen();
          }}
          sx={{
            position: "fixed",
            top: { xs: 10, sm: 20 }, // 响应式位置
            right: { xs: 10, sm: 20 }, // 响应式位置
            zIndex: 1000,
            width: { xs: 40, sm: 48 }, // 响应式大小
            height: { xs: 40, sm: 48 },
          }}
        >
          <FullscreenExitIcon sx={{ 
            fontSize: { xs: 24, sm: 32 }, // 响应式图标大小
            color: "#FFD700" 
          }} />
        </IconButton>
      )}

      {/* 主要内容区域 */}
      {viewMode === 'easy' ? (
        <>
          {/* 简单模式：显示提示文本 */}
          {tips.length > 0 && (
            <motion.div
              key={animationKey}
              style={{
                position: "fixed",
                bottom: "15vh",
                zIndex: 1000,
                maxWidth: "calc(100% - 40px)",
                padding: "10px",
                backgroundColor: "rgba(0, 0, 0, 0.7)",
                borderRadius: "8px",
                border: "2px solid #FFD700",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
              }}
              initial={{ opacity: 0, y: -20 }}
              animate={{
                opacity: [0, 1, 1, 0],
                y: [-20, 0, 0, -20],
                transition: {
                  duration: 10,
                  repeat: 0,
                  ease: "easeInOut",
                  times: [0, 0.1, 0.9, 1],
                },
              }}
            >
              <Typography
                variant="h6"
                component="div"
                sx={{
                  color: "#FFD700",
                  textAlign: "center",
                  fontWeight: "bold",
                  textShadow: "0 0 10px rgba(255, 215, 0, 0.5)",
                }}
              >
                {currentTip}
              </Typography>
            </motion.div>
          )}

          {/* 简单模式：显示桌面装饰 */}
          {desktopDecoration && (
            <motion.div
              style={{
                zIndex: 1, 
                filter: "drop-shadow(0 0 20px rgba(255, 215, 0, 0.5))",
              }}
              animate={{
                scale: [1, 1.02, 1],
                filter: [
                  "drop-shadow(0 0 20px rgba(255, 215, 0, 0.5))",
                  "drop-shadow(0 0 30px rgba(255, 215, 0, 0.8))",
                  "drop-shadow(0 0 20px rgba(255, 215, 0, 0.5))",
                ],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut",
                times: [0, 0.5, 1],
              }}
            >
              <Box
                component="img"
                src={desktopDecoration}
                onDoubleClick={() => {
                  setIsFullScreen(!isFullScreen);
                  if (isFullScreen) {
                    exitFullScreen();
                  } else {
                    goFullScreen();
                  }
                }}
                alt="桌面装饰"
                sx={{
                  height: "61.8vh",
                  width: "auto",
                  maxWidth: "100%",
                  objectFit: "contain",
                  display: "block",
                  "@media (maxWidth: 600px)": {
                    height: "auto",
                    maxHeight: "61.8vh",
                  },
                }}
              />
            </motion.div>
          )}
        </>
      ) : (
        /* DualTime模式：显示计时器和表盘 */
        <DualTimeComponent
          desktopDecoration={desktopDecoration}
          tips={tips}
          currentTip={currentTip}
          animationKey={animationKey}
        />
      )}

      {/* 返回按钮 */}
      {isFullScreen === false && (
        <IconButton
          color="primary"
          onClick={() => setSpiritualPractice(false)}
          sx={{
            position: "fixed",
            top: { xs: 10, sm: 20 }, // 响应式位置
            left: { xs: 10, sm: 20 }, // 响应式位置
            zIndex: 2,
            width: { xs: 40, sm: 48 }, // 响应式大小
            height: { xs: 40, sm: 48 },
            boxShadow: "0 2px 8px #FFD70044",
            "&:hover": {
              border: "2px solid #FFD700",
            },
          }}
        >
          <ArrowBackIcon sx={{ 
            fontSize: { xs: 24, sm: 32 }, // 响应式图标大小
            color: "#FFD700" 
          }} />
        </IconButton>
      )}

      
    </Box>
  );
}

export default SpiritualPracticeView; 
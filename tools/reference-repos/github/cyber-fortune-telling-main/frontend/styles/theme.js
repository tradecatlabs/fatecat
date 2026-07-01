import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#FFD700', // 金色作为主色调
      dark: '#F4C430',
      contrastText: '#2C1B47',
    },
    secondary: {
      main: '#1A237E', // 深蓝色作为次要色调
      dark: '#2A1B47',
    },
    background: {
      default: '#1A237E',
      paper: '#F5F3E8', // 卡片背景色
    },
    text: {
      primary: '#37474F',
      secondary: '#FFD700',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(255, 215, 0, 0.15)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          '&:hover': {
            backgroundColor: '#F4C430',
          },
        },
        outlined: {
          borderColor: '#FFD700',
          color: '#FFD700',
          '&:hover': {
            borderColor: '#F4C430',
            color: '#F4C430',
          },
        },
      },
    },
  },
});

export default theme; 
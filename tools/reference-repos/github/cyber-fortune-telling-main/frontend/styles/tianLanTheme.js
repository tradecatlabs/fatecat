import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#67A8D6', // 天蓝色
      dark: '#4A7BA3',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#7BB8E6', // 浅天蓝色
      dark: '#67A8D6',
    },
    background: {
      default: '#E8F2FA',
      paper: '#ffffff',
    },
    text: {
      primary: '#67A8D6',
      secondary: '#4A7BA3',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(103, 168, 214, 0.15)',
          borderRadius: 4,
          border: '2px solid #67A8D6',
          background: 'rgba(255,255,255,0.95)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          backgroundColor: '#67A8D6',
          color: '#ffffff',
          '&:hover': {
            backgroundColor: '#4A7BA3',
          },
        },
        outlined: {
          borderColor: '#67A8D6',
          color: '#67A8D6',
          '&:hover': {
            borderColor: '#4A7BA3',
            color: '#4A7BA3',
          },
        },
      },
    },
    MuiInput: {
      styleOverrides: {
        root: {
          '& input': { color: '#67A8D6' },
          '& .MuiInput-input': { color: '#67A8D6' },
          '&:before': { borderBottom: '2px solid #67A8D6' },
          '&:after': { borderBottom: '2px solid #67A8D6' },
          '& .MuiInput-underline:before': { borderBottom: '2px solid #67A8D6' },
          '& .MuiInput-underline:after': { borderBottom: '2px solid #67A8D6' },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          color: '#67A8D6',
          '& .MuiSelect-icon': { color: '#67A8D6' },
          '& .MuiSelect-select': { color: '#67A8D6' },
          '& .MuiOutlinedInput-notchedOutline': { borderColor: '#67A8D6' },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#67A8D6' },
          '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#67A8D6' },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#67A8D6',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h6: {
          color: '#67A8D6',
          fontWeight: 700,
          textAlign: 'center',
        },
      },
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

export default theme; 
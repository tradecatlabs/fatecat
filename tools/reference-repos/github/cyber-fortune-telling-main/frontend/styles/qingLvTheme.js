import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#006F31', // 中国传统色 - 青绿
      dark: '#004B21',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#2D8B57', // 稍浅的青绿色
      dark: '#006F31',
    },
    background: {
      default: '#E8F5E9',
      paper: '#ffffff',
    },
    text: {
      primary: '#006F31',
      secondary: '#2D8B57',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(0, 111, 49, 0.15)',
          borderRadius: 4,
          border: '2px solid #006F31',
          background: 'rgba(255,255,255,0.95)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          backgroundColor: '#006F31',
          color: '#ffffff',
          '&:hover': {
            backgroundColor: '#004B21',
          },
        },
        outlined: {
          borderColor: '#006F31',
          color: '#006F31',
          '&:hover': {
            borderColor: '#004B21',
            color: '#004B21',
          },
        },
      },
    },
    MuiInput: {
      styleOverrides: {
        root: {
          '& input': { color: '#006F31' },
          '& .MuiInput-input': { color: '#006F31' },
          '&:before': { borderBottom: '2px solid #006F31' },
          '&:after': { borderBottom: '2px solid #006F31' },
          '& .MuiInput-underline:before': { borderBottom: '2px solid #006F31' },
          '& .MuiInput-underline:after': { borderBottom: '2px solid #006F31' },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          color: '#006F31',
          '& .MuiSelect-icon': { color: '#006F31' },
          '& .MuiSelect-select': { color: '#006F31' },
          '& .MuiOutlinedInput-notchedOutline': { borderColor: '#006F31' },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#006F31' },
          '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#006F31' },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#006F31',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h6: {
          color: '#006F31',
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
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#F5A6C0', // 胭脂
      dark: '#D16B8A',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#FFD1DF', // 浅胭脂
      dark: '#F5A6C0',
    },
    background: {
      default: '#FFF3F7',
      paper: '#ffffff',
    },
    text: {
      primary: '#F5A6C0',
      secondary: '#D16B8A',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(245, 166, 192, 0.15)',
          borderRadius: 4,
          border: '2px solid #F5A6C0',
          background: 'rgba(255,255,255,0.95)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          backgroundColor: '#F5A6C0',
          color: '#ffffff',
          '&:hover': {
            backgroundColor: '#D16B8A',
          },
        },
        outlined: {
          borderColor: '#F5A6C0',
          color: '#F5A6C0',
          '&:hover': {
            borderColor: '#D16B8A',
            color: '#D16B8A',
          },
        },
      },
    },
    MuiInput: {
      styleOverrides: {
        root: {
          '& input': { color: '#F5A6C0' },
          '& .MuiInput-input': { color: '#F5A6C0' },
          '&:before': { borderBottom: '2px solid #F5A6C0' },
          '&:after': { borderBottom: '2px solid #F5A6C0' },
          '& .MuiInput-underline:before': { borderBottom: '2px solid #F5A6C0' },
          '& .MuiInput-underline:after': { borderBottom: '2px solid #F5A6C0' },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          color: '#F5A6C0',
          '& .MuiSelect-icon': { color: '#F5A6C0' },
          '& .MuiSelect-select': { color: '#F5A6C0' },
          '& .MuiOutlinedInput-notchedOutline': { borderColor: '#F5A6C0' },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#F5A6C0' },
          '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#F5A6C0' },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#F5A6C0',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h6: {
          color: '#F5A6C0',
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
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#F5F5F5', // 瓷白
      dark: '#CCCCCC',
      contrastText: '#2E2E2E',
    },
    secondary: {
      main: '#FFFFFF', // 更亮的瓷白
      dark: '#F5F5F5',
    },
    background: {
      default: '#FFFFFF',
      paper: '#F5F5F5',
    },
    text: {
      primary: '#2E2E2E',
      secondary: '#CCCCCC',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(245, 245, 245, 0.15)',
          borderRadius: 4,
          border: '2px solid #F5F5F5',
          background: 'rgba(255,255,255,0.98)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          backgroundColor: '#F5F5F5',
          color: '#2E2E2E',
          '&:hover': {
            backgroundColor: '#CCCCCC',
          },
        },
        outlined: {
          borderColor: '#F5F5F5',
          color: '#2E2E2E',
          '&:hover': {
            borderColor: '#CCCCCC',
            color: '#CCCCCC',
          },
        },
      },
    },
    MuiInput: {
      styleOverrides: {
        root: {
          '& input': { color: '#2E2E2E' },
          '& .MuiInput-input': { color: '#2E2E2E' },
          '&:before': { borderBottom: '2px solid #F5F5F5' },
          '&:after': { borderBottom: '2px solid #F5F5F5' },
          '& .MuiInput-underline:before': { borderBottom: '2px solid #F5F5F5' },
          '& .MuiInput-underline:after': { borderBottom: '2px solid #F5F5F5' },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          color: '#2E2E2E',
          '& .MuiSelect-icon': { color: '#2E2E2E' },
          '& .MuiSelect-select': { color: '#2E2E2E' },
          '& .MuiOutlinedInput-notchedOutline': { borderColor: '#F5F5F5' },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#F5F5F5' },
          '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#F5F5F5' },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#2E2E2E',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h6: {
          color: '#2E2E2E',
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
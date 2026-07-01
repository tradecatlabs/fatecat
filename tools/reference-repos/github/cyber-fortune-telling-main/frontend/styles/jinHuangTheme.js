import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#FFCD00', // 金黄
      dark: '#C9A100',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#FFE066', // 浅金黄
      dark: '#FFCD00',
    },
    background: {
      default: '#FFF9E3',
      paper: '#ffffff',
    },
    text: {
      primary: '#FFCD00',
      secondary: '#C9A100',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(255, 205, 0, 0.15)',
          borderRadius: 4,
          border: '2px solid #FFCD00',
          background: 'rgba(255,255,255,0.95)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          backgroundColor: '#FFCD00',
          color: '#ffffff',
          '&:hover': {
            backgroundColor: '#C9A100',
          },
        },
        outlined: {
          borderColor: '#FFCD00',
          color: '#FFCD00',
          '&:hover': {
            borderColor: '#C9A100',
            color: '#C9A100',
          },
        },
      },
    },
    MuiInput: {
      styleOverrides: {
        root: {
          '& input': { color: '#FFCD00' },
          '& .MuiInput-input': { color: '#FFCD00' },
          '&:before': { borderBottom: '2px solid #FFCD00' },
          '&:after': { borderBottom: '2px solid #FFCD00' },
          '& .MuiInput-underline:before': { borderBottom: '2px solid #FFCD00' },
          '& .MuiInput-underline:after': { borderBottom: '2px solid #FFCD00' },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          color: '#FFCD00',
          '& .MuiSelect-icon': { color: '#FFCD00' },
          '& .MuiSelect-select': { color: '#FFCD00' },
          '& .MuiOutlinedInput-notchedOutline': { borderColor: '#FFCD00' },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#FFCD00' },
          '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#FFCD00' },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#FFCD00',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h6: {
          color: '#FFCD00',
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
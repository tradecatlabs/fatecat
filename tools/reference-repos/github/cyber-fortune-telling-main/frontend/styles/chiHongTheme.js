import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#D10000', // 赤红
      dark: '#A30000',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#FF4C4C', // 浅赤红
      dark: '#D10000',
    },
    background: {
      default: '#FDECEC',
      paper: '#ffffff',
    },
    text: {
      primary: '#D10000',
      secondary: '#A30000',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(209, 0, 0, 0.15)',
          borderRadius: 4,
          border: '2px solid #D10000',
          background: 'rgba(255,255,255,0.95)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          backgroundColor: '#D10000',
          color: '#ffffff',
          '&:hover': {
            backgroundColor: '#A30000',
          },
        },
        outlined: {
          borderColor: '#D10000',
          color: '#D10000',
          '&:hover': {
            borderColor: '#A30000',
            color: '#A30000',
          },
        },
      },
    },
    MuiInput: {
      styleOverrides: {
        root: {
          '& input': { color: '#D10000' },
          '& .MuiInput-input': { color: '#D10000' },
          '&:before': { borderBottom: '2px solid #D10000' },
          '&:after': { borderBottom: '2px solid #D10000' },
          '& .MuiInput-underline:before': { borderBottom: '2px solid #D10000' },
          '& .MuiInput-underline:after': { borderBottom: '2px solid #D10000' },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          color: '#D10000',
          '& .MuiSelect-icon': { color: '#D10000' },
          '& .MuiSelect-select': { color: '#D10000' },
          '& .MuiOutlinedInput-notchedOutline': { borderColor: '#D10000' },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#D10000' },
          '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#D10000' },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#D10000',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h6: {
          color: '#D10000',
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
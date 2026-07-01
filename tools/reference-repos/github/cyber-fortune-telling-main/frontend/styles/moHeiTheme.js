import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2E2E2E', // 墨黑
      dark: '#000000',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#595959', // 浅墨黑
      dark: '#2E2E2E',
    },
    background: {
      default: '#1A1A1A',
      paper: '#232323',
    },
    text: {
      primary: '#F5F5F5',
      secondary: '#B0B0B0',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(46, 46, 46, 0.15)',
          borderRadius: 4,
          border: '2px solid #2E2E2E',
          background: 'rgba(35,35,35,0.98)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          backgroundColor: '#2E2E2E',
          color: '#ffffff',
          '&:hover': {
            backgroundColor: '#000000',
          },
        },
        outlined: {
          borderColor: '#2E2E2E',
          color: '#2E2E2E',
          '&:hover': {
            borderColor: '#000000',
            color: '#000000',
          },
        },
      },
    },
    MuiInput: {
      styleOverrides: {
        root: {
          '& input': { color: '#F5F5F5' },
          '& .MuiInput-input': { color: '#F5F5F5' },
          '&:before': { borderBottom: '2px solid #2E2E2E' },
          '&:after': { borderBottom: '2px solid #2E2E2E' },
          '& .MuiInput-underline:before': { borderBottom: '2px solid #2E2E2E' },
          '& .MuiInput-underline:after': { borderBottom: '2px solid #2E2E2E' },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          color: '#F5F5F5',
          '& .MuiSelect-icon': { color: '#F5F5F5' },
          '& .MuiSelect-select': { color: '#F5F5F5' },
          '& .MuiOutlinedInput-notchedOutline': { borderColor: '#2E2E2E' },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#2E2E2E' },
          '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#2E2E2E' },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#F5F5F5',
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        h6: {
          color: '#F5F5F5',
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
import { Box } from "@mui/material";

// Add custom loading animation component
const LoadingSpinner = () => (
  <Box
    component="img"
    src="/loading.png"
    alt="Loading..."
    sx={{
      width: 60,
      height: 60,
      animation:
        "customRotate 2s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite",
      "@keyframes customRotate": {
        "0%": {
          transform: "rotate(0deg)",
        },
        "50%": {
          transform: "rotate(180deg)",
        },
        "100%": {
          transform: "rotate(360deg)",
        },
      },
    }}
  />
);

export default LoadingSpinner; 
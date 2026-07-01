import { Box } from "@mui/material";
import { useState, useRef } from "react";

export default function FortuneMasterAvatar({ sx = {}, size = 120, ...props }) {
  const [imgSrc, setImgSrc] = useState("/api/random-fortune-master");
  const realImgUrlRef = useRef("");

  const fetchNewImage = async () => {
    let newUrl = "";
    let tryCount = 0;
    do {
      // 加时间戳防止缓存
      const res = await fetch(`/api/random-fortune-master?t=${Date.now()}`, {
        redirect: 'follow',
      });
      newUrl = res.url;
      tryCount++;
      // 最多尝试5次，防止死循环
      if (tryCount > 5) break;
    } while (newUrl === realImgUrlRef.current);
    realImgUrlRef.current = newUrl;
    setImgSrc(newUrl);
  };

  const handleRefresh = () => {
    fetchNewImage();
  };

  return (
    <Box
      component="img"
      src={imgSrc}
      alt="头像"
      sx={{
        width: size,
        height: size,
        borderRadius: "50%",
        objectFit: "cover",
        ...sx,
      }}
      onClick={handleRefresh}
      style={{ cursor: 'pointer' }}
      {...props}
    />
  );
} 
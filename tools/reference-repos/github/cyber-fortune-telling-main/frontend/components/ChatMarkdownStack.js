import { Stack, Card, CardContent } from "@mui/material";
import StyledMarkdown from "./StyledMarkdown";

function ChatMarkdownStack({ item, username, genderEmoji }) {
  return (
    <Stack spacing={3} alignItems="center">
      {item.role === "user" && (
        <>
          <div style={{ height: "30px" }}></div>
          <Card
            sx={{
              maxWidth: 800,
              width: "100%",
              margin: "20px",
              position: "relative",
            }}
          >
            <div style={{
              position: "absolute",
              display: "inline-block",
              top: "10px",
              left: "10px",
              backgroundColor: "white",
              borderRadius: "10px",
              padding: "10px",
              color: '#1a237e',
              // 添加阴影
              boxShadow: "0 0 10px 0 rgba(0, 0, 0, 0.1)",
            }}>{genderEmoji} {username}</div>
            <CardContent>
              <div style={{
                height: "50px",
              }}></div>
              <StyledMarkdown content={item.content} />
            </CardContent>
          </Card>
        </>
      )}
      {item.role === "assistant" && (
        <>
          <div style={{ height: "30px" }}></div>
          <Card sx={{ maxWidth: 800, width: "100%", margin: "20px" }}>
            <CardContent>
              <StyledMarkdown content={item.content} />
            </CardContent>
          </Card>
        </>
      )}
      {/* 如果 item.role 没有传入任何值，则不显示 */}
      {item.role === undefined && (
        <>
        <div style={{ height: "30px" }}></div>
        <Card sx={{ maxWidth: 800, width: "100%", margin: "20px" }}>
          <CardContent>
            <StyledMarkdown content={item.content} />
          </CardContent>
        </Card>
      </>
      )}
    </Stack>
  );
}

export default ChatMarkdownStack;

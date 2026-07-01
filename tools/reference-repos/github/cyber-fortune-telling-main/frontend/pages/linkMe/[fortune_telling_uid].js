import { Box } from "@mui/material";
import { useRouter } from "next/router";
import LinkMeContent from "@/components/LinkMeContent";




function LinkMe({ fortune_telling_uid }) {
  // 通过 url获取 uids参数, 如果uids参数存在，则使用uids参数，否则使用 fortune_telling_uid
  const { uids } = useRouter().query;
  const uidsArray = uids ? uids.split(",") : [fortune_telling_uid];

  return (
    <>
      {uidsArray.length === 1 && (
        <LinkMeContent fortune_telling_uid={uidsArray[0]} />
      )}
      {uidsArray.length > 1 && (
        <Box 
          sx={{ 
            display: 'flex', 
            flexDirection: { xs: 'column', md: 'row' }, 
            gap: 0, 
            height: '100vh' 
          }}
        >
          {uidsArray.map((uid, index) => (
            <Box key={index} sx={{ flex: 1, overflowY: 'auto', border: '1px solid #ccc', borderRadius: '10px' }}>
              <LinkMeContent fortune_telling_uid={uid} />
            </Box>
          ))}
        </Box>
      )}
    </>
  );
}

export async function getServerSideProps({ params }) {
  try {
    const { fortune_telling_uid } = params;
    return {
      props: {
        fortune_telling_uid: fortune_telling_uid,
      },
    };
  } catch (error) {
    return {
      props: {},
    };
  }
}

export default LinkMe;

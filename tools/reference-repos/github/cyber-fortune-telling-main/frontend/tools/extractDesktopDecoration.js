// Function to extract desktop decoration image source
const extractDesktopDecoration = (content) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(content, "text/html");
  const deskDecorImg = doc.querySelector("img.desk-decor");
  return deskDecorImg ? deskDecorImg.getAttribute("src") : "";
};

export default extractDesktopDecoration; 
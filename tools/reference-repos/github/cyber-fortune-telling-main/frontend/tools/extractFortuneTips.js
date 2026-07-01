import converter from "@/tools/converter";

// Function to extract fortune tips
const extractFortuneTips = (content) => {
  // Convert markdown to HTML first
  const htmlContent = converter.makeHtml(content);
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlContent, "text/html");
  const tipElements = doc.querySelectorAll(".fortune-tip");
  const tips = Array.from(tipElements).map((tip) => {
    // Remove any leading numbers, dots, and whitespace
    return tip.textContent.replace(/^\d*\.?\s*/, "");
  });
  return tips;
};

export default extractFortuneTips; 
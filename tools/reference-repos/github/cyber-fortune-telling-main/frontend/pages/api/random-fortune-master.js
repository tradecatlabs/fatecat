import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  const decorDir = path.join(process.cwd(), 'public', 'fortune-master');
  let files;
  try {
    files = fs.readdirSync(decorDir);
  } catch (err) {
    return res.status(500).json({ error: 'Failed to read directory' });
  }

  // 只匹配图片文件
  const imageFiles = files.filter(file => /\.(png|jpg|jpeg|gif)$/i.test(file));

  if (imageFiles.length === 0) {
    return res.status(404).json({ error: 'No images found' });
  }

  // 随机抽取一张
  const randomFile = imageFiles[Math.floor(Math.random() * imageFiles.length)];
  // 302重定向到图片路径，文件名进行URI编码
  const encodedFile = encodeURIComponent(randomFile);
  res.writeHead(302, { Location: `/fortune-master/${encodedFile}` });
  res.end();
}

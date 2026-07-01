import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  const { keyword } = req.query;
  if (!keyword) {
    return res.status(400).json({ error: 'Missing keyword parameter' });
  }

  const decorDir = path.join(process.cwd(), 'public', 'desk-decor');
  let files;
  try {
    files = fs.readdirSync(decorDir);
  } catch (err) {
    return res.status(500).json({ error: 'Failed to read directory' });
  }

  // 只匹配图片文件
  const imageFiles = files.filter(file => /\.(png|jpg|jpeg|gif)$/i.test(file));
  // 关键词模糊匹配
  const matched = imageFiles.filter(file => file.includes(keyword));

  if (matched.length === 0) {
    return res.status(404).json({ error: 'No matching images found' });
  }

  // 随机抽取一张
  const randomFile = matched[Math.floor(Math.random() * matched.length)];
  // 302重定向到图片路径，文件名进行URI编码
  const encodedFile = encodeURIComponent(randomFile);
  res.writeHead(302, { Location: `/desk-decor/${encodedFile}` });
  res.end();
}

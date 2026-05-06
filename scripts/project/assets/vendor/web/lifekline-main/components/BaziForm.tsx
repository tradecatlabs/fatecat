import React, { useState, useEffect } from 'react';
import { UserInput, Gender } from '../types';
import { Loader2, Sparkles, Copy, Check } from 'lucide-react';

interface BaziFormProps {
  onSubmit: (data: UserInput) => void;
  isLoading: boolean;
}

const TEMPLATE = `2002-02-19
12:00
济南
耿至宇`;

const BaziForm: React.FC<BaziFormProps> = ({ onSubmit, isLoading }) => {
  const [gender, setGender] = useState<Gender>(Gender.MALE);
  const [inputText, setInputText] = useState('');
  const [copied, setCopied] = useState(false);
  const [currentTime, setCurrentTime] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const update = () => {
      const now = new Date();
      setCurrentTime(now.toLocaleString('zh-CN', { 
        timeZone: 'Asia/Shanghai',
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit'
      }).replace(/\//g, '-'));
    };
    update();
    const timer = setInterval(update, 1000);
    return () => clearInterval(timer);
  }, []);

  const copyTemplate = () => {
    setInputText(TEMPLATE);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const lines = inputText.trim().split('\n').map(l => l.trim()).filter(Boolean);
    if (lines.length < 3) {
      setError('请至少输入日期、时间、地点三行');
      return;
    }

    const [date, time, location, name = ''] = lines;

    // 验证日期格式
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      setError('日期格式错误，请使用 YYYY-MM-DD');
      return;
    }

    // 验证时间格式
    if (!/^\d{1,2}:\d{2}$/.test(time)) {
      setError('时间格式错误，请使用 HH:MM');
      return;
    }

    // 调用后端 API 获取八字数据
    try {
      const resp = await fetch('http://localhost:8001/api/v1/bazi/simple', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name || '未知',
          gender: gender === Gender.MALE ? 'male' : 'female',
          birthDate: date,
          birthTime: time + ':00',
          birthPlace: { name: location, longitude: 116.4, latitude: 39.9, timezone: 'Asia/Shanghai' },
          options: { useTrueSolarTime: true }
        })
      });

      const data = await resp.json();
      if (!data.success) {
        setError(data.error || '计算失败');
        return;
      }

      const fp = data.data.fourPillars;
      const mf = data.data.majorFortune;

      // 构造 UserInput 传给 K 线生成
      onSubmit({
        name: name || '未知',
        gender,
        birthYear: date.split('-')[0],
        yearPillar: fp.year.fullName,
        monthPillar: fp.month.fullName,
        dayPillar: fp.day.fullName,
        hourPillar: fp.hour.fullName,
        startAge: String(mf?.startAge || 3),
        firstDaYun: mf?.periods?.[0]?.ganZhi || '',
        modelName: 'gemini-2.5-pro',
        apiBaseUrl: 'http://localhost:3000/api/v1',
        apiKey: 'cr_3bb0ac17173c6d90498c8b2bd1b313e2b30f617d9f705dbac7a97dd35226f30c',
      });
    } catch (err) {
      setError('无法连接八字服务，请确保后端已启动');
    }
  };

  return (
    <div className="w-full max-w-md bg-white p-6 rounded-2xl shadow-xl border border-gray-100">
      {/* 标题 */}
      <div className="text-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center justify-center gap-2">
          🎲 超级排盘
        </h2>
      </div>

      {/* 性别切换 */}
      <div className="bg-gray-50 rounded-xl p-4 mb-4">
        <p className="text-sm text-gray-600 mb-2">
          当前: <span className="font-bold">{gender === Gender.MALE ? '乾造（男）' : '坤造（女）'}</span>
        </p>
        <p className="text-xs text-gray-400 mb-2">（点击下方按钮切换性别）</p>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setGender(Gender.MALE)}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${
              gender === Gender.MALE
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-600 border hover:bg-gray-50'
            }`}
          >
            ♂ 乾造(男)
          </button>
          <button
            type="button"
            onClick={() => setGender(Gender.FEMALE)}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${
              gender === Gender.FEMALE
                ? 'bg-pink-600 text-white'
                : 'bg-white text-gray-600 border hover:bg-gray-50'
            }`}
          >
            ♀ 坤造(女)
          </button>
        </div>
      </div>

      {/* 输入说明 */}
      <div className="mb-3">
        <p className="text-sm font-medium text-gray-700 mb-1">请输入信息：</p>
        <p className="text-xs text-gray-500">日期/时间（公历）/地点/姓名</p>
        <p className="text-xs text-gray-400">已自动做真太阳时转换，可直接填北京时间</p>
        <p className="text-xs text-gray-400">仅接受公历日期，按四行逐行输入</p>
      </div>

      {/* 复制模板按钮 */}
      <button
        type="button"
        onClick={copyTemplate}
        className="w-full mb-3 py-2 px-3 bg-amber-50 hover:bg-amber-100 border border-amber-200 rounded-lg text-sm text-amber-800 flex items-center justify-center gap-2 transition"
      >
        {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
        点击复制模板
      </button>

      {/* 模板预览 */}
      <div className="bg-gray-100 rounded-lg p-3 mb-3 font-mono text-xs text-gray-600">
        <pre>{TEMPLATE}</pre>
      </div>

      {/* 输入框 */}
      <form onSubmit={handleSubmit}>
        <textarea
          value={inputText}
          onChange={(e) => { setInputText(e.target.value); setError(''); }}
          placeholder={`2002-02-19\n12:00\n济南\n耿至宇`}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none font-mono text-sm mb-3 resize-none"
        />

        {error && (
          <p className="text-red-500 text-xs mb-3">{error}</p>
        )}

        {/* 当前时间 */}
        <p className="text-xs text-gray-400 mb-3 text-center">
          ⏱️ 北京时间：{currentTime}
        </p>

        {/* 提交按钮 */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-indigo-900 to-gray-900 hover:from-black hover:to-black text-white font-bold py-3 rounded-xl shadow-lg transform transition-all hover:scale-[1.01] active:scale-[0.99] disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="animate-spin h-5 w-5" />
              <span>大师推演中(3-5分钟)</span>
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5 text-amber-300" />
              <span>生成人生K线</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default BaziForm;

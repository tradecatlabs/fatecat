import React, { useState } from 'react';
import { LifeDestinyResult, Gender } from '../types';
import { generateLifeAnalysis } from '../services/geminiService';
import { FileUp, FileDown, Loader2, AlertCircle, Sparkles } from 'lucide-react';

interface Props {
  onDataImport: (data: LifeDestinyResult) => void;
}

interface ParsedBasis {
  name: string;
  gender: Gender;
  birthYear: string;
  yearPillar: string;
  monthPillar: string;
  dayPillar: string;
  hourPillar: string;
  startAge: string;
  firstDaYun: string;
}

const MAX_CONTEXT_LEN = 8000; // 截断TXT，避免提示词过长

const ImportReportMode: React.FC<Props> = ({ onDataImport }) => {
  const [jsonFileName, setJsonFileName] = useState<string>('');
  const [txtFileName, setTxtFileName] = useState<string>('');
  const [contextReport, setContextReport] = useState<string>('');
  // 默认指向本地 gemincli 无头代理
  const [apiBaseUrl, setApiBaseUrl] = useState<string>('http://localhost:3000/gemini');
  const [apiKey, setApiKey] = useState<string>('cr_3bb0ac17173c6d90498c8b2bd1b313e2b30f617d9f705dbac7a97dd35226f30c');
  const [modelName, setModelName] = useState<string>('gemini-2.5-pro');
  const [status, setStatus] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const [parsed, setParsed] = useState<ParsedBasis | null>(null);

  const handleJsonUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(null);
    setJsonFileName(file.name);
    try {
      const text = await file.text();
      const data = JSON.parse(text);

      // 如果已经是生成好的 K 线 JSON，直接渲染，不必再调用 LLM
      if (data.chartPoints && data.analysis) {
        const ready: LifeDestinyResult = {
          chartData: data.chartPoints,
          analysis: data.analysis
        };
        onDataImport(ready);
        setParsed(null);
        setStatus('已载入现成的 K 线 JSON');
        return;
      }

      const input = data.input || {};
      const mf = data.majorFortune || data.majorFortuneInfo || {};
      const pillars = data.fourPillars || {};

      const basis: ParsedBasis = {
        name: input.name || '命主',
        gender: (input.gender || 'male').toLowerCase() === 'female' ? Gender.FEMALE : Gender.MALE,
        birthYear: (input.birthDate || '1900-01-01').slice(0, 4),
        yearPillar: pillars.year?.fullName || pillars.year?.name || '',
        monthPillar: pillars.month?.fullName || pillars.month?.name || '',
        dayPillar: pillars.day?.fullName || pillars.day?.name || '',
        hourPillar: pillars.hour?.fullName || pillars.hour?.name || '',
        startAge: String(mf.startAge || mf.start_age || 1),
        firstDaYun: mf.pillars?.[0]?.fullName || mf.pillars?.[0]?.name || ''
      };

      if (!basis.yearPillar || !basis.monthPillar || !basis.dayPillar || !basis.hourPillar) {
        throw new Error('JSON 缺少四柱 fullName');
      }
      if (!basis.firstDaYun) {
        throw new Error('JSON 缺少第一步大运 fullName');
      }
      setParsed(basis);
    } catch (err: any) {
      setParsed(null);
      setError(`解析 JSON 失败：${err.message}`);
    } finally {
      e.target.value = '';
    }
  };

  const handleTxtUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setTxtFileName(file.name);
    const text = await file.text();
    // 截断避免超长
    const trimmed = text.length > MAX_CONTEXT_LEN ? text.slice(0, MAX_CONTEXT_LEN) + '\n...[内容已截断]' : text;
    setContextReport(trimmed);
    e.target.value = '';
  };

  const handleSubmit = async () => {
    if (!parsed) {
      setError('请先导入排盘 JSON');
      return;
    }
    if (!apiKey.trim()) {
      setError('请输入 API Key');
      return;
    }
    setError(null);
    setIsLoading(true);
    setStatus('LLM 正在生成 K 线 JSON...');
    try {
      const result = await generateLifeAnalysis({
        name: parsed.name,
        gender: parsed.gender,
        birthYear: parsed.birthYear,
        yearPillar: parsed.yearPillar,
        monthPillar: parsed.monthPillar,
        dayPillar: parsed.dayPillar,
        hourPillar: parsed.hourPillar,
        startAge: parsed.startAge,
        firstDaYun: parsed.firstDaYun,
        modelName,
        apiBaseUrl,
        apiKey,
        contextReport
      });
      onDataImport(result);
      setStatus('');
    } catch (err: any) {
      setError(err.message || '生成失败');
    } finally {
      setIsLoading(false);
      setStatus('');
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto space-y-4">
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-5 h-5 text-indigo-500" />
          <h2 className="text-xl font-bold text-gray-800">导入排盘文件 → 一键生成人生K线</h2>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <label className="flex items-center justify-between gap-3 px-4 py-3 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-indigo-400 hover:bg-indigo-50 transition">
            <div className="flex items-center gap-2 text-sm text-gray-700">
              <FileUp className="w-5 h-5 text-indigo-500" />
              <span>{jsonFileName || '上传排盘 JSON（complete_result*.json）'}</span>
            </div>
            <input type="file" accept=".json" className="hidden" onChange={handleJsonUpload} />
          </label>

          <label className="flex items-center justify-between gap-3 px-4 py-3 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-amber-400 hover:bg-amber-50 transition">
            <div className="flex items-center gap-2 text-sm text-gray-700">
              <FileDown className="w-5 h-5 text-amber-500" />
              <span>{txtFileName || '可选：上传排盘 TXT 作为上下文'}</span>
            </div>
            <input type="file" accept=".txt" className="hidden" onChange={handleTxtUpload} />
          </label>
        </div>

        {parsed && (
          <div className="mt-3 text-xs text-gray-600 bg-gray-50 border border-gray-200 rounded-lg p-3 leading-relaxed">
            <div>姓名：{parsed.name} / 性别：{parsed.gender === Gender.MALE ? '乾造' : '坤造'}</div>
            <div>出生年：{parsed.birthYear}</div>
            <div>四柱：{parsed.yearPillar} | {parsed.monthPillar} | {parsed.dayPillar} | {parsed.hourPillar}</div>
            <div>起运：{parsed.startAge} 岁 / 首步大运：{parsed.firstDaYun}</div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
          <input
            className="w-full px-3 py-2 border rounded-lg text-sm"
            placeholder="API Base URL"
            value={apiBaseUrl}
            onChange={(e) => setApiBaseUrl(e.target.value)}
          />
          <input
            className="w-full px-3 py-2 border rounded-lg text-sm"
            placeholder="Model (默认 gemini-2.5-pro)"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
          />
          <input
            className="w-full px-3 py-2 border rounded-lg text-sm"
            placeholder="API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>

        {status && (
          <div className="mt-3 text-sm text-indigo-600 bg-indigo-50 border border-indigo-200 rounded-lg p-2 flex items-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin" />
            {status}
          </div>
        )}
        {error && (
          <div className="mt-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-2 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            {error}
          </div>
        )}

        <button
          onClick={handleSubmit}
          disabled={isLoading || !parsed}
          className="mt-4 w-full md:w-auto px-5 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2 justify-center"
        >
          {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
          {isLoading ? '生成中…' : '生成人生K线 JSON 并展示'}
        </button>
      </div>
    </div>
  );
};

export default ImportReportMode;

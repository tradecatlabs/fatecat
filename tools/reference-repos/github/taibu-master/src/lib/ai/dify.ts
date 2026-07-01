/**
 * Dify API 封装库
 *
 * 用于调用 Dify 工作流处理文件上传和网络搜索
 *
 * 两步流程：
 * 1. 先通过 /v1/files/upload 上传文件获取文件ID
 * 2. 再调用 /v1/workflows/run 时用JSON传递文件ID
 *
 * 参考：https://docs.dify.ai/api-reference/files/file-upload
 */

import type { DifyMode, DifyResponse } from '@/types';

// 环境变量
const DIFY_API_KEY = process.env.DIFY_API_KEY;
const DIFY_API_URL = process.env.DIFY_API_URL || 'https://api.dify.ai/v1';

// 超时时间（毫秒）
const DIFY_TIMEOUT = 30000;

// 文件限制
const MAX_FILE_SIZE = 15 * 1024 * 1024; // 15MB (Dify限制)
const ALLOWED_EXTENSIONS = ['pdf', 'txt', 'md', 'doc', 'docx', 'xlsx', 'xls', 'csv', 'html', 'xml'];

export interface DifyRequest {
    mode: DifyMode;
    query?: string;
    file?: File;
    userId: string;
}

export interface DifyResult {
    success: boolean;
    data?: DifyResponse;
    error?: string;
}

interface FileUploadResponse {
    id: string;
    name: string;
    size: number;
    extension: string;
    mime_type: string;
    created_by: string;
    created_at: number;
}

/**
 * 检查 Dify API 是否可用
 */
export function isDifyAvailable(): boolean {
    return !!DIFY_API_KEY;
}

/**
 * 验证文件类型和大小
 */
export function validateFile(file: File): { valid: boolean; error?: string } {
    if (file.size > MAX_FILE_SIZE) {
        return { valid: false, error: '文件大小不能超过15MB' };
    }

    const ext = file.name.split('.').pop()?.toLowerCase();
    if (!ext || !ALLOWED_EXTENSIONS.includes(ext)) {
        return {
            valid: false,
            error: `不支持的文件类型，请上传 ${ALLOWED_EXTENSIONS.join('、').toUpperCase()} 文件`
        };
    }

    return { valid: true };
}

/**
 * 第一步：上传文件到 Dify
 */
async function uploadFileToDify(
    file: File,
    userId: string,
    signal?: AbortSignal
): Promise<{ success: boolean; fileId?: string; error?: string }> {
    const uploadUrl = `${DIFY_API_URL}/files/upload`;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user', userId);

    try {
        const response = await fetch(uploadUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${DIFY_API_KEY}`,
            },
            body: formData,
            signal,
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('[dify] File upload error:', response.status, errorText);
            return { success: false, error: `文件上传失败: ${response.status}` };
        }

        const result: FileUploadResponse = await response.json();
        return { success: true, fileId: result.id };
    } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
            return { success: false, error: '请求超时' };
        }
        console.error('[dify] File upload failed:', error);
        return { success: false, error: '文件上传失败' };
    }
}

/**
 * 第二步：运行 Dify 工作流
 */
async function runDifyWorkflow(
    mode: DifyMode,
    userId: string,
    query?: string,
    fileId?: string,
    signal?: AbortSignal
): Promise<DifyResult> {
    // 构建 inputs 对象
    const inputs: Record<string, unknown> = {
        mode: mode,
    };

    if (query) {
        inputs.query = query;
    }

    if (fileId) {
        // 工作流中定义的文件变量名为 file，需要是数组格式
        inputs.file = [{
            type: 'document',
            transfer_method: 'local_file',
            upload_file_id: fileId,
        }];
    }

    const body = {
        inputs,
        response_mode: 'blocking',
        user: userId,
    };

    // 请求工作流URL
    const workflowUrl = `${DIFY_API_URL}/workflows/run`;

    try {
        const response = await fetch(workflowUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${DIFY_API_KEY}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
            signal,
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('[dify] Workflow error:', response.status, errorText);
            return { success: false, error: `工作流执行失败: ${response.status}` };
        }

        const result = await response.json();
        const data = parseDifyResponse(result);

        return { success: true, data };
    } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
            return { success: false, error: '请求超时' };
        }
        console.error('[dify] Workflow failed:', error);
        return { success: false, error: '工作流执行失败' };
    }
}

/**
 * 解析 Dify 工作流返回的数据
 */
function parseDifyResponse(result: unknown): DifyResponse {
    const data = result as Record<string, unknown>;
    const outputs = (data?.data as Record<string, unknown>)?.outputs as Record<string, unknown>;

    if (!outputs || typeof outputs !== 'object') {
        return {};
    }

    // 辅助函数：将值转换为字符串（支持字符串和数组）
    const toStringContent = (value: unknown): string | undefined => {
        if (typeof value === 'string') {
            return value;
        }
        if (Array.isArray(value)) {
            return value.filter(item => typeof item === 'string').join('\n');
        }
        return undefined;
    };

    return {
        web_content: toStringContent(outputs.web_content),
        file_content: toStringContent(outputs.file_content),
    };
}

/**
 * 调用 Dify 工作流 API（完整流程）
 */
export async function callDifyWorkflow(request: DifyRequest): Promise<DifyResult> {
    if (!DIFY_API_KEY) {
        return { success: false, error: 'Dify API 未配置' };
    }

    // 验证文件
    if (request.file) {
        const validation = validateFile(request.file);
        if (!validation.valid) {
            return { success: false, error: validation.error };
        }
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), DIFY_TIMEOUT);

    try {
        let fileId: string | undefined;

        // 第一步：如果有文件，先上传
        if (request.file) {
            const uploadResult = await uploadFileToDify(
                request.file,
                request.userId,
                controller.signal
            );
            if (!uploadResult.success) {
                return { success: false, error: uploadResult.error };
            }
            fileId = uploadResult.fileId;
        }

        // 第二步：运行工作流
        const result = await runDifyWorkflow(
            request.mode,
            request.userId,
            request.query,
            fileId,
            controller.signal
        );

        return result;
    } finally {
        clearTimeout(timeoutId);
    }
}

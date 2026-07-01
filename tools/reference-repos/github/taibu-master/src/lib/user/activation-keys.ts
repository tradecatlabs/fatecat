/**
 * 激活Key管理库
 * 
 * 提供激活Key的创建、验证、激活等功能
 */

import { getSystemAdminClient } from "@/lib/api-utils";
import type { MembershipType } from "@/lib/user/membership";

// Key类型
export type KeyType = 'membership' | 'credits';

// 激活Key信息
export interface ActivationKey {
    id: string;
    key_code: string;
    key_type: KeyType;
    membership_type: MembershipType | null;
    credits_amount: number | null;
    is_used: boolean;
    used_by: string | null;
    used_at: string | null;
    created_by: string;
    created_at: string;
}

// 创建Key的参数
export interface CreateKeyParams {
    keyType: KeyType;
    membershipType?: MembershipType;
    creditsAmount?: number;
    count: number;
}

// 激活结果
export interface ActivateResult {
    success: boolean;
    error?: string;
    keyType?: KeyType;
    membershipType?: MembershipType;
    creditsAmount?: number;
}

/**
 * 生成激活Key代码 (格式: sk-xxxx)
 */
function generateKeyCode(): string {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let code = 'sk-';
    for (let i = 0; i < 16; i++) {
        code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
}

/**
 * 批量创建激活Key (管理员)
 */
export async function createActivationKeys(
    adminId: string,
    params: CreateKeyParams
): Promise<{ success: boolean; keys?: string[]; error?: string }> {
    try {
        const supabase = getSystemAdminClient();

        // 验证参数
        if (params.keyType === 'membership' && !params.membershipType) {
            return { success: false, error: '会员类型Key需要指定会员等级' };
        }
        if (params.keyType === 'credits' && (!params.creditsAmount || params.creditsAmount <= 0)) {
            return { success: false, error: '积分类型Key需要指定有效的积分数量' };
        }
        if (params.count <= 0 || params.count > 100) {
            return { success: false, error: '创建数量需在1-100之间' };
        }

        // 生成Key
        const keysToCreate = [];
        for (let i = 0; i < params.count; i++) {
            keysToCreate.push({
                key_code: generateKeyCode(),
                key_type: params.keyType,
                membership_type: params.keyType === 'membership' ? params.membershipType : null,
                credits_amount: params.keyType === 'credits' ? params.creditsAmount : null,
                created_by: adminId,
            });
        }

        const { data, error } = await supabase
            .from('activation_keys')
            .insert(keysToCreate)
            .select('key_code');

        if (error) {
            console.error('[activation-keys] Failed to create keys:', error);
            return { success: false, error: '创建激活Key失败' };
        }

        return {
            success: true,
            keys: data?.map(k => k.key_code) || []
        };
    } catch (error) {
        console.error('[activation-keys] Error creating keys:', error);
        return { success: false, error: '服务器错误' };
    }
}

/**
 * 获取所有激活Key (管理员)
 */
export async function getAllActivationKeys(
    filters?: { isUsed?: boolean; keyType?: KeyType }
): Promise<ActivationKey[]> {
    try {
        const supabase = getSystemAdminClient();

        let query = supabase
            .from('activation_keys')
            .select('*')
            .neq('source', 'linuxdo_monthly')
            .order('created_at', { ascending: false });

        if (filters?.isUsed !== undefined) {
            query = query.eq('is_used', filters.isUsed);
        }
        if (filters?.keyType) {
            query = query.eq('key_type', filters.keyType);
        }

        const { data, error } = await query;

        if (error) {
            console.error('[activation-keys] Failed to fetch keys:', error);
            return [];
        }

        return data || [];
    } catch (error) {
        console.error('[activation-keys] Error fetching keys:', error);
        return [];
    }
}

/**
 * 删除激活Key (管理员)
 */
export async function deleteActivationKey(keyId: string): Promise<boolean> {
    try {
        const supabase = getSystemAdminClient();

        const { error } = await supabase
            .from('activation_keys')
            .delete()
            .eq('id', keyId);

        if (error) {
            console.error('[activation-keys] Failed to delete key:', error);
            return false;
        }

        return true;
    } catch (error) {
        console.error('[activation-keys] Error deleting key:', error);
        return false;
    }
}

/**
 * 用户激活Key
 */
export async function activateKey(
    userId: string,
    keyCode: string
): Promise<ActivateResult> {
    try {
        // 校验Key格式
        if (!keyCode || !keyCode.startsWith('sk-') || keyCode.length < 10) {
            return { success: false, error: '无效的激活码格式' };
        }
        const supabase = getSystemAdminClient();
        const { data, error } = await supabase.rpc('activate_key_as_service', {
            p_user_id: userId,
            p_key_code: keyCode,
        });

        if (error) {
            console.error('[activation-keys] RPC error:', error);
            return { success: false, error: '激活失败，请稍后重试' };
        }

        const result = Array.isArray(data) ? data[0] : data;
        if (!result?.success) {
            return { success: false, error: result?.error || '激活失败，请重试' };
        }

        return {
            success: true,
            keyType: result.key_type as KeyType,
            membershipType: (result.membership_type as MembershipType) || undefined,
            creditsAmount: result.credits_amount ?? undefined,
        };
    } catch (error) {
        console.error('[activation-keys] Error activating key:', error);
        return { success: false, error: '服务器错误' };
    }
}

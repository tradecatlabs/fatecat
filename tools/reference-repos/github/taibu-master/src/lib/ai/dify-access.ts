/**
 * Dify 功能权限校验库
 *
 * 会员权限规则：
 * - free: 只能使用 file（附件上传）
 * - plus: 可以使用 file 或 web，但不能同时使用
 * - pro: 可以同时使用 file 和 web
 */

import type { MembershipType } from '@/lib/user/membership';
import type { DifyMode } from '@/types';

export interface DifyAccessResult {
    allowed: boolean;
    reason?: string;
}

/**
 * 检查用户是否有权限使用指定的 Dify 模式
 */
export function checkDifyAccess(
    membershipType: MembershipType,
    mode: DifyMode
): DifyAccessResult {
    // free 用户只能使用 file
    if (membershipType === 'free') {
        if (mode === 'web' || mode === 'all') {
            return {
                allowed: false,
                reason: '免费用户无法使用网络搜索功能，请升级会员',
            };
        }
        return { allowed: true };
    }

    // plus 用户可以使用 file 或 web，但不能同时使用
    if (membershipType === 'plus') {
        if (mode === 'all') {
            return {
                allowed: false,
                reason: 'Plus 会员无法同时使用文件和搜索，请升级 Pro 会员',
            };
        }
        return { allowed: true };
    }

    // pro 用户可以使用所有模式
    return { allowed: true };
}


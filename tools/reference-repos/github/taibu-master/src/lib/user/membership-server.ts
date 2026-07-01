import { createAuthedClient, getSystemAdminClient } from "@/lib/api-utils";
import { isMembershipExpired, type MembershipType } from "@/lib/user/membership";

type MembershipReaderClient = {
    from: (table: 'users') => {
        select: (columns: string) => {
            eq: (column: 'id', userId: string) => {
                maybeSingle: () => PromiseLike<{
                    data: {
                        membership: MembershipType | null;
                        membership_expires_at: string | null;
                    } | null;
                    error: { message?: string } | null;
                }>;
            };
        };
    };
};

export class MembershipResolutionError extends Error {
    constructor(message: string, options?: { cause?: unknown }) {
        super(message);
        this.name = 'MembershipResolutionError';
        if (options && 'cause' in options) {
            Object.defineProperty(this, 'cause', {
                value: options.cause,
                enumerable: false,
                configurable: true,
                writable: true,
            });
        }
    }
}

export async function getEffectiveMembershipType(
    userId: string,
    options?: { client?: unknown },
): Promise<MembershipType> {
    try {
        const supabase = (options?.client ?? getSystemAdminClient()) as MembershipReaderClient;
        const { data, error } = await supabase
            .from("users")
            .select("membership, membership_expires_at")
            .eq("id", userId)
            .maybeSingle();

        if (error || !data) {
            if (error) {
                console.error("[membership] Failed to fetch membership:", error.message);
            } else {
                console.error("[membership] Missing membership row for user:", userId);
            }
            throw new MembershipResolutionError('获取会员状态失败', { cause: error });
        }

        const membership = (data.membership || "free") as MembershipType;

        if (isMembershipExpired({ membership, membership_expires_at: data.membership_expires_at })) {
            return "free";
        }

        return membership;
    } catch (error) {
        if (error instanceof MembershipResolutionError) {
            throw error;
        }
        console.error("[membership] Failed to resolve membership:", error);
        throw new MembershipResolutionError('获取会员状态失败', { cause: error });
    }
}

/**
 * 通过 access token 解析当前用户的有效会员等级
 * 统一入口，避免各模块重复实现 token -> userId -> membership 链路
 */
export async function resolveTokenMembership(accessToken?: string): Promise<MembershipType> {
    if (!accessToken) return 'free';
    try {
        const supabase = createAuthedClient(accessToken);
        const { data: { user } } = await supabase.auth.getUser();
        if (!user) {
            throw new MembershipResolutionError('认证已失效');
        }

        const membershipClient: MembershipReaderClient = {
            from(table) {
                return {
                    select(columns) {
                        return {
                            eq(column, userId) {
                                return {
                                    async maybeSingle() {
                                        const { data, error } = await supabase
                                            .from(table)
                                            .select(columns)
                                            .eq(column, userId)
                                            .maybeSingle();
                                        const membershipRow = data as {
                                            membership?: string | null;
                                            membership_expires_at?: string | null;
                                        } | null;

                                        return {
                                            data: membershipRow
                                                ? {
                                                    membership: (membershipRow.membership ?? null) as MembershipType | null,
                                                    membership_expires_at: (membershipRow.membership_expires_at ?? null) as string | null,
                                                }
                                                : null,
                                            error: error ? { message: error.message } : null,
                                        };
                                    },
                                };
                            },
                        };
                    },
                };
            },
        };

        return await getEffectiveMembershipType(user.id, { client: membershipClient });
    } catch (error) {
        if (error instanceof MembershipResolutionError) {
            throw error;
        }
        throw new MembershipResolutionError('获取会员状态失败', { cause: error });
    }
}

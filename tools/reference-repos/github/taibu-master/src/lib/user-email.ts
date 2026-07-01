type EmailLikeUser = {
    email?: string | null;
};

const LINUXDO_PRIVATE_RELAY_SUFFIX = '@privaterelay.linux.do';

export function isLinuxDoRelayEmail(email: string | null | undefined): boolean {
    return (email ?? '').trim().toLowerCase().endsWith(LINUXDO_PRIVATE_RELAY_SUFFIX);
}

export function getUserEmailDisplay(user: EmailLikeUser | null | undefined): string {
    const email = (user?.email ?? '').trim();
    if (!email) {
        return '';
    }

    if (isLinuxDoRelayEmail(email)) {
        return 'Linux.do 隐私邮箱';
    }

    return email;
}

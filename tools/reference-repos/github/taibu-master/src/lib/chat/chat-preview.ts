interface ShouldRequestChatPreviewInput {
    userId?: string | null;
    isLoading: boolean;
    isSendingToList: boolean;
}

export function shouldRequestChatPreview({
    userId,
    isLoading,
    isSendingToList,
}: ShouldRequestChatPreviewInput): boolean {
    return !!userId && !isLoading && !isSendingToList;
}

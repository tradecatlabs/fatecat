type QueryError = { message?: string } | null;

type ConversationDeleteClient = {
  rpc: (
    fn: string,
    args: Record<string, unknown>,
  ) => Promise<{ data: boolean | null; error: QueryError }>;
};

function normalizeError(error: QueryError) {
  if (!error) return null;
  return { message: typeof error.message === 'string' ? error.message : 'Unknown error' };
}

export async function deleteConversationGraph(
  supabase: ConversationDeleteClient,
  conversationId: string,
) {
  const { data, error } = await supabase.rpc('delete_conversation_graph', {
    p_conversation_id: conversationId,
  });

  if (error) {
    return { error: normalizeError(error), notFound: false };
  }

  return { error: null, notFound: data === false };
}

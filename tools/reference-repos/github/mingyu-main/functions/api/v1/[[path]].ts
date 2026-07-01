import { handlePublicApiRequest, normalizeApiPath } from '../../../src/lib/public-api/handler';

type PagesContext = {
  request: Request;
  params?: {
    path?: string | string[];
  };
};

export function onRequest(context: PagesContext) {
  const paramPath = context.params?.path;
  const segments = Array.isArray(paramPath)
    ? paramPath
    : typeof paramPath === 'string'
      ? paramPath.split('/').filter(Boolean)
      : normalizeApiPath(new URL(context.request.url).pathname);

  return handlePublicApiRequest(context.request, segments);
}

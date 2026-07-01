import { NextRequest } from "next/server";
import { getFeatureToggles, setFeatureToggle, FEATURE_MODULE_IDS, type FeatureModuleId } from "@/lib/app-settings";
import { jsonError, jsonOk, requireAdminUser } from "@/lib/api-utils";
import { createMemoryCache } from '@/lib/cache/memory';

const CACHE_TTL_MS = 30_000;
const togglesCache = createMemoryCache<Record<string, boolean>>(CACHE_TTL_MS);

export async function GET() {
  // feature-toggles 是公共配置，匿名用户也需要知道哪些功能开启

  const cached = togglesCache.get('all');
  if (cached !== null) {
    return jsonOk({ toggles: cached });
  }
  const toggles = await getFeatureToggles();
  togglesCache.set('all', toggles);
  return jsonOk({ toggles });
}

export async function POST(request: NextRequest) {
  try {
    const auth = await requireAdminUser(request);
    if ("error" in auth) {
      return jsonError(auth.error.message, auth.error.status);
    }

    const { featureId, disabled } = await request.json();
    if (
      typeof featureId !== 'string' ||
      !FEATURE_MODULE_IDS.includes(featureId as FeatureModuleId) ||
      typeof disabled !== 'boolean'
    ) {
      return jsonError('无效的参数', 400);
    }

    const success = await setFeatureToggle(featureId as FeatureModuleId, disabled);
    if (!success) {
      return jsonError('更新失败', 500);
    }

    togglesCache.clear();
    return jsonOk({ success: true, featureId, disabled });
  } catch (error) {
    console.error("[feature-toggles] Error:", error);
    return jsonError("服务器错误", 500);
  }
}

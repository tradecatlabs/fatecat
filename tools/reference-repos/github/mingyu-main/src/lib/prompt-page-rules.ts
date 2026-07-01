export function shouldShowPromptShareButton(options: {
  viewportWidth: number;
  hasNavigatorShare: boolean;
}) {
  return options.viewportWidth < 1024 && options.hasNavigatorShare;
}

export function buildBaziCustomPromptPatch() {
  return {
    baziShortcutMode: '自定义',
    baziPresetId: 'ai-mingge-zonglun',
    baziQuickQuestion: '',
  };
}

export function buildZiweiCustomPromptPatch() {
  return {
    ziweiShortcutMode: '自定义',
    ziweiTopic: 'chat',
    ziweiQuickQuestion: '',
  };
}

import type { ConversationListItem } from '@/types';

function replaceConversationArrow(title: string) {
  return title.replace(/ -> /g, ' 变 ');
}

export function getConversationDisplayParts(conv: ConversationListItem) {
  const question = conv.questionPreview || null;
  let mainTitle = replaceConversationArrow(conv.title);
  let subTitle: string | null = null;
  let changedTitle: string | null = null;

  if ((conv.sourceType === 'liuyao' || conv.sourceType === 'tarot') && mainTitle.includes(' - ')) {
    mainTitle = mainTitle.split(' - ').slice(1).join(' - ');
    subTitle = question;
  }

  if (conv.sourceType === 'liuyao' && mainTitle.includes(' 变 ')) {
    const parts = mainTitle.split(' 变 ');
    mainTitle = parts[0];
    changedTitle = parts.slice(1).join(' 变 ');
  }

  if ((conv.sourceType === 'bazi_personality' || conv.sourceType === 'bazi_wuxing') && mainTitle.includes(' - ')) {
    const parts = mainTitle.split(' - ');
    subTitle = parts[0];
    mainTitle = parts.slice(1).join(' - ');
  }

  if (conv.sourceType === 'hepan' && mainTitle.includes(' - ')) {
    const parts = mainTitle.split(' - ');
    subTitle = parts[0];
    mainTitle = parts.slice(1).join(' - ');
  }

  if ((conv.sourceType === 'palm' || conv.sourceType === 'face') && mainTitle.includes(' - ')) {
    mainTitle = mainTitle.split(' - ').slice(1).join(' - ');
  }

  return {
    mainTitle,
    subTitle,
    changedTitle,
  };
}

export function formatConversationMenuTitle(conv: ConversationListItem) {
  const { mainTitle, changedTitle } = getConversationDisplayParts(conv);
  return changedTitle ? `${mainTitle} 变 ${changedTitle}` : mainTitle;
}

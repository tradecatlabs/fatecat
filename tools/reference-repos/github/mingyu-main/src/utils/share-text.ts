export async function shareText(text: string): Promise<boolean> {
  if (navigator.share) {
    await navigator.share({ text });
    return true;
  }

  return false;
}

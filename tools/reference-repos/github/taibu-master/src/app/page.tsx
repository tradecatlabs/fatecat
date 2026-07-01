/**
 * 根页面
 *
 * 默认进入八字页面。
 */

import { redirect } from 'next/navigation';

export default async function HomePage() {
    redirect('/bazi');
}

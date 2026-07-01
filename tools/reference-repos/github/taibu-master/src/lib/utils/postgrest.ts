/**
 * PostgREST 字符串转义工具
 *
 * 用于 .or() / .ilike() 等 PostgREST 过滤器中的字符串值，
 * 防止特殊字符（NUL、反斜杠、双引号）导致查询注入或语法错误。
 */
export function quotePostgrestString(value: string): string {
  const sanitized = value
    .replace(/\u0000/g, '')
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"');
  return `"${sanitized}"`;
}

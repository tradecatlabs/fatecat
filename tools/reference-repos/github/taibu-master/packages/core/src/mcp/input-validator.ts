import type { ToolInputSchema, ToolSchema } from './contract.js';

const TRANSPORT_FIELDS = new Set(['detailLevel', 'seedScope']);

type ValidationIssue = {
  path: string;
  message: string;
};

function getValueType(value: unknown): string {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  return typeof value;
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function matchesType(value: unknown, expected: ToolSchema['type']): boolean {
  switch (expected) {
    case 'string':
      return typeof value === 'string';
    case 'number':
      return typeof value === 'number' && Number.isFinite(value);
    case 'boolean':
      return typeof value === 'boolean';
    case 'array':
      return Array.isArray(value);
    case 'object':
      return isPlainObject(value);
    default:
      return true;
  }
}

function joinPath(base: string, key: string | number): string {
  if (typeof key === 'number') {
    return `${base}[${key}]`;
  }
  return base ? `${base}.${key}` : key;
}

function formatPath(path: string): string {
  return path ? `'${path}'` : '输入';
}

function describeBranch(schema: ToolSchema): string {
  const constraints = Object.entries(schema.properties || {})
    .flatMap(([key, value]) => (value && 'const' in value && value.const !== undefined ? [`${key}=${String(value.const)}`] : []));
  const required = (schema.required || []).filter((field) => !TRANSPORT_FIELDS.has(field));

  if (constraints.length > 0 && required.length > 0) {
    return `${constraints.join('，')} 时需提供 ${required.join('、')}`;
  }
  if (constraints.length > 0) {
    return constraints.join('，');
  }
  if (required.length > 0) {
    return required.join('、');
  }
  return '满足对应字段组合';
}

function validateSchema(
  value: unknown,
  schema: ToolSchema | undefined,
  path: string,
  issues: ValidationIssue[],
  atRoot = false,
): void {
  if (!schema) return;

  if (schema.const !== undefined && value !== schema.const) {
    issues.push({ path, message: `${formatPath(path)} 必须为 ${String(schema.const)}` });
    return;
  }

  if (schema.enum && !schema.enum.includes(value)) {
    issues.push({
      path,
      message: `${formatPath(path)} 的值 '${String(value)}' 不在允许范围 [${schema.enum.join(', ')}] 内`,
    });
    return;
  }

  if (schema.type && !matchesType(value, schema.type)) {
    issues.push({
      path,
      message: `${formatPath(path)} 应为 ${schema.type} 类型，实际为 ${getValueType(value)}`,
    });
    return;
  }

  if (typeof value === 'string') {
    if (schema.minLength != null && value.length < schema.minLength) {
      issues.push({ path, message: `${formatPath(path)} 不能为空` });
    }
    if (schema.maxLength != null && value.length > schema.maxLength) {
      issues.push({ path, message: `${formatPath(path)} 长度不能超过 ${schema.maxLength}` });
    }
  }

  if (Array.isArray(value)) {
    if (schema.minItems != null && value.length < schema.minItems) {
      issues.push({ path, message: `${formatPath(path)} 至少需要 ${schema.minItems} 项` });
    }
    if (schema.maxItems != null && value.length > schema.maxItems) {
      issues.push({ path, message: `${formatPath(path)} 最多允许 ${schema.maxItems} 项` });
    }
    if (schema.items) {
      value.forEach((item, index) => validateSchema(item, schema.items, joinPath(path, index), issues));
    }
  }

  if (isPlainObject(value)) {
    for (const field of schema.required || []) {
      if (atRoot && TRANSPORT_FIELDS.has(field)) continue;
      if (!(field in value) || value[field] === undefined) {
        issues.push({ path: joinPath(path, field), message: `缺少必填参数 '${joinPath(path, field)}'` });
      }
    }

    for (const [field, fieldSchema] of Object.entries(schema.properties || {})) {
      if (atRoot && TRANSPORT_FIELDS.has(field)) continue;
      if (!(field in value) || value[field] === undefined) continue;
      validateSchema(value[field], fieldSchema, joinPath(path, field), issues);
    }
  }

  for (const branch of schema.allOf || []) {
    validateSchema(value, branch, path, issues, atRoot);
  }

  const condition = schema.if ? matchesSchema(value, schema.if) : undefined;
  if (condition === true && schema.then) {
    validateSchema(value, schema.then, path, issues, atRoot);
  } else if (condition === false && schema.else) {
    validateSchema(value, schema.else, path, issues, atRoot);
  }

  if (schema.anyOf?.length) {
    const matched = schema.anyOf.some((branch) => matchesSchema(value, branch));
    if (!matched) {
      issues.push({
        path,
        message: `${formatPath(path)} 需满足以下任一条件：${schema.anyOf.map(describeBranch).join('；')}`,
      });
    }
  }

  if (schema.oneOf?.length) {
    const matchCount = schema.oneOf.filter((branch) => matchesSchema(value, branch)).length;
    if (matchCount !== 1) {
      issues.push({
        path,
        message: `${formatPath(path)} 需且仅需满足以下条件之一：${schema.oneOf.map(describeBranch).join('；')}`,
      });
    }
  }
}

function matchesSchema(value: unknown, schema: ToolSchema): boolean {
  const issues: ValidationIssue[] = [];
  validateSchema(value, schema, '', issues);
  return issues.length === 0;
}

export function validateInput(args: unknown, schema: ToolInputSchema): void {
  if (!isPlainObject(args)) {
    throw new Error('参数校验失败: 输入必须是一个对象');
  }

  const issues: ValidationIssue[] = [];
  validateSchema(args, schema, '', issues, true);

  if (issues.length > 0) {
    const message = issues.map((issue) => issue.message).join('；');
    throw new Error(`参数校验失败: ${message}`);
  }
}

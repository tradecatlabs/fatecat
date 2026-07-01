import type { ScopeType } from '../../types/analysis';

export type PromptContext = {
  report_key: string;
  report_title: string;
  report_type: string;
  selected_topic: string;
  scope_type: ScopeType;
  scope_label: string;
  palace_name?: string;
  focus_notes: string[];
};

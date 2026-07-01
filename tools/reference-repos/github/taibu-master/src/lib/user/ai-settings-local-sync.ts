import {
  persistLocalVisualizationSettings,
  type VisualizationPreferenceLocalInput,
} from '@/lib/visualization/settings';

/**
 * After a successful settings save, sync visualization preferences to localStorage.
 * Returns true if sync succeeded (i.e. the save itself was truthy), false otherwise.
 */
export function syncVisualizationPreferencesAfterSave(
  storage: Pick<Storage, 'setItem'>,
  input: VisualizationPreferenceLocalInput,
  savedSettings: unknown,
) {
  if (!savedSettings) {
    return false;
  }

  persistLocalVisualizationSettings(storage, input);
  return true;
}

import type { OptionLabel } from "../data/types";

export const PROGRESS_STORAGE_KEY = "ipas-quiz:progress:v1";

export type StoredAnswer = {
  selected: OptionLabel;
  correct: boolean;
  answeredAt: string;
};

export type Progress = Record<string, StoredAnswer>;

export function loadProgress(): Progress {
  if (typeof window === "undefined") return {};
  try {
    const value = window.localStorage.getItem(PROGRESS_STORAGE_KEY);
    if (!value) return {};
    const parsed = JSON.parse(value);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

export function saveProgress(progress: Progress) {
  window.localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progress));
}

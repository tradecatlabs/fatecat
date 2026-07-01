export interface SsgwSign {
  id: number;
  title: string;
  qianwen: string;
  story: string;
  details: {
    [key: string]: string;
  };
}

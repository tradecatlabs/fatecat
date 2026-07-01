type PageTopbarProps = {
  title: string;
  onBack: () => void;
  wide?: boolean;
};

export function PageTopbar(props: PageTopbarProps) {
  const { title, onBack, wide = false } = props;

  return (
    <div className={`page-topbar${wide ? ' page-topbar-wide' : ''}`}>
      <button type="button" className="page-topbar-back" onClick={onBack}>
        返回
      </button>
      <h1 className="page-topbar-title">{title}</h1>
    </div>
  );
}

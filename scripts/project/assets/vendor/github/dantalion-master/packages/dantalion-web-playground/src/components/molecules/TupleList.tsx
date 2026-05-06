import type { ReactNode, VFC } from 'react';
import List, { Props as ListProps } from '../atoms/List';

/** Type definition of the required attributes. */
export interface Props extends Omit<ListProps, 'children'> {
  /** The children items. */
  readonly children?: readonly (readonly [ReactNode, ReactNode])[];
}

/** The generic list component which its items allow the Markdown format. */
const TupleList: VFC<Props> = ({ children, ...props }) => (
  // eslint-disable-next-line react/jsx-props-no-spreading
  <List {...props}>
    {children?.map(([caption, content], index) => (
      // eslint-disable-next-line react/no-array-index-key
      <section className="text-xl" key={index}>
        <h2 className="inline font-extrabold">{caption}</h2>
        <p className="inline ml-3">{content}</p>
      </section>
    ))}
  </List>
);
TupleList.displayName = 'TupleList';

export default TupleList;

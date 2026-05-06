import type { ResourceLanguage, TFunction, WithT } from 'i18next';
import type {
  Brain,
  Communication,
  Genius,
  LifeBase,
  Management,
  Motivation,
  Position,
  Potential,
  Response,
  Vector,
} from '@kurone-kito/dantalion-core';
import createGenericAccessor, { DetailAccessor } from './createGenericAccessor';
import createTAsync from './createTAsync';
import type {
  DesctiptionsType,
  DetailsBaseType,
  DetailsType,
  PersonalityDetailType,
  PersonalityType,
  VectorType,
} from './types';

/** The type definition of the concreted accessors collection */
export interface Accessors {
  /**
   * The instance provides a set of functions that retrieve
   * human-readable resources related to the thought method.
   */
  readonly brain: DetailAccessor<DetailsType, Brain>;

  /**
   * The instance provides a set of functions that retrieve
   * human-readable resources related to dialogue policy.
   */
  readonly communication: DetailAccessor<DetailsType, Communication>;

  /**
   * The instance provides a set of functions that retrieve
   * human-readable resources related to natural personality.
   */
  readonly genius: DetailAccessor<
    PersonalityType,
    Genius,
    PersonalityDetailType
  >;

  /** Get the resources of the descriptions heading. */
  readonly getDescription: (
    /** The genius type or birthday */
    type?: string
  ) => DesctiptionsType;

  /**
   * The instance provides a set of functions that retrieve
   * human-readable resources related to the base of ego type.
   */
  readonly lifeBase: DetailAccessor<
    DetailsBaseType<string[]>,
    LifeBase,
    string
  >;

  /**
   * The instance provides a set of functions that retrieve human-readable
   * resources related to risk and return thinking in specific people.
   */
  readonly management: DetailAccessor<DetailsType, Management>;

  /**
   * The instance provides a set of functions that retrieve human-readable
   * resources related to an environment that is easy to get motivated.
   */
  readonly motivation: DetailAccessor<string, Motivation, string>;

  /**
   * The instance provides a set of functions that retrieve
   * human-readable resources related to a talented role.
   */
  readonly position: DetailAccessor<DetailsType, Position>;

  /**
   * The instance provides functions that retrieve human-readable
   * resources related to that can exert when taking action.
   */
  readonly potential: DetailAccessor<
    readonly string[],
    readonly [Potential, Potential]
  >;

  /**
   * The instance provides a set of functions that retrieve
   * human-readable resources related to on-site or behind.
   */
  readonly response: DetailAccessor<DetailsType, Response>;

  /**
   * The instance provides a set of functions that retrieve human-readable
   * resources related to the major classification of personality.
   */
  readonly vector: DetailAccessor<VectorType, Vector>;
}

/**
 * Create the concreted accessors collection from the i18next instance
 * @param t Specify the i18next instance
 * @returns The instance of the concreted accessors collection
 */
export const createAccessors = (t: TFunction): Accessors => {
  const { tCategoryStringedDetail, tDetail, tObj, tStringedDetail } =
    createGenericAccessor(t);
  const potentialsDetail = tDetail<readonly string[]>('potentials');
  return {
    brain: tDetail('brain'),
    communication: tDetail('communication'),
    genius: tDetail('genius'),
    getDescription: (type) => tObj('descriptions', { type }),
    lifeBase: tCategoryStringedDetail('lifeBase'),
    management: tDetail('management'),
    motivation: tStringedDetail('motivation'),
    position: tDetail('position'),
    potential: {
      getByKey: (p) => potentialsDetail.getByKey([...p].sort().join('.')),
      getCategoryDetail: potentialsDetail.getCategoryDetail,
    },
    response: tDetail('response'),
    vector: tDetail('vector'),
  };
};

/**
 * Create the concreted accessors collection asynchronously
 *
 * It is a synonym function that combines
 * `createAccessors()` and `createTAsync()`.
 * @param lng The language.
 *
 * If omitted, the language used is detected from the current environment.
 * @param additions The additional resources.
 * @returns The instance of the concreted accessors collection asynchronously
 * @see useLocale()
 */
export default async (
  lng?: string,
  additions?: ResourceLanguage
): Promise<Accessors & WithT> => {
  const t = await createTAsync({ lng, additions });
  return { ...createAccessors(t), t };
};

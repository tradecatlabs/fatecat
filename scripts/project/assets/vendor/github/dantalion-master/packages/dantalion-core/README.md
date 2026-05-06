<!-- markdownlint-disable MD024 -->

# 🦁 Dantalion: Core library

[![npm version](https://badge.fury.io/js/%40kurone-kito%2Fdantalion-core.svg)](https://badge.fury.io/js/%40kurone-kito%2Fdantalion-core)
[![lerna](https://img.shields.io/badge/maintained%20with-lerna-cc00ff.svg)](https://lerna.js.org/)

“Dantalion” is the seventy-first demon in the demonological grimoire,
_[the Lesser Key of Solomon](https://en.wikipedia.org/wiki/The_Lesser_Key_of_Solomon)_.
He teaches all kinds of academic knowledge, but he can also read and
manipulate others’ hearts.

If you can predict the other person’s character, you can increase the
possibility of controlling the other person’s will. This package provides
a function that infers the personality details from the specified birthday.
By using this package, you can quickly implement birthday divination in
your Node.js apps. Its calculation is using the method of
_Four Pillars of Destiny (Ba-Zi)_.

## Note

- OS independent and dependent free.
- This package can specify a birthday within the range from February 1,
  1873, to December 31, 2050.
- This package does not consider time zones. If you are not satisfied with
  the inferred personality, moving the date back and forth may solve.

## Usage

Require: Node.js >= v12

### Add to dependency

```sh
npm install -S @kurone-kito/dantalion-core
```

### Get the personality

```js
const { getPersonality } = require('@kurone-kito/dantalion-core');

console.log(getPersonality('1993-10-09'));
```

#### Result

In strictly, The function gets the raw object, not the JSON.

```json
{
  "cycle": 10,
  "inner": "555",
  "lifeBase": "application",
  "outer": "789",
  "potential": ["Io", "Ii"],
  "workStyle": "125"
}
```

### Get detailed information on personality

```js
const { getDetail } = require('@kurone-kito/dantalion-core');

console.log(getDetail('555'));
```

#### Result

In strictly, The function gets the raw object, not the JSON.

```json
{
  "affinity": {
    "biz": {
      "100": 0,
      "108": 3,
      "125": 2,
      "555": 3,
      "789": 1,
      "888": 2,
      "919": 1,
      "000": 0,
      "001": 2,
      "012": 2,
      "024": 0,
      "025": 0
    },
    "love": {
      "100": 0,
      "108": 0,
      "125": 3,
      "555": 2,
      "789": 2,
      "888": 2,
      "919": 0,
      "000": 2,
      "001": 2,
      "012": 3,
      "024": 0,
      "025": 2
    }
  },
  "brain": "left",
  "communication": "fix",
  "management": "hope",
  "motivation": "skillUp",
  "position": "quick",
  "response": "action",
  "vector": "economically"
}
```

### Get all types

All types list.

```js
const { types } = require('@kurone-kito/dantalion-core');

console.log(types); // AllTypes Object
```

#### `AllTypes`

```ts
/** All types list. */
export interface AllTypes {
  readonly brain: readonly Brain[];
  readonly communication: readonly Communication[];
  readonly genius: readonly Genius[];
  readonly lifeBase: readonly LifeBase[];
  readonly lifeBaseCC: Record<LifeBase, string>;
  readonly management: readonly Management[];
  readonly motivation: readonly Motivation[];
  readonly position: readonly Position[];
  readonly potential: readonly Potential[];
  readonly potentialCC: Record<Potential, string>;
  readonly response: readonly Response[];
  readonly vector: readonly Vector[];
}
```

| Property        | Type                       | Description                                                   |
| :-------------- | :------------------------- | :------------------------------------------------------------ |
| `brain`         | `readonly Brain[]`         | The list that the types of thought methods.                   |
| `communication` | `readonly Communication[]` | The list that the types of dialogue policy.                   |
| `genius`        | `readonly Genius[]`        | The list of personality types.                                |
| `lifeBase`      | `readonly LifeBase[]`      | The list that the base of ego type.                           |
| `lifeBaseCC`    | `Record<LifeBase, string>` | The list that the base of ego type.                           |
| `management`    | `readonly Management[]`    | The list of the types that the risk management method.        |
| `motivation`    | `readonly Motivation[]`    | The list of the types that easy to the motivated environment. |
| `position`      | `readonly Position[]`      | The list of role types                                        |
| `potential`     | `readonly Potential[]`     | The list of the types that the potential.                     |
| `response`      | `readonly Response[]`      | The list of the types that the role.                          |
| `vector`        | `readonly Vector[]`        | The list of personality types.                                |

## API

### `getDetail`

```ts
type getDetail = (genius: Genius) => Detail | undefined;
```

#### Parameters

- `genius`: The types of personality.

#### Returns

Detailed information on the personality. If the param is invalid, it will be `undefined`.

### `getPersonality`

Get the personality information corresponding to the specified birthday.

```ts
type getPersonality = (
  birth: string | number | Date
) => Personality | undefined;
```

#### Parameters

- `birth`: Specify a birthday within the range from February 1, 1873,
  to December 31, 2050.
  Ignore the _time_ information.

#### Returns

The object that the personality information. If the date is over the range,
it will be `undefined`.

### `toCC`

```ts
type toCC = (personality: Personality) => string;
```

#### Parameters

- `personality`: Specify the personality object.

#### Returns

The CC string.

## Types (for TypeScript)

### `Affinity`

The lists of affinity by genius type.

```ts
interface Affinity {
  biz: Record<Genius, AffinityLevel>;
  love: Record<Genius, AffinityLevel>;
}
```

| Property | Type                            | Description   |
| :------- | :------------------------------ | :------------ |
| `biz`    | `Record<Genius, AffinityLevel>` | for business. |
| `love`   | `Record<Genius, AffinityLevel>` | for romance.  |

### `AffinityLevel`

Affinity level.

```ts
type AffinityLevel = 0 | 1 | 2 | 3;
```

| Key | Value        |
| :-: | :----------- |
| `0` | Hmm :/       |
| `1` | Good.        |
| `2` | Great!       |
| `3` | Fantastic!!! |

### `Brain`

The types of thought method.

```ts
type Brain = 'left' | 'right';
```

|   Key   | Value                                             |
| :-----: | :------------------------------------------------ |
| `left`  | Left brain type. Logical thinking is superior.    |
| `right` | Right brain type. Intuitive thinking is superior. |

### `Communication`

The types of dialogue policy.

```ts
type Communication = 'fix' | 'flex';
```

|  Key   | Value                                                             |
| :----: | :---------------------------------------------------------------- |
| `fix`  | This type of person would like to find a way from the conclusion. |
| `flex` | This type of person would like to express conclude fluidly.       |

### `Detail`

The detail for genius type.

```ts
interface Detail {
  affinity: Affinity;
  brain: Brain;
  communication: Communication;
  management: Management;
  motivation: Motivation;
  position: Position;
  response: Response;
  vector: Vector;
}
```

| Property        | Type            | Description                                     |
| :-------------- | :-------------- | :---------------------------------------------- |
| `affinity`      | `Affinity`      | The lists of affinity by genius type.           |
| `brain`         | `Brain`         | The types of thought method.                    |
| `communication` | `Communication` | The types of dialogue policy.                   |
| `management`    | `Management`    | The types that the risk management method.      |
| `motivation`    | `Motivation`    | The types of easy to the motivated environment. |
| `position`      | `Position`      | The types for role.                             |
| `response`      | `Response`      | The types for role.                             |
| `vector`        | `Vector`        | Vector of genius type.                          |

### `Genius`

The types of personality.

```ts
type Genius =
  | '000'
  | '001'
  | '012'
  | '024'
  | '025'
  | '100'
  | '108'
  | '125'
  | '555'
  | '789'
  | '888'
  | '919';
```

|  Key  | Value                                                                                   |
| :---: | :-------------------------------------------------------------------------------------- |
| `000` | This type of person would like to be freedom. And also, They have a good imagination.   |
| `001` | This type of person would like to do something different from others with their ideas.  |
| `012` | This type of person will like new somethings. They also value discussions, especially.  |
| `024` | This type of person is good at turning anxiety into action. They have a strong memory.  |
| `025` | This type of person has a strong camaraderie. And also, they have a lot of friends.     |
| `100` | This type of person is serious and perfectionist. They expose weak point when praised.  |
| `108` | This type of person is shy and honest. And they have a strong sense of responsibility.  |
| `125` | This type of person can accept temporary abstinence to fulfill their long-term goals.   |
| `555` | This type of person is quick to learn and can do anything. Also, they are dignified.    |
| `789` | This type of person value experience and achievement. Also, they prefer to be quiet.    |
| `888` | This type of person value the spirit of challenge and are interested in various things. |
| `919` | This type of person has the quick situational judgment and also is good at bargaining.  |

### `LifeBase`

The types that the base of ego.

```ts
type LifeBase =
  | 'application'
  | 'association'
  | 'development'
  | 'expression'
  | 'finance'
  | 'investment'
  | 'organization'
  | 'quest'
  | 'selfMind'
  | 'selfReliance';
```

| Key            | CC  | Value                                                                    |
| :------------- | :-- | :----------------------------------------------------------------------- |
| `application`  | _G_ | This type of person would like to self-experience seriously.             |
| `association`  | _I_ | This type of person would like to do it immediately when they think.     |
| `development`  | _D_ | This type of person would like to be perfectionists.                     |
| `expression`   | _C_ | This type of person would like to be honest with themselves.             |
| `finance`      | _E_ | This type of person would like to put everything within eye reach.       |
| `investment`   | _F_ | This type of person would like to be a down-to-earth collector.          |
| `organization` | _H_ | This type of person would like to live as a member of a group.           |
| `quest`        | _J_ | This type of person would like to learn from the wisdom of our pioneers. |
| `selfMind`     | _B_ | This type of person would like to be a leader of the team.               |
| `selfReliance` | _A_ | This type of person would like to be a lone wolf.                        |

### `Management`

The types that the risk management method.

```ts
type Management = 'care' | 'hope';
```

| Key    | Value                                                                                       |
| :----- | :------------------------------------------------------------------------------------------ |
| `care` | This type of person has a good intuition for risk but weak for chance perception.           |
| `hope` | This type of person has a good intuition for great opportunities, but weak risk perception. |

### `Motivation`

The types of easy to the motivated environment.

```ts
type Motivation =
  | 'competition'
  | 'ownMind'
  | 'power'
  | 'safety'
  | 'skillUp'
  | 'status';
```

| Key           | Value                                                            |
| :------------ | :--------------------------------------------------------------- |
| `competition` | The environment that can be compared with other peoples.         |
| `ownMind`     | The environment that they can do on their plan.                  |
| `power`       | The environment that they can do as soon as they think about it. |
| `safety`      | The environment that they can pursue security and peace.         |
| `skillUp`     | The environment that daily improvement can be felt.              |
| `status`      | The environment that they can be different from others.          |

### `Personality`

The details for Personality.

```ts
interface Personality {
  cycle: number;
  inner: Genius;
  lifeBase: LifeBase;
  outer: Genius;
  potentials: [Potential, Potential];
  workStyle: Genius;
}
```

| Property     | Type                     | Description                  |
| :----------- | :----------------------- | :--------------------------- |
| `cycle`      | `number`                 | The sub-personality (cycle). |
| `inner`      | `Genius`                 | The inner personality.       |
| `lifeBase`   | `LifeBase`               | The life base.               |
| `outer`      | `Genius`                 | The outer personality.       |
| `potentials` | `[Potential, Potential]` | The potential.               |
| `workStyle`  | `Genius`                 | The personality at working.  |

### `Position`

The types for role.

```ts
type Position = 'adjust' | 'brain' | 'direct' | 'quick';
```

| Key      | Value                                                        |
| :------- | :----------------------------------------------------------- |
| `adjust` | This type of person can solve interpersonal problems.        |
| `brain`  | This type of person can create interesting ideas.            |
| `direct` | This type of person has all abilities little by little.      |
| `quick`  | This type of person has a lot of energy, like a salesperson. |

### `Potential`

The potential type definition that can exert when taking action.

```ts
type Potential =
  | 'Ci'
  | 'Co'
  | 'Ei'
  | 'Eo'
  | 'Fi'
  | 'Fo'
  | 'Ii'
  | 'Io'
  | 'Ni'
  | 'No';
```

| key  | CC  | Value                                                                                        |
| :--- | :-- | :------------------------------------------------------------------------------------------- |
| `Ci` | _j_ | This type of person is good at sublimating existing works with respect.                      |
| `Co` | _i_ | This type of person is skilled at exploring one thing. They also tend to an originator.      |
| `Ei` | _d_ | This type of person is good at non-verbal and passive expression.                            |
| `Eo` | _c_ | This type of person is skilled at active expression through words.                           |
| `Fi` | _f_ | This type of person is relatively cautious and can see the meaning behind the numbers.       |
| `Fo` | _e_ | This type of person is good at using numbers and other evidence-based expressions.           |
| `Ii` | _b_ | This type of person is a good listener and can draw out the other person's point.            |
| `Io` | _a_ | This type of person is good at active and aggressive communication.                          |
| `Ni` | _h_ | This type of person has fine self-management skills and is good at maintaining organization. |
| `No` | _g_ | This type of person is very caring and good at developing organizations.                     |

### `Response`

The types for role.

```ts
type Response = 'action' | 'mind';
```

| Key      | Value                                                                 |
| :------- | :-------------------------------------------------------------------- |
| `action` | This type of person would like to always act with customers.          |
| `mind`   | This type of person would like to always act with only known peoples. |

### `Vector`

Personality types.

```ts
type Vector = 'authority' | 'economically' | 'humanely';
```

| Key            | Value                                                                  |
| :------------- | :--------------------------------------------------------------------- |
| `authority`    | This type of person would like to do the action for self-authority.    |
| `economically` | This type of person would like to do the action to build their wealth. |
| `humanely`     | This type of person would like to do the action for self-virtue.       |

## License

MIT

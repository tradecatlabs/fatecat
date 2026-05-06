<!-- markdownlint-disable MD024 -->

# 🦁 Dantalion: i18n resources library

[![npm version](https://badge.fury.io/js/%40kurone-kito%2Fdantalion-i18n.svg)](https://badge.fury.io/js/%40kurone-kito%2Fdantalion-i18n)
[![lerna](https://img.shields.io/badge/maintained%20with-lerna-cc00ff.svg)](https://lerna.js.org/)

This package provides a function that infers the personality details
from the specified birthday. By using this package, you can quickly
implement birthday divination in your Node.js apps. Its calculation
is using the method of _Four Pillars of Destiny (Ba-Zi)_.

This package is a library that obtains human-readable (Markdown format)
details for the output of the `@kurone-kito/dantalion-core` package.

This library uses the Intl API to determine the language and outputs
it in the appropriate language. It's only in Japanese and partly English
yet, but we'll gradually support multiple languages.

## Usage

Require: Node.js >= v12.1

### Add to dependency

```sh
npm install -S @kurone-kito/dantalion-core @kurone-kito/dantalion-i18n
```

### Get the details of the personality

```js
const { getPersonality } = require('@kurone-kito/dantalion-core');
const { genius } = require('@kurone-kito/dantalion-i18n');

const personality = getPersonality('1993-10-09');
console.log(personality.inner); // === '555'

const result = genius.getValue(personality.inner);

console.log(JSON.stringify(result));
```

#### Result

In strictly, The function gets the raw object, not the JSON.
Since it's a long sentence, it omitted some parts.

```json
{
  "name": "Easygoing type",
  "summary": "Balanced, capable and caring, a heroic position.",
  "detail": [
    "Many people have an air of all-around competence and boss authority, like an executive employee.",
    :
    :
  ],
  "weak": [
    "They don't like to apologize even when it is their fault. Even if they have apologetic, they are not very good at expressing it."
    :
    :
  ],
  "strategy": [
    "They can do everything on their own, so they tend to take care of everything on their own. When you entrust them with something, be careful not to let them do too much."
  ]
}
```

## API

### `createAccessors(t: i18next.TFunction): Accessors`

Create the concreted accessors collection from the i18next instance

#### Arguments

| Name | Type                                                          | Defaults     | Description                  |
| :--- | :------------------------------------------------------------ | :----------- | :--------------------------- |
| `t`  | [`i18next.TFunction`](https://www.i18next.com/overview/api#t) | _(Required)_ | Specify the i18next instance |

#### Returns

[`Accessors`](#accessors): The instance of the concreted accessors collection

### `createAccessorsAsync(lng?: string, additions?: i18next.ResourceLanguage): Promise<Accessors & i18next.WithT>`

Create the concreted accessors collection asynchronously

It is a synonym function that combines
[`createAccessors()`](#createaccessorst-i18nexttfunction-accessors) and
[`createTAsync()`](#createtasyncoptions-createtasyncoptions-promisei18nexttfunction).

#### Arguments

| Name        | Type                        | Defaults    | Description                                  |
| :---------- | :-------------------------- | :---------- | :------------------------------------------- |
| `lng`       | `string?`                   | (\*)        | The language to use                          |
| `additions` | `i18next.ResourceLanguage?` | `undefined` | Specify the additional resources if you need |

(\*: If omitted, the language used is detected from the current environment.
See: [useLocale()](#getlocale-string--undefined))

#### Returns

[`Promise<Accessors & i18next.WithT>`](#accessors):
The instance of the concreted accessors collection

### `createTAsync(options?: CreateTAsyncOptions): Promise<i18next.TFunction>`

Create and initialize the i18next instance asynchronously

#### Arguments

| Name      | Type                                           | Defaults | Description |
| :-------- | :--------------------------------------------- | :------- | :---------- |
| `options` | [`CreateTAsyncOptions?`](#createtasyncoptions) | `{}`     | The options |

#### Returns

[`Promise<i18next.TFunction>`](https://www.i18next.com/overview/api#t):
The i18next instance which already initialized the resources.

### `fallbackLanguage: 'en'`

The language that uses as a fallback.

### `getDetailMarkdown(accessors: Accessors, genius?: Genius): string`

Get the personality information.

#### Arguments

| Name        | Type                                  | Defaults     | Description                           |
| :---------- | :------------------------------------ | :----------- | :------------------------------------ |
| `accessors` | [`Accessors`](#accessors)             | _(Required)_ | The accessors instance for resources. |
| `genius`    | [`Genius?`](../dantalion-core#genius) | `undefined`  | The types of personality.             |

#### Returns

`string`:
The string that the personality information as the Markdown format.

If you specified the `undefined` value as an argument or omitted it,
it would be a list of the available types.

### `getLocale(): string | undefined`

Get the locale information from the Intl API.

#### Arguments

(None)

#### Returns

`string`: The locale string e.g. `en-US`.

### `getPersonalityMarkdown(accessors: Accessors, birth: string | number | Date): string`

Get the personality information corresponding to the specified birthday.

#### Arguments

| Name     | Type                       | Defaults     | Description                                                                                                     |
| :------- | :------------------------- | :----------- | :-------------------------------------------------------------------------------------------------------------- |
| `genius` | [`Accessors`](#accessors)  | _(Required)_ | The accessors instance for resources.                                                                           |
| `birth`  | `string \| number \| Date` | _(Required)_ | Specify a birthday within the range from February 1, 1873, to December 31, 2050. Ignore the _time_ information. |

#### Returns

`string`:
The string that the personality information as the Markdown format.
If the date is over the range, it will be error message.

### `locales: Record<string, string>`

The locales table.

The property keys have ISO 639-1 string and values exact name.

## Type definitions (for TypeScript)

The strings contained in the object are in Markdown format. In the
case of an array of strings, the elements separate for each paragraph.

### `Accessors`

The type definition of the concreted accessors collection

```ts
interface Accessors {
  readonly brain: DetailAccessor<DetailsType, Brain>;
  readonly communication: DetailAccessor<DetailsType, Communication>;
  readonly genius: DetailAccessor<
    PersonalityType,
    Genius,
    PersonalityDetailType
  >;
  readonly lifeBase: DetailAccessor<
    DetailsBaseType<string[]>,
    LifeBase,
    string
  >;
  readonly management: DetailAccessor<DetailsType, Management>;
  readonly motivation: DetailAccessor<string, Motivation, string>;
  readonly position: DetailAccessor<DetailsType, Position>;
  readonly potential?: DetailAccessor<
    readonly string[],
    readonly [Potential, Potential]
  >;
  readonly response: DetailAccessor<DetailsType, Response>;
  readonly vector: DetailAccessor<VectorType, Vector>;
  getDescription(type?: string): DesctiptionsType;
}
```

| Property        | Type                                                                 | Description                                                                                                                                 |
| :-------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `brain`         | `DetailAccessor<DetailsType, Brain>`                                 | The instance provides a set of functions that retrieve human-readable resources related to the thought method.                              |
| `communication` | `DetailAccessor<DetailsType, Communication>`                         | The instance provides a set of functions that retrieve human-readable resources related to dialogue policy.                                 |
| `genius`        | `DetailAccessor<PersonalityType, Genius, PersonalityDetailType>`     | The instance provides a set of functions that retrieve human-readable resources related to natural personality.                             |
| `lifeBase`      | `DetailAccessor<DetailsBaseType<string[]>, LifeBase, string>`        | The instance provides a set of functions that retrieve human-readable resources related to the base of ego type.                            |
| `management`    | `DetailAccessor<DetailsType, Management>`                            | The instance provides a set of functions that retrieve human-readable resources related to risk and return thinking in specific people.     |
| `motivation`    | `DetailAccessor<string, Motivation, string>`                         | The instance provides a set of functions that retrieve human-readable resources related to to an environment that is easy to get motivated. |
| `position`      | `DetailAccessor<DetailsType, Position>`                              | The instance provides a set of functions that retrieve human-readable resources related to a talented role.                                 |
| `potential`     | `DetailAccessor<readonly string[], readonly [Potential, Potential]>` | The instance provides functions that retrieve human-readable resources related to that can exert when taking action.                        |
| `response`      | `DetailAccessor<DetailsType, Response>`                              | The instance provides a set of functions that retrieve human-readable resources related to on-site or behind.                               |
| `vector`        | `DetailAccessor<VectorType, Vector>`                                 | The instance provides a set of functions that retrieve human-readable resources related to the major classification of personality.         |

| Method definition                                 | Description                                    |
| :------------------------------------------------ | :--------------------------------------------- |
| `getDescription(type?: string): DesctiptionsType` | Get the resources of the descriptions heading. |

### `CreateTAsyncOptions`

The type definition that the options of the createTAsync function.

```ts
interface CreateTAsyncOptions {
  readonly additions?: i18next.ResourceLanguage;
  readonly lng?: string;
  readonly use?:
    | i18next.Module
    | i18next.Newable<i18next.Module>
    | i18next.ThirdPartyModule[]
    | i18next.Newable<i18next.ThirdPartyModule>[];
}
```

| Property    | Type                                    | Description                                                                                  |
| :---------- | :-------------------------------------- | :------------------------------------------------------------------------------------------- |
| `additions` | `i18next.ResourceLanguage \| undefined` | Specify the additional resources if you need                                                 |
| `lng`       | `string \| undefined`                   | The language to use. If omitted, the language used is detected from the current environment. |
| `use`       | _(\*)_                                  | The use function is there to load additional plugins to i18next.                             |

(\*: See the type definition as it is long :/)

### `DesctiptionsType`

The type definition that the resources of description.

```ts
interface DesctiptionsType {
  readonly cc: string;
  readonly detail: string;
  readonly details: string;
  readonly genius1: string;
  readonly genius2: string;
  readonly invalid: string;
  readonly personality: string;
  readonly strategy: string;
  readonly weak: string;
}
```

| Property      | Type     | Description                                        |
| :------------ | :------- | :------------------------------------------------- |
| `cc`          | `string` | The title of personality code.                     |
| `detail`      | `string` | The title of the detail.                           |
| `details`     | `string` | The title of the details list.                     |
| `genius1`     | `string` | The detail of the genius.                          |
| `genius2`     | `string` | The detail of the genius.                          |
| `invalid`     | `string` | The error message when specified invalid birthday. |
| `personality` | `string` | The title of personality.                          |
| `strategy`    | `string` | The strategy.                                      |
| `weak`        | `string` | The weak points.                                   |

### `DetailAccessor<T, K, D>`

The type definition with a function to
access a resource of the specific category.

```ts
interface DetailAccessor<
  T extends i18next.TFunctionResult,
  K,
  D extends DetailsBaseType | string = DetailsBaseType
> {
  getByKey(key: K): T;
  getCategoryDetail(): D;
}
```

| Type | Constraint                  | Description                                                |
| :--- | :-------------------------- | :--------------------------------------------------------- |
| `T`  | `i18next.TFunctionResult`   | The type of resource as a return value.                    |
| `K`  | _(none)_                    | The type for the resource key.                             |
| `D`  | `DetailsBaseType \| string` | The type of resource as a return value of category detail. |

| Method definition        | Description                                                                |
| :----------------------- | :------------------------------------------------------------------------- |
| `getByKey(key: K): T`    | The function acquires the resource corresponding to the key.               |
| `getCategoryDetail(): D` | The function acquires the resource corresponding to the specific category. |

### `DetailsBaseType<T>`

The type definition that the pair of name and detail.

```ts
interface DetailsBaseType<T = string> {
  readonly detail: T;
  readonly name: string;
}
```

| Type | Constraint | Description          |
| :--- | :--------- | :------------------- |
| `T`  | `string`   | The type of details. |

| Property | Type     | Description                     |
| :------- | :------- | :------------------------------ |
| `detail` | `string` | The detail.                     |
| `name`   | `string` | The resource name as a heading. |

### `DetailsType`

The type definition that the name, detail and more descriptions.

```ts
interface DetailsType {
  readonly detail: string;
  readonly name: string;
  readonly more: readonly string[];
}
```

| Property | Type                | Description                     |
| :------- | :------------------ | :------------------------------ |
| `detail` | `string`            | The detail.                     |
| `more`   | `readonly string[]` | The more detailed descriptions. |
| `name`   | `string`            | The resource name as a heading. |

### `PersonalityDetailBaseType`

The type definition that the details of personality.

```ts
export interface PersonalityDetailBaseType {
  readonly inner: string;
  readonly outer: string;
  readonly workStyle: string;
}
```

| Property    | Type     | Description                             |
| :---------- | :------- | :-------------------------------------- |
| `inner`     | `string` | The resource of inner personality.      |
| `outer`     | `string` | The resource of outer personality.      |
| `workStyle` | `string` | The resource of personality at working. |

### `PersonalityDetailType`

The type definition that the details of personality.

```ts
export interface PersonalityDetailType {
  readonly descriptions: PersonalityDetailBaseType;
  readonly detail: string;
  readonly inner: string;
  readonly name: string;
  readonly outer: string;
  readonly workStyle: string;
}
```

| Property       | Type                                                      | Description                             |
| :------------- | :-------------------------------------------------------- | :-------------------------------------- |
| `descriptions` | [`PersonalityDetailBaseType`](#personalitydetailbasetype) | Long descriptions.                      |
| `detail`       | `string`                                                  | The detail.                             |
| `inner`        | `string`                                                  | The resource of inner personality.      |
| `name`         | `string`                                                  | The resource name as a heading.         |
| `outer`        | `string`                                                  | The resource of outer personality.      |
| `workStyle`    | `string`                                                  | The resource of personality at working. |

### `PersonalityType`

A type definition of a structure that stores a
description of a particular person's personality.

```ts
interface PersonalityType {
  readonly detail: readonly string[];
  readonly name: string;
  readonly strategy: readonly string[];
  readonly summary: string;
  readonly weak: readonly string[];
}
```

| Property   | Type                | Description                                                            |
| :--------- | :------------------ | :--------------------------------------------------------------------- |
| `detail`   | `readonly string[]` | The detail.                                                            |
| `name`     | `string`            | The resource name.                                                     |
| `strategy` | `readonly string[]` | The strategies for communicating with people of this personality type. |
| `summary`  | `string`            | The short summary as a heading.                                        |
| `weak`     | `readonly string[]` | The weak points.                                                       |

### `VectorType`

A type definition of a structure that
stores a description of a personality type.

```ts
interface VectorType {
  readonly detail: string;
  readonly name: string;
  readonly strategy: readonly string[];
}
```

| Property   | Type                | Description                                                            |
| :--------- | :------------------ | :--------------------------------------------------------------------- |
| `detail`   | `string`            | The detail.                                                            |
| `name`     | `string`            | The resource name as a heading.                                        |
| `strategy` | `readonly string[]` | The strategies for communicating with people of this personality type. |

## See also

- [i18next: internationalization-framework](https://www.i18next.com)

## License

MIT

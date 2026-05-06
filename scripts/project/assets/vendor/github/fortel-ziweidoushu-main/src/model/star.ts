interface Star {
    getType(): string
    getKey(): string
    getDisplayName(): string
    equals(star: Star): boolean
}

export { Star }

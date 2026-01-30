module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // Allow uppercase scopes for issue IDs like 0DIN-123
    "scope-case": [2, "always", ["lower-case", "upper-case", "kebab-case"]],
    // Allow longer subjects for descriptive commit messages
    "subject-case": [0],
    // Allow longer body lines for detailed descriptions
    "body-max-line-length": [0],
  },
};

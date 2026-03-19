# Agent Guidelines

## Build Commands

```bash
go run hello.go
```

## Code Style Guidelines

### General
- Write clear, readable code with descriptive variable and function names
- Keep functions small and focused (single responsibility principle)
- Avoid premature optimization; prioritize clarity first

### Go Specific
- Use `gofmt` for automatic formatting: `gofmt -w .`
- Use `go vet` for static analysis: `go vet ./...`
- Run `goimports` to manage import statements automatically
- Error handling: handle errors explicitly; avoid ignoring with `_`
- Return errors rather than panicking in production code

### Naming Conventions
- Variables/functions: `camelCase` (e.g., `getUserById`, `totalCount`)
- Types/structs: `PascalCase` (e.g., `UserService`, `ConfigStruct`)
- Constants: `PascalCase` or `ALL_CAPS` for exported, `camelCase` for unexported
- Packages: short, lowercase, no underscores (e.g., `fmt`, `io`)

### Imports
- Group stdlib and third-party imports separately
- Use `goimports` to manage automatically
- Avoid relative imports; use full package paths

### Error Handling
- Wrap errors with context using `fmt.Errorf("operation: %w", err)`
- Return errors early; avoid deep nesting
- Log errors at the boundary (main, API handlers), not deep in logic

### Testing
- Place tests in `*_test.go` files alongside source code
- Use table-driven tests for multiple test cases
- Test names: `Test<FunctionName>_<Scenario>`
- Use `t.Run` for subtests
- Coverage goal: focus on critical paths, not arbitrary percentage

### Documentation
- Document exported functions, types, and packages
- Use godoc-style comments: `// FunctionName does X`
- Keep comments up-to-date with code changes

### Concurrency
- Document when functions are safe for concurrent use
- Use `sync.WaitGroup` or context for cancellation
- Be cautious with shared state; prefer channels when possible

### Project Structure
- Use `cmd/` for application entry points
- Use `pkg/` for reusable libraries
- Use `internal/` for packages not importable from external projects
- Keep main package minimal; delegate to other packages

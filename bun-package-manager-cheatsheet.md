# Bun Cheat Sheet

Fast all-in-one JavaScript runtime and toolkit (bundler, test runner, package manager).

---

## Core Concepts

### What is Bun?
Bun is a modern JavaScript runtime built from scratch using Zig and JavaScriptCore (Safari's JS engine). It serves as a drop-in replacement for Node.js with significantly faster startup times and execution speed. Unlike Node.js which uses V8, Bun uses JavaScriptCore which contributes to its performance gains.

### Key Features
- **Runtime**: Execute JavaScript and TypeScript files directly without transpilation
- **Package Manager**: Install npm packages faster than npm/yarn/pnpm
- **Bundler**: Built-in bundler for production builds
- **Test Runner**: Native test framework with Jest-compatible API
- **Dev Server**: Hot reloading development server
- **Native TypeScript**: Run `.ts` files without configuration
- **Web APIs**: Built-in support for `fetch`, `WebSocket`, `ReadableStream`, etc.

### Architecture
Bun uses JavaScriptCore (the engine powering Safari) instead of V8 (Chrome/Node.js). This choice, combined with Zig for the core implementation, provides faster startup times and lower memory usage. Bun implements Node.js APIs natively in Zig rather than JavaScript, reducing overhead.

---

## Installation

### Install Bun
```bash
# macOS, Linux, WSL
curl -fsSL https://bun.sh/install | bash

# Upgrade
bun upgrade

# Specific version
curl -fsSL https://bun.sh/install | bash -s "bun-v1.0.0"
```

### Verify Installation
```bash
bun --version
```

---

## Running Code

### Execute Files
```bash
# Run JavaScript
bun run index.js

# Run TypeScript (no config needed)
bun run app.ts

# Run with watch mode
bun --watch server.ts

# Run with hot reload
bun --hot server.ts
```

**Explanation**: Bun automatically transpiles TypeScript and JSX. Watch mode restarts on file changes, while hot mode reloads without restarting the process.

### REPL (Interactive Shell)
```bash
bun repl
```

**Explanation**: Similar to `node` REPL, provides interactive JavaScript execution environment.

---

## Package Management

### Install Packages
```bash
# Install all dependencies from package.json
bun install

# Add package
bun add react

# Add dev dependency
bun add -d typescript

# Add global package
bun add -g prettier

# Install from lockfile only (CI)
bun install --frozen-lockfile
```

**Explanation**: Bun reads `package.json` like npm but uses its own lockfile (`bun.lockb`, a binary format). Installation is typically 2-10x faster than npm due to optimized downloading and linking.

### Remove Packages
```bash
bun remove lodash
```

### Update Packages
```bash
# Update all packages
bun update

# Update specific package
bun update react
```

### Package Scripts
```bash
# Run package.json scripts
bun run dev
bun run build

# Shorthand (if script exists)
bun dev
bun build
```

**Explanation**: Like `npm run`, but Bun executes scripts faster due to reduced startup overhead.

---

## Bun APIs

### File I/O
```typescript
// Read file
const file = Bun.file("package.json");
const text = await file.text();
const json = await file.json();
const buffer = await file.arrayBuffer();

// Write file
await Bun.write("output.txt", "Hello World");
await Bun.write("data.json", { key: "value" });

// Stream file
const stream = Bun.file("large.txt").stream();
```

**Explanation**: `Bun.file()` creates a file reference. Methods like `.text()` and `.json()` are lazy and optimized. `Bun.write()` handles various data types (strings, objects, buffers) automatically.

### HTTP Server
```typescript
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    
    if (url.pathname === "/") {
      return new Response("Hello World");
    }
    
    return new Response("Not Found", { status: 404 });
  },
});

console.log("Server running on http://localhost:3000");
```

**Explanation**: Bun's HTTP server is built on native code, not Node's `http` module. It's significantly faster and uses Web standard `Request`/`Response` objects instead of Node's `IncomingMessage`/`ServerResponse`.

### WebSocket Server
```typescript
Bun.serve({
  port: 3000,
  fetch(req, server) {
    if (server.upgrade(req)) {
      return; // WebSocket upgrade
    }
    return new Response("HTTP response");
  },
  websocket: {
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    },
    open(ws) {
      console.log("Client connected");
    },
    close(ws) {
      console.log("Client disconnected");
    },
  },
});
```

**Explanation**: WebSocket support is built-in with pub/sub capabilities. The `upgrade()` method handles the WebSocket handshake, and the `websocket` handlers define message behavior.

### Environment Variables
```typescript
// Access env vars
const apiKey = Bun.env.API_KEY;
const port = Bun.env.PORT || 3000;

// Or use process.env (Node.js compatible)
const dbUrl = process.env.DATABASE_URL;
```

**Explanation**: Bun automatically loads `.env` files without needing `dotenv` package. Both `Bun.env` and `process.env` work identically.

### Hashing & Crypto
```typescript
// Hash password
const hashed = await Bun.password.hash("mypassword");
const isValid = await Bun.password.verify("mypassword", hashed);

// SHA256
const hasher = new Bun.CryptoHasher("sha256");
hasher.update("data");
const hash = hasher.digest("hex");
```

**Explanation**: Bun provides native, fast hashing utilities. Password hashing uses bcrypt by default. `CryptoHasher` is faster than Node's `crypto` module.

---

## Bundler

### Bundle Code
```bash
# Bundle for browser
bun build ./src/index.tsx --outdir ./dist --target browser

# Bundle for Node.js
bun build ./src/server.ts --outdir ./dist --target node

# Minify output
bun build ./src/index.ts --outdir ./dist --minify

# Generate sourcemaps
bun build ./src/index.ts --outdir ./dist --sourcemap=external
```

**Explanation**: Bun's bundler is built-in and optimized for speed. It handles TypeScript, JSX, and imports without plugins. Target specifies runtime environment (browser vs node). Minification and sourcemaps work like other bundlers.

### Programmatic API
```typescript
await Bun.build({
  entrypoints: ['./src/index.tsx'],
  outdir: './dist',
  target: 'browser',
  minify: true,
  splitting: true, // Code splitting
  sourcemap: 'external',
});
```

**Explanation**: Programmatic bundling for build scripts. `splitting` enables code splitting for better caching. Returns build metadata including output files and errors.

---

## Testing

### Test Runner
```typescript
// math.test.ts
import { expect, test, describe } from "bun:test";

describe("Math operations", () => {
  test("addition", () => {
    expect(2 + 2).toBe(4);
  });

  test("subtraction", () => {
    expect(5 - 3).toBe(2);
  });
});
```

**Explanation**: Bun's test runner is Jest-compatible but faster. Import from `bun:test` instead of installing Jest. Supports `test`, `describe`, `beforeEach`, `afterEach`, etc.

### Run Tests
```bash
# Run all tests
bun test

# Watch mode
bun test --watch

# Run specific file
bun test math.test.ts

# Coverage (experimental)
bun test --coverage
```

**Explanation**: `bun test` automatically finds files matching `*.test.ts`, `*.test.js`, `*_test.ts`, etc. Watch mode reruns tests on file changes.

### Mocking
```typescript
import { mock } from "bun:test";

const mockFn = mock((x: number) => x * 2);
mockFn(5);

expect(mockFn).toHaveBeenCalledTimes(1);
expect(mockFn).toHaveBeenCalledWith(5);
```

**Explanation**: Built-in mocking without additional libraries. Similar to Jest's `jest.fn()`.

---

## TypeScript Support

### No Configuration Required
```bash
# Just run TypeScript files
bun run app.ts
```

**Explanation**: Bun transpiles TypeScript on-the-fly using its internal transpiler. No need for `tsc` or `ts-node`. Type checking is not performed during execution (use `tsc --noEmit` for type checking).

### tsconfig.json
```json
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "module": "esnext",
    "target": "esnext",
    "moduleResolution": "bundler",
    "types": ["bun-types"]
  }
}
```

**Explanation**: Recommended TypeScript configuration for Bun projects. `moduleResolution: "bundler"` enables Bun-specific module resolution. `bun-types` adds Bun API type definitions.

### Install Type Definitions
```bash
bun add -d bun-types
```

---

## Module System

### Import/Export (ESM)
```typescript
// Named exports
export const add = (a: number, b: number) => a + b;

// Default export
export default function main() {
  console.log("Hello");
}

// Import
import main, { add } from "./utils";
```

**Explanation**: Bun prioritizes ESM (ES Modules). Use `import`/`export` syntax. CommonJS (`require`) also works for Node.js compatibility.

### CommonJS Compatibility
```typescript
// Works in Bun
const express = require("express");
const fs = require("fs");

// Also works
import express from "express";
import fs from "fs";
```

**Explanation**: Bun seamlessly handles both ESM and CommonJS. You can mix them in the same project. Bun automatically resolves the correct format.

### Path Aliases
```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

```typescript
// Use aliases
import { config } from "@/config";
```

**Explanation**: Define path aliases in `tsconfig.json` and Bun respects them automatically without additional bundler configuration.

---

## Environment & Configuration

### .env Files
```bash
# .env
DATABASE_URL=postgresql://localhost/mydb
API_KEY=secret123
PORT=3000
```

```typescript
// Automatically loaded
console.log(Bun.env.DATABASE_URL);
```

**Explanation**: Bun loads `.env` files automatically without needing the `dotenv` package. Variables are available in `Bun.env` and `process.env`.

### bunfig.toml
```toml
# bunfig.toml - Bun configuration file

# Package manager settings
[install]
cache = "~/.bun/install/cache"
registry = "https://registry.npmjs.org"

# Development
[run]
bun = "bun"
```

**Explanation**: Optional configuration file for customizing Bun behavior. Can set registry mirrors, cache locations, and runtime flags.

---

## Best Practices

### Use Native Bun APIs
Prefer `Bun.file()` over `fs.readFile()` for better performance:
```typescript
// Faster
const data = await Bun.file("data.json").json();

// Slower (Node.js API)
import { readFile } from "fs/promises";
const data = JSON.parse(await readFile("data.json", "utf-8"));
```

**Explanation**: Bun's native APIs are optimized and often 2-10x faster than Node.js equivalents. They also have simpler interfaces.

### Leverage Built-in Transpilation
Don't configure Babel or SWC for TypeScript/JSX:
```typescript
// Just works, no config needed
import React from "react";

export default function App() {
  return <div>Hello World</div>;
}
```

**Explanation**: Bun handles TypeScript and JSX transpilation automatically. Save configuration overhead and execution time.

### Use `bun install` for Speed
Replace `npm install` in your workflows:
```bash
# CI/CD pipeline
bun install --frozen-lockfile
bun test
bun build
```

**Explanation**: Even if you don't use Bun as runtime, using it as a package manager significantly speeds up CI/CD pipelines.

### Hot Reload in Development
Use `--hot` for server development:
```bash
bun --hot server.ts
```

**Explanation**: Hot reload preserves server state between code changes, faster than full restarts with `--watch`.

### Type Safety
Install type definitions for better DX:
```bash
bun add -d bun-types @types/node
```

**Explanation**: Enables TypeScript autocomplete for Bun APIs and Node.js compatibility layer.

---

## Common Mistakes

### Using Incompatible Node.js Packages
**Problem**: Some native Node.js modules don't work in Bun.
```typescript
// May not work
import { Worker } from "worker_threads";
```

**Solution**: Check compatibility or use Bun alternatives. Bun has `Worker` but with different API:
```typescript
// Bun's Worker API
const worker = new Worker("worker.ts");
```

**Explanation**: Bun aims for Node.js compatibility but isn't 100% compatible. Native modules and some Node.js internals may fail. Check Bun's compatibility documentation.

### Forgetting `await` with Bun APIs
**Problem**: Bun APIs are async but look synchronous.
```typescript
// Wrong - returns Promise
const data = Bun.file("data.json").json();

// Correct
const data = await Bun.file("data.json").json();
```

**Explanation**: Many Bun APIs return Promises. Always check the API documentation and use `await` where required.

### Not Using `--frozen-lockfile` in CI
**Problem**: Dependencies might change between local and CI.
```bash
# Bad - may install different versions
bun install

# Good - fails if lockfile is outdated
bun install --frozen-lockfile
```

**Explanation**: In CI/CD, use `--frozen-lockfile` to ensure reproducible builds and catch lockfile drift.

### Mixing Package Managers
**Problem**: Using npm and bun in same project.
```bash
npm install lodash  # Creates package-lock.json
bun install         # Creates bun.lockb
```

**Solution**: Stick to one package manager per project.

**Explanation**: Multiple lockfiles cause version conflicts and confusion. Choose one package manager and commit its lockfile.

### Assuming Full Node.js Compatibility
**Problem**: Expecting all Node.js code to work unchanged.
```typescript
// Node.js specific features may not work
process.binding("http_parser");
```

**Solution**: Test thoroughly and check Bun documentation for compatibility status.

**Explanation**: Bun prioritizes Web standards over Node.js APIs. Some internal Node.js APIs aren't implemented. Use standard APIs when possible.

---

## Quick Reference

### Essential Commands
```bash
bun run file.ts          # Execute file
bun install              # Install dependencies
bun add package          # Add package
bun remove package       # Remove package
bun test                 # Run tests
bun build ./src --outdir ./dist  # Bundle code
bun upgrade              # Upgrade Bun
```

### Key APIs
```typescript
Bun.file(path)           // File operations
Bun.write(path, data)    // Write file
Bun.serve({...})         // HTTP server
Bun.env.VAR              // Environment variables
Bun.password.hash()      // Hash passwords
Bun.build({...})         // Bundle code
```

### Performance Tips
- Use `Bun.file()` instead of `fs` APIs
- Prefer native Bun APIs over Node.js equivalents
- Use `--hot` for development servers
- Use `bun install` even if not using Bun runtime
- Avoid unnecessary transpilation with external tools

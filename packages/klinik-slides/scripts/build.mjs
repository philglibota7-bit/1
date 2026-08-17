#!/usr/bin/env node
/**
 * Build für @klinik-sh/slides.
 *
 * Erzeugt in dist/:
 *   index.mjs       gebündeltes ESM (React bleibt extern)
 *   index.d.ts + …  Typdeklarationen (tsc --emitDeclarationOnly)
 *   tokens.css      Design-Tokens (:root)
 *   components.css  Komponenten-Regeln
 *   fonts.css       @font-face für Inter
 *   fonts/*.woff2   Schriftdateien
 *   styles.css      Sammel-Import für Anwendungen
 */
import { execFileSync } from "node:child_process";
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import * as esbuild from "esbuild";

const pkgRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(pkgRoot, "dist");
const src = join(pkgRoot, "src");

rmSync(dist, { recursive: true, force: true });
mkdirSync(dist, { recursive: true });

// 1. JS-Bundle -------------------------------------------------------------
await esbuild.build({
  entryPoints: [join(src, "index.ts")],
  outfile: join(dist, "index.mjs"),
  bundle: true,
  format: "esm",
  target: "es2020",
  jsx: "automatic",
  platform: "browser",
  sourcemap: false,
  legalComments: "none",
  external: ["react", "react-dom", "react/jsx-runtime"],
  logLevel: "info",
});

// 2. Typdeklarationen ------------------------------------------------------
execFileSync(
  process.execPath,
  [join(pkgRoot, "node_modules", "typescript", "lib", "tsc.js"), "--project", join(pkgRoot, "tsconfig.json")],
  { stdio: "inherit", cwd: pkgRoot },
);

// 3. CSS und Schriften ----------------------------------------------------
const css = (name) => readFileSync(join(src, "styles", name), "utf8");

const tokensCss = css("tokens.css");
const componentsCss = css("components.css");

writeFileSync(join(dist, "tokens.css"), tokensCss);
writeFileSync(join(dist, "components.css"), componentsCss);
writeFileSync(join(dist, "fonts.css"), css("fonts.css"));
cpSync(join(src, "fonts"), join(dist, "fonts"), { recursive: true });

// Tokens und Komponenten zusätzlich in EINER Datei ohne @import: die
// Design-Sync-Auslieferung übernimmt genau ein Stylesheet als Komponenten-CSS,
// und die Tokens müssen darin enthalten sein — sonst rendern ausgelieferte
// Folien ohne Farben, Schriftgrößen und Abstände.
writeFileSync(
  join(dist, "klinik-slides.css"),
  `/* @klinik-sh/slides — Tokens und Komponenten in einer Datei (generiert, nicht bearbeiten). */\n\n${tokensCss}\n${componentsCss}`,
);

writeFileSync(
  join(dist, "styles.css"),
  `/* @klinik-sh/slides — vollständiges Stylesheet.
   In der Anwendung genügt: import "@klinik-sh/slides/styles.css"; */
@import "./fonts.css";
@import "./tokens.css";
@import "./components.css";
`,
);

console.log(
  "dist/ fertig: index.mjs, index.d.ts, styles.css, klinik-slides.css, tokens.css, components.css, fonts.css, fonts/",
);

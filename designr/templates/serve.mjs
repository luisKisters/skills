#!/usr/bin/env node
// Tiny static server for designr mockups. No dependencies.
// Usage: node serve.mjs <root> [port]
// Binds 127.0.0.1. Sends no-store, so a reload always shows the newest file.
// Without a port it starts at 4600 and takes the first free one.
// GET /__designr answers {"root": ..., "port": ...}, so an agent can find and reuse it.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, join, extname, sep } from 'node:path';

const root = resolve(process.argv[2] || '.');
const asked = process.argv[3] ? Number(process.argv[3]) : 0;
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.md': 'text/markdown; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif',
  '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.otf': 'font/otf',
};

let port = asked || 4600;
const server = createServer(async (req, res) => {
  const send = (code, body, type = 'text/plain; charset=utf-8') => {
    res.writeHead(code, { 'content-type': type, 'cache-control': 'no-store' });
    res.end(body);
  };
  let path;
  try { path = decodeURIComponent(new URL(req.url, 'http://x').pathname); } catch { return send(400, 'Bad request'); }
  if (path === '/__designr') return send(200, JSON.stringify({ root, port }), TYPES['.json']);
  let file = join(root, path);
  if (file !== root && !file.startsWith(root + sep)) return send(403, 'Forbidden');
  try {
    if ((await stat(file)).isDirectory()) file = join(file, 'index.html');
    send(200, await readFile(file), TYPES[extname(file).toLowerCase()] || 'application/octet-stream');
  } catch {
    send(404, 'Not found');
  }
});

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE' && !asked && port < 4700) return server.listen(++port, '127.0.0.1');
  console.error(e.message);
  process.exit(1);
});
server.on('listening', () => console.log(`designr serve ${root} http://127.0.0.1:${port}/`));
server.listen(port, '127.0.0.1');

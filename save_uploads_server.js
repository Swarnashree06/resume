#!/usr/bin/env node
// save_uploads_server.js
// Simple Express server to accept uploaded certificate images and save them to ./img
// Usage: node save_uploads_server.js

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;
const imgDir = path.join(__dirname, 'img');
if (!fs.existsSync(imgDir)) fs.mkdirSync(imgDir, { recursive: true });
// Simple CORS middleware so browser pages (including file://) can talk to this server
app.use(function(req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

// health check
app.get('/health', (req, res) => res.json({ ok: true }));

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, imgDir);
  },
  filename: function (req, file, cb) {
    // ensure unique names
    const base = path.basename(file.originalname, path.extname(file.originalname));
    const ext = path.extname(file.originalname);
    let name = base + ext;
    let i = 1;
    while (fs.existsSync(path.join(imgDir, name))) {
      name = `${base}-${i}${ext}`;
      i++;
    }
    cb(null, name);
  }
});
const upload = multer({ storage });

app.post('/upload', upload.array('files'), (req, res) => {
  const saved = (req.files || []).map(f => f.filename);
  // update list.json
  const listPath = path.join(imgDir, 'list.json');
  let existing = [];
  try{ existing = JSON.parse(fs.readFileSync(listPath, 'utf8')); if(!Array.isArray(existing)) existing = []; }catch(_){}
  const merged = existing.concat(saved).filter((v,i,a)=>a.indexOf(v)===i);
  try{ fs.writeFileSync(listPath, JSON.stringify(merged, null, 2), 'utf8'); }catch(err){ console.warn('Failed to update list.json', err.message); }
  res.json({ ok: true, saved });
});

app.get('/', (req,res)=>res.send('Upload server is running. POST files to /upload'));

app.listen(PORT, ()=>{
  console.log(`Upload server listening on http://localhost:${PORT}`);
});

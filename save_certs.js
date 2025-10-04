#!/usr/bin/env node
// save_certs.js
// Usage: node save_certs.js <path-to-image1> <path-to-image2> ...
// Copies provided image files into the local img/ folder and writes img/list.json

const fs = require('fs');
const path = require('path');

function isImageFile(filename){
  const ext = path.extname(filename).toLowerCase();
  return ['.jpg','.jpeg','.png','.gif','.webp','.svg','.bmp'].includes(ext);
}

function ensureDir(dir){
  if(!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function uniqueDest(dest){
  if(!fs.existsSync(dest)) return dest;
  const dir = path.dirname(dest);
  const name = path.basename(dest, path.extname(dest));
  const ext = path.extname(dest);
  let i = 1;
  let candidate;
  do{ candidate = path.join(dir, `${name}-${i}${ext}`); i++; } while(fs.existsSync(candidate));
  return candidate;
}

(async function main(){
  const args = process.argv.slice(2);
  if(!args.length){
    console.log('Usage: node save_certs.js <path-to-image1> <path-to-image2> ...');
    console.log('Example: node save_certs.js "C:\\Users\\You\\Downloads\\cert1.jpg" cert2.png');
    process.exit(1);
  }

  const base = path.resolve(__dirname);
  const imgDir = path.join(base, 'img');
  ensureDir(imgDir);

  const saved = [];

  for(const src of args){
    const abs = path.resolve(src);
    if(!fs.existsSync(abs)){
      console.warn('Skipping (not found):', src);
      continue;
    }
    if(!isImageFile(abs)){
      console.warn('Skipping (not an image):', src);
      continue;
    }

    let destName = path.basename(abs);
    let dest = path.join(imgDir, destName);
    dest = uniqueDest(dest);
    try{
      fs.copyFileSync(abs, dest);
      const finalName = path.basename(dest);
      saved.push(finalName);
      console.log('Copied:', abs, '→', dest);
    }catch(err){
      console.error('Failed to copy', src, err.message);
    }
  }

  // update img/list.json with file names (overwrites or creates)
  if(saved.length){
    const listPath = path.join(imgDir, 'list.json');
    let existing = [];
    try{ existing = JSON.parse(fs.readFileSync(listPath, 'utf8')); if(!Array.isArray(existing)) existing = []; }catch(_){}
    const merged = existing.concat(saved).filter((v,i,a)=>a.indexOf(v)===i);
    try{ fs.writeFileSync(listPath, JSON.stringify(merged, null, 2), 'utf8'); console.log('Updated img/list.json'); }catch(err){ console.warn('Failed to write list.json', err.message); }
  } else {
    console.log('No images copied. img/list.json not updated.');
  }

  console.log('\nDone. Open certificates.html to view.');
})();

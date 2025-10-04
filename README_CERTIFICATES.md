Certificates helper scripts

This small helper copies image files you choose into the `img/` folder next to the resume and creates/updates `img/list.json` so `certificates.html` can display them.

Files added:
- `save_certs.js` — Node.js script. Usage: `node save_certs.js <path-to-image1> <path-to-image2> ...`
- `save_certs.py` — Python script. Usage: `python save_certs.py <path-to-image1> <path-to-image2> ...`

Behavior:
- Copies files into `img/` and avoids filename collisions by adding `-1`, `-2`, etc.
- Appends copied filenames to `img/list.json` (creates if missing).
- Only copies image file types: jpg, jpeg, png, gif, webp, svg, bmp.

Examples:
- Node: `node save_certs.js "C:\\Users\\You\\Downloads\\cert1.jpg" "C:\\Users\\You\\Desktop\\cert2.png"`
- Python: `python save_certs.py "C:\\Users\\You\\Downloads\\cert1.jpg" cert2.png`

Notes:
- Run the script from the project root (same directory as `index.html`).
- The scripts do not resize or alter images; `certificates.html` will display them as provided.
- If you prefer, I can also add an option to rename files to `cert1.jpg`, etc., or to clear `img/list.json` before writing.

Node upload server (to persist images from browser)

- Install dependencies (PowerShell):

	npm init -y; npm install express multer

- Start the server (PowerShell):

	node .\save_uploads_server.js

- Verify it's running:

	Open http://localhost:3000/health in your browser or run in PowerShell:

	Invoke-RestMethod http://localhost:3000/health

If the server isn't reachable you'll see a "Failed to fetch" error in the browser; make sure you've started the server and that your firewall isn't blocking localhost:3000.

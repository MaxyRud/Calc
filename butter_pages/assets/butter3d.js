/* Butter3D: a soft, slow-rise butter-stick squeeze toy in three.js (r128, global THREE).
   The model is 13.5 x 4 x 4 cm (the listing's measurements). Colours and label are sampled
   from the supplier photo. Deformation runs on the CPU:
     - press(): a fingertip dent with a volume-preserving bulge around it
     - squeeze(): a whole-hand squeeze across the width
   Recovery is overdamped, like slow-rise TPR: about 30% springs back fast and the rest creeps
   back over a few seconds. Nothing in it overshoots.

   Butter3D(container, opts) returns an api object; see the bottom of this file. */
(function () {
  "use strict";
  var L = 13.5, H = 4, D = 4, R = 0.62;              // cm
  var BUTTER = "#f2e792", BUTTER_D = "#e2d47a", NAVY = "#374a62";

  function labelCanvas(withText) {
    var w = 2048, h = Math.round(w * H / L), c = document.createElement("canvas");
    c.width = w; c.height = h;
    var x = c.getContext("2d");
    var g = x.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, "#fbf08f"); g.addColorStop(1, "#f6e47c");
    x.fillStyle = g; x.fillRect(0, 0, w, h);
    // very faint large-scale unevenness, like moulded TPR (the real toy is smooth and slightly glossy)
    for (var i = 0; i < 90; i++) {
      x.fillStyle = Math.random() < .5 ? "rgba(255,255,240,.035)" : "rgba(210,190,90,.03)";
      var r = 60 + Math.random() * 180;
      x.beginPath(); x.arc(Math.random() * w, Math.random() * h, r, 0, 6.283); x.fill();
    }
    if (withText) {
      x.fillStyle = NAVY; x.textBaseline = "alphabetic";
      var F = '"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif';
      // 4OZ.  (big 4, smaller OZ.)
      x.font = "600 " + Math.round(h * .33) + "px " + F; x.fillText("4", w * .2, h * .58);
      var w4 = x.measureText("4").width;
      x.font = "600 " + Math.round(h * .2) + "px " + F; x.fillText("OZ.", w * .2 + w4 + 4, h * .58);
      x.font = "500 " + Math.round(h * .095) + "px " + F; x.fillText("NET WT. (113 G)", w * .16, h * .74);
      // SALTED / BUTTER
      x.font = "700 " + Math.round(h * .085) + "px " + F;
      x.textAlign = "center"; x.fillText("SALTED", w * .565, h * .45); x.textAlign = "left";
      x.font = "700 " + Math.round(h * .38) + "px " + F;
      var bw = x.measureText("BUTTER").width, target = w * .35, sx = target / bw;
      x.save(); x.translate(w * .39, h * .84); x.scale(sx, 1); x.fillText("BUTTER", 0, 0); x.restore();
    }
    return c;
  }

  function roundedBox(seg) {
    var g = new THREE.BoxGeometry(L, H, D, seg[0], seg[1], seg[2]);
    var p = g.attributes.position, v = new THREE.Vector3(), inner = new THREE.Vector3(L / 2 - R, H / 2 - R, D / 2 - R);
    for (var i = 0; i < p.count; i++) {
      v.fromBufferAttribute(p, i);
      var c = new THREE.Vector3(Math.max(-inner.x, Math.min(inner.x, v.x)), Math.max(-inner.y, Math.min(inner.y, v.y)), Math.max(-inner.z, Math.min(inner.z, v.z)));
      var d = v.clone().sub(c);
      if (d.lengthSq() > 1e-9) { d.setLength(R); v.copy(c).add(d); }
      // a very slight soft sag in the middle of the long faces
      var sag = .06 * Math.cos(v.x / L * Math.PI);
      if (v.y > 0) v.y -= sag * (v.y / (H / 2));
      p.setXYZ(i, v.x, v.y, v.z);
    }
    g.computeVertexNormals();
    return g;
  }

  /* group duplicate vertices (face seams) so recomputed normals stay smooth */
  function seamGroups(pos) {
    var map = {}, groups = [];
    for (var i = 0; i < pos.count; i++) {
      var k = Math.round(pos.getX(i) * 400) + "," + Math.round(pos.getY(i) * 400) + "," + Math.round(pos.getZ(i) * 400);
      (map[k] = map[k] || []).push(i);
    }
    for (var k2 in map) if (map[k2].length > 1) groups.push(map[k2]);
    return groups;
  }

  function envMap(renderer) {
    var s = new THREE.Scene();
    var geo = new THREE.SphereGeometry(50, 32, 16);
    var mat = new THREE.ShaderMaterial({ side: THREE.BackSide, uniforms: {},
      vertexShader: "varying vec3 p; void main(){ p = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }",
      fragmentShader: "varying vec3 p; void main(){ float y = normalize(p).y; vec3 top = vec3(1.0,0.98,0.94); vec3 bot = vec3(0.55,0.5,0.42); gl_FragColor = vec4(mix(bot, top, smoothstep(-0.3,0.6,y)), 1.); }" });
    s.add(new THREE.Mesh(geo, mat));
    var panel = new THREE.Mesh(new THREE.PlaneGeometry(30, 14), new THREE.MeshBasicMaterial({ color: 0xffffff }));
    panel.position.set(-18, 26, 14); panel.lookAt(0, 0, 0); s.add(panel);
    var panel2 = panel.clone(); panel2.position.set(22, 14, 18); panel2.scale.set(.6, .6, 1); panel2.lookAt(0, 0, 0); s.add(panel2);
    var pm = new THREE.PMREMGenerator(renderer);
    var rt = pm.fromScene(s, 0.04); pm.dispose();
    return rt.texture;
  }

  function Butter3D(el, opts) {
    opts = opts || {};
    var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: !!opts.preserve });
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.LinearToneMapping; renderer.toneMappingExposure = opts.exposure || 1;
    renderer.shadowMap.enabled = opts.shadow !== false; renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.domElement.style.cssText = "display:block;width:100%;height:100%;touch-action:none;outline:none";
    el.appendChild(renderer.domElement);

    var scene = new THREE.Scene();
    if (opts.bg) scene.background = new THREE.Color(opts.bg);
    var camera = new THREE.PerspectiveCamera(opts.fov || 26, 1, 0.1, 200);

    var hemi = new THREE.HemisphereLight(0xffffff, 0xc9b98a, .7); scene.add(hemi);
    var key = new THREE.DirectionalLight(0xffffff, .72); key.position.set(-3, 16, 7); key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 9; key.shadow.bias = -0.0008;
    var sc = key.shadow.camera; sc.left = -12; sc.right = 12; sc.top = 12; sc.bottom = -12; sc.near = 1; sc.far = 40;
    scene.add(key);
    var rim = new THREE.DirectionalLight(0xffffff, .25); rim.position.set(9, 4, -8); scene.add(rim);
    var fill = new THREE.DirectionalLight(0xfff8e8, .22); fill.position.set(6, 2, 14); scene.add(fill);

    var floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: opts.shadowOpacity == null ? .2 : opts.shadowOpacity }));
    floor.rotation.x = -Math.PI / 2; floor.position.y = -H / 2 - .001; floor.receiveShadow = true;
    if (opts.floor !== false) scene.add(floor);

    var seg = opts.lowPoly ? [72, 18, 18] : [120, 30, 30];
    var geo = roundedBox(seg), base = geo.attributes.position.array.slice(), baseN = geo.attributes.normal.array.slice();
    var groups = seamGroups(geo.attributes.position);
    var plainTex = new THREE.CanvasTexture(labelCanvas(false)), labelTex;
    function prep(t) { t.encoding = THREE.sRGBEncoding; t.anisotropy = 8; t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping; return t; }
    prep(plainTex);
    function mat(map) { return new THREE.MeshPhysicalMaterial({ map: map, roughness: .55, metalness: 0, clearcoat: .4, clearcoatRoughness: .38 }); }
    var front = mat(plainTex), plain = mat(plainTex), readyRes;
    var mesh = new THREE.Mesh(geo, [plain, plain, plain, plain, front, plain]);
    mesh.castShadow = true; mesh.receiveShadow = false;
    var group = new THREE.Group(); group.add(mesh); scene.add(group);
    function drawLabel() {
      labelTex = prep(new THREE.CanvasTexture(labelCanvas(true)));
      front.map = labelTex; front.needsUpdate = true; render(); if (readyRes) readyRes();
    }
    if (document.fonts && document.fonts.load) document.fonts.load('700 100px "Barlow Semi Condensed"').then(drawLabel, drawLabel); else drawLabel();

    /* pose */
    var pose = Object.assign({ rx: .32, ry: -.32, dist: 30, ty: 0, tx: 0 }, opts.pose || {});
    function place() {
      var r = pose.dist;
      camera.position.set(r * Math.sin(pose.ry) * Math.cos(pose.rx), r * Math.sin(pose.rx), r * Math.cos(pose.ry) * Math.cos(pose.rx));
      camera.lookAt(pose.tx, pose.ty, 0);
    }
    place();

    /* deformation state */
    var dents = [];                 // {p:Vector3 local, n:Vector3 press dir (into body), r, d, hold, t0, d0}
    var squeezeK = 0, squeezeT = 0, squeezeX = 0, stretch = 0, stretchT = 0;
    var pos = geo.attributes.position, nrm = geo.attributes.normal;
    var tmp = new THREE.Vector3(), nv = new THREE.Vector3();
    function deform() {
      var a = pos.array, nb = baseN;
      for (var i = 0; i < a.length; i += 3) {
        var x = base[i], y = base[i + 1], z = base[i + 2];
        var dx = 0, dy = 0, dz = 0;
        for (var k = 0; k < dents.length; k++) {
          var de = dents[k]; if (de.d < 1e-4) continue;
          var ex = x - de.p.x, ey = y - de.p.y, ez = z - de.p.z, q = ex * ex + ey * ey + ez * ez;
          var f = Math.exp(-q / (2 * de.r * de.r));
          // push in along the press direction, deeper near the contact
          dx += de.n.x * de.d * f; dy += de.n.y * de.d * f; dz += de.n.z * de.d * f;
          // volume-preserving bulge: surrounding surface swells outward along its own normal
          var face = 1 - Math.abs(nb[i] * de.n.x + nb[i + 1] * de.n.y + nb[i + 2] * de.n.z);
          var b = de.d * .22 * Math.exp(-q / (2 * (de.r * 2.1) * (de.r * 2.1))) * (0.35 + face);
          dx += nb[i] * b; dy += nb[i + 1] * b; dz += nb[i + 2] * b;
        }
        if (squeezeK > 1e-4) {
          var g2 = Math.exp(-Math.pow(x - squeezeX, 2) / (2 * 2.4 * 2.4));
          var k2 = squeezeK * g2;
          dz += -z * k2; dy += y * k2 * .45;          // pinch the width, bulge the height
          dx += (x - squeezeX) * k2 * .12;             // material flows away from the grip
        }
        var sx = 1 + stretch, sw = 1 / Math.sqrt(1 + stretch);
        a[i] = (x + dx) * sx; a[i + 1] = (y + dy) * sw; a[i + 2] = (z + dz) * sw;
      }
      pos.needsUpdate = true;
      geo.computeVertexNormals();
      var n = nrm.array;
      for (var gI = 0; gI < groups.length; gI++) {
        var G = groups[gI], sx2 = 0, sy2 = 0, sz2 = 0;
        for (var j = 0; j < G.length; j++) { sx2 += n[G[j] * 3]; sy2 += n[G[j] * 3 + 1]; sz2 += n[G[j] * 3 + 2]; }
        var l = Math.hypot(sx2, sy2, sz2) || 1;
        for (j = 0; j < G.length; j++) { n[G[j] * 3] = sx2 / l; n[G[j] * 3 + 1] = sy2 / l; n[G[j] * 3 + 2] = sz2 / l; }
      }
      nrm.needsUpdate = true;
    }

    /* recovery: 30% fast, 70% slow creep (tau seconds) */
    var TAU = opts.tau || 1.5, FAST = .12;
    function rec(d0, t) { return d0 * (.3 * Math.exp(-t / FAST) + .7 * Math.exp(-t / TAU)); }
    var running = false, last = 0, listeners = [];
    function step(now) {
      var dt = Math.min(.05, (now - last) / 1000); last = now;
      var active = false;
      for (var k = dents.length - 1; k >= 0; k--) {
        var de = dents[k];
        if (de.hold) {
          de.target = Math.min(de.max, de.target + dt * .35);     // a held press keeps sinking a little
          de.d += (de.target - de.d) * (1 - Math.exp(-dt / .09));
          active = true;
        } else {
          de.t += dt; de.d = rec(de.d0, de.t);
          if (de.d < .004) dents.splice(k, 1); else active = true;
        }
      }
      if (squeezeT >= 0) {
        if (squeezeHold) { squeezeK += (squeezeTarget - squeezeK) * (1 - Math.exp(-dt / .12)); active = true; }
        else if (squeezeK > 1e-3) { squeezeT += dt; squeezeK = rec(squeezeK0, squeezeT); active = true; } else squeezeK = 0;
      }
      if (stretchHold) { stretch += (stretchTarget - stretch) * (1 - Math.exp(-dt / .1)); active = true; }
      else if (Math.abs(stretch) > 1e-3) { stretchT += dt; stretch = rec(stretch0, stretchT); active = true; } else stretch = 0;
      if (auto && !anyHold()) { pose.ry += dt * auto; place(); active = true; }
      deform(); render();
      var st = api.state(); listeners.forEach(function (f) { f(st); });
      if (active || auto) requestAnimationFrame(step); else running = false;
    }
    function kick() { if (!running) { running = true; last = performance.now(); requestAnimationFrame(step); } }
    function render() { renderer.render(scene, camera); }
    function anyHold() { return squeezeHold || stretchHold || dents.some(function (d) { return d.hold; }); }

    /* picking against the undeformed shape */
    var pickBox = new THREE.Mesh(new THREE.BoxGeometry(L, H, D), new THREE.MeshBasicMaterial({ visible: false }));
    group.add(pickBox);
    var ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
    function pick(cx, cy) {
      var r = renderer.domElement.getBoundingClientRect();
      ndc.set((cx - r.left) / r.width * 2 - 1, -((cy - r.top) / r.height) * 2 + 1);
      ray.setFromCamera(ndc, camera);
      var h = ray.intersectObject(pickBox)[0]; if (!h) return null;
      var p = group.worldToLocal(h.point.clone()), n = h.face.normal.clone();
      return { p: p, n: n.negate() };
    }

    var squeezeHold = false, squeezeTarget = 0, squeezeK0 = 0, stretchHold = false, stretchTarget = 0, stretch0 = 0, auto = 0;
    var api = {
      THREE: THREE, scene: scene, camera: camera, renderer: renderer, mesh: mesh, group: group, floor: floor, key: key,
      /* press at a client point; returns false if the pointer missed the stick */
      pressAt: function (cx, cy, depth) {
        var h = pick(cx, cy); if (!h) return false;
        api.release();
        dents.push({ p: h.p, n: h.n, r: opts.radius || 1.45, d: 0, target: depth || 1.3, max: (depth || 1.3) + .9, hold: true, t: 0, d0: 0 });
        kick(); return true;
      },
      moveTo: function (cx, cy) {
        var de = dents[dents.length - 1]; if (!de || !de.hold) return;
        var h = pick(cx, cy); if (h) { de.p.lerp(h.p, .5); de.n.lerp(h.n, .5).normalize(); }
      },
      /* programmatic press at local x (cm from centre), on top face */
      press: function (x, depth, r) {
        api.release();
        dents.push({ p: new THREE.Vector3(x || 0, H / 2, 0), n: new THREE.Vector3(0, -1, 0), r: r || 1.4, d: 0, target: depth || 1, max: (depth || 1) + .5, hold: true, t: 0, d0: 0 });
        kick();
      },
      release: function () {
        dents.forEach(function (d) { if (d.hold) { d.hold = false; d.d0 = d.d; d.t = 0; } });
        if (squeezeHold) { squeezeHold = false; squeezeK0 = squeezeK; squeezeT = 0; }
        if (stretchHold) { stretchHold = false; stretch0 = stretch; stretchT = 0; }
        kick();
      },
      squeeze: function (k, x) { squeezeHold = true; squeezeTarget = Math.max(0, Math.min(.55, k)); squeezeX = x || 0; squeezeT = 0; kick(); },
      stretchTo: function (s) { stretchHold = true; stretchTarget = Math.max(-.08, Math.min(.35, s)); kick(); },
      /* scrub a press directly (scroll-driven): depth in cm, no physics */
      setPress: function (x, depth) {
        dents = depth > .002 ? [{ p: new THREE.Vector3(x, H / 2, 0), n: new THREE.Vector3(0, -1, 0), r: 1.6, d: depth, hold: false, t: 99, d0: depth }] : [];
        deform(); render();
      },
      setSqueeze: function (k, x) { squeezeHold = false; squeezeK = k; squeezeX = x || 0; deform(); render(); },
      recovery: rec, tau: TAU,
      state: function () {
        var depth = 0; dents.forEach(function (d) { depth = Math.max(depth, d.d); });
        return { depth: depth, squeeze: squeezeK, stretch: stretch, holding: anyHold() };
      },
      setPose: function (p, instant) {
        if (instant || reduced) { Object.assign(pose, p); place(); render(); return; }
        var from = Object.assign({}, pose), t0 = performance.now(), dur = p.duration || 1400;
        (function f(t) {
          var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 4);
          for (var key2 in p) if (typeof p[key2] === "number" && key2 !== "duration") pose[key2] = from[key2] + (p[key2] - from[key2]) * e;
          place(); render(); if (k < 1) requestAnimationFrame(f);
        })(t0);
      },
      pose: pose,
      spin: function (speed) { auto = reduced ? 0 : speed || 0; kick(); },
      onUpdate: function (f) { listeners.push(f); },
      resize: function () {
        var w = el.clientWidth, h = el.clientHeight; if (!w || !h) return;
        renderer.setSize(w, h, false); camera.aspect = w / h;
        // keep the whole stick in frame on narrow screens
        camera.zoom = Math.min(1, (w / h) / (opts.fitAspect || 1.5)); camera.updateProjectionMatrix(); render();
      },
      render: render,
      /* extra static copies sharing the (deformable) geometry, for packs and renders */
      addCopy: function (x, y, z, ry, rz) {
        var m = new THREE.Mesh(geo, mesh.material); m.position.set(x || 0, y || 0, z || 0); m.rotation.y = ry || 0; m.rotation.z = rz || 0;
        m.castShadow = true; m.receiveShadow = true; group.add(m); render(); return m;
      },
      snapshot: function (type) { render(); return renderer.domElement.toDataURL(type || "image/png"); },
      ready: new Promise(function (res) { readyRes = res; }),
      dims: { L: L, H: H, D: D }
    };

    /* default pointer interaction */
    if (opts.interactive !== false) {
      var cvs = renderer.domElement, down = false;
      cvs.addEventListener("pointerdown", function (e) {
        if (api.pressAt(e.clientX, e.clientY, opts.depth || 1.3)) { down = true; cvs.setPointerCapture(e.pointerId); e.preventDefault(); el.dispatchEvent(new CustomEvent("butterpress")); }
      });
      cvs.addEventListener("pointermove", function (e) {
        if (down) api.moveTo(e.clientX, e.clientY);
        else if (e.pointerType === "mouse") cvs.style.cursor = pick(e.clientX, e.clientY) ? "grab" : "default";
      });
      var up = function () { if (!down) return; down = false; api.release(); el.dispatchEvent(new CustomEvent("butterrelease")); };
      cvs.addEventListener("pointerup", up); cvs.addEventListener("pointercancel", up);
      cvs.tabIndex = 0; cvs.setAttribute("role", "img"); cvs.setAttribute("aria-label", opts.label || "3D butter stick squeeze toy. Press it to squish.");
      cvs.addEventListener("keydown", function (e) {
        if (e.key === " " || e.key === "Enter") { e.preventDefault(); if (!e.repeat) { api.press(0, 1.1); el.dispatchEvent(new CustomEvent("butterpress")); } }
      });
      cvs.addEventListener("keyup", function (e) { if (e.key === " " || e.key === "Enter") { api.release(); el.dispatchEvent(new CustomEvent("butterrelease")); } });
    }

    if ("ResizeObserver" in window) new ResizeObserver(api.resize).observe(el);
    api.resize(); deform(); render();
    return api;
  }

  /* is WebGL available at all? pages fall back to the photo when not */
  Butter3D.supported = function () {
    try { var c = document.createElement("canvas"); return !!(window.WebGLRenderingContext && (c.getContext("webgl") || c.getContext("experimental-webgl"))) && !!window.THREE; } catch (e) { return false; }
  };
  window.Butter3D = Butter3D;
})();

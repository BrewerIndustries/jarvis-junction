// -------------------------------------------------------------------------------------------------
// Game-feel juice: particle bursts, screen shake, and haptics.
//
// Everything here is PURELY COSMETIC and non-deterministic.  It observes game
// events (via the sfx event hook) and reacts with visual/haptic flourish; it
// never touches the simulation, so replays and scores are unaffected.  Uses
// Math.random freely (cosmetic only) and honors prefers-reduced-motion.
// -------------------------------------------------------------------------------------------------

const REDUCED_MOTION = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : { matches: false };

// A short vibration on supporting devices.  `pattern` is ms or an array (see the
// Vibration API).  Silently does nothing where unsupported or motion-reduced.
export function haptic(pattern) {
    if (REDUCED_MOTION.matches) return;
    if (typeof navigator === 'undefined' || ! navigator.vibrate) return;
    try {
        navigator.vibrate(pattern);
    }
    catch (e) {
        // some browsers throw if not triggered by a user gesture; ignore
    }
}

// Add a brief shake animation class to an element (see .fx-shake* in style.css).
// `magnitude` is 'sm' | 'md' | 'lg'.
export function screen_shake(el, magnitude = 'md') {
    if (! el || REDUCED_MOTION.matches) return;
    let cls = `fx-shake-${magnitude}`;
    // Restart the animation even if it's already applied
    el.classList.remove('fx-shake-sm', 'fx-shake-md', 'fx-shake-lg');
    // force reflow so re-adding the class restarts the animation
    void el.offsetWidth;
    el.classList.add(cls);
    el.addEventListener('animationend', () => el.classList.remove(cls), { once: true });
}

// A canvas overlay that renders short-lived particles on top of the game board.
export class EffectsLayer {
    constructor(container) {
        this.container = container;
        this.canvas = document.createElement('canvas');
        this.canvas.className = 'effects-layer';
        this.ctx = this.canvas.getContext('2d');
        container.append(this.canvas);

        this.particles = [];
        this._raf = null;
        this._last = 0;
        this._dpr = 1;
        this.enabled = true;

        this._resize();
        if (window.ResizeObserver) {
            this._ro = new ResizeObserver(() => this._resize());
            this._ro.observe(container);
        }
    }

    _resize() {
        let rect = this.container.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return;
        let dpr = window.devicePixelRatio || 1;
        this._dpr = dpr;
        this.canvas.width = Math.round(rect.width * dpr);
        this.canvas.height = Math.round(rect.height * dpr);
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
    }

    // Spawn a burst.  client_x/client_y are viewport coordinates (as returned by
    // getBoundingClientRect-based helpers); we convert to canvas-local here.
    burst(client_x, client_y, opts = {}) {
        if (! this.enabled || REDUCED_MOTION.matches) return;
        let rect = this.container.getBoundingClientRect();
        let x = client_x - rect.x;
        let y = client_y - rect.y;

        let count = opts.count ?? 10;
        let colors = opts.colors ?? ['#e8c46a', '#f4e2a6', '#c8a24a'];
        let speed = opts.speed ?? 95;
        let size = opts.size ?? 3;
        let gravity = opts.gravity ?? 240;
        let life = opts.life ?? 0.55;
        let rise = opts.rise ?? 0;        // initial upward bias
        let square = opts.square ?? false; // confetti vs sparkle
        let spread = opts.spread ?? Math.PI * 2;
        let dir = opts.dir ?? -Math.PI / 2; // default: upward

        for (let i = 0; i < count; i++) {
            let ang = dir + (Math.random() - 0.5) * spread;
            let spd = speed * (0.45 + Math.random() * 0.9);
            this.particles.push({
                x, y,
                vx: Math.cos(ang) * spd,
                vy: Math.sin(ang) * spd - rise,
                spin: (Math.random() - 0.5) * 12,
                rot: Math.random() * Math.PI,
                life,
                max_life: life,
                size: size * (0.7 + Math.random() * 0.7),
                color: colors[(Math.random() * colors.length) | 0],
                gravity,
                square,
            });
        }
        this._ensure_running();
    }

    _ensure_running() {
        if (this._raf === null) {
            this._last = performance.now();
            this._raf = requestAnimationFrame(this._tick.bind(this));
        }
    }

    _tick(now) {
        let dt = Math.min(0.05, (now - this._last) / 1000);
        this._last = now;
        let ctx = this.ctx;
        let dpr = this._dpr;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        let alive = [];
        for (let p of this.particles) {
            p.life -= dt;
            if (p.life <= 0) continue;
            p.vy += p.gravity * dt;
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.rot += p.spin * dt;

            let a = Math.max(0, p.life / p.max_life);
            ctx.globalAlpha = a;
            ctx.fillStyle = p.color;
            let s = p.size * dpr;
            if (p.square) {
                ctx.save();
                ctx.translate(p.x * dpr, p.y * dpr);
                ctx.rotate(p.rot);
                ctx.fillRect(-s, -s, s * 2, s * 2);
                ctx.restore();
            }
            else {
                ctx.beginPath();
                ctx.arc(p.x * dpr, p.y * dpr, s, 0, Math.PI * 2);
                ctx.fill();
            }
            alive.push(p);
        }
        ctx.globalAlpha = 1;
        this.particles = alive;

        if (this.particles.length > 0) {
            this._raf = requestAnimationFrame(this._tick.bind(this));
        }
        else {
            this._raf = null;
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }

    destroy() {
        if (this._raf !== null) cancelAnimationFrame(this._raf);
        this._ro?.disconnect();
        this.canvas.remove();
    }
}

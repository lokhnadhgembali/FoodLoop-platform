"""
utils.py  -  FoodLoop shared utility functions
"""
import random
import io
import csv
from datetime import datetime, timezone


# ── SVG Icon helper (Lucide, 16 or 18px, stroke 1.5) ─────────────────────────

_ICONS: dict[str, str] = {
    "package":        '<path d="M16.5 9.4 7.55 4.24"/><polygon points="21 16 21 8 12 3 3 8 3 16 12 21 21 16"/><line x1="3.27" y1="6.96" x2="20.73" y2="6.96"/><line x1="12" y1="12.01" x2="12" y2="21.01"/>',
    "inbox":          '<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "check-circle":   '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    "scale":          '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "award":          '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
    "shopping-cart":  '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    "flame":          '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 3Z"/>',
    "ticket":         '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2"/><path d="M13 17v2"/><path d="M13 11v2"/>',
    "utensils":       '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "trending-up":    '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "pie-chart":      '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "bar-chart":      '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "clock":          '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "map-pin":        '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "user":           '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "users":          '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "snowflake":      '<line x1="2" x2="22" y1="12" y2="12"/><line x1="12" x2="12" y1="2" y2="22"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/>',
    "key":            '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/>',
    "shield-check":   '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "shield":         '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "arrow-left":     '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "log-in":         '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>',
    "user-plus":      '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/>',
    "leaf":           '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "brain":          '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/>',
    "zap":            '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "building":       '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
    "download":       '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "activity":       '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "circle-check":   '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "heart":          '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
}


def icon(name: str, size: int = 16, cls: str = "") -> str:
    """Return an inline Lucide SVG icon, inheriting text colour via currentColor."""
    paths = _ICONS.get(name, "")
    if not paths:
        return ""
    css = f' class="{cls}"' if cls else ""
    return (
        f'<svg{css} xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:middle;flex-shrink:0;display:inline-block;">'
        f'{paths}</svg>'
    )


# ── PIN & Security ──────────────────────────────────────────────────────────

def generate_pin() -> str:
    """Generate a secure random 4-digit numeric PIN string."""
    return str(random.randint(1000, 9999))


# ── Impact Calculators ───────────────────────────────────────────────────────

def co2e_avoided(qty_kg: float) -> float:
    """~2.5 kg CO₂e avoided per kg of food rescued from landfill."""
    return round(qty_kg * 2.5, 2)


def meals_saved(qty_kg: float) -> int:
    """~2 meals per kg of food redistributed."""
    return int(qty_kg * 2)


# ── Time / Expiry ────────────────────────────────────────────────────────────

def hours_until(dt: datetime) -> float:
    """Return float hours remaining until dt (negative if past)."""
    if dt is None:
        return -1.0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = (dt - datetime.now(timezone.utc)).total_seconds()
    return diff / 3600.0


def format_countdown(dt: datetime) -> str:
    """Human-readable countdown string for pickup_deadline."""
    h = hours_until(dt)
    if h < 0:
        return "Expired"
    elif h < 1:
        return f"{int(h * 60)}m left"
    elif h < 24:
        return f"{h:.1f}h left"
    else:
        return f"{int(h // 24)}d {int(h % 24)}h left"


def is_urgent(dt: datetime) -> bool:
    """True when < 2 hours remain."""
    return 0 < hours_until(dt) < 2


# ── CSV Export ───────────────────────────────────────────────────────────────

def export_history_csv(records: list) -> str:
    """Convert donation_history docs to CSV string."""
    if not records:
        return ""
    fields = [
        "donor_name", "recipient_name", "food_category",
        "quantity_kg", "meals_saved", "co2e_avoided_kg", "completed_at",
    ]
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for r in records:
        row = {k: r.get(k, "") for k in fields}
        if isinstance(row.get("completed_at"), datetime):
            row["completed_at"] = row["completed_at"].strftime("%Y-%m-%d %H:%M UTC")
        row["meals_saved"] = row.get("meals_saved") or meals_saved(float(row.get("quantity_kg") or 0))
        row["co2e_avoided_kg"] = row.get("co2e_avoided_kg") or co2e_avoided(float(row.get("quantity_kg") or 0))
        writer.writerow(row)
    return out.getvalue()


# ── Logo Helpers ─────────────────────────────────────────────────────────────

def get_logo_b64(variant="blue") -> str:
    """Return base64 string for the brand logo in blue or white."""
    import base64
    from pathlib import Path
    base_dir = Path(__file__).parent
    target = base_dir / f"logo_{variant}.png"
    if not target.exists():
        target = base_dir / "logo.png"
    if not target.exists():
        return ""
    try:
        return base64.b64encode(target.read_bytes()).decode()
    except Exception:
        return ""


def get_logo_img(height: int = 42, variant: str = "blue", margin_right=10) -> str:
    """Return HTML <img> tag with blue/white logo."""
    b64 = get_logo_b64(variant)
    if not b64:
        return ""
    return (
        f'<img src="data:image/png;base64,{b64}" '
        f'alt="FoodLoop" '
        f'style="height:{height}px;width:auto;vertical-align:middle;margin-right:{margin_right}px;display:inline-block;object-fit:contain;">'
    )


def fmt_kg(val: float) -> str:
    return f"{val:,.1f} kg"


def fmt_num(val) -> str:
    return f"{int(val):,}"


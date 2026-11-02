"""
utils.py  -  FoodLoop shared utility functions
"""
import random
import io
import csv
from datetime import datetime, timezone


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


# estate-module-odoo18
A clean, didactic Odoo 18 module that implements a simple real‑estate workflow (properties, offers, property types & tags) while showcasing good practices: computed fields, onchange, smart buttons, manual ordering, actions & security.

---

## ✨ Features

- **Estate Property** (`estate.property`)
  - Status flow: `new → offer → accepted → sold / canceled`
  - Inline **Offers** with ✓ / ✗ buttons on list rows
  - Availability, expected/selling price, garden options & auto **total_area**
  - Statusbar, header buttons, notebook tabs
- **Offers** (`estate.property.offer`)
  - Accept / Refuse actions; auto set buyer/selling price on accept
  - Validity → **date_deadline** auto‑compute
  - Link to **Property Type** via `type_id` (for exercises)
- **Property Types** (`estate.property.type`)
  - Manual ordering with **sequence** (drag handle)
  - Smart buttons: **Offers** (via action) & **Properties** (via method)
  - Counts: `offer_count`, `property_count`
- **Tags** (`estate.property.tag`) with colors & many2many on property
- **Menus & Actions** pre‑wired for list/form navigation
- **Security** skeleton (`ir.model.access.csv`, groups) to extend

---

## 📁 Repository Structure

```
estate/
├─ __init__.py
├─ __manifest__.py
├─ security/
│  ├─ ir.model.access.csv
│  └─ res_groups.xml
├─ models/
│  ├─ __init__.py
│  ├─ estate_mixin.py            # (optional) shared helpers
│  ├─ estate_property.py
│  ├─ estate_property_offer.py
│  ├─ estate_property_tag.py
│  └─ estate_property_type.py
└─ views/
   ├─ estate_menus.xml
   ├─ estate_property_views.xml
   ├─ estate_property_offer_views.xml
   ├─ estate_property_tag_views.xml
   ├─ estate_property_type_views.xml
   └─ res_users_views.xml        # example inheritance (optional)
```

> Tip: Keep XML view files focused per model to stay maintainable.

---

## 🚀 Installation

1. Ensure **Odoo 18** environment is running (Python 3.12).
2. Clone / copy this module into your custom addons path, e.g.:
   ```bash
   /mnt/d/Work/Internship/Nashta/odoo18/training/estate
   ```
3. Update the addons path in `odoo.conf` if needed.
4. Restart Odoo and upgrade the module:
   ```bash
   ./odoo-bin -c odoo.conf -u estate
   ```

---

## 🧭 Usage Guide

### Property Types
- Open **Estate → Configuration → Property Types**.
- Drag the **handle** to manually reorder by `sequence`.
- Open a type; use smart buttons:
  - **Offers** → opens filtered `estate.property.offer` with `type_id = active_id`.
  - **Properties** → opens related `estate.property` by `property_type_id`.

### Properties
- Create a **Property**; fill key info (title, expected price, availability).
- Garden fields become visible only if **Garden** is checked.
- **Total Area** computed from living area + garden area.
- **Offers** tab: users can add offers inline; accept/refuse with ✓ / ✗.
- Header buttons: **Sold** / **Cancel** (disabled if already terminal).

### Offers
- Set **price**, **partner**, and optional **validity** (days).
- **date_deadline** auto‑computes; Accept sets buyer/selling values.
- Offer’s `type_id` links back to **Property Type** (for smart button demo).

---

## 🧩 Key Technical Notes

- **Computed fields** use `@api.depends` and are stored when appropriate.
- **`@api.model_create_multi`** for efficient batch creation (v18).
- **Smart button action**:
  - XML action id: `action_estate_property_offer`
  - Called in form with: `name="%(action_estate_property_offer)d"` and `type="action"`.
  - Uses domain: `[('type_id', '=', active_id)]` so context comes from the form.
- **Manual ordering**:
  - List view: `default_order="sequence,name"` and `<field name="sequence" widget="handle"/>`.
- **View inheritance safety**:
  - When inheriting `res.users`, don’t put `active_id` in context; use `uid` or remove context unless needed.

---

## 🧪 Dev Tips

- Use **Developer mode** to inspect views and fields.
- For XML parse issues: check quotes and avoid unescaped `<` in attributes.
- If a smart button disappears:
  - Ensure the `<div class="oe_button_box" name="button_box">` is inside `<sheet>`.
  - Check the button’s `type` (`action` vs `object`) and that the action id exists.
- For `External ID not found`:
  - Confirm the **action** is defined **before** the view referencing it, or in the same data list in `__manifest__.py`.

---

## 📝 Manifest Example

```python
# __manifest__.py
{
    "name": "Estate",
    "version": "18.0.1.0.0",
    "summary": "Training module for real-estate workflow",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        # "views/res_users_views.xml",  # optional
    ],
    "application": True,
}
```

---

## 🔐 Security

- Start with basic **read/write** rules for your models.
- Add groups if you need separate rights for Sales / Manager.
- Keep ACLs in `security/ir.model.access.csv` minimal for training, expand later.

---

## 🤝 Acknowledgments

- Built for Odoo 18 training and exercises (offers ✓ / ✗, smart buttons, manual ordering).
- Thanks to the Odoo community for conventions and best practices.

---

## 📄 License

This training module is provided under the MIT License. See `LICENSE` (or update as needed).

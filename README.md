# WordCountStatus

A tiny Sublime Text plugin that adds a compact word count to the status bar.

**Example:**

📝36 words

It automatically updates as you type and shows the word count for the **selection** when text is highlighted, or the **entire file** when nothing is selected.

---

## ✨ Features

- 📝 Compact status bar display: `📝36 words`
- ✂️ Selection-aware: shows word count for highlighted text
- ⚡ Live updates while typing
- 🪶 Lightweight and fast (throttled updates)
- 🧩 No UI clutter — keeps Sublime’s native line/character stats intact

---

## 📦 Installation

### Package Control (recommended)

1. Press `Ctrl+Shift+P`
2. Select **Package Control: Install Package**
3. Search for **WordCountStatus**
4. Press Enter

---

### Manual Installation

1. Open Sublime → **Preferences → Browse Packages…**
2. Create a folder named `WordCountStatus`
3. Copy `word_count_status.py` into that folder
4. Restart Sublime Text

---

## 🧠 How It Works

- Counts words using a simple, reliable pattern
- If text is selected → counts selection
- If nothing selected → counts entire file
- Updates automatically on:
  - typing
  - selection change
  - file load/save
  - tab switch

---

## Settings (Optional)

You can disable the word count display.

1. Open **Preferences → Settings**
2. Add the following to your **User** settings (right panel):

```json
{
  "word_count_status_enabled": false
}

import sublime
import sublime_plugin
import re
import time

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
STATUS_KEY = "word_count_status"
MIN_INTERVAL_SEC = 0.25  # throttle updates


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def get_word_count(view: sublime.View) -> int:
    sel = view.sel()
    # If any selection is non-empty, count the first non-empty selection
    for r in sel:
        if not r.empty():
            return count_words(view.substr(r))
    # Otherwise count whole file
    return count_words(view.substr(sublime.Region(0, view.size())))


def status_enabled() -> bool:
    s = sublime.load_settings("Preferences.sublime-settings")
    return s.get("word_count_status_enabled", True)


def update_status(view: sublime.View) -> None:
    if view.is_loading() or view.settings().get("is_widget"):
        return

    if not status_enabled():
        view.erase_status(STATUS_KEY)
        return

    n = get_word_count(view)
    view.set_status(STATUS_KEY, f"📝{n:,} words")


class WordCountStatusListener(sublime_plugin.EventListener):
    def __init__(self):
        self._last = 0.0

    def _throttled(self, view: sublime.View):
        now = time.time()
        if now - self._last < MIN_INTERVAL_SEC:
            return
        self._last = now
        update_status(view)

    def on_activated_async(self, view):
        self._throttled(view)

    def on_modified_async(self, view):
        self._throttled(view)

    def on_selection_modified_async(self, view):
        self._throttled(view)

    def on_load_async(self, view):
        self._throttled(view)

    def on_post_save_async(self, view):
        self._throttled(view)


class WordCountStatusToggleCommand(sublime_plugin.WindowCommand):
    SETTING_KEY = "word_count_status_enabled"

    def run(self):
        s = sublime.load_settings("Preferences.sublime-settings")
        enabled = s.get(self.SETTING_KEY, True)
        s.set(self.SETTING_KEY, not enabled)
        sublime.save_settings("Preferences.sublime-settings")

        for w in sublime.windows():
            for v in w.views():
                if v.settings().get("is_widget"):
                    continue
                if enabled:
                    v.erase_status(STATUS_KEY)
                else:
                    update_status(v)


def plugin_loaded():
    # Respect setting on load and initialize open views
    for w in sublime.windows():
        for v in w.views():
            if not v.settings().get("is_widget"):
                update_status(v)

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import subprocess


class WorktrackerExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        stdin = event.get_argument() or ""
        res = subprocess.run(f"echo -e '{stdin}' | worktracker", capture_output=True, shell=True)
        output = res.stdout.decode('utf-8')
        error = res.stderr.decode('utf-8')

        description = ""
        name = ""

        if len(error) > 0:
            description = error
            name = "Error"
        else:
            description = output
            out_lines = output.splitlines()
            last_line = out_lines[-1] if len(out_lines) > 0 else ""
            if "Total time" in last_line:
                name = last_line

        description = '\n' + description

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=name,
                                         description=description,
                                         on_enter=HideWindowAction()))

        return RenderResultListAction(items)

if __name__ == '__main__':
    WorktrackerExtension().run()

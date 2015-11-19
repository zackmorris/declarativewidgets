# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import requests

from IPython.utils.traitlets import Unicode # Used to declare attributes of our widget

from .urth_widget import UrthWidget
from .urth_exception import UrthException


class Import(UrthWidget):
    """
    A Widget for interacting with the 'import' route in the NB server for installing bower components.
    """
    url = Unicode('', sync=True)
    counter = 0

    def __init__(self, **kwargs):
        self.log.info("Created a new Import widget.")

        self.on_msg(self._handle_custom_event_msg)
        super(Import, self).__init__(**kwargs)

    def _url_changed(self, old, new):
        self.log.info("Got post url {}...".format(new))
        if self._url_is_valid(new):
            self._send_update("importready", True)
            self.ok()
        else:
            self.error("Invalid or Unreacheable url {}".format(new))

    def _handle_custom_event_msg(self, _, content):
        event = content.get('event', '')
        if event == 'import':
            self._import(content.get('package', {}))

    def _url_is_valid(self, url):
        return True

    def _import(self, package):
        self.log.info("Installing package {0}.".format(package))
        try:
            payload = {"package": package}
            r = requests.post(self.url, json=payload)
            if r.status_code == 200:
                self.counter += 1
                self._send_update("installed", self.counter)
                self.ok()
            else:
                self.error("Error while installing package: {0}".format(str(r.status_code)))
        except requests.exceptions.RequestException as e:
            self.error(str(e))
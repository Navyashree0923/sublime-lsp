import os
import hashlib
import sublime

from urllib.request import urlretrieve

from LSP.plugin import (
    AbstractPlugin,
    register_plugin,
    filename_to_uri,
    unregister_plugin,
)


SERVER_URL = "https://jar-download.com/artifacts/com.github.camel-tooling/camel-lsp-server/1.6.0/source-code"
SERVER_SHA256:"LlCbTPYXMCvIhxSkEFTbI9872EnQeWfubqX7HAAtPd8"

def plugin_unloaded():
    unregister_plugin(CamelPlugin)


class CamelPlugin(AbstractPlugin):

    file_associations = [
        {
            "pattern": "**/*.sublime-snippet",
            "systemId": "$storage_uri/cache/sublime/sublime-snippet.xsd"
        },
        {
            "pattern": "**/*.tmPreferences",
            "systemId": "$storage_uri/cache/sublime/tmPreferences.xsd"
        },
        {
            "pattern": "**/*.tmTheme",
            "systemId": "$storage_uri/cache/sublime/tmTheme.xsd"
        },
        {
            "pattern": "**/*.hidden-tmTheme",
            "systemId": "$storage_uri/cache/sublime/tmTheme.xsd"
        }
    ]

    settings = None
    settings_name = "LSP-camel.sublime-settings"
    settings_resource_path = "Packages/{}/{}".format(__package__, settings_name)

    @classmethod
    def name(cls):
        return "Camel"

    @classmethod
    def configuration(cls):
        if cls.settings is None:
            cls.settings = sublime.load_settings(cls.settings_name)
        return (cls.settings, cls.settings_resource_path)

    @classmethod
    def needs_update_or_installation(cls):
        try:
            # check hash
            with open(cls.server_jar(), "rb") as stream:
                checksum = hashlib.sha256(stream.read()).hexdigest()
                return checksum.lower() != SERVER_SHA256.lower()
        except OSError:
            pass

        return True

    @classmethod
    def install_or_update(cls):
        server_dir = cls.server_dir()
        server_jar = cls.server_jar()

        # download new server binary
        os.makedirs(server_dir, exist_ok=True)
        urlretrieve(url=SERVER_URL, filename=server_jar)
        if cls.needs_update_or_installation():
            os.remove(server_jar)
            raise RuntimeError("Error downloading Camel server binary!")

        # clear old server binaries
        for file_name in os.listdir(server_dir):
            if os.path.splitext(file_name)[1].lower() != ".jar":
                continue

            try:
                file_path = os.path.join(server_dir, file_name)
                if not os.path.samefile(file_path, server_jar):
                    os.remove(file_path)
            except FileNotFoundError:
                pass

    @classmethod
    def on_pre_start(cls, window, initiating_view, workspace_folders, configuration):
        configuration.command = [
            "java", "-jar", cls.server_jar()
        ] + cls.settings.get("java_vmargs", [])

    @classmethod
    def on_settings_changed(cls, dotted):
        # prepend a list of fixed file associations
        dotted.set(
            "xml.fileAssociations",
            cls.file_associations + (dotted.get("xml.fileAssociations") or [])
        )
        # adjust working dir to package storage directory
        dotted.set("xml.server.workDir", cls.server_dir())

    @classmethod
    def additional_variables(cls):
        return {
            "package_path": cls.package_dir(),
            "storage_path": cls.server_dir(),
            "package_uri": cls.package_uri(),
            "storage_uri": cls.server_uri()
        }

    # internal methods

    @classmethod
    def package_dir(cls):
        return os.path.join(sublime.packages_path(), __package__)

    @classmethod
    def package_uri(cls):
        return filename_to_uri(cls.package_dir())

    @classmethod
    def server_dir(cls):
        return os.path.join(cls.storage_path(), __package__)

    @classmethod
    def server_uri(cls):
        return filename_to_uri(cls.server_dir())

    @classmethod
    def server_jar(cls):
        return os.path.join(cls.server_dir(), SERVER_URL.rsplit("/", 1)[1])


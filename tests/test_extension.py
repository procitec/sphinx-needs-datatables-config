from sphinx_needs_datatables_config.extension import setup


class FakeConfig:
    needs_datatable_config = {}


class FakeBuilder:
    format = "html"


class FakeApp:
    def __init__(self) -> None:
        self.builder = FakeBuilder()
        self.config = FakeConfig()
        self.extensions = []
        self.config_values = []
        self.directives = []
        self.events = []

    def setup_extension(self, name: str) -> None:
        self.extensions.append(name)

    def add_directive(self, *args, **kwargs) -> None:
        self.directives.append((args, kwargs))

    def add_config_value(self, *args, **kwargs) -> None:
        self.config_values.append((args, kwargs))

    def connect(self, event: str, callback) -> None:
        self.events.append((event, callback))


def test_setup_registers_dependency_and_config() -> None:
    app = FakeApp()

    metadata = setup(app)

    assert "sphinx_needs" in app.extensions
    assert app.directives[0][0][0] == "needtable"
    assert app.directives[0][1]["override"] is True
    assert app.config_values[0][0][0] == "needs_datatable_config"
    assert app.events[0][0] == "builder-inited"
    assert "version" in metadata
    assert metadata["parallel_read_safe"] is True

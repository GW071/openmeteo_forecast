from mcp.server.fastmcp import FastMCP
mcp = FastMCP(
    name= "OpenMeteo Forecast Server",
)

def autoload():
    import importlib, pkgutil, pathlib, sys, logging

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    pkg_name = __name__
    pkg_path = pathlib.Path(__file__).parent

    for finder, name, ispkg in pkgutil.iter_modules([str(pkg_path)]):
        if name.startswith("_"):
            continue
        full_name = f"{pkg_name}.{name}"
        try:
            importlib.import_module(full_name)
            logging.info("[autoload] imported %s", full_name)
        except Exception as e:
            logging.exception("[autoload] failed to import %s: %s", full_name, e)
from tools import mcp,autoload


def main():
    autoload()
    mcp.run(transport="stdio")
    # mcp.run(transport="stdio")

if __name__ == "__main__":
    main()

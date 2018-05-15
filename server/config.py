import codecs
import sys

import toml


default_config = """
title = \"DND Backend Config\"

[database]
address = \"localhost\"
port = 5432
username = \"develop\"
password = \"\"
"""


def getConfigDict(configPath):
    configDict = None
    try:
        configRaw = codecs.open(configPath, "rb", encoding='utf-8').read()
    except IOError:
        # Failed to read, create new config file.
        fh = open(configPath, "w")
        fh.write(default_config)
        fh.close()
        configRaw = codecs.open(configPath, "rb", encoding='utf-8').read()
    try:
        configDict = toml.loads(configRaw)
    except toml.TomlDecodeError as tomlExp:
        for string in tomlExp.args:
            print("ERROR: Invalid TOML syntax. " + string, file=sys.stderr)
        sys.exit(1)
    except TypeError as typeExp:
        for string in typeExp.args:
            print("ERROR: Invalid config file. " + string, file=sys.stderr)
        sys.exit(1)
    except BaseException:
        print(
            "ERROR: Invalid config file. Please make sure it is"
            " UTF-8 encoded and complies TOML specification.",
            file=sys.stderr)
        print(
            "Please review TOML specification at: https://github.com/toml-lang/toml",
            file=sys.stderr)
        sys.exit(1)
    return configDict

val = getConfigDict("config.toml")

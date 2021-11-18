import pathlib, os, sys
from yazaki.app import Yazaki

from dotenv import load_dotenv

app_path = f"{pathlib.Path().absolute()}"
env_path = f"{app_path}/.env"
load_dotenv(env_path)

y = Yazaki()


def main():
    doc = y.get_gedi()
    if doc != False:
        print("success")
        return

    print("error load")


if __name__ == "__main__":
    main()
    sys.exit(0)

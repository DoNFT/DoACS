from enum import Enum
from pathlib import Path

import environs


class IPFSServiceEnum(Enum):
    PINATA = "PINATA"
    NFT_STORAGE = "NFT_STORAGE"
    IPFS = "IPFS"


PROJECT_DIR = Path(__file__).parent.parent.resolve()
BACKEND_DIR = PROJECT_DIR / "backend"

env = environs.Env()
env.read_env(BACKEND_DIR / ".env", recurse=False)

HOST = env.str("HOST", "127.0.0.1")
PORT = env.int("PORT", 8000)
IPFS_API_HOST = env.str("IPFS_API_HOST", default="")
IPFS_API_TIMEOUT = env.float("IPFS_API_TIMEOUT", default=30.0)
PINATA_JWT_TOKEN = env("PINATA_JWT_TOKEN", default=None)
IPFS_SERVICE = env.enum("IPFS_SERVICE", type=IPFSServiceEnum, ignore_case=True, default="PINATA")
NFT_STORAGE_API_TOKEN = env("NFT_STORAGE_API_TOKEN", default=None)
IPFS_PROJECT_ID = env.str("IPFS_PROJECT_ID", default="")
IPFS_PROJECT_SECRET = env.str("IPFS_PROJECT_SECRET", default="")
PASSWORD = env.str("PASSWORD", default="")
FILE_NAME_ACCESSES = env.str("FILE_NAME_ACCESSES")

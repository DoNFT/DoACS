from enum import Enum
from pathlib import Path

import environs

from ipfs.service import IPFSServiceEnum


class Environment(Enum):
    DEV = "DEV"
    STAGE = "STAGE"
    PROD = "PROD"



PROJECT_DIR = Path(__file__).parent.parent.resolve()
BACKEND_DIR = PROJECT_DIR / "backend"

env = environs.Env()
env.read_env(BACKEND_DIR / ".env", recurse=False)

ENVIRONMENT = env.enum("ENVIRONMENT", type=Environment, ignore_case=True)

HOST = env.str("HOST", "127.0.0.1")
PORT = env.int("PORT", 8000)
WORKERS_NUM = env.int("WORKERS_NUM", 1)
WORKERS = env.int("WORKERS", 3)
PUBLIC_HOST = env.str("PUBLIC_HOST", "localhost")
IPFS_API_HOST = env.str("IPFS_API_HOST")
IPFS_API_TIMEOUT = env.float("IPFS_API_TIMEOUT", default=30.0)
IPFS_SERVICE = env.enum("IPFS_SERVICE", type=IPFSServiceEnum, ignore_case=True, default="NFT_STORAGE")
NFT_STORAGE_API_TOKEN = env("NFT_STORAGE_API_TOKEN", default=None)

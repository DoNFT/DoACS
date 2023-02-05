from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ipfs.service import IPFSServiceEnum
from ipfs.service import wrapper_ipfs_service
from settings import IPFS_API_HOST
from settings import IPFS_API_TIMEOUT
from settings import IPFS_PROJECT_ID
from settings import IPFS_PROJECT_SECRET
from settings import IPFS_SERVICE
from settings import NFT_STORAGE_API_TOKEN
from settings import PINATA_JWT_TOKEN

if IPFS_SERVICE == IPFSServiceEnum.IPFS:
    wrapper_ipfs_service.init(IPFS_API_TIMEOUT, IPFS_SERVICE, (IPFS_API_HOST, IPFS_PROJECT_ID, IPFS_PROJECT_SECRET))
elif IPFS_SERVICE == IPFSServiceEnum.NFT_STORAGE:
    wrapper_ipfs_service.init(IPFS_API_TIMEOUT, IPFS_SERVICE, NFT_STORAGE_API_TOKEN)
elif IPFS_SERVICE == IPFSServiceEnum.PINATA:
    wrapper_ipfs_service.init(IPFS_API_TIMEOUT, IPFS_SERVICE, PINATA_JWT_TOKEN)
ipfs_service = wrapper_ipfs_service.get_ipfs_service()
ipfs_router = wrapper_ipfs_service.get_router()

api_router = APIRouter(prefix="/api")
api_router.include_router(ipfs_router)
app = FastAPI(title=str(IPFS_SERVICE.value))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Origin"],
)

app.include_router(api_router)

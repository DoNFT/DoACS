from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile
from settings import FILE_NAME_ACCESSES
from settings import PASSWORD
from starlette.responses import Response

from .service import wrapper_ipfs_service

router = APIRouter(prefix="/ipfs")


# @router.post("/add_new_address")
# async def add_address(new_address, psw):
#     if psw != PASSWORD:
#         raise HTTPException(status_code=400, detail=f"Wrong password")
#
#     with open(FILE_NAME_ACCESSES) as f:
#         line = None
#         for line in f:
#             pass
#         last_line = line
#     if last_line:
#         addresses = await wrapper_ipfs_service.get_ipfs_service().cat(last_line)
#         addresses = addresses.decode("utf-8") + '\n'
#     else:
#         addresses = ""
#     addresses += new_address
#     new_hash = await wrapper_ipfs_service.get_ipfs_service().add(bytes(addresses, 'utf-8'))
#     with open(FILE_NAME_ACCESSES, "a") as f:
#         f.write('\n' + new_hash)


# @router.post("/get_address")
# async def get_address(payload: UploadFile = File(...)) -> str:
#     """
#     Get ipfs address of file
#     Returns: ipfs Hash
#     """
#     hash = await wrapper_ipfs_service.get_ipfs_service().add(payload.file.read(), only_hash=True)
#     return f"ipfs://{hash}"


@router.post("/upload")
async def upload(payload: UploadFile = File(...)) -> str:
    """
    Uploads file to ipfs
    Returns: ipfs Hash
    """
    # if not await wrapper_ipfs_service.get_ipfs_service().check_access(owner_address):
    #     raise HTTPException(status_code=400, detail=f"This address is not accessible {owner_address}")
    hash = await wrapper_ipfs_service.get_ipfs_service().add(payload.file.read())
    return f"ipfs://{hash}"


@router.get("/cat")
async def cat(ipfs_addr: str):
    """
    Cats the given ipfs addr
    Args:
        ipfs_addr: given ipfs hash

    Returns:
        file content
    """
    cid = wrapper_ipfs_service.get_ipfs_service().extract_cid(ipfs_addr)
    if cid is None:
        cid = ipfs_addr
        # raise ValueError(f'Cannot extract cid from {ipfs_addr}')
    payload = await wrapper_ipfs_service.get_ipfs_service().cat(cid)
    return Response(content=payload, media_type="application/octet-stream")


@router.get("/check_mimetype")
async def check_mimetype(url: str) -> str:
    content_type = await wrapper_ipfs_service.get_ipfs_service().get_meta_info(url, info_key='content-type')
    return content_type

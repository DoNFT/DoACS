from fastapi import Form

from .router import router
from .service import wrapper_ipfs_service


@router.post("/publish")
async def name_publish(hash: str = Form(...), key_name: str = Form(...)):
    return await wrapper_ipfs_service.get_ipfs_service().publish(hash, key_name)


@router.post("/key_gen")
async def key_gen(name: str = Form(...)):
    return await wrapper_ipfs_service.get_ipfs_service().key_gen(name)


@router.post("resolve")
async def resolve(path: str = Form(...)):
    return await wrapper_ipfs_service.get_ipfs_service().resolve(path)

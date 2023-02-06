from fastapi import Form

from .router import router
from .service import IPFSService
from .service import ipfs_service

if not isinstance(ipfs_service, IPFSService):
    raise TypeError(f'ipfs_service must be IPFSService. Get {str(ipfs_service)}')


@router.post("/publish")
async def name_publish(hash: str = Form(...), key_name: str = Form(...)):
    return await ipfs_service.publish(hash, key_name)


@router.post("/key_gen")
async def key_gen(name: str = Form(...)):
    return await ipfs_service.key_gen(name)


@router.post("resolve")
async def resolve(path: str = Form(...)):
    return await ipfs_service.resolve(path)

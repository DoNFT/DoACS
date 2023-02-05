from fastapi import File
from fastapi import Form
from fastapi import UploadFile

from .router import router
from .service import wrapper_ipfs_service


@router.post("/publish")
async def name_publish(hash: str = Form(...), key_name: str = Form(...)):
    res = await wrapper_ipfs_service.get_ipfs_service().publish(hash, key_name)
    ipns_url, ipfs_url = eval(res)['Name'], eval(res)['Value']
    return ipns_url, ipfs_url


# @router.post("/create_ipns")
# async def create(payload_file: UploadFile = File(...), signature: str = Form(...)):
#     ipfs_hash = await wrapper_ipfs_service.get_ipfs_service().add(payload_file.file.read())
#     ipfs_hash = ipfs_hash.replace('ipfs://', '')
#     ipns_key = await generate_ipns_key()
#     ipns_url = await wrapper_ipfs_service.get_ipfs_service().key_gen(ipns_key)
#     ipns_url = eval(ipns_url)['Id']
#     res = await wrapper_ipfs_service.get_ipfs_service().publish(ipfs_hash, ipns_url)
#     return ipns_key, eval(res)['Name'],


# @router.post("/update_ipns")
# async def update(payload_new_file: UploadFile = File(...), signature: str = Form(...), ipns_url: str = Form(...)):
#     ipfs_hash = await wrapper_ipfs_service.get_ipfs_service().add(payload_new_file.file.read())
#     ipfs_hash = ipfs_hash.replace('ipfs://', '')
#     res = await wrapper_ipfs_service.get_ipfs_service().publish(ipfs_hash, ipns_url)
#     return res


@router.post("/key_gen")
async def key_gen(name: str = Form(...)):
    res = await wrapper_ipfs_service.get_ipfs_service().key_gen(name)
    ipns_name, ipns_cid = eval(res)['Name'], eval(res)['Id']
    return ipns_name, ipns_cid


@router.post("resolve")
async def resolve(ipns_url: str = Form(...)):
    return await wrapper_ipfs_service.get_ipfs_service().resolve(ipns_url)


async def key_list():
    return await wrapper_ipfs_service.get_ipfs_service().key_list()


async def generate_ipns_key():
    keys = await key_list()
    ipns_keys = set([k['Name'] for k in eval(keys)['Keys']])
    i = 0
    while True:
        new_name = f'key_{i}'
        if new_name not in ipns_keys:
            break
        i += 1
    return new_name

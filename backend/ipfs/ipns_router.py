import asyncio
import json

from fastapi import Form
from fastapi import HTTPException

from settings import FILE_NAME_ACCESSES
from .access_controller import AccessController, Access
from .router import router
from .service import wrapper_ipfs_service

access_controller = AccessController(FILE_NAME_ACCESSES)
loop = asyncio.get_event_loop()
foo = loop.run_until_complete(access_controller.init())


@router.post("/publish")
async def name_publish(hash: str = Form(...), key_name: str = Form(...), wallet: str = Form(...)):
    # if not await wrapper_ipfs_service.get_ipfs_service().check_access(owner_address):
    #     raise HTTPException(status_code=400, detail=f"This address is not accessible {owner_address}")
    ipns_url = ''
    ipfs_url = ''
    file_accesses = await access_controller.get_file_accesses(key_name)
    if not file_accesses:
        await access_controller.create_new_addr(key_name, wallet)
        res = await wrapper_ipfs_service.get_ipfs_service().publish(hash, key_name)
        ipns_url, ipfs_url = eval(res)['Name'], eval(res)['Value']
        await update_cron_file(ipns_url, ipfs_url.replace('/ipfs/', ''))
    else:
        f = False
        for wall, access in file_accesses:
            if wall == wallet and access >= Access.EDIT.value:
                f = True
                res = await wrapper_ipfs_service.get_ipfs_service().publish(hash, key_name)
                ipns_url, ipfs_url = eval(res)['Name'], eval(res)['Value']
                await update_cron_file(ipns_url, ipfs_url.replace('/ipfs/', ''))
        if not f:
            raise ValueError(f'this wallet {wallet} has no rights to change')

    return ipns_url, ipfs_url


@router.get("/get_files_from_wallet")
async def get_files_from_wallet(wallet: str):
    return json.dumps(await access_controller.get_files_from_wallet(wallet))


@router.get("/get_file_accesses")
async def get_file_accesses(file_addr: str):
    return json.dumps(await access_controller.get_file_accesses(file_addr))


async def update_cron_file(ipns_url, ipfs_url):
    with open('ipns_keys.json', 'r') as f:
        ipns_keys = json.load(f)
        ipns_keys[ipns_url] = ipfs_url
    with open('ipns_keys.json', 'w') as f:
        json.dump(ipns_keys, f)


async def remove_ipns_url(ipns_url):
    with open('ipns_keys.json', 'r') as f:
        ipns_keys = json.load(f)
    ipns_key = ipns_url.split('/')[-1]
    if ipns_key in ipns_keys:
        del ipns_keys[ipns_key]
        with open('ipns_keys.json', 'w') as f:
            json.dump(ipns_keys, f)


@router.post("/change_access_to_file")
async def change_access_to_file(file_addr: str = Form(...), wallet: str = Form(...), file_access: int = Form(...),
                                owner_wallet: str = Form(...)):
    await access_controller.change_access_to_file(file_addr, wallet, file_access, owner_wallet)


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
    # if not await wrapper_ipfs_service.get_ipfs_service().check_access(owner_address):
    #     raise HTTPException(status_code=400, detail=f"This address is not accessible {owner_address}")

    res = await wrapper_ipfs_service.get_ipfs_service().key_gen(name)
    ipns_name, ipns_cid = eval(res)['Name'], eval(res)['Id']
    return ipns_name, ipns_cid


@router.post("remove")
async def remove(ipns_url: str = Form(...), owner_address: str = Form(...)):
    # if not await wrapper_ipfs_service.get_ipfs_service().check_access(owner_address):
    #     raise HTTPException(status_code=400, detail=f"This address is not accessible {owner_address}")
    if await access_controller.get_access(owner_address, ipns_url) < Access.OWNER:
        raise HTTPException(status_code=400, detail=f"This address is not accessible {owner_address}")
    res = await wrapper_ipfs_service.get_ipfs_service().remove(ipns_url)
    await remove_ipns_url(ipns_url)
    return res


@router.get("/get_keys")
async def get_keys():
    with open('ipns_keys.json', 'r') as f:
        ipns_keys = json.load(f)
    return ipns_keys


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

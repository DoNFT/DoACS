import json
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Union, Dict, List

from ipfs.service import wrapper_ipfs_service


class Access(Enum):
    READ = 0
    EDIT = 1
    OWNER = 2
    ADMIN = 3


ACCESS_TO_STR = {
    Access.READ.value: 'read',
    Access.EDIT.value: 'write',
    Access.OWNER.value: 'owner',
    Access.ADMIN.value: 'admin',
}


class ConsistencyError(Exception):
    pass


class PermissionDenied(Exception):
    pass


class AccessController:
    def __init__(self, path_to_ipfs_access_file: Union[Path, str]):
        self._path_to_ipfs_access_file = Path(path_to_ipfs_access_file)
        self._file_to_wallets: Dict[str, List[List[str, int]]] = dict()
        self._wallet_to_files: Dict[str, List[List[Union[str, int]]]] = dict()

    async def init(self):
        self._file_to_wallets: Dict[str, List[List[str, int]]] = await self._read_access_file()

        self._wallet_to_files: Dict[str, List[List[Union[str, int]]]] = self._generate_wallet_to_files()

    async def _read_access_file(self) -> Dict[str, List[List[Union[str, int]]]]:
        with open(self._path_to_ipfs_access_file) as f:
            line = None
            for line in f:
                pass
            last_line = line
        addr_to_wallet = dict()
        if last_line:
            addr_to_wallet = await wrapper_ipfs_service.get_ipfs_service().cat(last_line)
            addr_to_wallet = json.loads(addr_to_wallet)
        return addr_to_wallet

    async def _save_access_file(self):
        json_dump = json.dumps(self._file_to_wallets).encode('utf-8')
        new_hash = await wrapper_ipfs_service.get_ipfs_service().add(json_dump)
        with open(self._path_to_ipfs_access_file, "a") as f:
            f.write('\n' + new_hash)

    @staticmethod
    def _convert_to_set(ll: List[List]):
        res = set([tuple(l) for l in ll])
        return res

    async def _consistency_check(self):
        addr_to_wallet = await self._read_access_file()
        addr = ''
        try:
            for addr, files in self._file_to_wallets.items():
                if self._convert_to_set(addr_to_wallet[addr]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {addr_to_wallet[addr]} {files}')
        except KeyError:
            raise ConsistencyError(f'error wallet_to_files. not find {addr}')

        try:
            for addr, files in addr_to_wallet.items():
                if self._convert_to_set(self._file_to_wallets[addr]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {self._file_to_wallets[addr]} {files}')
        except KeyError:
            raise ConsistencyError(f'error wallet_to_files. not find {addr}')

        tmp_wallet_to_files = self._generate_wallet_to_files()
        wallet = ''
        try:
            for wallet, files in self._wallet_to_files.items():
                if self._convert_to_set(tmp_wallet_to_files[wallet]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {tmp_wallet_to_files[wallet]} {files}')
        except KeyError:
            raise ConsistencyError(f'error wallet_to_files. not find {wallet}')

        try:
            for wallet, files in tmp_wallet_to_files.items():
                if self._convert_to_set(self._wallet_to_files[wallet]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {self._wallet_to_files[wallet]} {files}')
        except KeyError:
            raise ConsistencyError(f'error wallet_to_files. not find {wallet}')

    # def _generate_file_to_wallets(self):
    #     file_to_wallets = defaultdict(list)
    #     for wall, files in self._wallet_to_files.items():
    #         for file, access in files:
    #             file_to_wallets[file].append((wall, access))
    #     return file_to_wallets

    def _generate_wallet_to_files(self):
        wallet_to_files = defaultdict(list)
        for file, walls in self._file_to_wallets.items():
            for wall, access in walls:
                wallet_to_files[wall].append((file, access))
        return wallet_to_files

    async def get_files_from_wallet(self, wallet):
        files = []
        for file, access in self._wallet_to_files[wallet]:
            files.append([file, ACCESS_TO_STR[access]])
        return files

    async def get_file_accesses(self, file_addr):
        file_accesses = []
        wallets = self._file_to_wallets.get(file_addr, [])
        for wall, access in wallets:
            file_accesses.append([wall, ACCESS_TO_STR[access]])
        return file_accesses

    async def change_access_to_file(self, file_addr: str, wallet: str, file_access: int, owner_wallet: str):
        if wallet == owner_wallet:
            raise ValueError("Can't change wallet owner")
        if file_access not in [-1, 0, 1]:
            return
        await self._consistency_check()
        f = False
        for wall, access in self._file_to_wallets[file_addr]:
            if wall != owner_wallet:
                continue
            f = True
            if access < Access.OWNER.value:
                raise PermissionDenied(f'{owner_wallet} does not have owner access')
        if not f:
            raise PermissionDenied(f'{owner_wallet} does not have owner access')
        f = False
        new_wallets = []
        for wall, access in self._file_to_wallets[file_addr]:
            if wall == wallet:
                f = True
                if file_access == -1:
                    continue
                else:
                    new_wallets.append([wall, int(file_access)])
            else:
                new_wallets.append([wall, access])
        if not f and file_access in [0, 1]:
            new_wallets.append([wallet, int(file_access)])
        self._file_to_wallets[file_addr] = new_wallets
        self._wallet_to_files = self._generate_wallet_to_files()
        await self._save_access_file()
        await self._consistency_check()

    async def create_new_addr(self, addr, wallet):
        await self._consistency_check()
        self._file_to_wallets[addr] = [[wallet, Access.OWNER.value]]
        self._wallet_to_files = self._generate_wallet_to_files()
        await self._save_access_file()
        await self._consistency_check()

    async def remove_addr(self, rm_addr):
        await self._consistency_check()
        del self._file_to_wallets[rm_addr]
        self._wallet_to_files = self._generate_wallet_to_files()
        await self._save_access_file()
        await self._consistency_check()

    async def get_access(self, wallet, file_addr):
        for addr, access in self._wallet_to_files[wallet]:
            if addr != file_addr:
                continue
            return access

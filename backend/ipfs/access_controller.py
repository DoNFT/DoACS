import json
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Union, Dict, List

from ipfs.cryptographer import FernetCryptographer
from ipfs.service import wrapper_ipfs_service
from settings import FERNET_KEY


class Access(Enum):
    READ = 0
    EDIT = 1
    OWNER = 3
    ADMIN = 2


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
        self._file_to_signs: Dict[str, List[List[str, int]]] = dict()
        self._sign_to_files: Dict[str, List[List[Union[str, int]]]] = dict()
        self._cryptographer = FernetCryptographer(FERNET_KEY)

    async def init(self):
        self._file_to_signs: Dict[str, List[List[str, int]]] = await self._read_access_file()

        self._sign_to_files: Dict[str, List[List[Union[str, int]]]] = self._generate_sign_to_files()

    async def _read_access_file(self) -> Dict[str, List[List[Union[str, int]]]]:
        with open(self._path_to_ipfs_access_file) as f:
            line = None
            for line in f:
                pass
            last_line = line
        addr_to_sign = dict()
        if last_line:
            addr_to_sign = await wrapper_ipfs_service.get_ipfs_service().cat(last_line)
            addr_to_sign = json.loads(addr_to_sign)
        return addr_to_sign

    async def _save_access_file(self):
        json_dump = json.dumps(self._file_to_signs).encode('utf-8')
        new_hash = await wrapper_ipfs_service.get_ipfs_service().add(json_dump)
        with open(self._path_to_ipfs_access_file, "a") as f:
            f.write('\n' + new_hash)

    @staticmethod
    def _convert_to_set(ll: List[List]):
        res = set([tuple(l) for l in ll])
        return res

    async def _consistency_check(self):
        addr_to_sign = await self._read_access_file()
        addr = ''
        try:
            for addr, files in self._file_to_signs.items():
                if self._convert_to_set(addr_to_sign[addr]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {addr_to_sign[addr]} {files}')
        except KeyError:
            raise ConsistencyError(f'error sign_to_files. not find {addr}')

        try:
            for addr, files in addr_to_sign.items():
                if self._convert_to_set(self._file_to_signs[addr]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {self._file_to_signs[addr]} {files}')
        except KeyError:
            raise ConsistencyError(f'error sign_to_files. not find {addr}')

        tmp_sign_to_files = self._generate_sign_to_files()
        sign = ''
        try:
            for sign, files in self._sign_to_files.items():
                if self._convert_to_set(tmp_sign_to_files[sign]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {tmp_sign_to_files[sign]} {files}')
        except KeyError:
            raise ConsistencyError(f'error sign_to_files. not find {sign}')

        try:
            for sign, files in tmp_sign_to_files.items():
                if self._convert_to_set(self._sign_to_files[sign]) != self._convert_to_set(files):
                    raise ConsistencyError(f'Not equal {self._sign_to_files[sign]} {files}')
        except KeyError:
            raise ConsistencyError(f'error sign_to_files. not find {sign}')

    # def _generate_file_to_wallets(self):
    #     file_to_wallets = defaultdict(list)
    #     for wall, files in self._wallet_to_files.items():
    #         for file, access in files:
    #             file_to_wallets[file].append((wall, access))
    #     return file_to_wallets

    def _generate_sign_to_files(self):
        sign_to_files = defaultdict(list)
        for file, signs in self._file_to_signs.items():
            for sign, access in signs:
                sign_to_files[sign].append((file, access))
        return sign_to_files

    async def get_files_from_sign(self, sign):
        sign = self._cryptographer.encrypt(sign)
        files = []
        for file, access in self._sign_to_files[sign]:
            files.append([file, ACCESS_TO_STR[access]])
        return files

    async def get_file_accesses(self, file_addr):
        file_accesses = []
        signs = self._file_to_signs.get(file_addr, [])
        for sign, access in signs:
            file_accesses.append([sign, ACCESS_TO_STR[access]])
        return file_accesses

    async def change_access_to_file(self, file_addr: str, sign: str, file_access: int):
        sign = self._cryptographer.encrypt(sign)
        if file_access not in [-1, 0, 1]:
            return
        await self._consistency_check()
        f = False
        new_signs = []
        for s, access in self._file_to_signs[file_addr]:
            if s == sign:
                f = True
                if file_access == -1:
                    continue
                else:
                    new_signs.append([s, int(file_access)])
            else:
                new_signs.append([s, access])
        if not f and file_access in [0, 1]:
            new_signs.append([sign, int(file_access)])
        self._file_to_signs[file_addr] = new_signs
        self._sign_to_files = self._generate_sign_to_files()
        await self._save_access_file()
        await self._consistency_check()

    async def create_new_addr(self, addr, sign):
        sign = self._cryptographer.encrypt(sign)
        await self._consistency_check()
        self._file_to_signs[addr] = [[sign, Access.OWNER.value]]
        self._sign_to_files = self._generate_sign_to_files()
        await self._save_access_file()
        await self._consistency_check()

    async def remove_addr(self, rm_addr):
        await self._consistency_check()
        del self._file_to_signs[rm_addr]
        self._sign_to_files = self._generate_sign_to_files()
        await self._save_access_file()
        await self._consistency_check()

    async def get_access(self, sign, file_addr):
        sign = self._cryptographer.encrypt(sign)
        for addr, access in self._sign_to_files[sign]:
            if addr != file_addr:
                continue
            return access

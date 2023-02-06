import StorageBack from "./StorageBack";
import FileCoinStorage from "./FileCoinStorage";
import {readData} from "@/crypto/helpers/DecentralizedStorage/CommonFunctions";
import {reactive, ref, watch} from "vue";

// export const storageTypeActive = ref(window.localStorage.getItem('metadata-storage') || 'own')
const storageTypeActive = ref('IPNS')
// watch(() => storageTypeActive.value, (newValue) => {
//     window.localStorage.setItem('metadata-storage', newValue)
// })
const storageControllerList = {
    // own: StorageBack,
    IPNS: FileCoinStorage
}

export default {
    constants: {
        IPFS_ONLY: false
    },
    getStorage: () => storageControllerList[storageTypeActive.value],
    async loadJSON(data = {}) {
        const controller = this.getStorage()
        return await controller.loadJSON(data)
    },
    async loadFile(file, ...args) {
        const controller = this.getStorage()
        return await controller.loadFile(file, ...args)
    },
    // ...FileCoinStorage,
    readData,
    async changeFile(newData, key){
        if(isFinite(key)) return await StorageBack.changeFile(newData, key);
        return await FileCoinStorage.changeFile(newData, key);
    },
    // only for IPNS
    async publish(ipfsKey, owner){
        return await FileCoinStorage.publish(ipfsKey, null, owner);
    },
    // only for IPNS
    async update(newIpfsKey, ipnsKey, owner){
        return await FileCoinStorage.publish(newIpfsKey, ipnsKey, owner);
    },
    // only for IPNS
    async getKeyList(){
        return await FileCoinStorage.getKeyList();
    },
    // only for IPNS
    async getFilePermissions(ipnsKey){
        return await FileCoinStorage.getFilePermissions(ipnsKey);
    },
    async modifyFilePermissions(ipnsKey, wallet, permission, owner){
        return await FileCoinStorage.modifyFilePermissions(ipnsKey, wallet, permission, owner);
    }
}
import {IpnsAPI} from "@/utils/API";
import {randomBytes} from "ethers/lib/utils";
import {ErrorList} from "@/crypto/helpers";

const FileCoinStorage = {
    async saveWithoutUpdate(file, uploadProgress = null) {
        if(!(file instanceof File)) {
            file = new Blob([JSON.stringify(file)], {type: 'application/json'});
        }
        const formData = new FormData();
        formData.append('payload', file)
        const config = {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
        if (typeof uploadProgress === 'function') config.onUploadProgress = uploadProgress
        const result = await IpnsAPI.post('/upload', formData, config)
        if(result.data && result.data.startsWith('ipfs://')) {
            return result.data.split('://').pop()
        }
        throw Error('IPFS value not valid')
    },
    async save(file, key = null) {
        if(!(file instanceof File)) {
            file = new Blob([JSON.stringify(file)], {type: 'application/json'});
        }
        const formData = new FormData();
        formData.append('payload', file)
        const result = await IpnsAPI.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        let ipfs = ''
        if(result.data && result.data.startsWith('ipfs://')) {
            ipfs = result.data.split('://').pop()
        }
        else throw Error('IPFS value not valid')

        return await this.publish(ipfs, key)
    },
    async publish(ipfsHash, ipnsKey = null, owner = null) {
        if(!owner) throw Error('Owner not defined')
        if(!ipnsKey) ({value: ipnsKey} = await this.keyGen())
        let ipnsHash = null
        let i = 0
        while (i < (+process.env.VUE_APP_IPNS_ATTEMPTS || 10)) {
            try {
                const response = await IpnsAPI.post('/publish', `hash=${ipfsHash}&key_name=${ipnsKey}&wallet=${owner}`)
                if(Array.isArray(response.data) && response.data.length === 2 && response.data[0] && response.data[1]) {
                    ipnsHash = response.data[0]
                    break;
                }
                else throw Error('IPFS value not valid')
            }
            catch (e) {}
            finally{
                i++
            }
        }
        if(ipnsHash && ipnsHash === ipnsKey) return `https://ipfs.io/ipns/${ipnsHash}`
        else throw Error('Could not publish to IPNS')
    },
    async keyGen() {
        const bytes = randomBytes(10)
        const keyName = bytes.join('') + Date.now();
        let keyValue = ''

        const response = await IpnsAPI.post('/key_gen', `name=${keyName}`)
        if(Array.isArray(response.data) && response.data.length === 2 && response.data[1]) {
            keyValue = response.data[1]
        }
        else throw Error('IPNS key pail failed')

        return {
            name: keyName,
            value: keyValue
        }
    },

    async loadJSON(data = {}){
        try{
            return await this.save(data)
        }
        catch (e){
            throw Error(ErrorList.LOAD_MEDIA_ERROR)
        }
    },
    async loadFile(file, withPublishToIPNS = true, uploadProgress = null){
        try{
            if (withPublishToIPNS) return await this.save(file)
            else return await this.saveWithoutUpdate(file, uploadProgress)
        }
        catch (e){
            throw Error(ErrorList.LOAD_MEDIA_ERROR)
        }
    },
    async changeFile(newData, key) {
        try{
            return await this.save(newData, key)
        }
        catch (e){
            throw Error(ErrorList.LOAD_MEDIA_ERROR)
        }
    },
    async getKeyList() {
        const response = await IpnsAPI.get('/get_keys')
        if(response.data){
            const list = Object.entries(response.data)
            return list.map(item => ({
                ipnsKey: item[0],
                ipfsKey: item[1]
            }))
        }
        throw Error('Response not valid')
    },
    async getFilePermissions(ipnsKey) {
        const response = await IpnsAPI.get('/get_file_accesses', {
            params: {
                file_addr: ipnsKey
            }
        })
        return response.data
    },
    async modifyFilePermissions(file_addr, wallet, file_access, owner_wallet) {
        const accessMap = {
            remove: -1,
            read: 0,
            write: 1,
            owner: 2,
            admin: 3,
        }
        const response = await IpnsAPI.post(
            '/change_access_to_file',
            `file_addr=${file_addr}&wallet=${wallet}&file_access=${accessMap[file_access]}&owner_wallet=${owner_wallet}`
        )
        return response.data
    }
}

export default FileCoinStorage
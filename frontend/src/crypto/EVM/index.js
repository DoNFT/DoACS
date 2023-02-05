import {
    ConnectionStore,
} from '@/crypto/helpers'
import alert from "@/utils/alert";
import {ethers} from "ethers";
import {log} from "@/utils/AppLogger";

class EVM {

    constructor(){

    }


    /* ---------- Connected methods ON  ----------  */
    async init(){
        return await this.connector.init(this)
    }
    async connectToWallet(...data){
        return await this.connector.connectToWallet(...data)
    }
    async disconnect(){
        return await this.connector.disconnect()
    }
    async isUserConnected(){
        return await this.connector.isUserConnected()
    }
    /*  ----------  Connected methods OFF  ----------  */


    async checkForENSName(address){
        if(ethers.utils.isAddress(address)){
            return {
                realAddress: address,
                ensName: address
            }
        }
        else{
            let realAddress;
            try{
                realAddress = await ConnectionStore.getProviderForENS().resolveName(address)
            }
            catch (e){
                log(e)
                throw new Error('CONTRACT_ADDRESS_ERROR')
            }
            if(realAddress && ethers.utils.isAddress(realAddress)){
                return {
                    realAddress: realAddress,
                    ensName: address
                }
            }
            else {
                throw new Error('CONTRACT_ADDRESS_ERROR')
            }
        }
    }

    tryToConnectToUnsupportedNetwork(){
        log('network not supported')
        alert.open('Sorry, we did not support this network')
    }
}

export default EVM
import { Contract } from "ethers";
import {stringCompare} from "@/utils/string";
import {log} from "@/utils/AppLogger";

import {
    DecentralizedStorage,
    Formatters,
    ConnectionStore,
    ErrorList,
    TokensABI,
    ActionTypes, Networks
} from '@/crypto/helpers'


class SmartContract {

    _address = null
    _type = null

    //  ethers contract instance
    _instance = null
    _provider = null

    metaData = {
        address: null,
        name: null,
        symbol: null,
        tokens: [],
        balance: 0
    }

    /*
    * @param options: object, address = string in hex, type = CollectionType
    * */
    constructor({address, type = 'common'}){
        this._address = address
        this._type = type
        this.metaData.address = address
    }

    _getProvider(){
        if(!this._provider) this._provider = ConnectionStore.getProvider();
        return this._provider
    }

}

export default SmartContract
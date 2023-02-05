import {defineStore} from "pinia";
import {catToFixed} from "@/utils/string";
import {Networks} from "@/crypto/helpers";

import {getAvailableNetworks} from "@/crypto/helpers/Networks";
const availableNetworks = getAvailableNetworks()

export const useStore = defineStore('main', {
    state: () => ({
        isAppReady: false,
        isWalletConnectModalOpen: false,
        walletConnectCode: '',
        walletConnectCloseHandler: null,

        networks: availableNetworks,
        wallets: [
            {id: 1, name: 'MetaMask', key: 'Metamask', color: '#FFFFFF', available: true},
            // {id: 3, name: 'WalletConnect', key: 'walletconnect', color: '#D9ECFF', available: true},
            // {id: 2, name: '1inch', key: '1inch', color: '#0E131D', available: true},
        ],

        connection: {
            userIdentity: null,
            userNetworkName: null,
            userNetworkSupported: false
        },

        explorers: {
            transaction: '',
            account: '',
            block: ''
        },
        shopURL: '',

        processStatus: {
            code: '',
            addition: []
        },

        walletConnectModalOpen: true
    }),
    getters: {
        userIdentityShort: state => catToFixed(state.connection.userIdentity || ''),
    },
    actions: {
        onLoginPageModalChange(value){
            this.walletConnectModalOpen = value
        },
        setProcessStatus(statusCode = '', ...additionParams){
            this.processStatus.code = statusCode
            this.processStatus.addition.splice(0, this.processStatus.addition.length, ...additionParams)
        },
        openWalletConnectQR(copyCode, closeHandler){
            this.walletConnectCode = copyCode
            this.walletConnectCloseHandler = closeHandler
            this.isWalletConnectModalOpen = true
        },
        closeWalletConnectQR({isAutomatic = false} = {}){
            if(!isAutomatic && this.walletConnectCloseHandler) this.walletConnectCloseHandler()
            this.isWalletConnectModalOpen = false
            this.walletConnectCloseHandler = null
        },
        setAppReady(){
            this.isAppReady = true
        },
        setUserIdentity(value = null){
            this.connection.userIdentity = value
        },
        setUserNetworkName(value = null){
            this.connection.userNetworkName = value
            if(value){
                const {
                    transactionExplorer,
                    accountExplorer,
                    blockExplorer
                } = Networks.getData(value)
                this.explorers.transaction = transactionExplorer
                this.explorers.account = accountExplorer
                this.explorers.block = blockExplorer
                const {store} = Networks.getSettings(value)
                this.shopURL = store
            }
        },
    }
})
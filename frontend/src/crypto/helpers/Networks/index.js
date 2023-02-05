const networks = {
    filecoin_hyperspace_test: {
        rpc: 'https://api.hyperspace.node.glif.io/rpc/v1',
        meta: {
            title: 'Filecoin Hyperspace',
            image: 'ether',
            chainId: 3141,
            transactionExplorer: "https://hyperspace.filfox.info/en/tx/",
            accountExplorer: "https://hyperspace.filfox.info/en/address/",
            gasLimit: 400000
        }
    }
}
Object.freeze(networks)

export function getAvailableNetworksRPC() {
    const resultObject = {}
    Object.entries(networks)
        .filter(([_, {rpc, meta: {chainId}}]) => rpc && chainId)
        .forEach(([_, {rpc, meta: {chainId}}]) => {
            resultObject[chainId] = rpc
        })
    return resultObject
}

export function getAvailableNetworks() {
    return Object.entries(networks)
        .filter(([name, {meta, contracts}]) => {
            return !!+process.env[`VUE_APP_NETWORK_${name.toUpperCase()}_SUPPORT`] &&
                meta.title &&
                (meta.chainId || meta.image === 'near')
        })
        .map(([name, {meta: {title, image, chainId}}], index) => ({
            id: chainId,
            name: title,
            key: image,
            available: true
        }))
}

export function getNameByChainID(chainID){
    const [name] = Object.entries(networks).find(([, data]) => data.meta.chainId === chainID) || ['unknown']
    let isSupport = (name !== 'unknown')? !!+process.env[`VUE_APP_NETWORK_${name.toUpperCase()}_SUPPORT`] : false
    return isSupport? name : 'unknown'
}

export function getData(networkName){
    return networks[networkName.toLowerCase()]?.meta || null
}

export function getSettings(networkName){
    return networks[networkName.toLowerCase()] || null
}
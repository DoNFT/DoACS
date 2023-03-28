<template>
  <Sketch class="token-page-cover">
    <div class="file-control">
      <div class="sketch__title">Upload to IPFS</div>
      <div class="file-control__load">
        <TokenMediaLoader :mode="'loadOnly'" @addFile="addFile"/>
      </div>
      <div class="file-control__list">
        <div v-for="(item, index) of fileList" :key="item.file.name + item.file.size + item.file.lastModified">
          <div>
            <div>{{ item.file.name }}</div>
            <template v-if="item.loadedKey">
              IPFS key: <a target="_blank" :href="computeIPFSLink(item.loadedKey)">{{ computeHash(item.loadedKey) }}</a>
              <span class="copy" @click="copyIPFSHash(item)">
                <svg v-if="item.isHashCopied" viewBox="0 0 24 24"><path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" /></svg>
                <svg v-else viewBox="0 0 24 24"><path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z" /></svg>
              </span>
            </template>
            <div class="error" v-if="item.error">{{ item.error }}</div>
          </div>
          <div title="Remove" @click="removeFile(index)">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" /></svg>
          </div>
          <div :style="{width: item.progress + '%'}"></div>
        </div>
      </div>
      <div class="file-control__btn">
        <span
            class="btn"
            :class="{na: !fileListUnUploaded.length || isUploadingProcess}"
            @click="fileListUnUploaded.length && !isUploadingProcess? loadToIPFS() : null"
        >Upload</span>
      </div>
    </div>

    <div class="file-control">
      <div class="sketch__title">Publish to IPNS</div>
      <div class="token-page__field file-control__input">
        <div>IPFS key:</div>
        <div>
          <input type="text" class="input" v-model.trim="ipfsHashForPublish">
        </div>
      </div>
      <template v-if="publishedTo">
        <div class="file-control__publish-result" v-if="publishedTo">
          IPNS key: {{ computeHash(IPNSHash) }}
          <span class="copy" @click="copyIPNSHash">
            <svg v-if="isIPNSCopied" viewBox="0 0 24 24"><path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" /></svg>
            <svg v-else viewBox="0 0 24 24"><path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z" /></svg>
          </span>
        </div>
        <div class="file-control__publish-result" v-if="publishedTo">
          Published to: <a :href="publishedTo" target="_blank">{{ publishedTo }}</a>
        </div>
      </template>
      <div class="file-control__btn">
        <span
            class="btn"
            :class="{na: !ipfsHashForPublish || publishProcess}"
            @click="ipfsHashForPublish.length && !publishProcess? publishToIPNS() : null"
        >Publish</span>
      </div>
    </div>

    <div class="file-control">
      <div class="sketch__title">Update IPNS</div>
      <div class="token-page__field file-control__input">
        <div>IPNS key:</div>
        <div>
          <input type="text" class="input" v-model.trim="updateIPNS.ipnsKey">
        </div>
      </div>
      <div class="token-page__field file-control__input">
        <div>New IPFS:</div>
        <div>
          <input type="text" class="input" v-model.trim="updateIPNS.newIpfsKey">
        </div>
      </div>
      <div class="file-control__publish-result" v-if="updateIPNS.updatedLink">
        Updated: <a :href="updateIPNS.updatedLink" target="_blank">{{ updateIPNS.ipnsKey }}</a>
      </div>
      <div class="file-control__btn">
        <span
            class="btn"
            :class="{na: !updateIPNS.ipnsKey || !updateIPNS.newIpfsKey || updateIPNS.isLoading}"
            @click="(updateIPNS.ipnsKey && updateIPNS.newIpfsKey && !updateIPNS.isLoading)? submitUpdateIPNS() : null"
        >Update</span>
      </div>
    </div>

    <div class="file-control">
      <div class="sketch__title">Key links</div>
      <div class="file-control__key-links">
        <div class="title">
          <div>IPNS key</div>
          <div>IPFS key</div>
        </div>
        <div v-for="item in keyLinks">
          <div>
            <span class="btn sm" @click="loadPermissions(item.ipnsKey)">Check permissions</span>
            <a target="_blank" :href="computeIPNSHash(item.ipnsKey)">{{ computeHash(item.ipnsKey) }}</a>
          </div>
          <div>
            <a target="_blank" :href="computeIPFSHash(item.ipfsKey)">{{ computeHash(item.ipfsKey) }}</a>
          </div>
        </div>
      </div>
    </div>

    <div class="file-control" v-if="filePermissions">
      <div class="sketch__title">File {{ computeHash(filePermissions.ipnsKey) }}</div>
      <div class="file-control__permissions">
        <div class="item" v-for="[wallet, permission] of filePermissions.permissions">
          <div>{{ computeHash(wallet) }}</div>
          <div>
            <select
                class="input default"
                @change="changedFilePermission(wallet, $event.target.value)"
                :value="permission"
            >
              <option disabled :value="null">Select permission</option>
              <option :value="'read'">read</option>
              <option :value="'write'">write</option>
              <option disabled :value="'owner'">owner</option>
              <option disabled :value="'admin'">admin</option>
            </select>
          </div>
          <div>
            <span class="rm" @click="removeGrants(wallet)">
              <svg viewBox="0 0 20 21" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.5 18L17.5 3M2.5 3L17.5 18" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            </span>
          </div>
        </div>
        <div class="item">
          <div>
            <input type="text" class="input default" placeholder="New wallet" v-model="grantPermission.wallet">
          </div>
          <div>
            <select
                class="input default"
                v-model="grantPermission.permission"
            >
              <option disabled :value="null">Select permission</option>
              <option :value="'read'">read</option>
              <option :value="'write'">write</option>
              <option disabled :value="'owner'">owner</option>
              <option disabled :value="'admin'">admin</option>
            </select>
          </div>
        </div>
        <div>
          <span class="btn" :class="{na: grantPermission.loading}" @click="!grantPermission.loading? addPermission() : null">Add wallet</span>
        </div>
      </div>
    </div>

    <!---->

  </Sketch>
</template>

<script setup>
    import Sketch from '@/components/UI/Sketch'
    import TokenMediaLoader from '@/components/UI/TokenMediaLoader'
    import {computed, onMounted, reactive, ref} from "vue";
    import {ConnectionStore, DecentralizedStorage} from "@/crypto/helpers";
    import copy from "copy-to-clipboard";
    import alert from "@/utils/alert";
    import {stringCompare} from "@/utils/string";

    // only for metamask sign
    const signMessage = async () => {
      const from = ConnectionStore.getUserIdentity()
      const exampleMessage = 'Sign changes to file.';
      const msg = `0x${Buffer.from(exampleMessage, 'utf8').toString('hex')}`;
      return await window.ethereum.request({
        method: 'personal_sign',
        params: [msg, from, 'address'],
      });
    }

    const getErrorMessage = e => e && (e.message || ('toString' in e? e.toString() : 'Error')) || 'Error';
    const computeHash = computed(() => hash => `${hash.slice(0, 4)}...${hash.slice(-4)}`)
    const computeIPNSHash = computed(() => hash => `https://ipfs.io/ipns/${hash}`)
    const computeIPFSHash = computed(() => hash => `https://ipfs.io/ipfs/${hash}`)

    const isUploadingProcess = ref(false)
    const fileList = ref([])
    const fileListUnUploaded = computed(() => fileList.value.filter(item => !item.loadedKey))
    const addFile = file => {
      fileList.value.push({
        file,
        isLoading: false,
        progress: 0,
        loadedKey: null,
        error: null,
        isHashCopied: false
      })
    }
    const computeIPFSLink = computed(() => hash => `https://ipfs.io/ipfs/${hash}`)
    const copyIPFSHash = item => {
      item.isHashCopied = copy(item.loadedKey)
      setTimeout(() => item.isHashCopied = false, 3000)
    }
    const removeFile = (index) => fileList.value.splice(index, 1)
    const loadToIPFS = async () => {
      isUploadingProcess.value = true
      for await (const fileItem of fileListUnUploaded.value) {
        try{
          const uploadProgress = ({loaded, total}) => fileItem.progress = Math.round(loaded / total * 100)
          fileItem.isLoading = true
          fileItem.loadedKey = await DecentralizedStorage.loadFile(fileItem.file, DecentralizedStorage.constants.IPFS_ONLY, uploadProgress)
        }
        catch (e) {
          fileItem.error = getErrorMessage(e)
        }
        finally {
          fileItem.isLoading = false
        }
      }
      isUploadingProcess.value = false
    }


    const publishProcess = ref(false)
    const ipfsHashForPublish = ref('')
    const publishedTo = ref('')
    const IPNSHash = computed(() => publishedTo.value.split('/ipns/').pop())
    const isIPNSCopied = ref(false)
    const copyIPNSHash = () => {
      isIPNSCopied.value = copy(IPNSHash.value)
      setTimeout(() => isIPNSCopied.value = false, 3000)
    }
    const publishToIPNS = async () => {
      publishedTo.value = ''
      const owner = ConnectionStore.getUserIdentity()
      try{
        publishProcess.value = true
        publishedTo.value = await DecentralizedStorage.publish(ipfsHashForPublish.value, owner)
      }
      catch (e) {
        alert.open(getErrorMessage(e))
      }
      finally {
        publishProcess.value = false
        loadKeyLinks()
      }
    }

    const updateIPNS = reactive({
      ipnsKey: '',
      newIpfsKey: '',
      isLoading: false,
      updatedLink: ''
    })
    const submitUpdateIPNS = async () => {
      updateIPNS.updatedLink = ''
      const owner = ConnectionStore.getUserIdentity()
      try{
        const signature = await signMessage()
        updateIPNS.isLoading = true
        updateIPNS.updatedLink = await DecentralizedStorage.update(updateIPNS.newIpfsKey, updateIPNS.ipnsKey, owner)
      }
      catch (e) {
        alert.open(getErrorMessage(e))
      }
      finally {
        updateIPNS.isLoading = false
        loadKeyLinks()
      }
    }


    const keyLinks = ref([])
    const loadKeyLinks = async () => {
      keyLinks.value = await DecentralizedStorage.getKeyList()
    }


    const filePermissions = ref(null)
    const loadPermissions = async (ipnsKey) => {
      filePermissions.value = {
        permissions: await DecentralizedStorage.getFilePermissions(ipnsKey),
        ipnsKey: ipnsKey
      }
    }
    const getFileOwner = () => {
      const ownerEntry = filePermissions.value.permissions.find(([_, permission]) => permission === "owner")
      if (!ownerEntry) throw Error('This file does not belong to anyone')
      return ownerEntry[0]
    }

    const changedFilePermission = async (wallet, newPermission) => {
      try{
        const ownerWallet = getFileOwner()
        if (stringCompare(ownerWallet, wallet)) throw Error('Can not modify changes')
        const signature = await signMessage()
        await DecentralizedStorage.modifyFilePermissions(
            filePermissions.value.ipnsKey,
            wallet,
            newPermission,
            ownerWallet
        )
      }
      catch (e) {
        alert.open(getErrorMessage(e))
      }
      finally {
        loadPermissions(filePermissions.value.ipnsKey)
      }
    }

    const grantPermission = reactive({
      wallet: '',
      permission: 'write',
      loading: false
    })
    const addPermission = async () => {
      grantPermission.loading = true
      if (!grantPermission.wallet.trim()) return
      try{
        const ownerWallet = getFileOwner()
        const signature = await signMessage()
        await DecentralizedStorage.modifyFilePermissions(
            filePermissions.value.ipnsKey,
            grantPermission.wallet,
            grantPermission.permission,
            ownerWallet
        )
        grantPermission.wallet = ''
      }
      catch (e) {
        alert.open(getErrorMessage(e))
      }
      finally {
        loadPermissions(filePermissions.value.ipnsKey)
        grantPermission.loading = false
      }
    }
    const removeGrants = async (wallet) => {
      try{
        const ownerWallet = getFileOwner()
        if (stringCompare(ownerWallet, wallet)) throw Error('Can not modify changes')
        const signature = await signMessage()
        await DecentralizedStorage.modifyFilePermissions(
            filePermissions.value.ipnsKey,
            wallet,
            'remove',
            ownerWallet
        )
        loadPermissions(filePermissions.value.ipnsKey)
      }
      catch (e) {
        alert.open(getErrorMessage(e))
      }
    }

    onMounted(() => {
      loadKeyLinks()
    })
</script>

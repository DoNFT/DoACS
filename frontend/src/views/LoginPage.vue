<template>
  <div class="lp-intro-cover">
    <div class="lp-intro">
      <div>
        <h1>
          Welcome to DoFiles demo by DoNFT
        </h1>
        <div>
          Decentralized DropBox on IPFS allows you:<br/>
          - publish file of IPFS<br/>
          - use IPNS approach to update files by link<br/>
          - manage access to updating files on IPNS<br/>
        </div>
        <div>
          <span class="btn" @click="openModal">Connect wallet</span>
        </div>
      </div>
      <div>
        <div class="lp-intro__logo">
          <div></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useStore} from "@/store/main";
const store = useStore()
import {onMounted} from "vue";

onMounted(() => {
  store.onLoginPageModalChange(false)
})

const openModal = () => store.onLoginPageModalChange(true)
</script>
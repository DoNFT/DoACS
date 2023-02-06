<template>
  <div class="lp-intro-cover">
    <div class="lp-intro">
      <div>
        <h1>
          Welcome to DoACS demo by DoNFT
        </h1>
        <div>
          Access Control Service allows you:
          - publish file of IPFS
          - use IPNS approach to update files by link
          - manage access to updating files on IPNS
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
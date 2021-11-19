<template>
  <v-card>
    <v-card-title>{{ housingName }}</v-card-title>
    <v-card-text>
      <website-access-component housing-id="housingId" />
      <housing-config />
    </v-card-text>
  </v-card>
</template>

<script>
import HousingConfig from './config/HousingConfig.vue'
import WebsiteAccessComponent from '../components/WebsiteAccessComponent.vue'

export default {
  components: {
    HousingConfig,
    WebsiteAccessComponent,
  },
  computed: {
    housingId: () => this.$route.params.id,
    housingName() {
      const { id } = this.$route.params

      return this.$store.state.housings.housings[id].name
    },
  },
}
</script>

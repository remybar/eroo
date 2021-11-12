<template>
  <v-card>
    <v-card-title>{{ housingName }}</v-card-title>
    <v-card-text>
      Pour accéder au site web:
      <v-btn
        small
        color="primary"
      >
        voir le site
      </v-btn>
      <housing-config />
    </v-card-text>
  </v-card>
</template>

<script>
import HousingConfig from './config/HousingConfig.vue'

export default {
  components: {
    HousingConfig,
  },
  computed: {
    housingName() {
      const { id } = this.$route.params

      return this.$store.state.housings.housings[id].name
    },
  },
}
</script>

<template>
  <v-card>
    <v-card-title>Ceci est votre logement</v-card-title>
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
}
</script>

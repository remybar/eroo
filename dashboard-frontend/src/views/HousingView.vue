<template>
  <div id="housing-view">
    <!-- TITLE -->
    <v-row class="mt-4">
      <!-- housing title -->
      <v-col cols="12" md="9" lg="9">
        <h1> NOM DU LOGEMENT </h1>
      </v-col>

      <!-- "see website" button -->
      <v-col class="d-flex justify-end" cols="12" md="3" lg="3">
        <v-btn color="primary" dark>
          Voir le site
        </v-btn>
      </v-col>
    </v-row>

    <!-- MENU -->
    <v-row class="mt-8">
      <v-col cols="12" md="12" lg="12">
        <v-tabs v-model="userTab" class="housing-view-tabs">
          <v-tab v-for="tab in tabs" :key="tab.icon">
            <v-icon size="20" class="me-3">
              {{ tab.icon }}
            </v-icon>
            <span>{{ tab.title }}</span>
          </v-tab>
        </v-tabs>

        <v-tabs-items id="housing-view-tabs-content" v-model="userTab" class="mt-5 pa-1">
          <v-tab-item>
            <housing-config-widget></housing-config-widget>
          </v-tab-item>
          <v-tab-item>
            <website-widget housing-id="1"></website-widget>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </div>
</template>

<script>

import { ref } from '@vue/composition-api'
import { mdiCogOutline, mdiSpiderWeb } from '@mdi/js'
import WebsiteWidget from '@/components/WebsiteWidget.vue'
import HousingConfigWidget from '@/components/HousingConfigWidget.vue'

export default {
  components: {
    HousingConfigWidget,
    WebsiteWidget,
  },
  setup() {
    const userTab = ref(null)

    const tabs = [
      { icon: mdiCogOutline, title: 'Configuration' },
      { icon: mdiSpiderWeb, title: 'Site Web' },
    ]

    return {
      tabs,
      userTab,
    }
  },

  // computed: {
  //   housingId: () => this.$route.params.id,
  //   housingName() {
  //     const { id } = this.$route.params

  //     return this.$store.state.housings.housings[id].name
  //   },
  // },
}
</script>
<style scoped>
  .housing-view-tabs {
    box-shadow: none !important;
  }
  .v-tabs-bar {
    background-color: transparent !important;
  }
  #housing-view-tabs-content {
    background-color: transparent;
  }
</style>

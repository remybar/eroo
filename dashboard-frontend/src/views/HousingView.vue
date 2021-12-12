<template>
  <container>
    <website-access-component housing-id="housingId" />
    <config-housing-form />
  </container>
</template>

<script>
import ConfigHousingForm from '@/components/forms/ConfigHousingForm.vue'
import WebsiteAccessComponent from '@/components/WebsiteAccessComponent.vue'

export default {
  components: {
    ConfigHousingForm,
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

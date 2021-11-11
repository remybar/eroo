<template>
  <v-card>
    <v-card-title>Ajouter un nouveau logement</v-card-title>
    <v-card-text>
      <add-housing-form />
    </v-card-text>
  </v-card>
</template>

<script>
import AddHousingForm from '@/components/forms/AddHousingForm.vue'

export default {
  components: {
    AddHousingForm,
  },
}
</script>

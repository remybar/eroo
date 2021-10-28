<template>
  <v-card>
    <v-card-title>Ajouter un nouveau logement</v-card-title>
    <v-card-text>
      Pour pouvoir ajouter votre logement et générer son site web, nous avons besoin:
      <ul>
        <li>d'un <strong>nom</strong>, qui apparaitra dans le menu de gauche et vous permettra de rapidement accéder aux paramètres de ce logement,</li>
        <li>de <strong>l'adresse Internet</strong> de votre annonce airbnb.</li>
      </ul>
    </v-card-text>
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

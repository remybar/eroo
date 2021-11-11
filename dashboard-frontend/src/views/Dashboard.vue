<template>
  <div>
    <v-card v-if="!hasHousings" class="mb-6">
      <v-card-title>Bienvenue sur Eroo ! 🚀</v-card-title>
      <v-card-text>Ajouter dès à présent votre premier logement en cliquant sur le bouton "Ajouter un logement" dans la barre de menu tout en baut.</v-card-text>
    </v-card>
    <v-card v-if="hasHousings" class="mb-6">
      <v-card-title>Bravo !</v-card-title>
      <v-card-text>Vous venez d'ajouter votre premier logement</v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  computed: {
    hasHousings() {
      return this.$store.state.housings.hasHousings
    },
    housings() {
      return this.$store.state.housings.housings
    },
  },
}
</script>

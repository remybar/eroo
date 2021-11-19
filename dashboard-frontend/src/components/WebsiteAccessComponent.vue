<template>
  <div>
    Pour accéder au site web:
    <v-btn
      small
      color="primary"
      :loading="isGenerating"
      :disabled="isGenerating"
      @click="showOrGenerateWebsite"
    >
      {{ buttonTitle }}
    </v-btn>
  </div>
</template>

<script>

// TODO BAR:
// - afficher les 3 états possibles pour le bouton (
// regénérer (avec un icone warning)
// loading
// voir le site

// - utiliser l'API qui permet de connaitre l'état de génération du site

export default {
  props: {
    housingId: {
      type: Number,
      required: true,
    },
  },
  computed: {
    isGenerating() {
      return this.$store.state.housings[this.housingId].isGeneratingWebsite
    },
    buttonTitle() {
      const { websiteUrl } = this.$store.state.housings[this.housingId]

      return websiteUrl ? 'Voir le site' : 'Générer le site'
    },
  },
  methods: {
    showOrGenerateWebsite() {
    },
  },
}
</script>

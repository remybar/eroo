<template>
  <v-card
    elevation="2"
    outlined
    class="mb-4"
  >
    <v-card-title>
      <v-row>
        <v-col md="8">
          <h2>Site Web</h2>
        </v-col>
        <v-col
          class="d-flex justify-end"
          md="4"
        >
          <v-btn
            color="primary"
            dark
          >
            Voir le site
          </v-btn>
        </v-col>
      </v-row>
    </v-card-title>
  </v-card>
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
}
</script>

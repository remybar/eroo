<template>
  <div class="website-widget">
    <!-- Website configuration -->
    <v-card flat class="mb-4">
      <v-card-title>
        Votre site web
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-row>
            <v-col cols="12" md="3">
              <label for="airbnb_url">URL airbnb</label>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field id="airbnb_url" v-model="airbnbUrl" outlined dense hide-details></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-btn color="primary">
                Générer
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

  <!-- Domain name -->
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
  setup() {
    const airbnbUrl = 'http://toto.be'

    return {
      airbnbUrl,
    }
  },
}
</script>

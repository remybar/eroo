<template>
  <v-form
    ref="form"
    @submit.prevent="processForm"
  >
    <v-row>
      <v-col
        cols="12"
        md="3"
      >
        <label for="housingname">Nom du logement</label>
      </v-col>

      <v-col
        cols="12"
        md="9"
      >
        <v-text-field
          id="housingname"
          v-model="housingname"
          name="housingname"
          :prepend-inner-icon="icons.mdiHomeOutline"
          outlined
          dense
          placeholder="Nom du logement (max. 13 caractères)"
          :rules="nameRules"
          required
        ></v-text-field>
      </v-col>
      <!--
      <v-col
        cols="12"
        md="3"
      >
        <label for="emailHorizontalIcons">Annonce Airbnb</label>
      </v-col>

      <v-col
        cols="12"
        md="9"
      >
        <v-text-field
          id="emailHorizontalIcons"
          v-model="airbnbUrl"
          :prepend-inner-icon="icons.mdiWeb"
          outlined
          dense
          placeholder="URL de votre annonce Airbnb"
          hide-details
        ></v-text-field>
      </v-col>
-->
      <v-col
        offset-md="3"
        cols="12"
      >
        <v-btn
          color="primary"
          type="submit"
        >
          Ajouter
        </v-btn>
        <v-btn
          type="reset"
          outlined
          class="mx-2"
        >
          Remise à zéro
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
// eslint-disable-next-line object-curly-newline
import { mdiHomeOutline, mdiWeb } from '@mdi/js'
import { ref } from '@vue/composition-api'

export default {
  data: () => ({
    nameRules: [
      v => !!v || 'Un nom est requis',
      v => (v && v.length <= 13) || 'Le nom ne doit pas dépasser 13 caractères',
    ],
  }),
  setup() {
    const housingname = ref('')

    return {
      housingname,

      // icons
      icons: {
        mdiHomeOutline,
        mdiWeb,
      },
    }
  },
  methods: {
    createHousing() {
      const housing = { name: this.housingname }
      this.$store.dispatch('housings/create', housing)
        .then(
          housingId => this.$router.push({ name: 'housing-page', params: { id: housingId } }),
          error => console.log(error),
        )
    },
    processForm() {
      if (this.$refs.form.validate()) {
        this.createHousing()
      }
    },
  },
}
</script>

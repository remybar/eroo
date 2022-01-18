<template>
  <v-card flat class="mb-4">
    <v-card-title>
      Paramètres généraux
    </v-card-title>
    <v-card-text>
      <v-form>
        <!-- max number of people -->
        <v-row align="center">
          <v-col cols="12" md="3">
            <label class="v-label" for="max-people-count">Nombre maximum de personnes</label>
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="maxNumberOfPeople"
              :items="numberOfPeopleList"
              hide-details
              outlined
              required
            ></v-select>
          </v-col>
        </v-row>

        <!-- extra guest limit -->
        <v-row align="center">
          <v-col cols="12" md="3">
            <label class="v-label" for="extra-guest-enabled">Tarif personne supplémentaire</label>
          </v-col>
          <v-col cols="12" md="2">
            <v-switch
              id="extra-guest-enabled"
              v-model="extraGuestEnabled"
              color="info"
              inset
              :label="`${extraGuestSwitchLabel(extraGuestEnabled)}`"
            >
            </v-switch>
          </v-col>
          <v-col v-if="extraGuestEnabled" cols="12" md="2">
            <v-select
              id="first-extra-guest"
              v-model="firstExtraGuest"
              :items="firstExtraGuestList"
              hide-details
            >
            </v-select>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>
<script>
export default {
  props: {
    config: {
      type: Object,
      required: true,
    },
  },

  data: () => {
    const numberOfPeopleList = [...Array(100).keys()].slice(1)
    const firstExtraGuestList = []
    const numberRules = [
      v => !!v || 'Ce champ est requis',
      v => /^\d+$/.test(v) || 'Doit être un nombre',
    ]

    return {
      numberOfPeopleList,
      numberRules,
      firstExtraGuestList,
    }
  },
  computed: {
    maxNumberOfPeople: {
      get() {
        return this.config.maxNumberOfPeople
      },
      set(value) {
        this.updateExtraGuestList(value)
        this.emitUpdatedConfig(value, this.extraGuestEnabled, this.firstExtraGuest)
      },
    },
    extraGuestEnabled: {
      get() {
        return this.config.extraGuestEnabled
      },
      set(value) {
        this.emitUpdatedConfig(this.maxNumberOfPeople, value, this.firstExtraGuest)
      },
    },
    firstExtraGuest: {
      get() {
        return this.config.firstExtraGuest
      },
      set(value) {
        this.emitUpdatedConfig(this.maxNumberOfPeople, this.extraGuestEnabled, value)
      },
    },
  },
  created() {
    this.updateExtraGuestList(this.maxNumberOfPeople)
  },
  methods: {
    updateExtraGuestList(maxNumberOfPeople) {
      this.firstExtraGuestList = Array.from({ length: maxNumberOfPeople }, (x, i) => (i === 0 ? '1ère personne' : `${i + 1}ème personne`))
      const [firstExtraGuest] = this.firstExtraGuestList

      if (!this.firstExtraGuestList.includes(this.firstExtraGuest)) {
        this.firstExtraGuest = firstExtraGuest
      }
    },
    extraGuestSwitchLabel(value) {
      return value ? 'à partir de la ' : 'désactivé'
    },
    emitUpdatedConfig(maxNumberOfPeople, extraGuestEnabled, firstExtraGuest) {
      this.$emit('update', { maxNumberOfPeople, extraGuestEnabled, firstExtraGuest })
    },
  },
}
</script>

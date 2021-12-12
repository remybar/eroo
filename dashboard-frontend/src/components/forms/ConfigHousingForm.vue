<template>
  <v-card
    elevation="2"
    outlined
    class="mb-4"
  >
    <v-card-title>
      <v-row>
        <v-col md="8">
          <h2>Configuration</h2>
        </v-col>
        <v-col
          class="d-flex justify-end"
          md="4"
        >
          <v-btn
            color="primary"
            dark
          >
            Sauver
          </v-btn>
        </v-col>
      </v-row>
    </v-card-title>

    <v-card-text>
      <h3>Vos saisons</h3>
      <!-- title + add season button -->
      <v-row>
        <v-col
          class="d-flex justify-end"
          cols="12"
          offset-md="8"
          md="4"
        >
          <v-btn
            color="info"
            dark
            small
            @click="addSeason"
          >
            <v-icon
              dark
              left
            >
              {{ icons.mdiPlus }}
            </v-icon>
            Ajouter une saison
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>

    <!-- season table -->
    <v-data-table
      class="mx-8"
      :headers="headers"
      :items="seasons"
      no-data-text="Ajoutez une nouvelle saison en cliquant sur le bouton &quot;Ajouter une saison&quot; au dessus de ce tableau."
      disable-sort
      hide-default-footer
    >
      <template
        v-slot:item="{ item }"
      >
        <tr>
          <td colspan="4">
            <v-edit-dialog :return-value.sync="item.name">
              <v-chip
                class="ma-2"
                :color="item.color"
              >
                {{ item.name }}
              </v-chip>
              <template
                v-slot:input
                persistent
                large
              >
                <v-text-field
                  v-model="item.name"
                  label="Modifier"
                  single-line
                  counter
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </td>
          <td>
            <v-icon
              small
              class="me-2"
              @click="addPeriod(item)"
            >
              {{ icons.mdiPlus }}
            </v-icon>
            <v-icon
              small
              class="me-2"
              @click="deleteSeason(item)"
            >
              {{ icons.mdiDeleteOutline }}
            </v-icon>
          </td>
        </tr>

        <template v-if="hasPeriod(item)">
          <tr
            v-for="(period, index) in item.periods"
            :key="period.start"
          >
            <td></td>
            <td>
              <v-edit-dialog
                :return-value.sync="item.periods[index].start"
              >
                {{ period.start }}
                <template v-slot:input>
                  <v-date-picker
                    v-model="item.periods[index].start"
                    locale="fr-fr"
                  ></v-date-picker>
                  <v-text-field
                    :value="period.start"
                    label="Date de début"
                    prepend-icon="mdi-calendar"
                    readonly
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </td>
            <td>
              <v-edit-dialog
                :return-value.sync="item.periods[index].end"
              >
                {{ period.end }}
                <template v-slot:input>
                  <v-date-picker
                    v-model="item.periods[index].end"
                    locale="fr-fr"
                  ></v-date-picker>
                  <v-text-field
                    :value="period.end"
                    label="Date de fin"
                    prepend-icon="mdi-calendar"
                    readonly
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </td>
            <td>days</td>
            <td>
              <v-icon
                small
                class="me-2"
                @click="deletePeriod(item, index)"
              >
                {{ icons.mdiDeleteOutline }}
              </v-icon>
            </td>
          </tr>
        </template>
        <tr v-else="">
          <td
            colspan="4"
            class="text-center"
          >
            Cliquez sur le bouton '+' pour ajouter une nouvelle période.
          </td>
        </tr>
      </template>
    </v-data-table>
    <h3>Vos tarifs</h3>
    <h3>Vos taxes</h3>
  </v-card>
</template>

<script>
import { mdiDeleteOutline, mdiPencilOutline, mdiPlus } from '@mdi/js'
import data from './datatable.json'

export default {

  filters: {
    formatPrice(price) {
      return `${price}€`
    },
  },
  data: () => ({
    icons: {
      mdiDeleteOutline,
      mdiPencilOutline,
      mdiPlus,
    },
    headers: [
      { text: 'SAISON', value: 'name' },
      { text: 'DEBUT', value: 'start' },
      { text: 'FIN', value: 'end' },
      { text: 'JOURS', value: 'days' },
      { text: 'ACTIONS', value: 'actions' },
    ],
    seasons: [],
  }),

  created() {
    this.initialize()
  },

  methods: {
    initialize() {
      this.seasons = JSON.parse(JSON.stringify(data))
    },
    hasPeriod(season) {
      return season.periods.length > 0
    },
    addSeason() {
      const newSeason = {
        id: this.seasons.length + 1,
        name: 'nouvelle saison',
        periods: [],
        base_price: 0,
      }
      this.seasons.push(newSeason)
    },
    deleteSeason(season) {
      this.seasons.splice(this.seasons.indexOf(season), 1)
    },
    deletePeriod(season, periodIndex) {
      const seasonIdx = this.seasons.indexOf(season)
      this.seasons[seasonIdx].periods.splice(periodIndex, 1)
    },
    addPeriod(season) {
      const newPeriod = { start: 'à définir', end: 'à définir' }
      const seasonId = this.seasons.indexOf(season)
      this.seasons[seasonId].periods.push(newPeriod)
    },
  },
}
</script>

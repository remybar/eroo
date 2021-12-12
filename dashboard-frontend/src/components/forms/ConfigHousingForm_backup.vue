<template>
  <div>
    <v-card-text>
      <v-row>
        <v-col
          class="d-flex justify-end"
          cols="12"
          offset-md="8"
          md="4"
        >
          <v-btn
            color="primary"
            dark
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

    <v-data-table
      :headers="headers"
      :items="seasons"
      disable-sort
      hide-default-footer
    >
      <template v-slot:item="{ item }">
        <tr
          v-for="(period, index) in item.periods"
          :key="period.id"
        >
          <!-- name -->
          <td
            v-if="needRowspan(item, index)"
            :rowspan="rowspan(item)"
          >
            <v-edit-dialog :return-value.sync="item.name">
              {{ item.name }}
              <template v-slot:input>
                <v-text-field
                  v-model="item.name"
                  label="Edit"
                  single-line
                  counter
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </td>

          <!-- period -->
          <td>
            <v-edit-dialog
              :return-value.sync="item.periods[index]"
              large
              persistent
            >
              {{ period | formatPeriod }}
              <v-icon
                ml-4
                small
                @click="deletePeriod(item, period)"
              >
                {{ icons.mdiDeleteOutline }}
              </v-icon>
              <template v-slot:input>
                <v-date-picker
                  v-model="item.periods[index].range"
                  range
                  locale="fr-fr"
                ></v-date-picker>
                <v-text-field
                  :value="period | formatPeriod"
                  label="Dates"
                  prepend-icon="mdi-calendar"
                  readonly
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </td>

          <!-- base price -->
          <td
            v-if="needRowspan(item, index)"
            :rowspan="rowspan(item)"
          >
            <v-edit-dialog :return-value.sync="item.base_price">
              {{ item.base_price | formatPrice }}
              <template v-slot:input>
                <v-text-field
                  v-model="item.base_price"
                  label="Edit"
                  single-line
                  counter
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </td>

          <!-- action -->
          <td
            v-if="needRowspan(item, index)"
            :rowspan="rowspan(item)"
          >
            <v-btn
              outlined
              small
              @click="addPeriod(item)"
            >
              Ajouter période
            </v-btn>
            <v-btn
              outlined
              small
              ml-4
              @click="deleteSeason(item)"
            >
              Supprimer
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { mdiDeleteOutline, mdiPencilOutline, mdiPlus } from '@mdi/js'
import moment from 'moment'
import data from './datatable.json'

export default {

  filters: {
    formatPeriod(period) {
      if (period.range.length === 0) {
        return 'nouvelle période à définir'
      }
      const [start, end] = period.range
      const startPeriod = moment(start).format('DD/MM')
      const endPeriod = moment(end).format('DD/MM')

      return `${startPeriod} - ${endPeriod}`
    },
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
      { text: 'PERIODES', value: 'periods' },
      { text: 'PRIX DE BASE PAR NUITEE', value: 'base_price' },
      { text: 'ACTIONS', value: 'actions' },
    ],
    seasons: [],
    editedIndex: -1,
    editedSeason: {},
    defaultSeason: {},
  }),

  created() {
    this.initialize()
  },

  methods: {
    initialize() {
      this.seasons = JSON.parse(JSON.stringify(data))
    },

    addPeriod(season) {
      const newPeriod = { range: [] }
      const seasonId = this.seasons.indexOf(season)
      this.seasons[seasonId].periods.push(newPeriod)
    },

    addSeason() {
      const newSeason = {
        id: this.seasons.length + 1,
        name: 'nouvelle saison',
        periods: [{ range: [] }],
        base_price: 0,
      }
      this.seasons.push(newSeason)
    },

    needRowspan(season, periodIndex) {
      return season.periods.length > 0 && periodIndex === 0
    },

    rowspan(season) {
      return season.periods.length > 0 ? season.periods.length : 1
    },

    deleteSeason(season) {
      this.seasons.splice(this.seasons.indexOf(season), 1)
    },

    deletePeriod(season, period) {
      const seasonIdx = this.seasons.indexOf(season)
      const periodIdx = this.seasons[seasonIdx].periods.indexOf(period)
      this.seasons[seasonIdx].periods.splice(periodIdx, 1)
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedSeason = { ...this.defaultSeason }
        this.editedIndex = -1
      })
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.seasons[this.editedIndex], this.editedSeason)
      } else {
        this.seasons.push(this.editedSeason)
      }
      this.close()
    },
  },
}
</script>

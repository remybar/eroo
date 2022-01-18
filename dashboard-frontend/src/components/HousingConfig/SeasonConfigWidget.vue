<template>
  <v-card flat class="mb-4">
    <v-card-title>
      Vos saisons
    </v-card-title>

    <v-card-text>
      <!-- buttons bar -->
      <v-row class="mx-8 mb-4">
        <v-col
          class="d-flex justify-end"
          cols="12"
          offset-md="8"
          md="4"
        >
          <v-btn color="info" dark small @click="$emit('reset')">
            <v-icon dark left>
              {{ icons.mdiDeleteOutline }}
            </v-icon>
            Remise à zéro
          </v-btn>

          <!-- add season management -->
          <v-dialog v-model="isAddDialogVisible" persistent max-width="800px">
            <template #activator="{ on, attrs }">
              <v-btn
                class="ml-4"
                color="info"
                dark
                small
                v-bind="attrs"
                v-on="on"
              >
                <v-icon dark left>
                  {{ icons.mdiPlus }}
                </v-icon>
                Ajouter une saison
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <span class="headline">Ajouter une saison</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-row>
                        <v-col cols="12" md="3">
                          <label for="name">Nom de la saison</label>
                        </v-col>
                        <v-col cols="12" md="9">
                          <v-text-field
                            id="name"
                            v-model="seasonBeingAdded.name"
                            outlined
                            dense
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" md="3">
                          <label for="price">Prix de base</label>
                        </v-col>
                        <v-col cols="12" md="9">
                          <v-text-field
                            id="price"
                            v-model="seasonBeingAdded.base_price"
                            outlined
                            dense
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <v-row v-if="config.extraGuestEnabled">
                        <v-col cols="12" md="3">
                          <label for="price">Prix personne supplémentaire</label>
                        </v-col>
                        <v-col cols="12" md="9">
                          <v-text-field
                            id="price"
                            v-model="seasonBeingAdded.extra_guest_price"
                            outlined
                            dense
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-date-picker
                        v-model="dates"
                        range
                        color="info"
                      ></v-date-picker>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="error"
                  outlined
                  @click="cleanDialog()"
                >
                  Annuler
                </v-btn>
                <v-btn
                  color="success"
                  @click="addDiscount()"
                >
                  Ajouter
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>

      <!-- season table -->
      <v-data-table
        id="season-table"
        class="mx-8"
        :headers="headers"
        :items="seasons"
        no-data-text="Veuillez ajouter une saison en cliquant sur le bouton 'Ajouter une saison'"
        disable-sort hide-default-footer
      >
        <template v-slot:item="{ item, seasonIndex }">
          <tr v-for="(period, index) in item.periods" :key="period.start">
            <!-- season name -->
            <td
              v-if="index === 0"
              class="left-border-column right-border-column" :rowspan="periodCount(item)"
            >
              <v-edit-dialog :return-value.sync="item.name">
                <!-- display -->
                {{ item.name }}

                <!-- editor -->
                <template v-slot:input persistent large>
                  <v-text-field v-model="item.name" label="Modifier" single-line></v-text-field>
                </template>
              </v-edit-dialog>
            </td>

            <!-- season start -->
            <td :class="getPeriodClass(item, index)">
              <v-edit-dialog :return-value.sync="item.periods[index].start">
                <!-- display -->
                {{ period.start }}

                <!-- editor -->
                <template v-slot:input>
                  <v-date-picker v-model="item.periods[index].start" locale="fr-fr"></v-date-picker>
                  <v-text-field
                    :value="period.start"
                    label="Date de début"
                    prepend-icon="mdi-calendar"
                    readonly
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </td>

            <!-- season stop -->
            <td :class="getPeriodClass(item, index)">
              <v-edit-dialog :return-value.sync="item.periods[index].end">
                <!-- display -->
                {{ period.end }}

                <!-- editor -->
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

            <td :class="getPeriodClass(item, index)">
              <v-btn
                v-if="index === 0"
                icon outlined dark x-small
                color="info"
              >
                <v-icon dark>
                  {{ icons.mdiPlus }}
                </v-icon>
              </v-btn>
              <v-btn
                v-else=""
                icon outlined dark x-small
                color="info"
              >
                <v-icon dark>
                  {{ icons.mdiDeleteOutline }}
                </v-icon>
              </v-btn>
            </td>

            <!-- base price -->
            <td
              v-if="index === 0"
              class="left-border-column right-border-column" :rowspan="periodCount(item)"
            >
              <v-edit-dialog :return-value.sync="item.base_price">
                <!-- display -->
                {{ item.base_price | formatPrice }}

                <!-- editor -->
                <template v-slot:input>
                  <v-text-field
                    v-model="item.base_price"
                    label="Edit"
                    single-line
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </td>

            <!-- extra guest price -->
            <td
              v-if="index === 0 && config.extraGuestEnabled"
              class="left-border-column right-border-column" :rowspan="periodCount(item)"
            >
              <v-edit-dialog :return-value.sync="item.extra_guest_price">
                <!-- display -->
                {{ item.extra_guest_price | formatPrice }}

                <!-- editor -->
                <template v-slot:input>
                  <v-text-field
                    v-model="item.extra_guest_price"
                    label="Edit"
                    single-line
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </td>

            <!-- action -->
            <td
              v-if="index === 0"
              class="left-border-column right-border-column" :rowspan="periodCount(item)"
            >
              <v-btn
                icon outlined dark x-small
                color="info"
                @click="$emit('remove', seasonIndex)"
              >
                <v-icon dark>
                  {{ icons.mdiDeleteOutline }}
                </v-icon>
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
<script>
import { mdiDeleteOutline, mdiPlus } from '@mdi/js'

export default {
  filters: {
    formatPrice(price) {
      return `${price}€`
    },
  },
  props: {
    seasons: {
      type: Array,
      default: () => [],
      required: true,
    },
    config: {
      type: Object,
      default: () => ({}),
      required: true,
    },
  },
  data: () => {
    const defaultSeason = {
      name: '',
      periods: [
        {
          start: '01-01',
          end: '31-12',
        },
      ],
      base_price: 0,
      extra_guest_price: 0,
    }
    const dates = ['2019-09-10', '2019-09-20']

    return {
      icons: {
        mdiDeleteOutline,
        mdiPlus,
      },
      defaultSeason,
      seasonBeingAdded: { ...defaultSeason },
      isAddDialogVisible: false,
      dates,
    }
  },
  computed: {
    headers() {
      const headers = [
        { text: 'SAISON', value: 'name' },
        { text: 'DEBUT', value: 'start' },
        { text: 'FIN', value: 'end' },
        { text: '', value: 'period_actions' },
        { text: 'PRIX DE BASE', value: 'base_price' },
      ]

      if (this.config.extraGuestEnabled) {
        headers.push({ text: 'PRIX PERS. SUPPL.', value: 'extra_guest_price' })
      }
      headers.push({ text: 'ACTIONS', value: 'actions' })

      return headers
    },
  },
  methods: {
    periodCount(season) {
      return season.periods.length
    },
    getPeriodClass(season, periodIndex) {
      return (periodIndex !== season.periods.length - 1) ? 'no-border-row' : ''
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
    cleanDialog() {
      this.seasonBeingAdded = { ...this.defaultSeason }
      this.isAddDialogVisible = false
    },
    addSeason() {
      console.log(this.seasonBeingAdded)
      this.$emit('add', this.seasonBeingAdded)
      this.cleanDialog()
    },
  },
}
</script>
<style scoped>
#season-table .no-border-row {
    border-bottom: none;
}
#season-table .left-border-column {
  border-left: thin solid rgba(94, 86, 105, 0.14);
}
#season-table .right-border-column {
  border-right: thin solid rgba(94, 86, 105, 0.14);
}
</style>

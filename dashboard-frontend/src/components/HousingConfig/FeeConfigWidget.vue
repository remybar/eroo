<template>
  <v-card flat class="mb-4">
    <v-card-title>
      Vos frais fixes
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

          <!-- add fee management -->
          <v-dialog v-model="isAddDialogVisible" persistent max-width="600px">
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
                Ajouter un frais
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <span class="headline">Ajouter un frais</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" md="3">
                      <label for="name">Nom du frais</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="name"
                        v-model="feeBeingAdded.name"
                        outlined
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="3">
                      <label for="price">Prix</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="price"
                        v-model="feeBeingAdded.price"
                        outlined
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="3"></v-col>
                    <v-col cols="12" md="9">
                      <v-switch
                        id="by-day"
                        v-model="feeBeingAdded.by_day"
                        outlined
                        dense
                        inset
                        :label="`${byDayToString(feeBeingAdded.by_day)}`"
                      >
                      </v-switch>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="3"></v-col>
                    <v-col cols="12" md="9">
                      <v-switch
                        id="by-people"
                        v-model="feeBeingAdded.by_people"
                        outlined
                        dense
                        inset
                        :label="`${byPeopleToString(feeBeingAdded.by_people)}`"
                      >
                      </v-switch>
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
                  @click="addFee()"
                >
                  Ajouter
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>

      <!-- fee table -->
      <v-data-table
        id="fee-table"
        class="mx-8"
        :headers="headers"
        :items="fees"
        no-data-text="Veuillez ajouter un nouveau frais en cliquant sur le bouton 'Ajouter un frais'"
        disable-sort hide-default-footer
      >
        <!-- name -->
        <template #[`item.name`]="{ item }">
          <v-edit-dialog :return-value.sync="item.name">
            <!-- display -->
            {{ item.name }}

            <!-- editor -->
            <template v-slot:input>
              <v-text-field
                v-model="item.name"
                label="Edit"
                single-line
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <!-- price -->
        <template #[`item.price`]="{item}">
          <v-edit-dialog :return-value.sync="item.price">
            <!-- display -->
            {{ item.price | formatPrice }}

            <!-- editor -->
            <template v-slot:input>
              <v-text-field
                v-model="item.price"
                label="Edit"
                single-line
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <!-- by_day -->
        <template #[`item.by_day`]="{item}">
          <v-switch
            v-model="item.by_day"
            inset
            color="info"
            :label="`${byDayToString(item.by_day)}`"
          >
          </v-switch>
        </template>

        <!-- by_people -->
        <template #[`item.by_people`]="{item}">
          <v-switch
            v-model="item.by_people"
            inset
            color="info"
            :label="`${byPeopleToString(item.by_people)}`"
          >
          </v-switch>
        </template>

        <!-- action -->
        <template #[`item.action`]="{item, index}">
          <v-btn
            icon outlined dark x-small
            color="info"
            @click="$emit('remove', index)"
          >
            <v-icon dark>
              {{ icons.mdiDeleteOutline }}
            </v-icon>
          </v-btn>
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
    fees: {
      type: Array,
      default: () => [],
      required: true,
    },
  },
  data: () => {
    const defaultFee = {
      name: '',
      price: 0,
      by_day: false,
      by_people: false,
    }

    return {
      headers: [
        { text: 'NOM', value: 'name' },
        { text: 'PRIX', value: 'price' },
        { text: 'JOUR / SEJOUR', value: 'by_day' },
        { text: 'PERS. / LOGEMENT', value: 'by_people' },
        { text: '', value: 'action' },
      ],
      icons: {
        mdiDeleteOutline,
        mdiPlus,
      },
      defaultFee,
      feeBeingAdded: { ...defaultFee },
      isAddDialogVisible: false,
    }
  },
  methods: {
    byDayToString(byDay) {
      return byDay ? 'par jour' : 'pour le séjour'
    },
    byPeopleToString(byPeople) {
      return byPeople ? 'par personne' : 'par logement'
    },
    cleanDialog() {
      this.feeBeingAdded = { ...this.defaultFee }
      this.isAddDialogVisible = false
    },
    addFee() {
      this.$emit('add', this.feeBeingAdded)
      this.cleanDialog()
    },
  },
}
</script>

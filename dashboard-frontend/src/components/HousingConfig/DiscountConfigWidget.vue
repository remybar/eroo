<template>
  <v-card flat class="mb-4">
    <v-card-title>
      Vos remises
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

          <!-- add discount management -->
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
                Ajouter une remise
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <span class="headline">Ajouter une remise</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" md="3">
                      <label for="name">Nom de la remise</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="name"
                        v-model="discountBeingAdded.name"
                        outlined
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="3">
                      <label for="days-count">Nombre de jours min.</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="days-count"
                        v-model="discountBeingAdded.days_count"
                        outlined
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="3">
                      <label for="discount-value">Pourcentage de remise</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="discount-value"
                        v-model="discountBeingAdded.discount"
                        outlined
                        dense
                      ></v-text-field>
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

      <!-- discounts table -->
      <v-data-table
        id="discount-table"
        class="mx-8"
        :headers="headers"
        :items="discounts"
        no-data-text="Veuillez ajouter une nouvelle remise en cliquant sur le bouton 'Ajouter une remise'"
        disable-sort hide-default-footer
      >
        <!-- name -->
        <template #[`item.name`]="{item}">
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

        <!-- days_count -->
        <template #[`item.days_count`]="{item}">
          <v-edit-dialog :return-value.sync="item.days_count">
            <!-- display -->
            {{ item.days_count }}

            <!-- editor -->
            <template v-slot:input>
              <v-text-field
                v-model="item.days_count"
                label="Edit"
                single-line
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <!-- discount -->
        <template #[`item.discount`]="{item}">
          <v-edit-dialog :return-value.sync="item.discount">
            <!-- display -->
            {{ item.discount | formatDiscount }}

            <!-- editor -->
            <template v-slot:input>
              <v-text-field
                v-model="item.discount"
                label="Edit"
                single-line
              ></v-text-field>
            </template>
          </v-edit-dialog>
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
    formatDiscount(discount) {
      return `${discount}%`
    },
  },
  props: {
    discounts: {
      type: Array,
      default: () => [],
      required: true,
    },
  },
  data: () => {
    const defaultDiscount = {
      name: '',
      days_count: 1,
      discount: 0,
    }

    return {
      headers: [
        { text: 'NOM', value: 'name' },
        { text: 'NOMBRE DE JOURS', value: 'days_count' },
        { text: 'REMISE EN %', value: 'discount' },
        { text: '', value: 'action' },
      ],
      icons: {
        mdiDeleteOutline,
        mdiPlus,
      },
      defaultDiscount,
      discountBeingAdded: { ...defaultDiscount },
      isAddDialogVisible: false,
    }
  },
  methods: {
    cleanDialog() {
      this.discountBeingAdded = { ...this.defaultDiscount }
      this.isAddDialogVisible = false
    },
    addDiscount() {
      console.log(this.discountBeingAdded)
      this.$emit('add', this.discountBeingAdded)
      this.cleanDialog()
    },
  },
}
</script>

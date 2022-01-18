<template>
  <div class="housing-config-widget">
    <global-config-widget
      :config="config"
      @update="updateConfig($event)"
    ></global-config-widget>
    <season-config-widget
      :config="config"
      :seasons="seasons"
      @reset="resetSeasons()"
      @add="addSeason($event)"
      @update="updateSeason($event)"
      @remove="removeSeason($event)"
    ></season-config-widget>
    <fee-config-widget
      :fees="fees"
      @reset="resetFees()"
      @add="addFee($event)"
      @update="updateFee($event)"
      @remove="removeFee($event)"
    ></fee-config-widget>
    <discount-config-widget
      :discounts="discounts"
      @reset="resetDiscounts()"
      @add="addDiscount($event)"
      @update="updateDiscount($event)"
      @remove="removeDiscount($event)"
    ></discount-config-widget>
  </div>
</template>
<script>

import SeasonConfigWidget from '@/components/HousingConfig/SeasonConfigWidget.vue'
import FeeConfigWidget from '@/components/HousingConfig/FeeConfigWidget.vue'
import DiscountConfigWidget from '@/components/HousingConfig/DiscountConfigWidget.vue'
import GlobalConfigWidget from '@/components/HousingConfig/GlobalConfigWidget.vue'
import data from '@/components/data.json'

export default {
  components: {
    GlobalConfigWidget,
    SeasonConfigWidget,
    FeeConfigWidget,
    DiscountConfigWidget,
  },
  data: () => ({
    config: {},
    seasons: [],
    fees: {},
    discounts: {},
  }),
  created() {
    const p = JSON.parse(JSON.stringify(data))
    this.config = p.config
    this.seasons = p.seasons
    this.fees = p.fees
    this.discounts = p.discounts
  },
  methods: {
    updateConfig(config) {
      this.config = config
    },
    resetSeasons() {
      this.seasons.splice(0)
    },
    addSeason(value) {
      const newSeason = { id: this.seasons.length + 1, ...value }
      this.seasons.push(newSeason)
    },
    updateSeason(index, season) {
      this.seasons[index] = season
    },
    removeSeason(index) {
      this.seasons.splice(index, 1)
    },
    resetFees() {
      this.fees.splice(0)
    },
    addFee(value) {
      const newFee = { id: this.fees.length + 1, ...value }
      this.fees.push(newFee)
    },
    updateFee(index, fee) {
      this.fees[index] = fee
    },
    removeFee(index) {
      this.fees.splice(index, 1)
    },
    resetDiscounts() {
      this.discounts.splice(0)
    },
    addDiscount(value) {
      const newDiscount = { id: this.discounts.length + 1, ...value }
      this.discounts.push(newDiscount)
    },
    updateDiscount(index, discount) {
      this.discounts[index] = discount
    },
    removeDiscount(index) {
      this.discounts.splice(index, 1)
    },
  },
}
</script>
